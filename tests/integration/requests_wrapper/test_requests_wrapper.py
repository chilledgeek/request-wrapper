from unittest import TestCase, skip

from requests_wrapper.requests_wrapper import RequestsWrapper


class TestRequestsWrapper(TestCase):
    def setUp(self) -> None:
        self.sut = RequestsWrapper

    @skip("Manual tests...replace placeholders with actual values!")
    def test_get_works_with_test_api_service(self):
        temp_instance = self.sut(
            api_keys=["<api_key>"],
            call_limit_per_second=2
        )

        for _ in range(10):
            response = temp_instance.call("get",
                                          api_key_header="Authorization",
                                          url="<my_url>",
                                          params={"q": "<my_query_term>"}
                                          )

            self.assertEqual(response.status_code, 200)

    @skip("Manual tests...replace placeholders with actual values!")
    def test_get_works_with_test_api_service_using_multiple_api_keys(self):
        temp_instance = self.sut(
            api_keys=["<api_key1>", "<api_key2>", "<api_key3>", "<api_key4>"],
            call_limit_per_second=100
        )

        for _ in range(620):
            response = temp_instance.call("get",
                                          api_key_header="Authorization",
                                          url="<my_url>",
                                          params={"q": "<my_query_term>"}
                                          )

            self.assertEqual(response.status_code, 200)
