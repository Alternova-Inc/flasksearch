# Flask Search Engine Microservice

A lightweight and powerful search engine microservice built with Flask and Elasticsearch Serverless. This microservice provides a ready-to-use search API that can be integrated into any application requiring robust search capabilities.

## Features

- 🚀 Built with Flask for lightweight and fast API endpoints
- 🔍 Powered by Elasticsearch Serverless for scalable search capabilities
- 📚 RESTful API design
- 🔒 Easy to configure and deploy
- 📝 API documentation using Bruno

## Prerequisites

- Python 3.12.9+
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
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
```bash
cp .env.example .env
```
Edit the `.env` file with your Elasticsearch Serverless credentials:
```
ELASTICSEARCH_URL=your-elasticsearch-url
ELASTICSEARCH_API_KEY=your-api-key
```

## Usage

1. Start the Flask server:
```bash
flask run
```

2. The service will be available at `http://localhost:5000`

## API Endpoints

### Search
- `POST /api/v1/search`
  - Search across indexed documents
  - Request body:
    ```json
    {
      "query": "search term",
      "filters": {},
      "page": 1,
      "size": 10
    }
    ```

### Index Management
- `POST /api/v1/index`
  - Index new documents
- `DELETE /api/v1/index/{id}`
  - Remove documents from the index

## Configuration

The service can be configured through environment variables or a configuration file. See `.env.example` for available options.

## Development

This project uses:
- Flask for the web framework
- Elasticsearch for search functionality
- Bruno for API documentation and testing

### Project Structure
```
flasksearch/
├── app/
│   ├── __init__.py
│   ├── routes.py
│   └── search_logic.py
├── tests/
├── requirements.txt
└── README.md
```

## Testing

Run tests using:
```bash
pytest
```

## API Documentation

API documentation is available in the `bruno` directory. To view the documentation:

1. Install Bruno
2. Open the bruno collection in the Bruno app
3. Browse the available endpoints and examples

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 