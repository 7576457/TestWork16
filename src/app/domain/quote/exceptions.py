class QuoteNotFound(Exception):
    def __init__(self, message: str = "No quotes found"):
        super().__init__(message)


class AuthorNotFound(QuoteNotFound):
    def __init__(self, author: str):
        message = f"No quotes found for author '{author}'"
        super().__init__(message)


class TagNotFound(QuoteNotFound):
    def __init__(self, tag: str):
        message = f"No quotes found with tag '{tag}'"
        super().__init__(message)


class AuthorAndTagNotFound(QuoteNotFound):
    def __init__(self, author: str, tag: str):
        message = f"No quotes found for author '{author}' with tag '{tag}'"
        super().__init__(message)
