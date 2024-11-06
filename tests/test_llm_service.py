import pytest
from src.llm_service import LLMService
import json
from datetime import datetime, timedelta

def test_connection_helper(llm_service: LLMService) -> bool:
    """Helper function to test API connection"""
    message = llm_service.client.messages.create(
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": "Say 'Connection successful!' if you can read this.",
            }
        ],
        model="claude-3-5-sonnet-20241022",

    )
    return "Connection successful!" in message.content[0].text

@pytest.fixture
def llm_service():
    return LLMService()

def test_api_connection(llm_service):
    """Test that we can connect to Claude API"""
    assert test_connection_helper(llm_service)

def test_parse_simple_vacation_registration(llm_service):
    """Test parsing a simple vacation registration command"""
    # Get next Monday's date for comparison
    today = datetime.now()
    next_monday = today + timedelta(days=(7 - today.weekday()))
    next_monday_str = next_monday.strftime("%Y-%m-%d")

    # Test the parser
    result = llm_service.parse_vacation_command("Register a vacation for next Monday")
    result_dict = json.loads(result)

    assert result_dict["command"] == "register_vacation"
    assert result_dict["start_date"] == next_monday_str
    assert result_dict["end_date"] is None
