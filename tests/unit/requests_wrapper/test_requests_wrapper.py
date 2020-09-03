from unittest import TestCase
from unittest.mock import Mock, patch

from requests_wrapper.api_key_tracker import ApiKeyTracker
from requests_wrapper.requests_wrapper import RequestsWrapper


class TestRequestsWrapper(TestCase):
    def setUp(self) -> None:
        self.keys = ["apikey1", "apikey2", "apikey3"]
        self.sut = RequestsWrapper(self.keys,
                                   call_limit_per_second=1)

    def test_api_key_trackers_are_of_correct_type(self):
        # assert
        for api_key_tracker in self.sut._api_key_trackers:
            self.assertIsInstance(api_key_tracker, ApiKeyTracker)

    def test_get_least_used_key_returns_expected_api_key(self):
        # arrange
        first_key_index = self.sut._get_least_used_key_index()
        self.sut._api_key_trackers[first_key_index].log_call()
        second_key_index = self.sut._get_least_used_key_index()
        self.sut._api_key_trackers[second_key_index].log_call()

        # act
        third_key_index = self.sut._get_least_used_key_index()

        # assert
        self.assertNotEqual(self.sut._api_key_trackers[first_key_index].value,
                            self.sut._api_key_trackers[second_key_index].value)
        self.assertNotEqual(self.sut._api_key_trackers[first_key_index].value,
                            self.sut._api_key_trackers[third_key_index].value)
        self.assertNotEqual(self.sut._api_key_trackers[second_key_index].value,
                            self.sut._api_key_trackers[third_key_index].value)

    @patch("requests.get")
    def test_call_calls_get_time_in_seconds_till_available(self, mock_requests_get):
        # arrange
        mock_requests_get.return_value = Mock()
        self.sut._get_least_used_key_index = Mock(return_value=0)
        self.sut._api_key_trackers[0].get_time_in_seconds_till_available = Mock(return_value=0)

        # act
        self.sut.call(http_method="get")

        # assert
        self.sut._api_key_trackers[0].get_time_in_seconds_till_available.assert_called_once()

    @patch("time.sleep")
    @patch("requests.get")
    def test_call_calls_sleep_with_expected_inputs(self, mock_requests_get, mock_time_sleep):
        # arrange
        mock_requests_get.return_value = Mock()
        self.sut._get_least_used_key_index = Mock(return_value=0)
        self.sut._api_key_trackers[0].get_time_in_seconds_till_available = Mock(return_value=999)

        # act
        self.sut.call(http_method="get")

        # assert
        mock_time_sleep.assert_called_once_with(999)


    @patch("requests.get")
    def test_call_calls_get_least_used_key_index(self, mock_requests_get):
        # arrange
        mock_requests_get.return_value = Mock()
        self.sut._get_least_used_key_index = Mock(return_value=0)

        # act
        self.sut.call(http_method="get")

        # assert
        self.sut._get_least_used_key_index.assert_called_once()

    @patch("requests.post")
    def test_call_with_post_method(self, mock_requests_post):
        # arrange
        mock_requests_post.return_value = Mock()
        self.sut._get_least_used_key_index = Mock(return_value=0)

        # act
        self.sut.call(http_method="post")

        # assert
        mock_requests_post.assert_called_once()

    @patch("requests.put")
    def test_call_with_put_method(self, mock_requests_put):
        # arrange
        mock_requests_put.return_value = Mock()
        self.sut._get_least_used_key_index = Mock(return_value=0)

        # act
        self.sut.call(http_method="put")

        # assert
        mock_requests_put.assert_called_once()

    @patch("requests.get")
    def test_call_preserves_header_kwargs(self, mock_requests_get):
        # arrange
        mock_requests_get.return_value = Mock()
        self.sut._get_least_used_key_index = Mock(return_value=0)

        original_kwargs = {"headers": {"key1": "value1"}, "other_kwargs": "value2"}
        expected_kwargs = {"headers": {"key1": "value1",
                                       "Authorization": "apikey1"},
                           "other_kwargs": "value2"}

        # act
        self.sut.call(http_method="get", **original_kwargs)

        # assert
        mock_requests_get.assert_called_once_with(**expected_kwargs)

    @patch("requests.get")
    def test_call_calls_log_call(self, mock_requests_get):
        # arrange
        mock_requests_get.return_value = Mock()
        self.sut._get_least_used_key_index = Mock(return_value=0)
        self.sut._api_key_trackers[0].log_call = Mock()

        # act
        self.sut.call(http_method="get")

        # assert
        self.sut._api_key_trackers[0].log_call.assert_called_once()
