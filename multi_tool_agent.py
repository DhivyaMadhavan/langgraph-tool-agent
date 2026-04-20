from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.messages import SystemMessage, HumanMessage, ToolMessage
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, List
from dotenv import load_dotenv
import requests
import os

load_dotenv(override=True)

model_api_key = os.getenv("GOOGLE_API_KEY")

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=model_api_key
)

@tool
def get_weather(city:str) -> str:
    """get the weather information from the weather api"""

    weather_api_key = os.getenv("WEATHER_API_KEY")
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": weather_api_key,
        "units": "metric"
    }

    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        return "Could not fetch weather"

    data = response.json()
    
    return f"{city}: {data['weather'][0]['description']}, {data['main']['temp']}°C"

@tool
def calculator(expression: str) -> str:
    """Evaluate a mathematical expression safely."""
    try:
        result = eval(expression, {"__builtins__": {}}, {})        
        return str(result)
    except Exception as e:
        return f"Error calculating: {str(e)}"    
    
@tool
def get_current_date() -> str:
    """Get the current system date and time."""
    from datetime import datetime
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")    
    return now  

tools = [get_weather,calculator,get_current_date]
tools_by_name = {tool.name: tool for tool in tools}
llm_with_tools = llm.bind_tools(tools)

class AgentState(TypedDict):
    messages: List
    use_tools: bool
    tool_used: str
    tool_output: str
    final_response: str

#nodes
def llm_call(state: AgentState):
    messages = state["messages"]

    response = llm_with_tools.invoke(
        [
            SystemMessage(
                content="You are a helpful assistant."
            )
        ] + messages
    )

    return {
        "messages": messages + [response],
        "final_response": response.content
        
    }

def tool_node(state: AgentState):
    tool_messages = []

    tool_name = None
    tool_output = None

    for tool_call in state["messages"][-1].tool_calls:
        tool_name = tool_call["name"]

        tool = tools_by_name[tool_name]
        observation = tool.invoke(tool_call["args"])

        tool_output = str(observation)

        tool_messages.append(
            ToolMessage(
                content=tool_output,
                tool_call_id=tool_call["id"]
            )
        )

    return {
        "messages": state["messages"] + tool_messages,
        "tool_used": tool_name,
        "tool_output": tool_output,
        "use_tools": True
    }
def should_continue(state: AgentState) -> AgentState:
    """Decide if we should continue the loop or stop based upon whether the LLM made a tool call"""

    last_message = state["messages"][-1]

    if last_message.tool_calls:
        return "tool_node"

    return END

#build graph
agent_builder = StateGraph(AgentState)

agent_builder.add_node("llm_call",llm_call)
agent_builder.add_node("tool_node",tool_node)

agent_builder.add_edge(START,"llm_call")
agent_builder.add_conditional_edges(
    "llm_call",
    should_continue,
    ["tool_node",END]
)
agent_builder.add_edge("tool_node","llm_call")
agent = agent_builder.compile()


#invoke
queries = [
    "calculate 5*6",
    "what is the weather in Chennai",
    "what is the current date"
]

for q in queries:
    input_message = HumanMessage(content=q)

    result = agent.invoke({
        "messages": [input_message],
        "use_tools": False,
        "tool_used": "",
        "tool_output": "",
        "final_response": ""
    })

    print("\n---")
    print("question:", q)
    print("use_tools:", result.get("use_tools"))
    print("tool used:", result.get("tool_used"))
    print("tool output:", result.get("tool_output"))
    print("final_response:", result.get("final_response"))
