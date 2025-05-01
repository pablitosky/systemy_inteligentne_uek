from qdrant_client.models import Filter, FieldCondition, MatchValue, MatchText, Range
from qdrant_client import QdrantClient
import streamlit as st
import pandas as pd


client = QdrantClient(url="http://qdrant:6333")

@st.cache_data
def get_data():
    df = pd.read_pickle("vectordb.pkl")
    return df

df = get_data()

def get_most_similar_movie(title:str):
    min_rate=0.7
    print("Searching for similar movies to:", title)
    try:
        query_vector = df.loc[df['Series_Title'] == title, 'vector'].values[0]
        query_title = df.loc[df['Series_Title'] == title, 'Series_Title'].values[0]
    except IndexError:
        print("Movie not found in the dataset.")
        return None

    search_result = client.query_points(
        collection_name="movies",
        query=query_vector,
        query_filter=Filter(
            must=[
                #FieldCondition(key="Genre", match=MatchText(text=genre)), 
                FieldCondition(key="IMDB_Rating", range=Range(gt=min_rate))],
            must_not=[FieldCondition(key="Series_Title", match=MatchValue(value=query_title))]
        ),
        with_payload=True,
        limit=3,
    ).points

    return [dict(x) for x in search_result]