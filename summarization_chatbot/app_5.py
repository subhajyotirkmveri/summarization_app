import streamlit as st 
import requests
import bs4 as bs
from transformers import pipeline, T5Tokenizer, T5ForConditionalGeneration
import torch
import base64
from PIL import Image
import PyPDF2
import re

# Model and tokenizer loading
checkpoint = "LaMini-Flan-T5-248M"
tokenizer = T5Tokenizer.from_pretrained(checkpoint)
base_model = T5ForConditionalGeneration.from_pretrained(checkpoint, device_map='auto', torch_dtype=torch.float32)

# Function to Read .txt File and return its Text
def file_text(filepath):
    with open(filepath) as f:
        text = f.read().replace("\n", '')
        print ("number of character in this txt file = ", len(text))
        return text, len(text)

def pdf_file_preprocessing(pdf_path):
    with open(pdf_path, 'rb') as pdfFileObject:
        pdfReader = PyPDF2.PdfReader(pdfFileObject)
        count = len(pdfReader.pages)
        print("\nTotal Pages in pdf =", count)
        
        c = input("Do you want to read the entire pdf? [Y]/N: ").strip().lower()
        start_page = 1
        end_page = count 
        
        if c == 'n':
            start_page = int(input("Enter start page number (Indexing start from 1): ").strip())
            end_page = int(input(f"Enter end page number (Less than  or equal to {count}): ").strip())
            
            if start_page < 1 or start_page > count:
                print("\nInvalid Start page given")
                sys.exit()
                
            if end_page < 1 or end_page > count:
                print("\nInvalid End page given")
                sys.exit()
                
        text = ""
        for i in range(start_page, end_page + 1):
            page = pdfReader.pages[i-1]
            text += page.extract_text()
        print ("number of character in this document = ", len(text))   
        return text, len(text)

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

# LLM pipeline- using summarization pipeline
def llm_pipeline(text, min_tokens=25, max_tokens=None):
    pipe_sum = pipeline(
        'summarization',
        model=base_model,
        tokenizer=tokenizer,
        max_length=max_tokens or len(text)//8,
        min_length=min_tokens)
    result = pipe_sum(text)
    result = result[0]['summary_text']
    return result


# Function to display PDF
@st.cache_data
def displayPDF(file):
    with open(file, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="600" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

# Streamlit code 
st.set_page_config(page_title='Summarize Chatbot', layout="wide", page_icon="📃", initial_sidebar_state="expanded")

def main():

    st.title("Summarize Chatbot ")
    image = Image.open('summary.png')
    st.image(image, width=200)

    choice = st.sidebar.selectbox("Select your choice", ["Type your Text (or Copy-Paste)", "Load from .txt file", "Load from .pdf file", "From Wikipedia Page URL"])

    min_tokens = st.sidebar.number_input("Minimum Tokens for Summary", min_value=1, value=25)
    max_tokens = st.sidebar.number_input("Maximum Tokens for Summary", min_value=1, value=None)

    if choice ==  "Type your Text (or Copy-Paste)":
        st.subheader("Summarize Text")
        input_text = st.text_area("Enter your text here")
        if input_text is not None:
            if st.button("Summarize Text"):
                col1, col2 = st.columns([1, 1])
                with col1:
                    st.markdown("**Your Input Text**")
                    st.info(input_text)
                with col2:
                    st.markdown("**Summary Result**")
                    result = llm_pipeline(input_text, min_tokens, max_tokens)
                    st.success(result)
                    
    elif choice == "Load from .txt file":
        st.subheader("Summarize text Document")

        uploaded_file = st.file_uploader("Upload your .txt file here", type=['txt'])
        if uploaded_file is not None:
            if st.button("Summarize text Document"):
                col1, col2 = st.columns([1, 1])
                filepath = "uploaded_txts/" + uploaded_file.name

                with open(filepath, "wb") as temp_file:
                    temp_file.write(uploaded_file.read())

                with col1:
                    st.info(" Text file uploaded successfully")
                    with open(filepath, "r") as file:
                        file_contents = file.read()
                        st.text_area("Text File Contents", value=file_contents, height=400)

                with col2:
                    input_text, input_length = file_text(filepath)                
                    summary = llm_pipeline(input_text, min_tokens, max_tokens)
                    st.info("Summarization")
                    st.success(summary)                   
      
                
    elif choice == "Load from .pdf file":
        st.subheader("Summarize Document")
        uploaded_file = st.file_uploader("Upload your document here", type=['pdf'])

        #if uploaded_file is not None:
        if uploaded_file:
            filepath = "uploaded_pdfs/" + uploaded_file.name
            with open(filepath, "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.success("PDF file uploaded successfully!")
            
            if st.button("Summarize Document"):
                col1, col2 = st.columns([1, 1])
                #filepath = "uploaded_pdfs/" + uploaded_file.name


                with col1:
                    st.info("Display document")
                    pdf_view = displayPDF(filepath)
                    st.info("Navigate to the terminal to select the number of pages you'd like to summarize")

                with col2:
                    input_text, input_length = pdf_file_preprocessing(filepath)                
                    summary = llm_pipeline(input_text, min_tokens, max_tokens)
                    st.info("Summarization")
                    st.success(summary)                    
                    
    elif choice == "From Wikipedia Page URL":
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
                    summary = llm_pipeline(wiki_text(wiki_URL), min_tokens, max_tokens)
                    st.success(summary)

# Initializing the app
if __name__ == "__main__":
    main()

