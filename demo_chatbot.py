"""
Test script to demonstrate the Sales Prediction Chatbot
This will show a complete interaction workflow
"""

from sales_chatbot import SalesPredictionChatbot
import os
from dotenv import load_dotenv

def run_complete_demo():
    """Run a complete demonstration of the chatbot"""
    
    print("🚀 Starting Sales Prediction Chatbot Demo")
    print("=" * 50)
    
    # Load environment variables
    load_dotenv()
    
    # Get API key
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key or api_key == 'your-openai-api-key-here':
        print("❌ Please configure your OpenAI API key in the .env file")
        return
    
    try:
        # Initialize chatbot
        print("🤖 Initializing chatbot...")
        chatbot = SalesPredictionChatbot(api_key)
        print("✅ Chatbot initialized successfully!")
        print()
        
        # Test queries to demonstrate different capabilities
        test_queries = [
            "Predict sales for item 3 on 2024-05-01",
            "What about item 5 tomorrow?",
            "Show me predictions for item 2 on 2024-12-25",
            "How much will item 1 sell next Friday?"
        ]
        
        print("🧪 Running Test Queries:")
        print("=" * 30)
        
        for i, query in enumerate(test_queries, 1):
            print(f"\n📝 Test {i}: '{query}'")
            print("-" * 40)
            
            try:
                # Process the query
                response = chatbot.handle_query(query)
                print(f"🤖 Response: {response}")
                
            except Exception as e:
                print(f"❌ Error processing query: {e}")
            
            print()
        
        print("🎉 Demo completed successfully!")
        print("\n📊 Conversation History:")
        print("-" * 25)
        
        for i, conversation in enumerate(chatbot.conversation_history, 1):
            print(f"\n{i}. Query: {conversation['query']}")
            print(f"   Parameters: {conversation['parameters']}")
            print(f"   Result: {conversation['result']}")
            print(f"   Response: {conversation['response']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error running demo: {e}")
        return False

if __name__ == "__main__":
    success = run_complete_demo()
    if success:
        print("\n✨ All tests completed successfully!")
    else:
        print("\n💥 Demo failed. Please check the configuration.")
