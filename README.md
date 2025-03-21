# Flask Search Engine Microservice

A lightweight and powerful search engine microservice built with Flask and Elasticsearch Serverless, featuring a modern React frontend. This full-stack application provides both a ready-to-use search API and an intuitive web interface for searching and managing data.

## Features

- 🚀 Built with Flask for lightweight and fast API endpoints
- 🔍 Powered by Elasticsearch Serverless for scalable search capabilities
- 🎨 Modern React frontend with Material-UI components
- 🔒 API Token authentication
- 📚 RESTful API design
- 🌐 CORS support
- 📝 API documentation using Bruno
- ✅ Comprehensive test suite
- 🔄 Real-time search suggestions
- 📱 Responsive design for all devices

## Prerequisites

- Python 3.12.9
- Node.js 14+ (for frontend)
- Elasticsearch Serverless account and credentials
- Bruno (for API testing and documentation)

## Installation

1. Clone the repository:
```bash
git clone <your-repository-url>
cd flasksearch
```

2. Create a virtual environment and activate it:
```bash
# Using conda (recommended)
conda create -n flasksearch python=3.12.9
conda activate flasksearch

# Or using venv
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install backend dependencies:
```bash
pip install -r requirements.txt
```

4. Install frontend dependencies:
```bash
cd frontend
npm install
cd ..
```

5. Configure environment variables:
```bash
cp .env.example .env
```
Edit the `.env` file with your configuration:
```ini
# Flask configuration
FLASK_APP=app
FLASK_ENV=development
FLASK_DEBUG=1
PORT=5001

# Elasticsearch configuration
ELASTICSEARCH_URL=your-elasticsearch-url
ELASTICSEARCH_API_KEY=your-api-key
ELASTICSEARCH_INDEX=your-index-name

# API configuration
API_TOKEN=your-secure-api-token
API_VERSION=v1
CORS_ORIGINS=*
```

## Project Structure

```
flasksearch/
├── app/
│   ├── __init__.py          # App initialization and configuration
│   ├── routes.py            # API route definitions
│   ├── controllers/
│   │   └── items.py         # Item-related business logic
│   └── middleware/
│       └── auth.py          # Authentication middleware
├── frontend/                # React frontend application
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── services/        # API integration services
│   │   └── styles/          # CSS and styling
│   ├── public/             # Static assets
│   └── package.json        # Frontend dependencies
├── api_docs/               # Bruno API documentation
├── data/                   # Sample data and scripts
├── scripts/               # Utility scripts
├── tests/                 # Test files
│   ├── conftest.py        # Test configuration and fixtures
│   └── test_items.py      # Item endpoint tests
├── requirements.txt       # Python dependencies
└── README.md
```

## API Endpoints

### Authentication

All API endpoints require authentication using the `X-API-Token` header. The token should match the `API_TOKEN` environment variable.

Example:
```http
X-API-Token: your-secure-api-token
```

### Available Endpoints

#### Create or Update Item
- `PUT /api/v1/items`
  - Create or update an item in the search index
  - Required fields: `id`, `name`, `suggest_input`
  - Optional fields: `description`, `tags`, `metadata`

```json
{
  "id": "123",
  "name": "Sample Item",
  "description": "A detailed description",
  "tags": ["tag1", "tag2"],
  "suggest_input": ["Sample Item", "Sample"],
  "metadata": {
    "type": "establishment",
    "address": "123 Main St"
  }
}
```

#### Get Item
- `GET /api/v1/items/:id`
  - Retrieve an item by its ID

#### Health Check
- `GET /api/status`
  - Check if the service is running
  - No authentication required

### Response Formats

#### Success Responses
```json
{
  "message": "Item successfully indexed",
  "id": "123",
  "index": "items"
}
```

#### Error Responses
```json
{
  "error": "Unauthorized",
  "detail": "Invalid or missing API token"
}
```

Common HTTP status codes:
- 200: Success
- 400: Bad Request
- 401: Unauthorized
- 404: Not Found
- 500: Internal Server Error

## Development

### Running the Application

1. Start the backend:
```bash
flask run
```

2. Start the frontend development server:
```bash
cd frontend
npm start
```

The backend API will be available at `http://localhost:5001`
The frontend application will be available at `http://localhost:3000`

### Testing

The project includes a comprehensive test suite using pytest. The tests cover:

1. **Authentication**
   - Token validation
   - Unauthorized access handling

2. **Item Operations**
   - Creating/updating items
   - Retrieving items
   - Error handling for non-existent items
   - Input validation

3. **Test Data**
   - Uses real sample data from `data/test_establishments.json`
   - Ensures realistic testing scenarios

#### Running Tests

```bash
# Run all tests with verbose output
pytest

# Run specific test file
pytest tests/test_items.py

# Run specific test function
pytest tests/test_items.py::test_create_item
```

#### Test Structure

- `tests/conftest.py`: Contains test fixtures and configuration
  - Flask test app setup
  - Test client
  - Sample data loading
  - Authentication headers

- `tests/test_items.py`: Item endpoint tests
  - `test_create_item`: Tests item creation
  - `test_get_item`: Tests item retrieval
  - `test_get_nonexistent_item`: Tests 404 handling
  - `test_create_item_without_auth`: Tests authentication
  - `test_create_item_invalid_data`: Tests input validation

### Testing the API with Bruno

1. Install Bruno from [https://www.usebruno.com/](https://www.usebruno.com/)
2. Open the `api_docs` folder in Bruno
3. Set up your environment variables in Bruno
4. Use the provided request collections to test the API

## Frontend Features

The React frontend provides:

- 🔍 Real-time search with suggestions
- 📱 Responsive design for mobile and desktop
- 🎨 Modern Material-UI components
- 🔄 Automatic API integration
- 📊 Search result visualization
- ⚡ Fast and efficient rendering

### Frontend Development

To work on the frontend:

```bash
cd frontend
npm install    # Install dependencies
npm start      # Start development server
npm run build  # Create production build
npm test       # Run frontend tests
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 

## Development Credits

This project was primarily developed through AI-assisted pair programming using Claude (Anthropic) via the Cursor IDE. The AI assistant helped with:

- 🤖 Architecture design and best practices
- 📝 Code implementation and documentation
- 🔍 Problem-solving and debugging
- 🧪 Test suite development
- 🎨 Frontend component design
- 📚 API documentation

This collaboration showcases the potential of human-AI pair programming in creating robust, well-documented software solutions. While the AI provided guidance and implementation suggestions, all final decisions and code reviews were performed by human developers to ensure quality and reliability. 