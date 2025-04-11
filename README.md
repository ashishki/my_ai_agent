# AI Business Agent

## Overview

AI Business Agent is an advanced AI-powered platform designed to help small and medium-sized businesses integrate artificial intelligence solutions tailored specifically to their unique needs. This platform can:

- **Create Custom AI Agents:** Analyze detailed business requirements to recommend and generate an AI assistant customized to automate specific tasks and workflows.
- **Evaluate and Improve Existing AI Agents:** Continuously analyze the performance of existing AI agents, providing detailed insights and practical recommendations for enhancement, including model fine-tuning and parameter optimization.

## Features

- **Quick Business Analysis:** Quickly processes basic business data, generating initial AI recommendations.
- **Detailed Business Analysis:** Collects comprehensive data (audience, competitors, strategic goals, current technologies, pain points) to produce in-depth AI-driven insights.
- **Multiple AI Models Support:** Seamlessly integrates with powerful language models such as OpenAI GPT-4 and Mistral, allowing flexibility in cost, speed, and accuracy.
- **Data Caching and Logging:** Utilizes Redis for rapid data caching and PostgreSQL for structured logging, enhancing performance and facilitating detailed monitoring.
- **Real-time Monitoring and Analytics:** Integrated with Grafana for monitoring system metrics, response times, and user feedback in real time.
- **CI/CD and Containerization:** Automated testing and deployment through GitHub Actions, ensuring stability, scalability, and easy maintenance.

## Technical Stack

- **Backend Framework:** FastAPI (Python)
- **Database:** PostgreSQL
- **Caching:** Redis
- **Containerization:** Docker, Docker Compose
- **Monitoring:** Grafana
- **CI/CD:** GitHub Actions
- **AI Models:** OpenAI GPT-4, Mistral
- **Testing:** pytest, pytest-asyncio

## Project Structure

```
ai_business_agent/
├── .github/                 # GitHub Actions configuration
├── alembic/                 # Database migrations
├── app/
│   ├── main.py              # Entry point of the FastAPI application
│   ├── routers/             # API endpoints
│   ├── models/
│   │   ├── db_models.py     # SQLAlchemy models
│   │   └── schemas.py       # Pydantic models
│   ├── services/            # Business logic and AI integrations
│   │   ├── llm.py
│   │   ├── mistral.py
│   │   ├── cache.py
│   │   └── logger.py
│   └── tests/               # Automated tests
├── scripts/                 # Utility and synthetic data scripts
├── Dockerfile               # Docker build configuration
├── docker-compose.yml       # Docker Compose configuration
├── requirements.txt         # Project dependencies
└── pytest.ini               # Pytest configuration
```

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Git

### Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/ai_business_agent.git
cd ai_business_agent
```

Create `.env` file based on `.env.example` and fill in required secrets:

```dotenv
POSTGRES_PASSWORD=your_db_password
OPENAI_API_KEY=your_openai_api_key
MISTRAL_API_KEY=your_mistral_api_key
```

Build and start containers:

```bash
docker-compose up --build
```

The API will be accessible at:

```
http://localhost:8000
```

## Testing

Run tests locally:

```bash
pytest
```

## Monitoring

Access Grafana dashboard at:

```
http://localhost:3000
```

Default login credentials: `admin` / `admin`

## Roadmap

- [x] Project infrastructure setup (Docker, CI/CD)
- [x] API endpoints for quick and detailed business analysis
- [x] Integration with OpenAI and Mistral
- [x] Basic caching, logging, and monitoring
- [ ] Synthetic data generation for testing
- [ ] Dynamic learning module based on user feedback
- [ ] AI-agent constructor module

## Contributing

Contributions are welcome! Please open issues or submit pull requests for improvements and new features.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contact

Your Name - your.email@example.com

