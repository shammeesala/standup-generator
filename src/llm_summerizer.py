from openai import OpenAI
from src.config import Config

class LLMSummarizer:
    def __init__(self):
        # Initialize the OpenAI client using the key from config
        self.client = OpenAI(api_key=Config.OPENAI_API_KEY)
        
    def generate_standup(self, raw_activity: str) -> str:
        """
        Sends the raw GitHub activity to the LLM and asks for a standup summary.
        """
        if not raw_activity.strip() or "No commits found" in raw_activity and "No pull requests found" in raw_activity:
            return "No GitHub activity found for the specified period. Nothing to summarize!"

        system_prompt = (
            "You are a helpful assistant for a software engineer. "
            "Your job is to read a raw list of their recent GitHub commits and Pull Requests, "
            "and summarize what they accomplished into a professional, concise daily standup report. "
            "Format the output as a bulleted list. Do not use technical jargon needlessly, just explain *what* was done. "
            "Combine related commits into a single bullet point if they try to achieve the same feature or fix."
        )

        user_prompt = f"Here is my raw GitHub activity. Please generate a standup summary:\n\n{raw_activity}"

        try:
            print("Sending data to the LLM for summarization...")
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo", # Using 3.5-turbo as it's fast and cheap for simple summarization
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3, # Low temperature so the output is consistent and factual
                max_tokens=300
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error communicating with the LLM API: {str(e)}"
