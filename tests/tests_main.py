import unittest
from unittest.mock import patch, MagicMock
import http.client
import json
import base64
import os
import sys

# Add the directory containing 'main.py' to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '')))

# Import functions from the main script
from main import get_encoded_credentials, make_request, get_domains_and_write_to_file, visualize

class TestMainFunctions(unittest.TestCase):

    @patch.dict(os.environ, {'COLLIBRA_USERNAME': 'test_user', 'COLLIBRA_PASSWORD': 'test_password'})
    def test_get_encoded_credentials(self):
        username = os.getenv('COLLIBRA_USERNAME')
        password = os.getenv('COLLIBRA_PASSWORD')
        encoded_credentials = get_encoded_credentials(username, password)
        expected_credentials = base64.b64encode(f"{username}:{password}".encode()).decode()
        self.assertEqual(encoded_credentials, expected_credentials)

    @patch('http.client.HTTPSConnection')
    def test_make_request(self, MockHTTPSConnection):
        mock_conn = MockHTTPSConnection.return_value
        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps({"key": "value"}).encode()
        mock_conn.getresponse.return_value = mock_response

        conn = http.client.HTTPSConnection("dummy_instance")
        headers = {'Authorization': 'Basic dummy_credentials'}
        response = make_request(conn, "GET", "/dummy_endpoint", headers)
        self.assertEqual(response, {"key": "value"})

    @patch('http.client.HTTPSConnection')
    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    @patch('json.dump')
    @patch('main.visualize')
    def test_get_domains_and_write_to_file(self, mock_visualize, mock_json_dump, mock_open, MockHTTPSConnection):
        mock_conn = MockHTTPSConnection.return_value
        mock_response = MagicMock()
        mock_response.read.side_effect = [
            json.dumps({'results': [{'id': '1', 'type': {'name': 'DomainType1'}}, {'id': '2', 'type': {'name': 'DomainType2'}}]}).encode(),
            json.dumps([{'name': 'AssetType1', 'symbolData': {'color': '#FFFFFF'}}]).encode(),
            json.dumps([]).encode()
        ]
        mock_conn.getresponse.return_value = mock_response

        with patch.dict(os.environ, {'COLLIBRA_USERNAME': 'test_user', 'COLLIBRA_PASSWORD': 'test_password'}):
            get_domains_and_write_to_file()

        mock_open.assert_called_once_with("domain_asset_types.json", "w")
        mock_json_dump.assert_called_once()
        mock_visualize.assert_called_once()

    def test_visualize(self):
        # Mocking plotly express functions
        with patch('plotly.express.treemap') as mock_treemap:
            domain_asset_types = {
                "DomainType1": ["AssetType1"],
                "DomainType2": ["AssetType2"]
            }
            instance_name = "dummy_instance"
            colors = ['#FFFFFF', '#000000']

            visualize(domain_asset_types, instance_name, colors)

            mock_treemap.assert_called_once()

if __name__ == '__main__':
    unittest.main()