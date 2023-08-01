import os
from pathlib import Path



dataset_root_path = str(Path(__file__).parent / 'dataset')
qdrant_host = "localhost"
qdrant_host_port = "6333"


prefix_bucket = 'queplan_insurance/'
bucket_name = 'anyoneai-datasets'  
maxkeys = 9999999
tiktoken_embeds = "text-embedding-ada-002"
model_name="distiluse-base-multilingual-cased-v1"

TIKTOKEN_EMBBEDINGS_MODEL = os.getenv('TIKTOKEN_EMBBEDINGS_MODEL', tiktoken_embeds)
OPEN_AI_API_KEY=os.getenv('OPEN_AI_API_KEY')
AWS_S3=os.getenv('AWS_S3')
AWS_S3_SECRET=os.getenv('AWS_S3_SECRET')
OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")

DATASET_ROOT_PATH=os.getenv('DATASET_ROOT_PATH', dataset_root_path)
QDRANT_HOST=os.getenv('QDRANT_HOST', qdrant_host)
QDRANT_HOST_PORT=os.getenv('QDRANT_HOST_PORT', qdrant_host_port)
CHUNK_SIZE=os.getenv('CHUNK_SIZE', 2_000)
CHUNK_OVERLAP=os.getenv('CHUNK_OVERLAP', 1_000)

# From huggingface
EMBBEDINGS_MODEL=os.getenv('EMBBEDINGS_MODEL', model_name)

COLLECTION_CHUNKS=os.getenv('COLLECTION_CHUNKS', 'chunks')
COLLECTION_SUMMARY=os.getenv('COLLECTION_SUMMARY', 'summary')