import unittest
from unittest.mock import Mock, patch
import sys
sys.path.append('../')
from goodreadsapiclient.api_client import GoodreadsAPIClient
from goodreadsapiclient.exception import InvalidGoodreadsURL

class TestGoodreadsAPIClient(unittest.TestCase):
    def test_book_url_type(self):
        """Raise InvalidGoodreadsURL Exception when the datatype of the input url is not a string 
        """
        self.assertRaises(InvalidGoodreadsURL, GoodreadsAPIClient().get_book_details,0)
        self.assertRaises(InvalidGoodreadsURL, GoodreadsAPIClient().get_book_details,0.2)
        self.assertRaises(InvalidGoodreadsURL, GoodreadsAPIClient().get_book_details,True)

    def test_book_url_diff(self):
        """Raise InvalidGoodreadsURL Exception when the form of the input url is not of base goodread's url
        """
        self.assertRaises(InvalidGoodreadsURL, GoodreadsAPIClient().get_book_details,"https://www.gooreads.com/book/show/22034.The_Godfather")
        self.assertRaises(InvalidGoodreadsURL, GoodreadsAPIClient().get_book_details,"https://www.goodreads.com/book1/show/12177850-a-song-of-ice-and-fire")
        self.assertRaises(InvalidGoodreadsURL, GoodreadsAPIClient().get_book_details,"https://www.google.com")

    def test_book_url_invalid(self):
        """Raise InvalidGoodreadsURL Exception when the form of the input url is not a valid goodread's book webpage url
        """
        self.assertRaises(InvalidGoodreadsURL, GoodreadsAPIClient().get_book_details,"https://www.goodreads.com/book/show/2204.The_Godfather")
        self.assertRaises(InvalidGoodreadsURL, GoodreadsAPIClient().get_book_details,"https://www.goodreads.com/book/show/The_Godfather")

    @patch('requests.get',side_effect=Exception())
    def test_api_exception(self,mock_except):
        """Raise InvalidGoodreadsURL Exception when the goodread's book webpage url returns an Generic Exception
        """
        self.assertRaises(InvalidGoodreadsURL, GoodreadsAPIClient().get_book_details,"https://www.goodreads.com/book/show/53152636-mexican-gothic")
    
    @patch('requests.get')
    def test_api_status(self,mock_get):
        """Raise InvalidGoodreadsURL Exception when the goodread's book webpage url does not return success response
        """
        mock_get.return_value.status_code = 404
        self.assertRaises(InvalidGoodreadsURL, GoodreadsAPIClient().get_book_details,"https://www.goodreads.com/book/show/53152636-mexican-gothic")

        mock_get.return_value.status_code = 302
        self.assertRaises(InvalidGoodreadsURL, GoodreadsAPIClient().get_book_details,"https://www.goodreads.com/book/show/53152636-mexican-gothic")

    @patch('requests.get')
    def test_empty_xml_data(self,mock_get_xml):
        """Returns {} when the xml data from the api response text is an empty string
        """
        mock_get_xml.return_value.status_code = 200
        mock_get_xml.return_value.text = ""
        api_response = GoodreadsAPIClient().get_book_details("https://www.goodreads.com/book/show/29236299-gemina")
        self.assertDictEqual({},api_response)

    def test_missing_value(self):
        """Return key's value as None when the required key doesn't exist in xml data
        """
        api_response = GoodreadsAPIClient().get_book_details("https://www.goodreads.com/book/show/53152636-mexican-gothic")
        missing_value = api_response['publication_year']
        self.assertIsNone(missing_value)
    
    def test_multiple_value(self):
        """Return all the authors name joined with comma when the book has multiple authors
        """
        api_response = GoodreadsAPIClient().get_book_details("https://www.goodreads.com/book/show/44890073-all-the-ways-we-said-goodbye")
        multiple_value = api_response['authors']
        self.assertEqual("Beatriz Williams, Lauren Willig, Karen White",multiple_value)

if __name__ == '__main__':
   unittest.main()