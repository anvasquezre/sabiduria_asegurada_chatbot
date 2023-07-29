
# Importing libraries

from typing import Dict, List, Optional, Union

import config
import pandas as pd
import yfinance as yf
from pymongo import MongoClient, collection
import pymongo


def get_data(tickers: List[str], kwargs: Optional[Dict] = {}) -> pd.DataFrame:
    # TODO Check new sources for data initialization
    """This function gets the data from yahoo finance and returns a dataframe to initialise the database

    Args:
        tickers (str): tickers, e.g. "AAPL MSFT"
        kwargs (dict, optional): kwargs for yfinance. Defaults to {}.

    Returns:
        pd.DataFrame: dataframe with the data
    """
    # Downloading the data
    data = yf.download(tickers=tickers, period="7d", interval="1m", **kwargs)
    data = data.stack().reset_index()
    cols = ["Datetime", "level_1", "Close", "Volume"]
    data = data[cols].copy()
    data.columns = ["time", "stock_id", "value", "volume"]
    return data


def save_data(data: pd.DataFrame, table_name:str) -> None:
    """ This function saves the data to the database

    Args:
        data (pd.DataFrame): pd.DataFrame with the data
        table_name (str): name of the collection

    Returns:
        None: 
    """    
    dict_data = data[["time","value","volume"]].copy()
    # Renaming time column to timestamp to match the timeseries format in mongodb
    dict_data.rename(columns = {"time":"timestamp"}, inplace = True)
    meta_data = data[["stock_id"]].copy()
    dict_data["metadata"] = meta_data.to_dict(orient = "records")
         
    try:
        # Starting the session and saving the data
        with client.start_session(causal_consistency=True) as session:
            collection = db[table_name]
            collection.insert_many(dict_data.to_dict(orient = "records")
                                   , session=session
                                   )
            print("Data saved to database in collection: ", table_name)
    except Exception as e:
        return print("Error saving data to database: ", e)
    
    return 


def save_tickers(tickers: Dict, asset_type:str,collection_name:str = config.TICK_COLLECTION ) -> None:
    """This function saves the tickers to the database

    Args:
        tickers (dict): dictionary with the tickers
    """

    ticks = pd.DataFrame().from_dict(tickers, orient="index")
    ticks.reset_index(inplace=True, drop=False)
    ticks.columns = ["ticker", "yahoo_ticker"]
    ticks["asset_type"] = asset_type
    
    with client.start_session(causal_consistency=True) as session:
        collection = db[collection_name]
        collection.insert_many(ticks.to_dict(orient="records"), session=session)
    
    
                    
def main():
    # Get data
    try: 
        tickers_crypto = config.TICKERS_CRYPTO
        tickers_forex = config.TICKERS_FOREX

        save_tickers(tickers_crypto, "crypto")
        save_tickers(tickers_forex, "forex")
        
        tickers = list(tickers_crypto.values())
        tickers.extend(list(tickers_forex.values()))
        
        data = get_data(tickers)
        save_data(data, config.REAL_TIME_COLLECTION)

        return print("Data Initialized and saved to database")
    except Exception as e:
        return print("Error initializing data: ", e)



if __name__ == "__main__":
    ####DATABASE NAME ###########
    print(config.DB_NAME)
    client = MongoClient(config.DB_URI)
    db = client[config.DB_NAME]
    # Creating the collections
    db.create_collection(
        config.REAL_TIME_COLLECTION,
        timeseries =  {
            "timeField" : "timestamp",
            "metaField": "metadata",
            "granularity": "seconds"
        },
    )

    db.create_collection(
        config.CANDLE_VALUES_COLLECTION,
        timeseries =  {
            "timeField" : "timestamp",
            "metaField": "metadata",
            "granularity": "seconds"
        }
    )

    db.create_collection(
        config.CANDLE_SIGNALS_COLLECTION,
        timeseries =  {
            "timeField" : "timestamp",
            "metaField": "metadata",
            "granularity": "seconds"
        }
    )

    db.create_collection(
        config.SCORES_COLLECTION,
        timeseries =  {
            "timeField" : "timestamp",
            "metaField": "metadata",
            "granularity": "seconds"
        }
    )

    main()
    # Creating the indexes
    collection = db[config.REAL_TIME_COLLECTION]
    collection.create_index([("timestamp", pymongo.DESCENDING), ("metadata.stock_id")])
