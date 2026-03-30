class HttpRequest:
    def __init__(self, builder):
        self.url = builder.url
        self.method = builder.method
        self.headers = builder.headers
        self.body = builder.body
        self.timeout = builder.timeout
        # ... остальные поля (аналогично)

    def __str__(self):
        return f"Request to {self.url} via {self.method}"

class HttpRequestBuilder:
    def __init__(self):
        self.url = None
        self.method = "GET"
        self.headers = {}
        self.body = None
        self.timeout = 30

    def set_url(self, url):
        self.url = url
        return self # Fluent interface

    def set_method(self, method):
        self.method = method
        return self

    def add_header(self, key, value):
        self.headers[key] = value
        return self

    def build(self):
        if not self.url:
            raise ValueError("URL is required for HTTP Request")
        return HttpRequest(self)