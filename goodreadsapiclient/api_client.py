import requests
import xmltodict
from goodreadsapiclient.exception import InvalidGoodreadsURL

class GoodreadsAPIClient:
    def __init__(self):
        """Initialise the GoodreadsAPIClient object
        """
        self.goodread_base_url = "https://www.goodreads.com/book/show"
        self.route_to_xml = "/<book_id>.xml?key=<dev_key>"
        self.dev_key = "5VI9EeBQZ7z2P7SadUXFvQ"

    def get_book_details(self,book_url: str) -> dict:
        """It takes a Goodread's URL string as input and gives out information of the book

        Args:
            book_url (str): valid and full Goodread's URL string of a book

        Returns:
            dict: information of the book in form of a python dictionary
        """

        #Validate book url to be in the form of the goodreads api base format
        if type(book_url) != str or self.goodread_base_url != book_url[:len(self.goodread_base_url)]:
            raise InvalidGoodreadsURL()
        
        #Request GET method to check whether the input url is indeed valid goodread's book webpage
        try:
            api_response_status = requests.get(book_url, allow_redirects=False).status_code
        except:
            api_response_status = 404

        if api_response_status not in [200,201,202]:
            raise InvalidGoodreadsURL()
        
        #Scrap the book id from the url after the url validation is success
        book_id = []
        for char in book_url[len(self.goodread_base_url)+1:]:
            if char.isdigit():
                book_id.append(char)
            else:
                break
        
        book_id = ''.join(book_id)

        self.route_to_xml = self.route_to_xml.replace('<book_id>', book_id)
        self.route_to_xml = self.route_to_xml.replace('<dev_key>', self.dev_key)

        show_book_api = self.goodread_base_url + self.route_to_xml
        
        #Get xml data from the api, parse it and return as response
        try:
            api_response = requests.get(show_book_api, allow_redirects=False)
            api_response_json = xmltodict.parse(api_response.text)['GoodreadsResponse']['book']
            response = {}

            response['title'] = str(api_response_json['title']) if api_response_json['title'] else None
            response['average_rating'] = float(api_response_json['average_rating']) if api_response_json['average_rating'] else None
            response['ratings_count'] = int(api_response_json['ratings_count']) if api_response_json['ratings_count'] else None
            response['num_pages'] = int(api_response_json['num_pages']) if api_response_json['num_pages'] else None
            response['image_url'] = str(api_response_json['image_url']) if api_response_json['image_url'] else None
            response['publication_year'] = str(api_response_json['publication_year']) if api_response_json['publication_year'] else None
            if not api_response_json['authors']:
                response['authors'] = None
                return response
                
            author_name_list = []
            for authors in api_response_json['authors'].values():
                if 'name' in authors:
                    author_name_list.append(authors['name'])
                else:
                    for author in authors:
                        for key,value in author.items():
                            if key == 'name':
                                author_name_list.append(value)
            
            response['authors'] = ', '.join(author_name_list)

            return response
        except:
            return {}

        