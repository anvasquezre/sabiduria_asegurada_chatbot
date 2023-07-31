import os
from pathlib import Path

dataset_root_path = str(Path(__file__).parent.parent / 'dataset')







DATASET_ROOT_PATH = os.getenv('DATASET_ROOT_PATH', dataset_root_path)