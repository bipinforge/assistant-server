Here's the updated README with virtual environment activation and uv installation steps:

```markdown
# Ingestion Server

A FastAPI-based document ingestion and retrieval server that supports multiple embedding providers (OpenAI, Hugging Face) and integrates with MongoDB and vector databases.

## Features

- Document ingestion and processing
- Multiple embedding providers (OpenAI, Hugging Face)
- Vector database management
- Document retrieval and semantic search
- MongoDB integration for metadata storage
- Assistant with retrieval capabilities
- REST API endpoints for file management and document operations

## Project Structure

```
├── main.py                              # FastAPI application entry point
├── controller.py                        # API route controllers
├── src/
│   ├── assistant.py                    # AI assistant with retrieval
│   ├── document_loader_manager.py      # Document loading utilities
│   ├── file_service.py                 # File handling operations
│   ├── ingestion_service.py            # Document ingestion logic
│   ├── retrieval_service.py            # Document retrieval and search
│   ├── mongo_client.py                 # MongoDB client
│   ├── vector_db_manager.py            # Vector database management
│   ├── openai_embedding_manager.py     # OpenAI embedding integration
│   ├── huggingface_embedding_manager.py # Hugging Face embedding integration
│   └── schemas/
│       ├── conversation_schema.py       # Conversation data models
│       └── file_schema.py              # File data models
├── uploads/                             # Directory for uploaded files
├── pyproject.toml                      # Project configuration
└── README.md                           # This file
```

## Prerequisites

- Python 3.8+
- [uv](https://github.com/astral-sh/uv) package manager

## Installation

### 1. Install uv

Install uv using pip:

```bash
pip install uv
```

Or install via Homebrew (macOS):

```bash
brew install uv
```

For other installation methods, see [uv documentation](https://docs.astral.sh/uv/getting-started/installation/).

### 2. Clone the repository

```bash
git clone <repository-url>
cd ingestion-server
```

### 3. Create and activate virtual environment

Create a virtual environment using uv:

```bash
uv venv
```

Activate the virtual environment:

**On macOS/Linux:**
```bash
source .venv/bin/activate
```

**On Windows:**
```cmd
.venv\Scripts\activate
```

### 4. Install dependencies

Install project dependencies using uv:

```bash
uv sync
```

## Running the Application

Start the FastAPI development server on port 3000:

```bash
fastapi dev --port 3000
```

The application will be available at `http://localhost:3000`

### API Documentation

Once the server is running, you can access:
- **Swagger UI**: `http://localhost:3000/docs`
- **ReDoc**: `http://localhost:3000/redoc`

## Configuration

Configure the following environment variables:

- `OPENAI_API_KEY` - Your OpenAI API key (if using OpenAI embeddings)
- `MONGODB_URI` - MongoDB connection string
- `VECTOR_DB_URL` - Vector database connection URL (if applicable)
- `HF_MODEL_NAME` - Hugging Face model name (if using HF embeddings)

## Usage

### Upload a Document

```bash
curl -X POST "http://localhost:3000/upload" \
  -F "file=@document.pdf"
```

### Retrieve Documents

```bash
curl -X GET "http://localhost:3000/retrieve?query=your+search+query"
```

## Dependencies

See pyproject.toml for the complete list of dependencies. Key packages include:

- FastAPI - Web framework
- Pydantic - Data validation
- Motor - Async MongoDB driver
- OpenAI - OpenAI API client
- Transformers - Hugging Face models

## Contributing

Please follow PEP 8 style guidelines and include tests for new features.

## License

[Add your license information here]
```
