import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # LLM Settings
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai") # openai or gemini

    # Crawler Settings
    USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
    
    # Application Settings
    DB_PATH = os.path.join("data", "info_system.db")
    
    # Keywords for high value filtering (comma separated in env)
    HIGH_VALUE_KEYWORDS = os.getenv("HIGH_VALUE_KEYWORDS", "AI,LLM,Agent,Python,Automation").split(",")

    # Model Configuration
    MODEL_SELECTION = "gemini-2.5-flash-lite-preview-09-2025" 
    MODEL_ANALYSIS = "gemini-2.5-flash-preview-09-2025"

config = Config()
