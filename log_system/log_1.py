# coding=utf8

from elasticsearch import Elasticsearch

client = Elasticsearch()

response = client.search(
    index='my-index',
    body={
        "query": {
            "bool": {
                "must": [{"match": {"title": "python"}}],
                "must_not": [{"match": {"description": "beta"}}],
                "filter": [{"term": {"category": "search"}}]
            }
        },
        "aggs": {
            "per_tag": {
                "terms": {"field": "tags"},
                "aggs": {
                    "max_lines": {"max": {"field": "lines"}}
                }
            }
        }
    }
)

for hit in response['hits']['hits']:
    print(hit['_score'], hit['_score']['title'])
