import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, JobQueue, Job
from binance.client import Client

# 配置你的Telegram bot token
TOKEN = '6758894168:AAHlqQgC-vl2NIopELcPnd4FPPd6Rh2LS1U'
# 要发送消息的聊天ID
CHAT_ID = '1873325987'
# Binance API密钥和Secret
Binance_API_KEY = '5eRJW33kScb9JvsLaf55ho2SgFstYnJubMJaTNmA880KeQ6EayntQ6sDiHuaEvJh'
Binance_API_SECRET = 'QdJd1YMRkQAeOZEa3Jv3sHEw3vX9KrJeqfgf4IqgmwPJ7VT0SverNljusdcrpCer'

# 启用日志
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# 创建Binance客户端
binance_client = Client(api_key=Binance_API_KEY, api_secret=Binance_API_SECRET)

def start(update: Update, context: CallbackContext):
    update.message.reply_text('Bot已启动，将定期推送Binance交易对价格更新。')

def get_binance_price(symbol: str):
    try:
        price = binance_client.get_symbol_ticker(symbol=symbol)['price']
        return price
    except Exception as e:
        logger.error(f"Error getting price for symbol {symbol}: {e}")
        return None

def send_binance_prices(updater, job):
    trading_pairs = [('BTC', 'USDT'), ('ETH', 'USDT'), ('LTC', 'USDT')]  # 定义要检查的交易对
    prices = {}

    for base, quote in trading_pairs:
        symbol = f"{base}{quote}"
        price = get_binance_price(symbol)
        if price:
            prices[symbol] = price

    price_updates = "\n".join([f"{symbol}: {price}" for symbol, price in prices.items()])
    updater.bot.send_message(chat_id=CHAT_ID, text=f'最新Binance交易对价格更新:\n{price_updates}')

def main():
    # 创建Updater对象
    updater = Updater(TOKEN, use_context=True)

    # 获取dispatcher和JobQueue
    dp = updater.dispatcher
    job_queue = updater.job_queue

    # 注册命令handler
    dp.add_handler(CommandHandler("start", start))

    # 启动时注册定时任务，例如每10分钟执行一次
    job = job_queue.run_repeating(send_binance_prices, interval=600, first=0)

    # 启动bot
    updater.start_polling()

    # 阻塞直到停止
    updater.idle()

if __name__ == '__main__':
    main()