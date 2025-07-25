# Configuration file for Sales Prediction Chatbot

# OpenAI Settings
OPENAI_MODEL = "gpt-3.5-turbo"
OPENAI_TEMPERATURE = 0.1
OPENAI_MAX_TOKENS = 300

# Model Files
MODEL_PATH = "xgb_sales_model_v3.pkl"
DATA_PATH = "sales_data_with_mapped_ids_v3.csv"
ENCODER_PATH = "festival_encoder_v3.pkl"

# Chatbot Settings
CONFIDENCE_THRESHOLD = 0.5
MAX_CONVERSATION_HISTORY = 50

# Logging
LOG_LEVEL = "INFO"
LOG_FILE = "chatbot.log"
