class GoodreadsAPIClientException(Exception):
    """Base Exception for GoodreadsAPIClient

    Args:
        Exception (): takes the Exception base class as input
    """

class InvalidGoodreadsURL(GoodreadsAPIClientException):
    """Custom exception which is to be triggered when the input url given to GoodreadsAPIClient is invalid

    Args:
        GoodreadsAPIClientException (): takes the GoodreadsAPIClientException base class as input
    """