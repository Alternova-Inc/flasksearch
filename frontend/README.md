# Flask Search Frontend - Proof of Concept

This is the frontend for the Flask Search application. It provides a user interface for searching and displaying results from the backend API. This is a **proof of concept** implementation and is not intended for production use without further development.

## Setup

1. Make sure the backend API is running (typically on http://localhost:5001)

2. Create a `.env` file in the frontend directory:
   ```
   cp .env.example .env
   ```

3. Edit the `.env` file and add your API token:
   ```
   API_URL=http://localhost:5001
   API_TOKEN=your_api_token_here
   ```
   **IMPORTANT**: Never commit your `.env` file to version control. It is already added to `.gitignore`.

4. Start the development server:
   ```
   python server.py
   ```

5. Open your browser and navigate to http://localhost:8080

## Features

- Real-time search results as you type
- Location-based search using zipcode
- Responsive design that works on mobile and desktop
- Secure API token handling via environment variables

## Development

The frontend is built with:
- HTML, CSS, and JavaScript
- Tailwind CSS for styling

### Files

- `index.html` - Main HTML file with the search interface
- `api-client.js` - Client for connecting to the backend API
- `.env.js` - Script to load environment variables
- `server.py` - Simple development server
- `.env.example` - Template for environment variables
- `.gitignore` - Prevents sensitive files from being committed

## Connecting to the Backend

The frontend connects to the backend API using the `api-client.js` file. The API URL and token are configured in the `.env` file.

By default, the frontend expects the backend API to be running at http://localhost:5001. You can change this by updating the `API_URL` in the `.env` file.

## API Endpoints

The backend provides one main endpoint:

1. **Suggestions Endpoint**
   - URL: `/api/v1/suggestions`
   - Method: GET
   - Headers: 
     - `Accept: application/json`
     - `X-API-Token: YOUR_API_TOKEN`
   - Query Parameters:
     - `query`: Search term (optional)
     - `zipcode`: Location zipcode (optional)
   - Response: JSON with items and metadata

## Response Format

The backend returns a JSON response with the following structure:

```json
{
  "items": [
    {
      "name": "Item Name",
      "description": "Item Description",
      "address": "Item Address",
      "tags": ["tag1", "tag2"],
      "id": "1",
      "_score": 0.0
    }
  ],
  "meta": {
    "count": 10,
    "total": 100,
    "query": "search term",
    "zipcode": "10001",
    "time_ms": 50
  }
}
```

## Proof of Concept Limitations

As this is a proof of concept, there are several limitations:

1. Limited error handling and user feedback
2. No pagination for large result sets
3. Basic styling and UI components
4. No automated tests
5. Simple development server not suitable for production

## Future Improvements

For a production-ready application, consider:

1. Adding proper error handling and user feedback
2. Implementing pagination for large result sets
3. Enhancing the UI with more interactive components
4. Adding automated tests
5. Using a production-grade web server
6. Implementing user authentication
7. Adding analytics and monitoring 