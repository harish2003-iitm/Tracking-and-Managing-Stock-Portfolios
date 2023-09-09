from flask import Flask, render_template
import yfinance as yf
import matplotlib
import matplotlib.pyplot as plt
from io import BytesIO
import base64

matplotlib.use('Agg')

app = Flask(__name__)

def get_stock_price(symbol):
  try:
    stock = yf.Ticker(symbol)
    history = stock.history(period="1d")  
    if not history.empty:
      price = history["Open"].iloc[0]  
      return price
  except:
    return 'N/A'

@app.route("/")
def index():

  stocks = ["AAPL", "GOOG", "TSLA","AMZN","MSFT"]
  stock_prices = {}

  for symbol in stocks:
    price = get_stock_price(symbol)
    if price == 'N/A':
      price = 0.0
    stock_prices[symbol] = price

  fig, ax = plt.subplots(figsize=(10,6))

  ax.plot(stock_prices.keys(), stock_prices.values(), marker='o', linestyle='-')
  ax.set_xlabel('Stock')  
  ax.set_ylabel('Price (USD)')
  ax.set_title('Stock Prices')

  img = BytesIO()
  fig.savefig(img, format='png')
  img.seek(0)

  img_base64 = base64.b64encode(img.read()).decode()

  plt.close(fig)

  return render_template('index.html',
                         stock_prices=stock_prices,
                         plot=img_base64,
                         )

@app.route('/real_time_updates')
def real_time_updates():
   
    return render_template('real_time_updates.html')



if __name__ == '__main__':
  app.run(debug=True)
app.py
