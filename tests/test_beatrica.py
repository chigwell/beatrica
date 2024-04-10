from unittest.mock import patch, MagicMock
import pytest
from beatrica.beatrica import review


@pytest.fixture
def mock_beatrica_diff_tracker():
    with patch('beatrica.beatrica.BeatricaDiffTracker') as mock:
        yield mock

@pytest.fixture
def mock_chat_openai():
    with patch('beatrica.beatrica.ChatOpenAI') as mock:
        mock.return_value = MagicMock()
        yield mock

@pytest.fixture
def mock_chat_mistralai():
    with patch('beatrica.beatrica.ChatMistralAI') as mock:
        mock.return_value = MagicMock()
        yield mock

@pytest.fixture
def mock_generate_summary_memory():
    with patch('beatrica.beatrica.generate_summary_memory') as mock:
        mock.return_value = MagicMock()
        yield mock


def test_review_initialization_openai(mock_beatrica_diff_tracker, mock_chat_openai):
    with pytest.raises(SystemExit) as pytest_wrapped:
        review(base_branch="main", llm_type="openai", model_name="gpt-4-0125-preview", api_key=None, max_tokens=500)
    assert pytest_wrapped.type == SystemExit
    assert pytest_wrapped.value.code == 0
