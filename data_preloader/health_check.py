import time
import config
from qdrant_client import QdrantClient

def main():
    """ Main function to check the connection to the database
    """
    client = QdrantClient(host=config.QDRANT_HOST, port=config.QDRANT_PORT)
    
    while True:
        try:
            ping = client.tr
            if ping:
                print("Connected to database")
                time.sleep(10)
                break
        except:
            print("Couldn't connect to database, container still building, trying again in 5 seconds")
            time.sleep(5)
            continue


if __name__ == "__main__":
    main()
