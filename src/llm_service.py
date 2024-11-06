import os
from anthropic import Anthropic
from typing import Dict, Any
from datetime import date, datetime

SYSTEM_PROMPT = '''
You are a helpful vacation request parser. Convert natural language requests into structured commands.

Available commands: register_vacation, update_vacation, delete_vacation, list_vacations

Examples:
Input: "Register a vacation for next Monday"
Output: {"command": "register_vacation", "start_date": "2024-11-11", "end_date": null, "comment": null}

Input: "I want to take the week after Christmas off"
Output: {"command": "register_vacation", "start_date": "2024-12-26", "end_date": "2024-12-31", "comment": "Christmas vacation"}

Input: "Delete vacation number 1234"
Output: {"command": "delete_vacation", "vacation_id": 1234}

Input: "Show me my vacations"
Output: {"command": "list_vacations"}

Only return valid JSON, no other text.
'''

class LLMService:
    def __init__(self):
        self.client = Anthropic(
            api_key=os.getenv("ANTHROPIC_API_KEY"),
        )

    def system_prompt(self):
        current_date = datetime.now().strftime("%Y-%m-%d")
        return f"{SYSTEM_PROMPT}\nToday's date is {current_date}."

    def parse_vacation_command(self, user_input: str) -> Dict[str, Any]:
        """Parse natural language input into structured vacation command"""
        
        message = self.client.messages.create(
            max_tokens=1024,
            system=self.system_prompt(),
            model="claude-3-5-sonnet-20241022",
            messages=[
                {
                    "role": "user",
                    "content": user_input,
                }
            ]
        )
        return message.content[0].text
