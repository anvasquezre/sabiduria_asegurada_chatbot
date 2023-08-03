import qdrant_client, grpc
from langchain.vectorstores import Qdrant
import os
import config
from langchain.embeddings import HuggingFaceEmbeddings, SentenceTransformerEmbeddings
from typing import Any, List, Optional

def load_embeddings(model_name:str = config.EMBBEDINGS_MODEL ) -> Any:
    """ Load HuggingFaceEmbeddings

    Returns:
        Any: embeddings model
    """    
    embeddings = HuggingFaceEmbeddings(model_name=model_name)
    return embeddings


def connect_db(collection:str, 
               distance_strategy:str = "COSINE",
               embeddings = load_embeddings()) -> Qdrant:
    """ Connect to Qdrant collection

    Args:
        collection (str): Name of collection
        distance_strategy (str, optional): Distance Estrategy #EUCLID, #COSINE, #DOT. Defaults to "COSINE".
    """    

    client = qdrant_client.QdrantClient(
        host=config.QDRANT_HOST,
        port=config.QDRANT_HOST_PORT,
        grpc_port=6334, 
        prefer_grpc=True
        )


    db = Qdrant(client=client,
                collection_name=collection,
                embeddings=embeddings, 
                distance_strategy=distance_strategy)
    return db

def aconnect_db(collection:str, 
               distance_strategy:str = "COSINE",
               embeddings = load_embeddings()) -> Qdrant:
    """ Connect to Qdrant collection

    Args:
        collection (str): Name of collection
        distance_strategy (str, optional): Distance Estrategy #EUCLID, #COSINE, #DOT. Defaults to "COSINE".
    """    
    client = qdrant_client.QdrantClient(
        host=config.QDRANT_HOST,
        port=config.QDRANT_HOST_PORT,
        grpc_port=6334, 
        prefer_grpc=True
        )

    db = Qdrant(client=client,
                collection_name=collection,
                embeddings=embeddings, 
                distance_strategy=distance_strategy)
    return db