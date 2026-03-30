# 1. Используем Builder
       .set_url("https://api.example.com")
       .set_method("POST")
       .add_header("Content-Type", "application/json")
       .build())

pipeline = BaseHttpRequestExecutor()

# Оборачиваем его в нужные декораторы
pipeline = LoggingMiddleware(pipeline)
pipeline = AuthMiddleware(pipeline)
pipeline = CacheMiddleware(pipeline)

# 3. Выполняем
final_result = pipeline.execute(req)