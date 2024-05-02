import streamlit as st 
from langchain.chains.summarize import load_summarize_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader, DirectoryLoader
from transformers import pipeline
from transformers import T5Tokenizer, T5ForConditionalGeneration
import torch
import base64           # to read the pdf
from PIL import Image

# load the model & tokenizer
checkpoint = "LaMini-Flan-T5-248M"
tokenizer = T5Tokenizer.from_pretrained(checkpoint)
base_model = T5ForConditionalGeneration.from_pretrained(checkpoint, device_map='auto', torch_dtype=torch.float32)

# file loader and preprocessing
def file_preprocessing(file):
    loader =  PyPDFLoader(file)
    pages = loader.load_and_split()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=50)
    texts = text_splitter.split_documents(pages)
    final_texts = ""
    for text in texts:
        final_texts = final_texts + text.page_content
    return final_texts, len(final_texts)

# LLM pipeline- using summarization pipeline
def llm_pipeline(filepath):
    input_text, input_length = file_preprocessing(filepath)
    pipe_sum = pipeline(
        'summarization',
        model=base_model,
        tokenizer=tokenizer,
        max_length=input_length//8, 
        min_length=25)
    result = pipe_sum(input_text)
    result = result[0]['summary_text']
    return result

# Function to summarize text
def text_summary(text):
    pipe_sum = pipeline(
        'summarization',
        model=base_model,
        tokenizer=tokenizer,
        max_length=len(text)//8,
        min_length=25)
    result = pipe_sum(text)
    result = result[0]['summary_text']
    return result

# Function to display PDF
@st.cache_data
def displayPDF(file):
    with open(file, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = F'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="600" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

# Streamlit code 
st.set_page_config(page_title='Summarize Chatbot', layout="wide", page_icon="📃", initial_sidebar_state="expanded")

def main():

    st.title("Summarize Chatbot with PDF or Text Support")
    image = Image.open('summary.png')
    st.image(image, width=200)

    choice = st.sidebar.selectbox("Select your choice", ["Summarize Text", "Summarize Document"])

    if choice == "Summarize Text":
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
                    result = text_summary(input_text)
                    st.success(result)

    elif choice == "Summarize Document":
        st.subheader("Summarize Document")
        uploaded_file = st.file_uploader("Upload your document here", type=['pdf'])
        if uploaded_file is not None:
            if st.button("Summarize Document"):
                col1, col2 = st.columns([1, 1])
                filepath = "uploaded_pdfs/" + uploaded_file.name

                with open(filepath, "wb") as temp_file:
                    temp_file.write(uploaded_file.read())

                with col1:
                    st.info("File uploaded successfully")
                    pdf_view = displayPDF(filepath)

                with col2:
                    summary = llm_pipeline(filepath)
                    st.info("Summarization")
                    st.success(summary)

# Initializing the app
if __name__ == "__main__":
    main()

