import streamlit as st
import requests
import bs4 as bs
from transformers import pipeline, T5Tokenizer, T5ForConditionalGeneration
import torch
import base64

# Model and tokenizer loading
checkpoint = "LaMini-Flan-T5-248M"
tokenizer = T5Tokenizer.from_pretrained(checkpoint)
base_model = T5ForConditionalGeneration.from_pretrained(checkpoint, device_map='auto', torch_dtype=torch.float32)

# LLM pipeline
def llm_pipeline_wiki(text):
    pipe_sum = pipeline(
        'summarization',
        model=base_model,
        tokenizer=tokenizer,
        max_length=500,
        min_length=50)
    result = pipe_sum(text)
    result = result[0]['summary_text']
    return result

# Function to retrieve text from Wikipedia URL
def wiki_text(url):
    response = requests.get(url)
    soup = bs.BeautifulSoup(response.text, 'html.parser')
    paragraphs = soup.find_all('p')
    article_text = ""
    for p in paragraphs:
        article_text += p.text
    
    # Removing all unwanted characters
    article_text = re.sub(r'\[[0-9]*\]', '', article_text)
    return article_text

# Streamlit code
st.set_page_config(page_title='Summarize Chatbot', layout="wide", page_icon="📃", initial_sidebar_state="expanded")

app_heading_html =  f"""
    <div class="container">
        <img class="logo-img" src="data:image/png;base64,{base64.b64encode(open("logo.png", "rb").read()).decode()}" width=70 height=70>
        <p class="logo-text">{"Wikipedia summarization"}</p>
    </div>
    """

st.markdown(app_heading_html, unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    wiki_URL = st.text_input('Enter the URL of the Wikipedia article to analyze.', value="", placeholder='https://en.wikipedia.org/wiki/')

    if wiki_URL:
        st.components.v1.iframe(src=wiki_URL, width=None, height=550, scrolling=True)

with col2:
    if wiki_URL:
        if st.button("Summarize"):
            summary = llm_pipeline_wiki(wiki_text(wiki_URL))
            st.success(summary)

