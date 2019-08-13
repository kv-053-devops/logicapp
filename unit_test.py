import unittest
# import requests
import json

from logic_server import app
app.testing = True

get_root_test_string = "The root uri"
logic_app_url = "/logic/query_data"
http_code_api_method_get = 405
http_code_api_method_post = 400


class TestApi(unittest.TestCase):
    def test_root_uri(self):
        with app.test_client() as client:
            resp = client.get('/')
            clinet_output = str(resp.data.decode('utf-8'))
            self.assertTrue(clinet_output.startswith(get_root_test_string))

    def test_logic_api_method_get(self):
        with app.test_client() as client:
            resp = client.get(logic_app_url)
            status_output = resp._status_code
            self.assertEqual(status_output, http_code_api_method_get)

    def test_logic_api_method_post(self):
        with app.test_client() as client:
            resp = client.post(logic_app_url)
            status_output = resp._status_code
            self.assertEqual(status_output, http_code_api_method_post)


if __name__ == '__main__':
    unittest.main()