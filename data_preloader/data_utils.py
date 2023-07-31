from typing import Optional, Tuple
import config
import boto3
from pathlib import Path
import os


def get_s3_client() -> boto3.client:
    """ Connect to S3 bucket based on config.py

    Returns:
        boto3.client: S3 client
    """    
    return boto3.client(
        's3',
        aws_access_key_id=config.AWS_S3,
        aws_secret_access_key=config.AWS_S3_SECRET,
    )
    
def get_s3_resource() -> boto3.resource:
    """ Connect to S3 bucket resource based on config.py

    Returns:
        boto3.resource: S3 resource
    """    
    return boto3.resource(
        's3',
        aws_access_key_id=config.AWS_S3,
        aws_secret_access_key=config.AWS_S3_SECRET,
    )
    
    
def get_filepaths(bucket_name:Optional[str] = config.bucket_name, 
                  prefix: Optional[str] = config.prefix_bucket,
                  maxkeys: Optional[int]= config.maxkeys) -> Tuple[list[str], list[str]]:
    """ Get list of filepaths from S3 bucket

    Args:
        bucket_name (str): S3 bucket name
        prefix (str): S3 bucket prefix
        maxkeys (int): max number of keys to retrieve

    Returns:
        list: Tuple of list of saving filepaths, list of keys in S3 bucket
    """    
    s3_client = get_s3_client()
    response = s3_client.list_objects(Bucket=bucket_name, Prefix=prefix, MaxKeys=maxkeys)['Contents']
    
    dataset_path = str(Path(config.DATASET_ROOT_PATH) / "raw_pdfs")
    
    if not os.path.exists(dataset_path):
        os.makedirs(dataset_path)
        
    list_filepath = []
    list_keys = []
    
    for s3_key in response:
        s3_object = s3_key['Key']
        
        path, filename = os.path.split(s3_object)
        
        filepath = os.path.join(dataset_path, filename)
        list_filepath.append(filepath) 
        list_keys.append(s3_object)
    
    return list_filepath, list_keys

def download_resources(list_filepath: list[str], 
                       list_keys: list[str], 
                       bucket_name:Optional[str] = config.bucket_name) -> None:
    """ Download resources from S3 bucket

    Args:
        list_filepath (list): list of saving filepaths
        list_keys (list): list of keys in S3 bucket
        bucket_name (str): S3 bucket name
    """    
    s3_resource = get_s3_resource()
    
    for key,path in zip(list_keys[1:],list_filepath[1:]):
        if os.path.exists(path):
            print(f"File already downloaded: {path}")
        else:
            s3_resource.meta.client.download_file(bucket_name, key,path)
            
def list_files(dataset_path: Optional[str] = str(Path(config.DATASET_ROOT_PATH) /  "raw_pdfs")) -> list[str]:
    """ List files in dataset_path

    Args:
        dataset_path (str): path to dataset

    Returns:
        list: list of files in dataset_path
    """    
    return os.listdir(dataset_path)


def download_all_files() -> None:
    s3_client = get_s3_client()
    s3_resource = get_s3_resource()
    list_filepath, list_keys = get_filepaths()
    download_resources(list_filepath, list_keys)
    print("Data downloaded successfully \n\n","\n".join(list_files()))
    return list_filepath, list_files()