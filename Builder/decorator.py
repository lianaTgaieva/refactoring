from abc import ABC, abstractmethod

# Базовый интерфейс для всех компонентов
class HttpExecutor(ABC):
    @abstractmethod
    def execute(self, request):
        pass

# Null Object - базовое выполнение (отправка запроса)
class BaseHttpRequestExecutor(HttpExecutor):
    def execute(self, request):
        print(f"--- Sending actual HTTP request to {request.url} ---")
        return "Response Data"

# Базовый Декоратор
class MiddlewareDecorator(HttpExecutor):
    def __init__(self, wrapped_executor):
        self.wrapped = wrapped_executor

    @abstractmethod
    def execute(self, request):
        pass

class LoggingMiddleware(MiddlewareDecorator):
    def execute(self, request):
        print("[Log] Starting request...")
        result = self.wrapped.execute(request)
        print("[Log] Request finished.")
        return result

class AuthMiddleware(MiddlewareDecorator):
    def execute(self, request):
        print("[Auth] Adding auth tokens...")
        return self.wrapped.execute(request)

class CacheMiddleware(MiddlewareDecorator):
    def execute(self, request):
        print("[Cache] Checking cache...")
        return self.wrapped.execute(request)