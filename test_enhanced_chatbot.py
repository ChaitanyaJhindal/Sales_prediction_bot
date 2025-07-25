#!/usr/bin/env python3
"""
Test script for the enhanced sales chatbot
This script demonstrates the new capabilities including:
- Finding most sold items
- Handling different date formats
- Sales analysis and summaries
"""

import os
from sales_chatbot import SalesPredictionChatbot
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_chatbot():
    """Test the enhanced chatbot functionality"""
    
    # Initialize chatbot (you'll need to set your OpenAI API key)
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("❌ Please set your OPENAI_API_KEY in the .env file")
        return
    
    try:
        chatbot = SalesPredictionChatbot(api_key)
        print("🤖 Enhanced Sales Chatbot Test\n" + "="*50)
        
        # Test queries that demonstrate new capabilities
        test_queries = [
            "Which was the most sold item in May?",
            "Sales for item 2 whole May",
            "Predict sales for item 3 on 4-5-2024",
            "Show me sales summary for item 1 in May 2024",
            "What item sold the most in May 2024?"
        ]
        
        for i, query in enumerate(test_queries, 1):
            print(f"\n📝 Test {i}: {query}")
            print("-" * 40)
            
            try:
                response = chatbot.handle_query(query)
                print(f"🤖 Response:\n{response}")
            except Exception as e:
                print(f"❌ Error: {e}")
            
            print()
        
        print("✅ Test completed!")
        
    except Exception as e:
        print(f"❌ Error initializing chatbot: {e}")

if __name__ == "__main__":
    test_chatbot()
