import api_client

def exec_cli_interface():
    book_url = input("Enter a goodread's book url: ")

    print("-" * 50)
    dict_response_from_api = api_client.GoodreadsAPIClient().get_book_details(book_url)
    for key, value in dict_response_from_api.items(): 
        if value:
            print ("{:<20} : {:<20}".format(key.upper(),value))
        else:
            print ("{:<20} : ".format(key.upper()))
    
    print("-" * 50)

if __name__ == "__main__":
    exec_cli_interface()
    