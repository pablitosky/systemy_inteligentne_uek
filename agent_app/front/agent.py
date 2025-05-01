from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent
from langchain_core.tools import tool
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import HumanMessage
import random 
import os
import time
from vectordb import get_most_similar_movie

@tool
def recommend_most_similar_movies(movie_title:str) -> str:
    """Function to recommend most similar movies.
    Args:
        movie_title (str): The title of the movie to find similar movies for.
        Returns:
        str: A string containing the recommended movies."""

    response = get_most_similar_movie(movie_title)

    return response
# Define your tools
tools = [recommend_most_similar_movies]
checkpointer = MemorySaver()

# Create the agent specifying Gemini 2.0 Flash model

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-001", api_key=os.getenv("GOOGLE_API_KEY"))
agent = create_react_agent(llm, tools=tools, prompt="""
You are a helpful assistant. You have access to the private database of movies and can recommend similar movies based on the title provided.
""", checkpointer=checkpointer)


def call_agent(message:str, config:dict):
    """Function to call the agent with a message."""

    # Invoke the agent with the message
    messages = agent.invoke(
    {"messages": [HumanMessage(content=message)]},
    config=config)

    response = messages["messages"][-1].content

    # Return the response text
    return response


def response_stream(text):
    """Function to stream the response from the agent."""
    for word in text.split(" "):
        yield word + ' '
        time.sleep(0.1)