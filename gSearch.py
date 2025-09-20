import streamlit as st
import google.generativeai as genai
from duckduckgo_search import DDGS

# --- Configure Gemini ---
genai.configure(api_key="AIzaSyDbTBJAWFB3xxSLIZ6o09ll7nZ47pvtDD8")  # replace with your key

# --- DuckDuckGo Search ---
def duckduckgo_search(query: str, max_results=5) -> str:
    """Fetch search results from DuckDuckGo"""
    with DDGS() as ddgs:
        results = ddgs.text(query, max_results=max_results)
        return "\n".join([f"{r['title']} - {r['href']}\nSnippet: {r['body']}" for r in results])

# --- Websearch Agent ---
def websearch_agent(query: str) -> str:
    """General purpose web search + Gemini summarizer"""
    search_results = duckduckgo_search(query)
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(
        f"""
You are a helpful web assistant.
User asked: {query}

Here are search results:
{search_results}

Using the above results and your own knowledge if needed, 
summarize the key information and provide a clear, 
useful answer to the user.
"""
    )
    return response.text

# --- Streamlit UI ---
st.set_page_config(page_title="WebSearch AI", page_icon="🌐")

st.title("🌐 WebSearch AI Assistant")
st.write("Ask any question, and I’ll search the web + summarize using Gemini AI.")

query = st.text_input("Enter your query:")
if st.button("Search") and query:
    with st.spinner("Searching and summarizing..."):
        answer = websearch_agent(query)
    st.subheader("Answer:")
    st.write(answer)
