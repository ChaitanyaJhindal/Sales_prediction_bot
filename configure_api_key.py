"""
Configure OpenAI API Key for Sales Prediction Chatbot
"""

import os
from pathlib import Path

def configure_api_key():
    """Interactive script to configure OpenAI API key"""
    
    print("🔑 OpenAI API Key Configuration")
    print("=" * 40)
    
    # Check if .env file exists
    env_file = Path(".env")
    if not env_file.exists():
        print("❌ .env file not found!")
        print("Please make sure you're in the correct directory.")
        return False
    
    print("📝 Please enter your OpenAI API key:")
    print("(Get one from: https://platform.openai.com/api-keys)")
    
    while True:
        api_key = input("\nAPI Key: ").strip()
        
        if not api_key:
            print("❌ API key cannot be empty!")
            continue
        
        if len(api_key) < 20:
            print("❌ API key seems too short. Please check and try again.")
            continue
        
        if not api_key.startswith('sk-'):
            print("⚠️  OpenAI API keys usually start with 'sk-'. Are you sure this is correct? (y/n)")
            confirm = input().strip().lower()
            if confirm not in ['y', 'yes']:
                continue
        
        break
    
    # Read current .env file
    try:
        with open(env_file, 'r') as f:
            content = f.read()
        
        # Replace the API key
        if "OPENAI_API_KEY=" in content:
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if line.startswith('OPENAI_API_KEY='):
                    lines[i] = f'OPENAI_API_KEY={api_key}'
                    break
            content = '\n'.join(lines)
        else:
            # Add the API key if not present
            content += f'\nOPENAI_API_KEY={api_key}\n'
        
        # Write back to file
        with open(env_file, 'w') as f:
            f.write(content)
        
        print("✅ API key configured successfully!")
        print("\nYou can now run:")
        print("• python sales_chatbot.py (command line)")
        print("• streamlit run streamlit_app.py (web interface)")
        
        return True
        
    except Exception as e:
        print(f"❌ Error configuring API key: {e}")
        return False

def main():
    """Main function"""
    success = configure_api_key()
    if not success:
        print("\n❌ Configuration failed. Please try again.")
        return False
    
    print("\n🎉 Configuration completed successfully!")
    return True

if __name__ == "__main__":
    main()
