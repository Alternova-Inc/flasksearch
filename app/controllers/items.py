from flask import jsonify, request, current_app
from elasticsearch import NotFoundError
import os

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
        query (str): The search query
        zipcode (str): The zipcode to calculate distance from
        size (int): Maximum number of results to return
    
    Returns:
        JSON response with search results and metadata
    """
    try:
        start_time = current_app.elasticsearch.options(request_timeout=30).info()['version']['build_timestamp']
        import time
        start_time = time.time()
        
        es = current_app.elasticsearch
        index_name = os.getenv('ELASTICSEARCH_INDEX', 'items')
        
        # Base query
        search_body = {
            "size": size,
            "_source": True,
            "track_total_hits": True
        }
        
        # Build query based on parameters
        if query:
            # Multi-match query across multiple fields with boosting
            search_body["query"] = {
                "bool": {
                    "should": [
                        # Exact matches in name get highest priority
                        {"match_phrase": {"name": {"query": query, "boost": 10}}},
                        # Fuzzy matching on name
                        {"match": {"name": {"query": query, "fuzziness": "AUTO", "boost": 5}}},
                        # Match on description
                        {"match": {"description": {"query": query, "boost": 3}}},
                        # Match on tags
                        {"match": {"tags": {"query": query, "boost": 4}}},
                        # Match on suggest_input (for autocomplete)
                        {"match": {"suggest_input": {"query": query, "boost": 2}}}
                    ],
                    "minimum_should_match": 1
                }
            }
        else:
            # If no query, return all documents
            search_body["query"] = {"match_all": {}}
        
        # Sort by distance if zipcode is provided
        if zipcode and zipcode.strip():
            # Check if the item has location data
            search_body["sort"] = [
                {
                    "_geo_distance": {
                        "location": {
                            "zip": zipcode
                        },
                        "order": "asc",
                        "unit": "km",
                        "ignore_unmapped": True
                    }
                },
                "_score"  # Secondary sort by relevance score
            ]
        else:
            # Otherwise sort by score
            search_body["sort"] = ["_score"]
        
        # Execute search
        result = es.search(index=index_name, body=search_body)
        
        # Calculate time taken
        end_time = time.time()
        time_taken_ms = round((end_time - start_time) * 1000)
        
        # Format response
        hits = result['hits']['hits']
        total_hits = result['hits']['total']['value']
        
        # Extract items from hits
        items = []
        for hit in hits:
            item = hit['_source']
            item['_score'] = hit['_score']
            
            # Add distance if available
            if zipcode and 'sort' in hit and len(hit['sort']) > 0:
                item['distance_km'] = hit['sort'][0]
                
            items.append(item)
        
        # Return formatted response
        return jsonify({
            "items": items,
            "meta": {
                "total": total_hits,
                "count": len(items),
                "time_ms": time_taken_ms,
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
    
