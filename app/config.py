import os

qdrant_host = "localhost"
qdrant_host_port = "6333"
model_name = "distiluse-base-multilingual-cased-v1"

QDRANT_HOST=os.getenv('QDRANT_HOST', qdrant_host)
QDRANT_HOST_PORT=os.getenv('QDRANT_HOST_PORT', qdrant_host_port)
COLLECTION_CHUNKS=os.getenv('COLLECTION_CHUNKS', 'chunks')
COLLECTION_SUMMARY=os.getenv('COLLECTION_SUMMARY', 'summary')


EMBBEDINGS_MODEL=os.getenv('EMBBEDINGS_MODEL', model_name)


OPENAI_MODEL = "gpt-3.5-turbo-16k"