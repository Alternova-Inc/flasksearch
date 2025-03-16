# Search Suggestions Frontend

A simple HTML + JavaScript application that provides a search interface with suggestions.

## Features

- Real-time search suggestions as you type
- Display of search statistics (number of results and search time)
- Responsive design using Tailwind CSS
- HTMX for AJAX requests

## Getting Started

### Running the Frontend

1. Start the frontend server:

```bash
python server.py
```

2. Open your browser and navigate to:

```
http://localhost:8080
```

### How It Works

- The search input uses HTMX to make requests to the `/api/v1/suggestions` endpoint
- Currently using a mock API implementation until the real backend endpoint is created
- The mock API simulates network delay and filters suggestions based on the query

## Integration with Backend

When the real suggestions endpoint is implemented in the Flask backend:

1. Remove the mock API script import from `index.html`
2. Remove the HTMX request override in the JavaScript
3. Update the HTMX attributes in the search input to point to the correct endpoint

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

## Future Improvements

- Add pagination for large result sets
- Implement advanced filtering options
- Add keyboard navigation for suggestions
- Improve accessibility 