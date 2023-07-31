import time
import config
from qdrant_client import QdrantClient
import os

def main():
    """ Main function to check the connection to the database
    """
    client = QdrantClient(host=config.QDRANT_HOST, port=config.QDRANT_HOST_PORT)
    
    while True:
        try:
            test = client.get_collections()
            if test:
                print("Connected to database")
                time.sleep(5)
                break
        except:
            print("Couldn't connect to database, container still building, trying again in 5 seconds")
            time.sleep(30)
            continue


if __name__ == "__main__":
    print("Starting health check")
    print("Host: ", os.getenv('QDRANT_HOST')," Port: ", os.getenv('QDRANT_HOST_PORT'))
    main()
