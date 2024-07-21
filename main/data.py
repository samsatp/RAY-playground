from minio.error import S3Error
from minio import Minio
import pandas as pd
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class StorageManager:
    def __init__(self) -> None:
        self.endpoint = 'http://storage:9000'
        self.client = Minio(endpoint=self.endpoint,
                            access_key=os.getenv('MINIO_ROOT_USER'),
                            secret_key=os.getenv('MINIO_ROOT_PASSWORD'),
                            secure=False)
        self.default_bucket_name = os.getenv('MINIO_DEFAULT_BUCKETS')
    
    def get_object(self, object_name)->pd.DataFrame | None:
        try:
            df = pd.read_csv(
                f"s3://{self.default_bucket_name}/{object_name}",
                storage_options={
                    "key": os.getenv('MINIO_ROOT_USER'),
                    "secret": os.getenv('MINIO_ROOT_PASSWORD'),
                    "client_kwargs": {"endpoint_url": self.endpoint}
                }
            )
            return df
        except S3Error as e:
            logger.error(f"S3Error: {e}")
            return None
        except FileNotFoundError as e:
            logger.error(f"FileNotFoundError, {e}")
            return None
        
    def put_object(self):
        # 1. Download data from: https://www.kaggle.com/datasets/gorororororo23/european-restaurant-reviews
        os.system('bash ./get_data.sh')
        file_path = os.path.join('data','European Restaurant Reviews.csv')
        assert os.path.exists(file_path), 'Incorrect filename'

        # 2. upload to Storage
        file_path = "data/European Restaurant Reviews.csv"  # Path to your CSV file
        object_name = "European Restaurant Reviews.csv"  # Name of the object to be saved in the bucket

        result = self.client.fput_object(
            bucket_name=self.default_bucket_name,
            object_name=object_name,
            file_path=file_path)
        return result.location

    


def process_data(path:str, embedding_model = "all-MiniLM-L12-v2"):
    #1. read the CSV data and transform into a list of (reviews, sentiment) tuples
    import pandas as pd
    df = pd.read_csv(path)
    reviews, label = df.Review.values, df.Sentiment.values

    #2. transform the reviews to vectors ready to train
    from sentence_transformers import SentenceTransformer
    import torch
    model = SentenceTransformer(embedding_model)

    review_embeddings = model.encode(reviews)
    label = torch.from_numpy(label.str.lower() == 'positive')

    return zip(review_embeddings, label)