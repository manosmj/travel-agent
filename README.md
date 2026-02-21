# 🌍 LangGraph-Based AI Travel Recommendation Assistant

A sophisticated AI-powered travel recommendation system built with LangGraph, combining retrieval-augmented generation (RAG) capabilities with advanced language models. Get personalized travel suggestions, itineraries, and destination insights powered by cutting-edge AI technology.

---

## 🚀 Technologies Used

- **Python 3.8+**
- **LangGraph** — Agent orchestration and workflow management
- **ChromaDB** — Vector database for document retrieval
- **Sentence Transformers** — Text embedding (all-MiniLM-L6-v2)
- **Large Language Model** — For natural language understanding and generation
- **LangChain** — Text chunking and metadata management
- **OpenWeather API** — Real-time weather data retrieval

---

## 🧠 Key Features

- **Intelligent Travel Recommendations:**
  - Personalized destination suggestions based on user preferences
  - Multi-step itinerary planning with detailed day-by-day schedules
  - Weather-aware travel advisory and packing recommendations

- **RAG Implementation:**
  - Embeds and stores travel advisory documents in ChromaDB
  - Retrieves relevant context for user queries
  - Augments LLM prompt with retrieved context for accurate responses

- **Advanced AI Capabilities:**
  - Real-time weather data integration
  - Semantic embedding using Sentence Transformers
  - Multi-agent workflow orchestration with LangGraph
  - Context-aware conversation management

- **Data Processing:**
  - Efficient document chunking and metadata handling
  - Secure API key management
  - Advanced semantic embedding and retrieval

---

## 📦 Project Structure

```
travel-agent/
├── src/
│   ├── langgraph_agent.py      # Main LangGraph agent implementation
│   ├── weather_app.py          # Weather-focused advisory implementation
│   ├── weather_forecast.py     # Forecast weather using Open Weather API
│   ├── vectordb.py             # Collect, Chunk and Store travel data
│   └── utils/                  # Utility functions and helpers
├── data/
│   ├── travel_guides/          # Travel advisory documents
│   ├── weather/                # Weather data files
│   └── destinations/           # Destination information
├── chroma_db/                  # ChromaDB persistent storage
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
└── .gitignore                  # Excludes .env, venv, etc.
```

---

## ⚡️ How to Run

### 1. Clone the repository
```sh
git clone https://github.com/manosmj/travel-agent.git
cd travel-agent
```

### 2. Set up a Python environment
```sh
python -m venv venv
venv\Scripts\activate  # On Windows
# Or
source venv/bin/activate  # On Mac/Linux
```

### 3. Install dependencies
```sh
pip install -r requirements.txt
```

### 4. Configure API Keys
Create `.env` file and add your API keys as environment variables:
```sh
# For OpenWeather API
OPENWEATHER_API_KEY="your-openweather-api-key"

# For LLM Service (choose one)
GROQ_API_KEY="your-groq-api-key"
# or
GOOGLE_API_KEY="your-google-api-key"
# or
OPENAI_API_KEY="your-openai-api-key"
```

### 5. Prepare Data
- Ensure travel advisory documents are in `data/travel_guides/`
- Ensure weather data files are in `data/weather/`

### 6. Launch the Application
```sh
python src/langgraph_agent.py
```

---

## 🔒 Security Notes
- **Never commit API keys or .env files to GitHub**
- Keep sensitive configuration in environment variables
- Regular security audits recommended
- Validate all user inputs before processing
- Use environment variables for all sensitive data

---

## 📝 Usage

### Getting Travel Recommendations
```python
from src.langgraph_agent import TravelAssistant

assistant = TravelAssistant()
recommendation = assistant.get_recommendation(
    destination="Paris",
    duration_days=7,
    budget="moderate",
    interests=["art", "food", "history"]
)
```

### Checking Weather
- Enter a country/city name to get weather information
- View weather analysis and travel recommendations
- Access historical weather patterns and travel advisories

---

## 📚 References
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [ChromaDB Documentation](https://www.trychroma.com/)
- [Sentence Transformers](https://www.sbert.net/)
- [OpenWeather API](https://openweathermap.org/api)
- [LangChain](https://langchain.org/)

---

## 👤 Author
- [manosmj](https://github.com/manosmj)

---

## 🔒 License
This project is licensed under the MIT License.
---