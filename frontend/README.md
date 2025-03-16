# Flask Search Frontend

This is the frontend for the Flask Search application. It provides a user interface for searching and displaying suggestions from the backend API.

## Setup

1. Make sure the backend API is running (typically on http://localhost:5000)

2. Create a `.env` file in the frontend directory:
   ```
   cp .env.example .env
   ```

3. Edit the `.env` file and add your API token:
   ```
   API_URL=http://localhost:5000
   API_TOKEN=your_api_token_here
   ```

4. Start the development server:
   ```
   python server.py
   ```

5. Open your browser and navigate to http://localhost:8080

## Features

- Real-time search suggestions as you type
- Location-based search using zipcode
- Responsive design that works on mobile and desktop

## Development

The frontend is built with:
- HTML, CSS, and JavaScript
- HTMX for AJAX requests
- Tailwind CSS for styling

### Files

- `index.html` - Main HTML file
- `api-client.js` - Client for connecting to the backend API
- `.env.js` - Script to load environment variables
- `server.py` - Simple development server

## Connecting to the Backend

The frontend connects to the backend API using the `api-client.js` file. The API URL and token are configured in the `.env` file.

By default, the frontend expects the backend API to be running at http://localhost:5000. You can change this by updating the `API_URL` in the `.env` file.

## API Endpoints

The backend provides one main endpoint:

1. **Suggestions Endpoint**
   - URL: `/api/v1/suggestions`
   - Method: GET
   - Headers: 
     - `Content-Type: application/json`
     - `X-API-Token: YOUR_API_TOKEN`
   - Query Parameters:
     - `query`: Search term (optional)
     - `zipcode`: Location zipcode (optional)
   - Response: List of suggestions with metadata

## Integration with Backend

When the real suggestions endpoint is implemented in the Flask backend:

1. Remove the mock API script import from `index.html`
2. Remove the HTMX request override in the JavaScript
3. Update the API token in the HTMX headers attribute

## Mock Data

The mock implementation includes sample data for:
- Restaurants
- Cafes
- Bars
- Dessert shops

Each item includes:
- Name
- Category
- Tags
- Location (zipcode, latitude, longitude)

## Future Improvements

- Add pagination for large result sets
- Implement advanced filtering options
- Add keyboard navigation for suggestions
- Improve accessibility 