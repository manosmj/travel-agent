# 🌍 LangGraph-Based AI Travel Agent Assistant

An intelligent AI-powered travel agent built with LangGraph that helps users with travel planning, package recommendations, and destination information. The system leverages advanced language models and custom tools to provide comprehensive travel assistance.

---

## 🚀 Technologies Used

- **Python 3.8+**
- **LangGraph** — Agent orchestration and agentic workflow management
- **LangChain** — Language model integrations and core utilities
- **Groq API** — Primary LLM provider (llama-3.1-8b-instant)
- **OpenAI API** — Alternative LLM provider (gpt-4o-mini)
- **python-dotenv** — Environment variable management

---

## 🧠 Key Features

- **Multi-Agent Architecture:**
  - Agentic workflow powered by LangGraph
  - Tool binding and execution for complex tasks
  - State management for conversation context

- **Custom Tools:**
  - Repository download and extraction capabilities
  - Weather forecast integration
  - Dynamic tool composition and execution

- **Multi-LLM Support:**
  - Groq API integration (primary: llama-3.1-8b-instant)
  - OpenAI API support (gpt-4o-mini)
  - Configurable temperature and model selection

- **Flexible Configuration:**
  - Environment-based API key management
  - Easy model switching and parameter tuning

---

## 📦 Project Structure

```
travel-agent/
├── src/
│   ├── travel_agent.py         # Main LangGraph agent implementation
│   ├── llm.py                  # LLM initialization and model selection
│   ├── custom_tools.py         # Custom tool definitions
│   ├── paths.py                # Path configuration
├── data/                       # Data directory (for user-provided data)
├── .env.example                # Environment variables template
├── .eslintrc.json              # ESLint configuration
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
└── .gitignore                  # Excludes .env, venv, __pycache__, etc.
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
Copy `.env.example` to `.env` and add your API keys:
```sh
# For Groq API (Primary LLM)
GROQ_API_KEY="your-groq-api-key"

# For OpenAI API (Alternative LLM)
OPENAI_API_KEY="your-openai-api-key"
```

### 5. Launch the Application
```sh
python src/travel_agent.py
```

---

## 🔒 Security Notes
- **Never commit API keys or .env files to GitHub** — Use `.env.example` as a template
- Keep sensitive credentials in environment variables only
- Use `.gitignore` to exclude `.env`, `venv/`, `__pycache__/`, and other sensitive files
- Validate and sanitize user inputs before processing
- Review LangGraph workflow execution for security implications
- Rotate API keys periodically

---

## 📝 Usage

### Running the Travel Agent
```python
from src.travel_agent import State

# The agent runs in an interactive loop
# It uses LangGraph to manage workflow steps:
# 1. LLM node - analyzes user input and decides which tools to use
# 2. Tools node - executes selected tools
# 3. Continues until the agent produces a final response
```

### Supported Models

**Groq API:**
- `llama-3.1-8b-instant` (recommended, default)
- `llama3-8b-8192`

**OpenAI API:**
- `gpt-4o-mini`

### State Management
The agent maintains state with:
- `messages` — Conversation history
- `weather_info` — Weather-related data
- `user_purpose` — Travel purpose context
- `user_departure` — Departure location
- `user_destination` — Destination location

---

## 📚 References
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [LangChain Documentation](https://langchain.org/)
- [Groq API Documentation](https://console.groq.com/docs)
- [OpenAI API Documentation](https://platform.openai.com/docs)

---

## 👤 Author
- [manosmj](https://github.com/manosmj)

---

## 🔒 License
This project is licensed under the MIT License.
---