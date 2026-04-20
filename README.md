# LangGraph Tool Agent

A **tool-based AI agent** built using **LangGraph** and **LangChain**, capable of dynamically selecting and executing tools like a calculator, weather API, and date utility.

---

## Overview

This project demonstrates how to build an **agentic system** where a Large Language Model (LLM):

* Understands user queries
* Decides whether a tool is needed
* Calls the appropriate tool
* Uses the result to generate a final response

The agent follows a **ReAct-style loop (Reason → Act → Observe)** using LangGraph.

---

## Features

* **Iterative Agent Loop** (LLM → Tool → LLM)
* **Multi-tool Support**

  * Calculator
  * Weather API
  * Current Date
* **Structured Output**

  * Question
  * Tool usage
  * Tool name
  * Tool response
  * Final answer
*  Built using **LangGraph StateGraph**
*  Integrated with **Google Gemini (via LangChain)**

---

## Architecture

```text
START
  ↓
LLM Call
  ↓
Check: Tool Needed?
  ├── Yes → Tool Node → LLM Call (loop)
  └── No  → END
```

---

## Tools Implemented

### Calculator

Evaluates mathematical expressions safely.

### Weather Tool

Fetches real-time weather data using OpenWeather API.

### Current Date Tool

Returns the current system date and time.

---

Observability (LangSmith Tracing)

This project includes tracing and debugging support using LangSmith, which allows you to:

Visualize agent execution step-by-step
Inspect LLM decisions and tool calls
Debug errors and performance issues
Monitor agent behavior in real time

## Tech Stack

* Python
* LangGraph
* LangChain
* Google Generative AI (Gemini)
* OpenWeather API
* dotenv

---

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/your-username/langgraph-tool-agent.git
cd langgraph-tool-agent
```

---

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows
```

---

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Add environment variables

Create a `.env` file in the root directory:

```env
GOOGLE_API_KEY=your_google_api_key
WEATHER_API_KEY=your_openweather_api_key

# LangSmith Tracing
export LANGCHAIN_API_KEY=your_langsmith_api_key
export LANGSMITH_ENDPOINT=https://api.smith.langchain.com
export LANGCHAIN_TRACING=true
export LANGCHAIN_PROJECT=langgraph-tool-agent
```

---


---

## 🧪 Example Usage

```text
Input: calculate 5*6

Output:
question: calculate 5*6
use_tools: True
tool used: calculator
response from tool: 30
final_response: The answer is 30.
```

---

## Limitations

* ❌ No long-term memory (stateless across runs)
* ❌ Cannot answer general knowledge outside tools
* ❌ No multi-step planning beyond tool loop

---

Viewing Traces

After running the agent, you can view traces in LangSmith:

Go to: https://smith.langchain.com
Open your project: langgraph-tool-agent
Inspect:
LLM calls
Tool executions
State transitions

Why LangSmith?

LangSmith helps you understand:

User Query → LLM Decision → Tool Call → Tool Output → Final Response

This is especially useful for:

debugging agent loops
improving prompt design
analyzing tool usage

## Future Improvements

* Add conversational memory
* Integrate web search tool
* Improve tool selection reasoning
* Add structured JSON outputs
* Build a UI (Streamlit / FastAPI)

---

## Learnings

This project demonstrates:

* How to build **agentic workflows**
* How LLMs decide when to use tools
* How to structure state in LangGraph
* Differences between chatbots and agents

---

## License

MIT License

---

##  Acknowledgements

* LangChain
* LangGraph
* Google Generative AI
* OpenWeather API

---
