import openai
import re
import json
import pandas as pd
from datetime import datetime, timedelta
import os
from typing import Dict, List, Optional, Tuple
import logging
from predict import predict_sales
from dotenv import load_dotenv
import calendar
from collections import defaultdict

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SalesPredictionChatbot:
    def __init__(self, openai_api_key: str):
        """
        Initialize the Sales Prediction Chatbot
        
        Args:
            openai_api_key (str): OpenAI API key for LLM integration
        """
        self.client = openai.OpenAI(api_key=openai_api_key)
        self.conversation_history = []
        
        # Load available item IDs and date ranges for better context
        self._load_data_context()
        
    def _load_data_context(self):
        """Load context about available data for better parameter extraction"""
        try:
            # Get the directory where this script is located
            script_dir = os.path.dirname(os.path.abspath(__file__))
            data_path = os.path.join(script_dir, 'sales_data_with_mapped_ids_v3.csv')
            
            self.df = pd.read_csv(data_path)
            self.df['ORDERDATE'] = pd.to_datetime(self.df['ORDERDATE'])
            
            self.available_items = sorted(self.df['ITEMID_Mapped'].unique().tolist())
            self.date_range = {
                'min_date': self.df['ORDERDATE'].min().strftime('%Y-%m-%d'),
                'max_date': self.df['ORDERDATE'].max().strftime('%Y-%m-%d')
            }
            
            logger.info(f"Loaded context: {len(self.available_items)} items, dates from {self.date_range['min_date']} to {self.date_range['max_date']}")
            
        except Exception as e:
            logger.error(f"Error loading data context: {e}")
            self.available_items = []
            self.date_range = {'min_date': '2020-01-01', 'max_date': '2024-12-31'}
            self.df = None

    def _parse_date_input(self, date_str: str) -> List[str]:
        """
        Parse various date formats and return list of dates
        
        Args:
            date_str (str): Date string in various formats
            
        Returns:
            List[str]: List of dates in YYYY-MM-DD format
        """
        if not date_str:
            return []
            
        date_str = date_str.lower().strip()
        
        # Handle "whole may", "entire may", "all of may"
        if any(word in date_str for word in ['whole', 'entire', 'all of']) and 'may' in date_str:
            year = datetime.now().year
            if '2024' in date_str:
                year = 2024
            return [f"{year}-05-{day:02d}" for day in range(1, 32)]
        
        # Handle "may 2024", "may"
        if 'may' in date_str:
            year = datetime.now().year
            if '2024' in date_str:
                year = 2024
            return [f"{year}-05-{day:02d}" for day in range(1, 32)]
        
        # Handle "4-5-2024" (assume DD-MM-YYYY)
        if re.match(r'\d{1,2}-\d{1,2}-\d{4}', date_str):
            parts = date_str.split('-')
            if len(parts) == 3:
                day, month, year = parts
                try:
                    return [f"{year}-{month.zfill(2)}-{day.zfill(2)}"]
                except:
                    pass
        
        # Handle standard formats
        try:
            parsed_date = datetime.strptime(date_str, '%Y-%m-%d')
            return [parsed_date.strftime('%Y-%m-%d')]
        except:
            pass
            
        return []

    def find_most_sold_item(self, period: str = None, month: int = None, year: int = None) -> str:
        """
        Find the most sold item in a specific period
        
        Args:
            period (str): Period description (e.g., "may", "whole may")
            month (int): Month number (1-12)
            year (int): Year
            
        Returns:
            str: Analysis result
        """
        if self.df is None:
            return "Data not available for analysis."
            
        try:
            df_filtered = self.df.copy()
            
            # Filter by month and year if specified
            if month:
                df_filtered = df_filtered[df_filtered['ORDERDATE'].dt.month == month]
            if year:
                df_filtered = df_filtered[df_filtered['ORDERDATE'].dt.year == year]
            
            if df_filtered.empty:
                return f"No data found for the specified period."
            
            # Group by item and sum total sales
            sales_by_item = df_filtered.groupby('ITEMID_Mapped')['TOTAL_ITEMSOLD'].sum().sort_values(ascending=False)
            
            if sales_by_item.empty:
                return "No sales data found for the specified period."
            
            top_item = sales_by_item.index[0]
            total_sales = sales_by_item.iloc[0]
            
            # Get additional stats
            top_5_items = sales_by_item.head(5)
            period_desc = f"May {year}" if month == 5 and year else "the specified period"
            
            result = f"**Most Sold Item in {period_desc}:**\n"
            result += f"🏆 **Item ID {top_item}** with **{int(total_sales)} total units sold**\n\n"
            result += "**Top 5 Items:**\n"
            for i, (item_id, sales) in enumerate(top_5_items.items(), 1):
                result += f"{i}. Item {item_id}: {int(sales)} units\n"
            
            return result
            
        except Exception as e:
            logger.error(f"Error in find_most_sold_item: {e}")
            return f"Error analyzing sales data: {e}"

    def get_sales_summary(self, item_id: int = None, dates: List[str] = None) -> str:
        """
        Get sales summary for specific item(s) and date(s)
        
        Args:
            item_id (int): Item ID to analyze
            dates (List[str]): List of dates to analyze
            
        Returns:
            str: Sales summary
        """
        if self.df is None:
            return "Data not available for analysis."
            
        try:
            df_filtered = self.df.copy()
            
            # Filter by item if specified
            if item_id:
                df_filtered = df_filtered[df_filtered['ITEMID_Mapped'] == item_id]
            
            # Filter by dates if specified
            if dates:
                date_objects = [pd.to_datetime(date) for date in dates]
                df_filtered = df_filtered[df_filtered['ORDERDATE'].isin(date_objects)]
            
            if df_filtered.empty:
                return f"No data found for the specified criteria."
            
            total_sales = df_filtered['TOTAL_ITEMSOLD'].sum()
            avg_sales = df_filtered['TOTAL_ITEMSOLD'].mean()
            max_sales = df_filtered['TOTAL_ITEMSOLD'].max()
            min_sales = df_filtered['TOTAL_ITEMSOLD'].min()
            
            result = f"**Sales Summary:**\n"
            if item_id:
                result += f"Item ID: {item_id}\n"
            if dates and len(dates) <= 5:
                result += f"Dates: {', '.join(dates)}\n"
            elif dates:
                result += f"Date Range: {len(dates)} days\n"
            
            result += f"\n📊 **Statistics:**\n"
            result += f"• Total Sales: {int(total_sales)} units\n"
            result += f"• Average Daily Sales: {avg_sales:.1f} units\n"
            result += f"• Maximum Daily Sales: {int(max_sales)} units\n"
            result += f"• Minimum Daily Sales: {int(min_sales)} units\n"
            
            return result
            
        except Exception as e:
            logger.error(f"Error in get_sales_summary: {e}")
            return f"Error analyzing sales data: {e}"

    def extract_parameters(self, user_query: str) -> Dict:
        """
        Use OpenAI to extract parameters and determine query type from natural language query
        
        Args:
            user_query (str): User's natural language query
            
        Returns:
            Dict: Extracted parameters with query type and relevant information
        """
        
        system_prompt = f"""
        You are a parameter extraction assistant for a sales prediction and analytics system.
        
        Available item IDs: {self.available_items}
        Available date range: {self.date_range['min_date']} to {self.date_range['max_date']}
        Current date: {datetime.now().strftime('%Y-%m-%d')}
        
        Analyze the user query and determine the query type and extract relevant parameters:
        
        QUERY TYPES:
        1. "prediction" - User wants to predict sales for specific item and date
        2. "analysis" - User wants to analyze historical sales data
        3. "most_sold" - User wants to find the most sold item in a period
        4. "summary" - User wants sales summary for item/period
        
        Extract these parameters:
        - query_type: one of the above types
        - item_id: integer (if specified)
        - date: YYYY-MM-DD format (if single date)
        - date_range: list of dates or period description
        - month: month number (1-12) if mentioned
        - year: year if mentioned
        - period_description: natural description of time period
        
        For date formats:
        - "4-5-2024" should be interpreted as 4th May 2024 (DD-MM-YYYY)
        - "whole may" or "entire may" means all days in May
        - "may 2024" means May 2024
        - Handle relative dates like "tomorrow", "next week"
        
        Return ONLY a JSON object:
        {{
            "query_type": "<prediction|analysis|most_sold|summary>",
            "item_id": <integer or null>,
            "date": "<YYYY-MM-DD or null>",
            "date_range": ["YYYY-MM-DD", ...] or null,
            "month": <1-12 or null>,
            "year": <year or null>,
            "period_description": "<description or null>",
            "confidence": <float between 0-1>,
            "missing_info": ["list of missing required parameters"],
            "clarification_needed": "<question to ask user if parameters unclear>"
        }}
        
        Examples:
        - "Predict sales for item 3 on 2024-05-01" → {{"query_type": "prediction", "item_id": 3, "date": "2024-05-01", "confidence": 1.0, "missing_info": []}}
        - "Which was most sold item in may" → {{"query_type": "most_sold", "month": 5, "year": 2024, "period_description": "May 2024", "confidence": 0.9, "missing_info": []}}
        - "Sales for item 2 whole may" → {{"query_type": "summary", "item_id": 2, "month": 5, "period_description": "whole May", "confidence": 0.9, "missing_info": []}}
        - "on 4 may" → {{"query_type": "prediction", "date": "2024-05-04", "confidence": 0.7, "missing_info": ["item_id"], "clarification_needed": "Which item would you like to predict sales for on May 4th?"}}
        - "4-5-2024" → {{"query_type": "prediction", "date": "2024-05-04", "confidence": 0.8, "missing_info": ["item_id"], "clarification_needed": "Which item would you like to predict sales for on May 4th, 2024?"}}
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_query}
                ],
                temperature=0.1,
                max_tokens=400
            )
            
            content = response.choices[0].message.content.strip()
            
            # Parse JSON response
            try:
                parameters = json.loads(content)
                return parameters
            except json.JSONDecodeError:
                # Fallback: try to extract JSON from response
                json_match = re.search(r'\{.*\}', content, re.DOTALL)
                if json_match:
                    parameters = json.loads(json_match.group())
                    return parameters
                else:
                    raise ValueError("Could not parse JSON from LLM response")
                    
        except Exception as e:
            logger.error(f"Error in parameter extraction: {e}")
            return {
                "query_type": "prediction",
                "item_id": None,
                "date": None,
                "confidence": 0.0,
                "missing_info": ["item_id", "date"],
                "clarification_needed": "I couldn't understand your request. Please specify the item ID and date for sales prediction."
            }

    def generate_response(self, prediction_result: str, user_query: str, parameters: Dict) -> str:
        """
        Generate a natural language response based on prediction results
        
        Args:
            prediction_result (str): Result from the prediction model
            user_query (str): Original user query
            parameters (Dict): Extracted parameters
            
        Returns:
            str: Natural language response
        """
        
        system_prompt = f"""
        You are a helpful sales prediction assistant. Generate a natural, conversational response based on the prediction results.
        
        User's original query: "{user_query}"
        Extracted parameters: Item ID {parameters.get('item_id')}, Date {parameters.get('date')}
        Prediction result: "{prediction_result}"
        
        Guidelines:
        1. Be conversational and helpful
        2. Explain the prediction clearly
        3. Mention both actual and predicted values if available
        4. Add context about the prediction (e.g., if it's higher/lower than actual)
        5. Offer to help with more predictions
        6. Keep it concise but informative
        
        Avoid technical jargon and make it user-friendly.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Generate response for: {prediction_result}"}
                ],
                temperature=0.7,
                max_tokens=200
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return f"Here are your prediction results: {prediction_result}"

    def handle_query(self, user_query: str) -> str:
        """
        Main method to handle user queries end-to-end
        
        Args:
            user_query (str): User's natural language query
            
        Returns:
            str: Generated response
        """
        
        logger.info(f"Processing query: {user_query}")
        
        # Extract parameters from query
        parameters = self.extract_parameters(user_query)
        
        # Check confidence and missing information
        if parameters.get('confidence', 0) < 0.5 or parameters.get('missing_info'):
            return parameters.get('clarification_needed', 
                                "I need more information. Please specify your request clearly.")
        
        query_type = parameters.get('query_type', 'prediction')
        
        try:
            # Handle different query types
            if query_type == 'most_sold':
                month = parameters.get('month')
                year = parameters.get('year', datetime.now().year)
                return self.find_most_sold_item(
                    period=parameters.get('period_description'),
                    month=month,
                    year=year
                )
            
            elif query_type == 'summary':
                item_id = parameters.get('item_id')
                month = parameters.get('month')
                year = parameters.get('year', datetime.now().year)
                
                # Generate date range if month specified
                dates = None
                if month and year:
                    days_in_month = calendar.monthrange(year, month)[1]
                    dates = [f"{year}-{month:02d}-{day:02d}" for day in range(1, days_in_month + 1)]
                elif parameters.get('date'):
                    dates = [parameters.get('date')]
                
                return self.get_sales_summary(item_id=item_id, dates=dates)
            
            elif query_type == 'analysis':
                item_id = parameters.get('item_id')
                month = parameters.get('month')
                year = parameters.get('year', datetime.now().year)
                
                if month and year:
                    days_in_month = calendar.monthrange(year, month)[1]
                    dates = [f"{year}-{month:02d}-{day:02d}" for day in range(1, days_in_month + 1)]
                    return self.get_sales_summary(item_id=item_id, dates=dates)
                else:
                    return "Please specify a time period for analysis."
            
            else:  # prediction type
                item_id = parameters.get('item_id')
                date = parameters.get('date')
                
                # Validate parameters
                if item_id not in self.available_items:
                    return f"Item ID {item_id} is not available. Available items: {', '.join(map(str, self.available_items[:10]))}{'...' if len(self.available_items) > 10 else ''}"
                
                if not date:
                    return "Please specify a date for the prediction."
                
                try:
                    # Validate date format
                    datetime.strptime(date, '%Y-%m-%d')
                except ValueError:
                    return f"Invalid date format. Please use YYYY-MM-DD format."
                
                # Run prediction
                prediction_result = predict_sales(item_id, date)
                
                # Generate natural language response
                response = self.generate_response(prediction_result, user_query, parameters)
                
                # Add to conversation history
                self.conversation_history.append({
                    'query': user_query,
                    'parameters': parameters,
                    'result': prediction_result,
                    'response': response
                })
                
                return response
                
        except Exception as e:
            logger.error(f"Error processing query: {e}")
            return f"I encountered an error while processing your request: {str(e)}"

    def get_help_message(self) -> str:
        """Return help message for users"""
        return f"""
        🤖 **AI Sales Agent Help**
        
        I can help you with various sales-related queries!
        
        **Available Items:** {', '.join(map(str, self.available_items[:10]))}{'...' if len(self.available_items) > 10 else ''}
        **Date Range:** {self.date_range['min_date']} to {self.date_range['max_date']}
        
        **What I can do:**
        
        🔮 **Sales Predictions:**
        • "Predict sales for item 3 on 2024-05-01"
        • "What are the sales for item 5 tomorrow?"
        • "Sales for item 2 on 4-5-2024"
        
        📊 **Sales Analysis:**
        • "Which was the most sold item in May?"
        • "Show me sales summary for item 2 in May"
        • "Total sales for item 3 whole May"
        
        🏆 **Top Performers:**
        • "Most sold item in May 2024"
        • "Which item sold the most in May?"
        
        **Date Formats I understand:**
        • Standard: 2024-05-01
        • Alternative: 4-5-2024 (DD-MM-YYYY)
        • Natural: "whole May", "entire May", "May 2024"
        • Relative: "tomorrow", "next week"
        
        Just ask naturally and I'll understand! 😊
        """

def main():
    """Main function to run the chatbot"""
    
    # Get OpenAI API key from environment variables
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key or api_key == 'your-openai-api-key-here':
        print("❌ OpenAI API key not found or not configured!")
        print("\n📝 Setup instructions:")
        print("1. Edit the .env file in this directory")
        print("2. Replace 'your-openai-api-key-here' with your actual API key")
        print("3. Get an API key from: https://platform.openai.com/api-keys")
        print("\n💡 Alternatively, you can set the environment variable directly:")
        print("   Windows: $env:OPENAI_API_KEY=\"your-api-key\"")
        return
    
    # Initialize chatbot
    try:
        chatbot = SalesPredictionChatbot(api_key)
        print("🤖 Sales Prediction Chatbot initialized successfully!")
        print(chatbot.get_help_message())
        print("\n" + "="*60)
        
    except Exception as e:
        print(f"❌ Error initializing chatbot: {e}")
        return
    
    # Main chat loop
    print("\n💬 Start chatting! (Type 'help' for assistance, 'quit' to exit)")
    
    while True:
        try:
            user_input = input("\n👤 You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("👋 Goodbye! Thanks for using the Sales Prediction Chatbot!")
                break
                
            elif user_input.lower() in ['help', '?']:
                print(chatbot.get_help_message())
                continue
                
            elif not user_input:
                continue
            
            # Process the query
            print("🤖 Bot: ", end="", flush=True)
            response = chatbot.handle_query(user_input)
            print(response)
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye! Thanks for using the Sales Prediction Chatbot!")
            break
        except Exception as e:
            print(f"❌ An error occurred: {e}")
            continue

if __name__ == "__main__":
    main()
