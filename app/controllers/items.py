from flask import jsonify, request, current_app
from elasticsearch import NotFoundError
import os
import time

def get_item(id):
    """Get a single item by its ID."""
    try:
        es = current_app.elasticsearch
        result = es.get(index=os.getenv('ELASTICSEARCH_INDEX', 'items'), id=str(id))
        return jsonify(result['_source']), 200
    except NotFoundError:
        return jsonify({"error": "Item not found"}), 404
    except Exception as e:
        current_app.logger.error(f"Error retrieving item {id}: {str(e)}")
        return jsonify({"error": "Failed to retrieve item"}), 500

def create_or_update_item():
    """Create or update an item in the search index."""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['id', 'name', 'suggest_input']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    "error": "Invalid request body",
                    "detail": f"Missing required field: {field}"
                }), 400

        # Optional fields with defaults
        data.setdefault('description', '')
        data.setdefault('tags', [])
        data.setdefault('metadata', {})

        # Ensure id is converted to string for consistency
        item_id = str(data['id'])
        data['id'] = item_id

        es = current_app.elasticsearch
        result = es.index(
            index=os.getenv('ELASTICSEARCH_INDEX', 'items'),
            id=item_id,
            document=data,
            refresh=True  # Make the document immediately searchable
        )

        return jsonify({
            "message": "Item successfully indexed",
            "id": item_id,
            "index": result['_index']
        }), 200

    except ValueError as e:
        return jsonify({
            "error": "Invalid request body",
            "detail": str(e)
        }), 400
    except Exception as e:
        current_app.logger.error(f"Error indexing item: {str(e)}")
        return jsonify({"error": "Failed to index item"}), 500

def delete_item(item_id):
    """Delete an item from Elasticsearch by its ID."""
    try:
        es = current_app.elasticsearch
        # First check if the item exists
        if not es.exists(index=os.getenv('ELASTICSEARCH_INDEX', 'items'), id=str(item_id)):
            return jsonify({"error": "can't find item"}), 404
            
        response = es.delete(index=os.getenv('ELASTICSEARCH_INDEX', 'items'), id=str(item_id))
        if response.get('result') == 'deleted':
            return jsonify({"message": "Item successfully deleted", "id": str(item_id)}), 200
        
    except Exception as e:
        current_app.logger.error(f"Error deleting item: {str(e)}")
        return jsonify({"error": "Failed to delete item"}), 500

def search_items(query=None, zipcode=None, size=20):
    """
    Search for items using a multi-field query and sort by distance to zipcode.
    
    Args:
        query (str): The search query (required)
        zipcode (str): The zipcode to calculate distance from (required)
        size (int): Maximum number of results to return
    
    Returns:
        JSON response with search results and metadata
        400 error if required parameters are missing
    """
    try:
        # Validate required parameters
        if not query or not query.strip():
            return jsonify({
                "error": "Bad Request",
                "detail": "Query parameter is required"
            }), 400
            
        if not zipcode or not zipcode.strip():
            return jsonify({
                "error": "Bad Request",
                "detail": "Zipcode parameter is required"
            }), 400

        print(f"Searching for items with query: {query}, zipcode: {zipcode}, size: {size}")
        start_time = time.time()
        es = current_app.elasticsearch
        index_name = os.getenv('ELASTICSEARCH_INDEX', 'items')
        
        # Initialize search body with common parameters
        search_body = {
            "size": size,
            "_source": True,
            "track_total_hits": True,
            "sort": [
                {
                    "_script": {
                        "type": "number",
                        "script": {
                            "lang": "painless",
                            "source": """
                                try {
                                    def addr = doc['address'].value;
                                    if (addr == null) { return 99999; }
                                    
                                    def matcher = /\\b(\\d{5})\\b/.matcher(addr);
                                    if (!matcher.find()) { return 99999; }
                                    
                                    def itemZip = matcher.group(1);
                                    def searchZip = params.zip;
                                    
                                    return Math.abs(Integer.parseInt(itemZip) - Integer.parseInt(searchZip));
                                } catch (Exception e) {
                                    return 99999;
                                }
                            """,
                            "params": {
                                "zip": zipcode
                            }
                        },
                        "order": "asc"
                    }
                },
                "_score"
            ]
        }

        # Build the query with all search conditions
        search_body["query"] = {
            "bool": {
                "must": [
                    {
                        "bool": {
                            "should": [
                                {"match_phrase": {"name": {"query": query, "boost": 10}}},
                                {"match": {"name": {"query": query, "fuzziness": "AUTO", "boost": 3}}},
                                {"match": {"description": {"query": query, "boost": 3}}},
                                {"match": {"tags": {"query": query, "boost": 4}}},
                                {"match": {"suggest_input": {"query": query, "boost": 4}}}
                            ],
                            "minimum_should_match": 1
                        }
                    }
                ]
            }
        }

        # Execute search
        result = es.search(index=index_name, body=search_body)
        
        # Process results
        hits = result['hits']['hits']
        items = [{
            **hit['_source'],
            '_score': hit['_score'],
            'distance': hit['sort'][0] if 'sort' in hit and len(hit['sort']) > 0 and hit['sort'][0] != 99999 else None
        } for hit in hits]

        return jsonify({
            "items": items,
            "meta": {
                "total": result['hits']['total']['value'],
                "count": len(items),
                "time_ms": round((time.time() - start_time) * 1000),
                "query": query,
                "zipcode": zipcode
            }
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Error searching items: {str(e)}")
        return jsonify({
            "error": "Failed to search items",
            "detail": str(e)
        }), 500
    
