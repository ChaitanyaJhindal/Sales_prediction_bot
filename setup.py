"""
Setup script for Sales Prediction Chatbot
Helps users get started quickly with the chatbot
"""

import os
import subprocess
import sys
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def install_requirements():
    """Install required packages"""
    print("📦 Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ All packages installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing packages: {e}")
        return False

def check_files():
    """Check if all required files exist"""
    required_files = [
        "xgb_sales_model_v3.pkl",
        "sales_data_with_mapped_ids_v3.csv",
        "festival_encoder_v3.pkl",
        "predict.py",
        "sales_chatbot.py"
    ]
    
    missing_files = []
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Missing required files: {', '.join(missing_files)}")
        return False
    
    print("✅ All required files found!")
    return True

def check_api_key():
    """Check if OpenAI API key is set"""
    # Check .env file first
    env_file = Path(".env")
    if env_file.exists():
        with open(env_file, 'r') as f:
            content = f.read()
            if "OPENAI_API_KEY=your-openai-api-key-here" in content:
                print("⚠️  Please edit the .env file and add your actual OpenAI API key")
                print("Replace 'your-openai-api-key-here' with your real API key")
                print("Get one from: https://platform.openai.com/api-keys")
                return False
            elif "OPENAI_API_KEY=" in content and len(content.split("OPENAI_API_KEY=")[1].split()[0]) > 10:
                print("✅ OpenAI API key found in .env file")
                return True
    
    # Check environment variable
    api_key = os.getenv('OPENAI_API_KEY')
    if api_key:
        print("✅ OpenAI API key found in environment variable")
        return True
    else:
        print("⚠️  OpenAI API key not found")
        print("Please either:")
        print("1. Edit the .env file and add your API key")
        print("2. Set environment variable: $env:OPENAI_API_KEY=\"your-key\"")
        print("3. Get an API key from: https://platform.openai.com/api-keys")
        return False

def main():
    """Main setup function"""
    print("🤖 Sales Prediction Chatbot Setup")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Check required files
    if not check_files():
        return False
    
    # Install requirements
    if not install_requirements():
        return False
    
    # Check API key
    check_api_key()
    
    print("\n" + "=" * 40)
    print("🎉 Setup completed!")
    print("\nNext steps:")
    print("1. Command line: python sales_chatbot.py")
    print("2. Web interface: streamlit run streamlit_app.py")
    print("\nFor help, check README.md")
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)
