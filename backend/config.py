import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Configuration class for the application"""
    
    # Gemini API Configuration
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    
    # Flask Configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-for-development')
    DEBUG = os.getenv('DEBUG', 'True') == 'True'
    
    # Server Configuration
    HOST = '0.0.0.0'
    PORT = 5000
    
    # School Information
    SCHOOL_INFO = {
        'name': 'PRIMARY SCHOOL NAIKIWAD VANZANA',
        'taluka': 'CHIKHLI',
        'district': 'NAVSARI',
        'dise_code': '24240108404'
    }
    
    @staticmethod
    def validate():
        """Validate required configuration"""
        if not Config.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY is not set in environment variables")
        return True