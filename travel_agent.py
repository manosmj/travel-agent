from typing import Dict, Any, Annotated
from typing_extensions import TypedDict
from langchain_groq import ChatGroq
from langchain.messages import HumanMessage, SystemMessage
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from dotenv import load_dotenv
from custom_tools import get_all_tools, weather_forecast
from langchain_core.messages import ToolMessage
from langchain_core.runnables.graph import MermaidDrawMethod
from llm import get_llm
import os
from dotenv import load_dotenv

load_dotenv()

grq_api = os.environ.get("GROQ_API_KEY")

# Initialize the LLM
llm = get_llm("llama-3.1-8b-instant", 0.7)

# Initialize a recommender LLM for picking the best option
recommender_llm = get_llm("llama-3.1-8b-instant", 0.3)

# Define your agent's state - this is your agent's memory
class State(TypedDict):
    messages: Annotated[list, add_messages]
    weather_info: str
    user_purpose: str
    user_departure: str
    user_destination: str

# The LLM node - where your agent thinks and decides
def llm_node(state: State):
    """Your agent's brain - decides whether to use tools or respond."""
    tools = get_all_tools()
    llm_with_tools = llm.bind_tools(tools)  # Give your agent access to tools
    
    response = llm_with_tools.invoke(state["messages"])
    return {"messages": [response]}

def tools_node(state: State):
    """Node that executes the tools called by the LLM."""
    messages = state["messages"]
    # Get the last message which should be the assistant's response
    last_message = messages[-1]
    
    # Get all available tools
    tool_map = {tool.name: tool for tool in get_all_tools()}
    
    # Process tool calls
    tool_results = []
    weather_data = ""
    
    # Check if the message has tool calls
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        for tool_call in last_message.tool_calls:
            tool_name = tool_call["name"]
            tool_args = tool_call["args"]
            
            # Execute the tool
            if tool_name in tool_map:
                tool_func = tool_map[tool_name]
                result = tool_func.invoke(tool_args)
                
                # Capture weather forecast data
                if tool_name == "weather_forecast":
                    weather_data = str(result)
                
                tool_results.append(
                    ToolMessage(
                        content=str(result),
                        tool_call_id=tool_call["id"]
                    )
                )
    
    # Update state with weather info and return with messages
    return {
        "messages": tool_results,
        "weather_info": weather_data
    }

def should_continue(state: State):
    """Determine whether to continue to tools node or end."""
    messages = state["messages"]
    last_message = messages[-1]
    
    # If the LLM has called tools, continue to tools node
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"
    # Otherwise, end the conversation
    return "end"

def recommender_node(state: State):
    """Node that recommends the best travel mode based on weather and purpose."""
    messages = state["messages"]
    
    # Get the last assistant message which contains all travel recommendations
    travel_recommendations = ""
    for msg in reversed(messages):
        if hasattr(msg, "content") and msg.content and not msg.content.startswith("I want to travel"):
            travel_recommendations = msg.content
            break
    
    # Create a prompt for the recommender agent
    recommender_prompt = f"""
    Based on the following information, recommend THE SINGLE BEST travel mode for this trip.
    
    Travel Details:
    - From: {state['user_departure']}
    - To: {state['user_destination']}
    - Purpose: {state['user_purpose']}
    
    Current Weather Information:
    {state['weather_info']}
    
    Available Travel Options:
    {travel_recommendations}
    
    Your task:
    1. Analyze the weather conditions at both departure and destination
    2. Consider the travel purpose
    3. Recommend ONLY ONE travel mode that is most suitable
    4. Provide a brief explanation (3-4 sentences) of why this is the best option
    
    Format your response as:
    **Recommended Travel Mode:** [MODE NAME]
    
    **Why:** [Brief explanation considering weather and purpose]
    
    **Key Details:**
    - Estimated Time: [time]
    - Estimated Cost: [cost]
    - Weather Impact: [how weather affects this mode]
    """
    
    # Get recommendation from recommender LLM
    response = recommender_llm.invoke([
        SystemMessage(content="You are a travel mode recommendation expert. Based on weather conditions and travel purpose, recommend the single best travel option."),
        HumanMessage(content=recommender_prompt)
    ])
    
    return {"messages": [response]}


def create_tool_registry() -> Dict[str, Any]:
    """Create a registry mapping tool names to their functions."""
    tools = get_all_tools()
    return {tool.name: tool for tool in tools}

def create_graph():
    """Create and configure the LangGraph workflow."""
    # Create the graph
    graph = StateGraph(State)

    # Add nodes
    graph.add_node("llm", llm_node)
    graph.add_node("tools", tools_node)
    graph.add_node("recommender", recommender_node)

    # Set entry point
    graph.set_entry_point("llm")

    # Add conditional edges - after LLM, check if tools are needed
    graph.add_conditional_edges(
        "llm",
        should_continue,
        {"tools": "tools", "end": "recommender"}
    )

    # After tools execution, go back to LLM for further processing
    graph.add_edge("tools", "llm")
    
    # From recommender node, end the graph
    graph.add_edge("recommender", END)

    return graph.compile()

def main():

    print("LangGraph Chatbot with Custom Tools")
    print("Type 'exit' or 'quit' to end the session.")

    # Create the graph
    app = create_graph()

    # Display available tools
    tool_registry = create_tool_registry()
    print(f"Available tools: {', '.join(tool_registry.keys())}\n")

    # System message with dynamic tool information
    tool_descriptions = "\n".join(
        [f"- {name}: {tool.description}" for name, tool in tool_registry.items()]
    )
   
    system_content = f"""You are an intelligent Travel Information Assistant designed to provide comprehensive travel suggestions and recommendations.

    When a user provides their travel details (departure city, destination city, and purpose of travel), analyze whether airport is present in this information and provide:

    1. **Travel Options**: Suggest multiple transportation modes including:
    - Flight options (if applicable)
    - Train services
    - Bus/Coach services
    - Car rental or driving options
    - Bike/Cycling routes (if suitable)

    2. **Key Information to Include**:
    - Estimated travel time for each option
    - Approximate cost range
    - Comfort and convenience levels
    - Best time to travel based on the destination
    - Weather considerations

    3. **Purpose-Based Recommendations**:
    - For Business: Prioritize quick, reliable, and professional options
    - For Emergency: Suggest fastest available options
    - For Family Visit: Consider comfort and affordability
    - For Tourism: Highlight scenic routes and experiences
    - For Other purposes: Provide balanced recommendations

    4. **Additional Helpful Details**:
    - Best booking platforms or channels
    - Seasonal considerations and peak times
    - Safety and health requirements
    - Visa or documentation if crossing borders
    - Local transportation at the destination
    - Budget tips and cost-saving options

    5. **Format Your Response**:
    - Be clear and organized
    - Use bullet points for easy reading
    - Prioritize recommendations based on the travel purpose
    - Provide actionable advice
    
    """

    # Initialize conversation state
    initial_state = {"messages": [SystemMessage(content=system_content)]}

    try:
        while True:
            user_destination = input("Enter the city you want to travel to: ")
            user_departure = input("Enter your departure city: ")
            user_purpose = input("Enter the purpose of your travel (e.g., Business, Emergency, Family Visit, Tourism or others): ")
            
            if user_destination in {"exit", "quit"} or user_departure in {"exit", "quit"}:
                print("👋 Goodbye!")
                break

            # Create user input requesting tool usage
            user_input = f"""
                I want to travel to {user_destination} from {user_departure}.
                The purpose of my travel is {user_purpose}.
                
                Please use the weather_forecast tool to get current weather information for both cities.
                Then provide comprehensive travel suggestions including:
                - Current weather conditions at both locations
                - Suitable travel options (flights, trains, buses, cars, bikes)
                - Travel time estimates
                - Cost estimates
                - Weather-aware recommendations
                - Any important travel tips based on the weather conditions
            """

            # Initialize state with all required information
            initial_state = {
                "messages": [
                    SystemMessage(content=system_content),
                    HumanMessage(content=user_input)
                ],
                "user_purpose": user_purpose,
                "user_departure": user_departure,
                "user_destination": user_destination
            }

            # Run the graph
            print("\n🤖 Analyzing travel options...\n")
            result = app.invoke(initial_state)

            # Display the recommended travel mode
            last_message = result["messages"][-1]
            if hasattr(last_message, "content") and last_message.content:
                print(f"✈️ Bot Recommendation:\n{last_message.content}\n")

    except KeyboardInterrupt:
        print("\n👋 Session terminated.")

if __name__ == "__main__":
    main()