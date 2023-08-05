
# Importing libraries
from data_utils import download_all_files
from document_utils import (
    get_chunks,
    load_docs,
    load_from_docs_qdrant,
    load_from_texts_qdrant,
    divide_policies,
    map_docs_metadata,
    load_embeddings
)
import config
import pandas as pd

def main():
    # Downloading data from S3
    _ , list_names = download_all_files()
    # Splitting data by policies and saving it to raw_chunks folder
    divide_policies(list_names)
    # Loading splitted data
    docs = load_docs("raw_chunks")

    # Gettings chunks from docs
    chunks = get_chunks(docs)

    # Getting embeddings function
    embeddings = load_embeddings()
    
    try:
        load_from_docs_qdrant(chunks, embeddings)
        print(f"Chunks saved in chunks collection {config.COLLECTION_CHUNKS}: {len(chunks)}")
    except Exception as e:
        print(e)
        
    # Creating a summary set of title from the metadata
    doc_metadata = map_docs_metadata(docs)
    
    summary_df = pd.DataFrame().from_dict(doc_metadata, orient='index').reset_index(drop=False)
    titles = summary_df['title'].to_list()
    metadata = summary_df[['index','num_tokens','num_articles']].rename({"index": "source"},axis=1).to_dict(orient='records')

    # loading summary data to Qdrant
    try:
        load_from_texts_qdrant(titles, embeddings, metadata)
        print(f"Summary saved in summary collection {config.COLLECTION_SUMMARY}: {len(titles)}")
    except Exception as e:
        print(e)

    
if __name__ == "__main__":
    main()