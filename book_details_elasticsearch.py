from elasticsearch5 import Elasticsearch
import json
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def store_book_details(search_book: str, book_dict: dict) -> None:
    elasticsearch = Elasticsearch()

    elasticsearch.index(index='book_details', doc_type='books', id=search_book.lower(), body=json.dumps(book_dict))
    logging.info('Details stored...')