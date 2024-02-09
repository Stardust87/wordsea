import os

MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
LLAMACPP_URL = os.getenv("LLAMACPP_URL", "http://localhost:8080")
