from typing import List, Set
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from Backend.backend.models.friends import Friend
from Backend.backend.schemas.friend.response.friends_related import FriendsFind
from Backend.backend.crud.relation_crud import get_friends
from Backend.backend.schemas.search.search_schema import UserSearchResult, SearchFilters
from fastapi import HTTPException
from elasticsearch import Elasticsearch
from Backend.backend.utils.index_user import es


async def search_users_by_filters(filters: SearchFilters, session: AsyncSession) -> List[UserSearchResult]:
    user_id = filters.user_id
    search = filters.search

    # 친구 목록 가져옴
    friends = await get_friends(user_id, session)
    if not friends:
        return []

    # 친구 ID 리스트 생성
    friend_ids = [friend.friend_id for friend in friends]

    # 중복 제거
    friend_ids = list(set(friend_ids))

    # Elasticsearch 인덱스 매핑 확인
    index_mapping = es.indices.get_mapping(index="users")

    # Elasticsearch 쿼리 구성
    try:
        query = {
            "query": {
                "bool": {
                    "must": [
                        {
                            "multi_match": {
                                "query": search,
                                "fields": ["category", "company"],
                                "analyzer": "ngram_analyzer"  # n-gram 검색 분석기 사용
                            }
                        }
                    ],
                    "filter": [
                        {
                            "terms": {
                                "id": friend_ids
                            }
                        }
                    ]
                }
            }
        }

        res = es.search(index="users", body=query)

        if res['hits']['total']['value'] == 0:
            return []

        hits = res['hits']['hits']
        results = []
        seen_ids = set()
        for hit in hits:
            source = hit['_source']
            if source['id'] not in seen_ids:
                result = UserSearchResult(
                    id=source['id'],
                    name=source.get('name', ''),
                    region=source.get('region', ''),
                    gender=source.get('gender', ''),
                    age=source.get('age'),
                    job=source.get('job', ''),
                    company=source.get('company', ''),
                    category=source.get('category', ''),
                    image_url=source.get('image_url')
                )
                results.append(result)
                seen_ids.add(source['id'])

        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

