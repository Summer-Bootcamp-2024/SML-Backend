from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from Backend.backend.crud.relation_crud import get_friends
from Backend.backend.schemas.search.search_schema import UserSearchResult, SearchFilters
from fastapi import HTTPException
from Backend.backend.utils.index_user import es


async def search_users_by_filters(filters: SearchFilters, session: AsyncSession) -> List[UserSearchResult]:
    user_id = filters.user_id
    search = filters.search
    filter_by = filters.filter_by

    # 친구 목록 가져옴
    friends = await get_friends(user_id, session)
    if not friends:
        return []

        # 1촌 친구 목록 가져옴 (중복 제거)
    first_friend_ids = {friend.friend_id for friend in await get_friends(user_id, session, max_depth=1)}

    # 1촌을 제외한 2촌 친구 ID 리스트 생성 (중복 제거)
    second_friend_ids = list(set(friend.friend_id for friend in friends) - first_friend_ids)

    # Elasticsearch 인덱스 매핑 확인
    index_mapping = es.indices.get_mapping(index="users")
    print(index_mapping)
    # Elasticsearch 쿼리 구성
    try:
        must_query = {
            "multi_match": {
                "query": search,
                "fields": [filter_by] if filter_by else ["category", "company", "job"],  # 필터링 조건 적용
                "analyzer": "ngram_analyzer"
            }
        }

        query = {
            "query": {
                "bool": {
                    "must": [must_query],
                    "filter": [
                        {
                            "terms": {
                                "id": second_friend_ids
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

