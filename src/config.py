import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    @classmethod
    def validate(cls):
        missing_vars = []
        if not cls.GITHUB_TOKEN:
            missing_vars.append("GITHUB_TOKEN")
        if not cls.OPENAI_API_KEY:
            missing_vars.append("OPENAI_API_KEY")

        if missing_vars:
            raise ValueError(
                f"Missing required environment variables: {', '.join(missing_vars)}.\n"
                "Please check your .env file or environment variables."
            )
