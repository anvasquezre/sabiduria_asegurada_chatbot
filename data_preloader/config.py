import os
from pathlib import Path


open_api_key = "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"
aws_s3 = "AKIA2JHUK4EGBAMYAYFY"
aws_s3_secret = "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"
dataset_root_path = str(Path(__file__).parent / 'dataset')
qdrant_host = "localhost"
qdrant_host_port = "6333"


prefix_bucket = 'queplan_insurance/'
bucket_name = 'anyoneai-datasets'  
maxkeys = 9999999
tiktoken_embeds = "gpt-3.5-turbo-16k"

TIKTOKEN_EMBBEDINGS_MODEL = os.getenv('TIKTOKEN_EMBBEDINGS_MODEL', tiktoken_embeds)
OPEN_AI_API_KEY=os.getenv('OPEN_AI_API_KEY', open_api_key)
AWS_S3=os.getenv('AWS_S3', aws_s3)
AWS_S3_SECRET=os.getenv('AWS_S3_SECRET', aws_s3_secret)
OPENAI_API_KEY=os.getenv("OPENAI_API_KEY", open_api_key)
DATASET_ROOT_PATH=os.getenv('DATASET_ROOT_PATH', dataset_root_path)
QDRANT_HOST=os.getenv('QDRANT_HOST', qdrant_host)
QDRANT_HOST_PORT=os.getenv('QDRANT_HOST_PORT', qdrant_host_port)
CHUNK_SIZE=os.getenv('CHUNK_SIZE', 2_000)
CHUNK_OVERLAP=os.getenv('CHUNK_OVERLAP', 1_000)


COLLECTION_CHUNKS=os.getenv('COLLECTION_CHUNKS', 'chunks')
COLLECTION_SUMMARY=os.getenv('COLLECTION_SUMMARY', 'summary')