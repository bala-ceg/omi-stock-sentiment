from flask import Flask, render_template, request, jsonify
import logging
import time
import os
from collections import defaultdict
from tenacity import retry, stop_after_attempt, wait_exponential
import requests
import json
import openai


app = Flask(__name__)


# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_base = os.getenv("OPENAI_BASE_URL")
ALPHAVANTAGE_KEY = os.getenv("ALPHAVANTAGE_KEY")

# Store for aggregating messages
message_buffer = defaultdict(list)
last_print_time = defaultdict(float)
AGGREGATION_INTERVAL = 30  # seconds

notification_cooldowns = defaultdict(float)
NOTIFICATION_COOLDOWN = 60  # 1 minute cooldown between notifications for each session


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def analyze_stock_intent(text):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant. Extract the stock ticker symbol from the below User Input. Return the Response in JSON Format with key as stock_ticker_symbol"},
                {"role": "user", "content": text}
            ],
            temperature=0.3,
            max_tokens=60
        )
        stock_symbol = response.choices[0].message['content'].strip()
        return {"intent": "yes" if stock_symbol else "no", "symbol": stock_symbol}
    except Exception as e:
        logger.error(f"Error in analyze_stock_intent: {e}")
        return {"intent": "no", "symbol": None}

def get_stock_sentiment(symbol):
    url = f'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers={symbol}&apikey={ALPHAVANTAGE_KEY}'
    try:
        response = requests.get(url)
        data = response.json()
        
        if 'feed' not in data:
            return {"error": "No sentiment data available"}

        sentiments = [item['ticker_sentiment'][0]['ticker_sentiment_label'] for item in data['feed'] if item['ticker_sentiment']]
        sentiment_counts = {s: sentiments.count(s) for s in set(sentiments)}
        filtered_sentiment_counts = {key: value for key, value in sentiment_counts.items() if key != 'Neutral'}
        highest_sentiment = max(filtered_sentiment_counts, key=sentiment_counts.get)

        return {
            "highest_sentiment": highest_sentiment,
            "sentiment_counts": sentiment_counts,
            "news_data": data['feed'][:5]  # Return only the first 5 news items
        }
    except Exception as e:
        logger.error(f"Error fetching stock sentiment: {e}")
        return {"error": f"Failed to fetch stock sentiment: {str(e)}"}


@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    logger.info(f"Received data: {data}")

    session_id = data.get("id")
    if not session_id:
        return jsonify({"status": "error", "message": "No session id provided"}), 400

    overview = data.get("structured", {}).get("overview")
    if not overview:
        return jsonify({"status": "error", "message": "No overview provided"}), 400

    current_time = time.time()

    #Check notification cooldown
    time_since_last_notification = current_time - notification_cooldowns[session_id]
    if time_since_last_notification < NOTIFICATION_COOLDOWN:
        return jsonify({"status": "success"}), 200

    intent = analyze_stock_intent(overview)
    if not intent :
        return jsonify({"status": "error"}), 400

    try:
        symbol_data = json.loads(intent['symbol'])  # Convert string to dictionary
        output_data = {
            'intent': intent['intent'],
            'symbol': symbol_data['stock_ticker_symbol']  # Extract the ticker symbol
        }
        print(output_data)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        print(intent)

    stock_symbol = output_data['symbol']
    print(f"Stock intent detected for session {stock_symbol}!")
  
    if intent["intent"] == "yes":
        logger.warning(f"Stock intent detected for session {session_id}!")
        notification_cooldowns[session_id] = current_time

        sentiment_data = get_stock_sentiment(stock_symbol)
        if "error" not in sentiment_data:
            return jsonify({
                "message": f"Stock: {stock_symbol}, Sentiment: {sentiment_data['highest_sentiment']}"
            }), 200
        else:
            return jsonify({"status": "error", "message": sentiment_data["error"], "Reason": "Please provide a valid stock"}), 500



