from datetime import datetime, timedelta
from unittest import TestCase
from unittest.mock import Mock

from requests_wrapper.api_key_tracker import ApiKeyTracker


class TestApiKeyTracker(TestCase):
    def setUp(self) -> None:
        self.sut = ApiKeyTracker("my_api_key", 5)

    def test_log_call_modifies_last_called_time(self):
        # arrange
        start_time = Mock(datetime)
        self.sut.last_called_time = start_time

        # act
        self.sut.log_call()

        # assert
        self.assertNotEqual(self.sut.last_called_time, start_time)

    def test_log_call_modifies_call_count(self):
        # arrange
        start_time = Mock(datetime)
        self.sut.last_called_time = start_time
        call_count = int(self.sut.call_count)

        # act
        self.sut.log_call()

        # assert
        self.assertEqual(self.sut.call_count,call_count + 1)

    def test_get_time_in_seconds_till_available_returns_zero_if_not_called_before(self):
        # arrange
        self.sut.last_called_time = None

        # act
        output = self.sut.get_time_in_seconds_till_available()

        # assert
        self.assertEqual(output, 0)

    def test_get_time_in_seconds_till_available_returns_zero_if_waited_long_enough(self):
        # arrange
        self.sut.last_called_time = datetime.now() - timedelta(seconds=10)

        # act
        output = self.sut.get_time_in_seconds_till_available()

        # assert
        self.assertEqual(output, 0)

    def test_get_time_in_seconds_till_available_returns_zero_if_no_call_limit(self):
        # arrange
        self.sut.call_limit_per_second = 0
        self.sut.last_called_time = datetime.now()

        # act
        output = self.sut.get_time_in_seconds_till_available()

        # assert
        self.assertEqual(output, 0)

    def test_get_time_in_seconds_till_available_returns_non_zero_if_not_waited_long_enough(self):
        # arrange
        self.sut.call_limit_per_second = 0.01
        self.sut.last_called_time = datetime.now()

        # act
        output = self.sut.get_time_in_seconds_till_available()

        # assert
        self.assertGreater(output, 0)
