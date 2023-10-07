import pandas as pd
import pytest
from f4 import Cleanliness_Analysing
from unittest.mock import create_autospec


def mock_read_csv(*args, **kwargs):
    data = {
        'id': [1, 2, 3],
        'name': ['a', 'b', 'c'],
        'property_type': ['Apartment', 'House', 'Condo'],
        'listing_id': [1, 2, 3],
        'reviewer_name': ['Alice', 'Bob', 'Charlie'],
        'comments': ['Very clean!', 'Somewhat clean', 'Not clean at all'],
    }
    return pd.DataFrame(data)

@pytest.fixture
def frame(mocker):
    mocker.patch("f4.Cleanliness_Analysing.setup_ui")  # Mock setup_ui
    instance = create_autospec(Cleanliness_Analysing, instance=True)  # Create a mock instance of the class
    mocker.patch.object(instance, 'figure', create=True)  # Mock figure attribute after instance creation
    return instance


@pytest.fixture
def mock_dataframe(mocker):
    mocker.patch('pandas.read_csv', side_effect=mock_read_csv)  # Mock read_csv method

def test_update_chart(frame, mock_dataframe):
    selected_keyword = "clean"
    # Test will fail if any exception occurs in the method
    frame.update_chart(selected_keyword)

@pytest.fixture
def mock_draw_chart_data():
    data = {
        'property_type': ['Apartment', 'House'],
        'number_of_people': [5, 10]
    }
    return pd.DataFrame(data)

def test_draw_chart(frame, mock_draw_chart_data):
    selected_keyword = "clean"
    # Test will fail if any exception occurs in the method
    frame.draw_chart(mock_draw_chart_data, selected_keyword)
