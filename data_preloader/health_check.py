import time
import config
from pymongo import MongoClient
client = MongoClient(config.DB_URI)

def main():
    """ Main function to check the connection to the database
    """    
    while True:
        try:
            ping = client.admin.command('ping')
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
