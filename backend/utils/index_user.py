from typing import List
from elasticsearch import Elasticsearch
from Backend.backend.schemas.search.search_schema import UserSearchResult
from Backend.backend.utils.es_setup import create_index

es = Elasticsearch("http://elasticsearch:9200")

def index_users(users: List[UserSearchResult]):
    if not es.indices.exists(index="users"):
        create_index(es)
    for user in users:
        user_dict = user.dict()
        es.index(index="users", id=user.id, body=user_dict)
