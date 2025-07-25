# 🤖 Enhanced AI Sales Agent

An intelligent sales chatbot that uses OpenAI's GPT models to process natural language queries for sales predictions, historical analysis, and performance insights using your trained XGBoost model.

## 🌟 Features

### 🔮 **Sales Predictions**
- **Natural Language Processing**: Ask questions in plain English
- **Smart Date Parsing**: Handles multiple date formats (YYYY-MM-DD, DD-MM-YYYY, "4-5-2024")
- **Parameter Extraction**: Automatically extracts item IDs and dates from user queries

### 📊 **Sales Analytics**
- **Historical Analysis**: Analyze sales data for specific periods
- **Top Performers**: Find most sold items in specific time periods
- **Sales Summaries**: Get detailed statistics for items and time ranges
- **Period Analysis**: Support for "whole May", "May 2024", date ranges

### 🎯 **Smart Query Understanding**
- **Multi-Query Types**: Predictions, analysis, top performers, summaries
- **Context Awareness**: Maintains conversation history
- **Flexible Input**: Handles various query formats and phrasings
- **Intelligent Clarification**: Asks for missing information when needed

### 💻 **Multiple Interfaces**
- **Web Interface**: Beautiful Streamlit app with chat UI
- **Command Line**: Terminal-based chatbot
- **API Ready**: Modular design for easy integration

## 🎯 What You Can Ask

### Sales Predictions
- "Predict sales for item 3 on 2024-05-01"
- "What are sales for item 5 on 4-5-2024?"
- "Sales prediction for item 2 tomorrow"

### Sales Analysis
- "Which was the most sold item in May?"
- "Show me sales summary for item 2 in May 2024"
- "Total sales for item 3 whole May"
- "Most sold item in May 2024"

### Flexible Date Formats
- Standard: `2024-05-01`
- Alternative: `4-5-2024` (DD-MM-YYYY)
- Natural: `"whole May"`, `"May 2024"`
- Relative: `"tomorrow"`, `"next week"`

## 📁 Project Structure

```
Sales_Prediction_Project_v3/
├── sales_chatbot.py          # Main chatbot logic
├── streamlit_app.py          # Web interface using Streamlit
├── predict.py                # Original prediction script
├── config.py                 # Configuration settings
├── requirements.txt          # Python dependencies
├── README.md                 # This file
├── xgb_sales_model_v3.pkl    # Trained XGBoost model
├── sales_data_with_mapped_ids_v3.csv  # Sales data
└── festival_encoder_v3.pkl   # Festival encoder
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up OpenAI API Key

Get your API key from [OpenAI Platform](https://platform.openai.com/api-keys)

**Option A: Using .env file (Recommended)**
```bash
# Edit the .env file in the project directory
# Replace 'your-openai-api-key-here' with your actual API key
```

**Option B: Environment Variable**
```bash
# Windows (PowerShell)
$env:OPENAI_API_KEY="your-api-key-here"

# Windows (Command Prompt)
set OPENAI_API_KEY=your-api-key-here
```

**Option C: Enter in the application when prompted**

### 3. Run the Chatbot

**Command Line Interface:**
```bash
python sales_chatbot.py
```

**Web Interface (Streamlit):**
```bash
streamlit run streamlit_app.py
```

## 💬 Usage Examples

### Natural Language Queries

The chatbot understands various types of queries:

```
👤 "Predict sales for item 3 on 2024-05-01"
🤖 Based on the model, item 3 on May 1st, 2024 had actual sales of 45 units, and our prediction shows 42 units. That's pretty close!

👤 "What about item 5 tomorrow?"
🤖 For item 5 on July 25th, 2025, our model predicts 38 units will be sold.

👤 "Show me predictions for item 2 next Friday"
🤖 I'd be happy to predict sales for item 2 on July 31st, 2025. The model shows a prediction of 52 units.

👤 "How much will item 1 sell on Christmas?"
🤖 For item 1 on December 25th, 2024, considering it's a festival day, our model predicts 67 units (actual was 65 units).
```

### Supported Query Types

- **Direct queries**: "Predict sales for item X on YYYY-MM-DD"
- **Relative dates**: "tomorrow", "next week", "last Friday"
- **Festival dates**: "Christmas", "New Year", etc.
- **Casual language**: "What about...", "Show me...", "How much..."

## 🏗️ Architecture

### Core Components

1. **SalesPredictionChatbot Class**
   - `extract_parameters()`: Uses GPT to extract item ID and date from queries
   - `generate_response()`: Creates natural language responses
   - `handle_query()`: Main query processing pipeline

2. **Parameter Extraction**
   - Uses OpenAI GPT-3.5-turbo for natural language understanding
   - Validates extracted parameters against available data
   - Handles ambiguous queries with clarification requests

3. **Prediction Integration**
   - Leverages existing `predict.py` functionality
   - Maintains compatibility with trained XGBoost model
   - Provides both actual and predicted values when available

### Data Flow

```
User Query → Parameter Extraction → Validation → Prediction → Response Generation → User
     ↓              ↓                    ↓           ↓              ↓
   GPT-3.5    JSON Parameters      Data Check    XGBoost     Natural Language
```

## ⚙️ Configuration

Edit `config.py` to customize:

```python
# OpenAI Settings
OPENAI_MODEL = "gpt-3.5-turbo"  # or "gpt-4" for better accuracy
OPENAI_TEMPERATURE = 0.1        # Lower = more consistent
OPENAI_MAX_TOKENS = 300         # Response length limit

# Confidence threshold for parameter extraction
CONFIDENCE_THRESHOLD = 0.5      # Minimum confidence to proceed
```

## 🔧 Advanced Features

### Custom Date Parsing

The chatbot handles various date formats:
- Absolute: "2024-05-01", "May 1st, 2024"
- Relative: "tomorrow", "next week", "in 3 days"
- Named: "Christmas", "New Year's Eve"

### Error Handling

- Missing parameters → Asks clarifying questions
- Invalid item IDs → Shows available options
- Invalid dates → Requests correct format
- Model errors → User-friendly error messages

### Conversation Context

- Maintains chat history for follow-up questions
- Remembers previous queries for context
- Supports conversation continuity

## 🐛 Troubleshooting

### Common Issues

1. **"Please set your OPENAI_API_KEY environment variable"**
   - Solution: Set your OpenAI API key as shown in setup

2. **"Required file not found"**
   - Solution: Ensure all .pkl and .csv files are in the same directory

3. **"Item ID X is not available"**
   - Solution: Use `help` command to see available item IDs

4. **"Invalid date format"**
   - Solution: Use YYYY-MM-DD format or natural language like "tomorrow"

### Performance Tips

- Use GPT-3.5-turbo for faster responses
- Increase `CONFIDENCE_THRESHOLD` for more accurate extraction
- Monitor token usage for cost optimization

## 📊 Available Data

The chatbot automatically loads information about:
- Available item IDs from your dataset
- Date range of historical data
- Festival encodings for special dates

Use the `help` command to see current data availability.

## 🔮 Future Enhancements

- **Multi-item predictions**: Batch predictions for multiple items
- **Trend analysis**: Identify sales patterns and trends
- **Visualization**: Charts and graphs for prediction results
- **Voice interface**: Speech-to-text integration
- **API endpoint**: REST API for external integrations

## 📝 License

This project is part of your sales prediction system. Customize as needed for your use case.

## 🤝 Contributing

Feel free to extend the chatbot with additional features:
1. Fork the project
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 🌐 Streamlit Cloud Deployment

### Live Demo
🔗 **[Try the Live App](https://salespredictionbot-n4c8qgdbzoxamf3ivhnleg.streamlit.app/)** *(Update this URL after deployment)*

### Deploy Your Own Instance

1. **Fork this repository** to your GitHub account
2. **Go to [Streamlit Community Cloud](https://share.streamlit.io/)**
3. **Sign in** with your GitHub account
4. **Click "New app"** and select your forked repository
5. **Set the main file** to `streamlit_app.py`
6. **Configure secrets**:
   - Go to "Advanced settings" > "Secrets"
   - Add your OpenAI API key:
     ```toml
     OPENAI_API_KEY = "your-actual-openai-api-key-here"
     ```
7. **Click "Deploy"** and wait for the build to complete

### Environment Variables
- `OPENAI_API_KEY`: Your OpenAI API key for AI functionality

---

**Happy Predicting! 🚀**
