# Stock Sentiment Analyzer with OMI

Stock Sentiment Analyzer is a Flask-based web application designed to simplify stock sentiment analysis. It integrates OpenAI’s GPT-3.5-turbo for natural language processing and Alpha Vantage to fetch real-time sentiment data, empowering users with actionable insights from stock-related queries.

---

## Features

- **NLP for Stock Queries**: Extracts stock symbols from natural language inputs.
- **Sentiment Analysis**: Fetches and analyzes sentiment data for stocks via Alpha Vantage.
- **Validation**: Validates stock tickers against Yahoo Finance for accuracy.
- **Cooldown Mechanism**: Limits API calls to prevent excessive usage.
- **User Interface**: Clean, responsive design built with Tailwind CSS.
- **Error Handling**: Robust error management with detailed logging.

---


## Getting Started

### Prerequisites

- Python 3.10 or higher
- OpenAI API key
- Alpha Vantage API key

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/stock-sentiment-analyzer.git
   cd stock-sentiment-analyzer
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up environment variables by creating a `.env` file:
   ```env
   OPENAI_API_KEY=your_openai_api_key
   ALPHAVANTAGE_KEY=your_alpha_vantage_api_key
   ```
4. Run the application:
   ```bash
   python app.py
   ```
5. Access the application:
   Open your browser and navigate to `http://127.0.0.1:5000`.

---

## API Endpoints

### `POST /webhook`
- **Description**: Accepts user queries and responds with sentiment insights.
- **Request Body**:
  ```json
  {
    "id": "session_id",
    "structured": {
      "overview": "Analyze the Apple stock for me"
    }
  }
  ```
- **Response**:
  ```json
  {
    "message": "Stock: AAPL, Sentiment: Positive"
  }
  ```

### `GET /`
- **Description**: Displays the homepage with application instructions.

---

## Project Structure

```
.
├── app.py                # Main Flask application
├── templates/
│   └── index.html        # Frontend HTML templates
├── static/
│   └── css/              # Tailwind CSS styles
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables
├── README.md             # Project documentation
└── LICENSE               # License information
```

---

## Built With

- **Flask**: Python web framework.
- **OpenAI GPT-3.5-turbo**: For natural language processing.
- **Alpha Vantage API**: Real-time stock sentiment analysis.
- **Yahoo Finance API**: Ticker symbol validation.
- **Tailwind CSS**: Frontend design and styling.
- **Tenacity**: Retry mechanism for API calls.

---

## Contributing

We welcome contributions! To contribute:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature-name`).
3. Commit your changes (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin feature-name`).
5. Open a pull request.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## Disclaimer

The sentiment analysis provided is for informational purposes only and should not be considered financial advice. Please consult a financial advisor before making investment decisions.

