from elasticsearch import Elasticsearch


def create_index(es: Elasticsearch):

        es.indices.create(
            index="users",
            body={
                "settings": {
                    "analysis": {
                        "tokenizer": {
                            "ngram_tokenizer": {
                                "type": "ngram",
                                "min_gram": 2,
                                "max_gram": 3,
                                "token_chars": ["letter", "digit"]
                            }
                        },
                        "analyzer": {
                            "ngram_analyzer": {
                                "type": "custom",
                                "tokenizer": "ngram_tokenizer",
                                "filter": ["lowercase"]
                            }
                        }
                    }
                },
                "mappings": {
                    "properties": {
                        "category": {
                            "type": "text",
                            "analyzer": "ngram_analyzer",
                            "fields": {
                                "keyword": {
                                    "type": "keyword"
                                }
                            }
                        },
                        "company": {
                            "type": "text",
                            "analyzer": "ngram_analyzer",
                            "fields": {
                                "keyword": {
                                    "type": "keyword"
                                }
                            }
                        }
                    }
                }
            }
        )