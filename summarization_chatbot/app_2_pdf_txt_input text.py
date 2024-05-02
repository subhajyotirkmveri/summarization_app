import streamlit as st 
from langchain.chains.summarize import load_summarize_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader, DirectoryLoader
from transformers import pipeline
from transformers import T5Tokenizer, T5ForConditionalGeneration
import torch
import base64           # to read the pdf
from PIL import Image
import PyPDF2

# load the model & tokenizer
checkpoint = "LaMini-Flan-T5-248M"
tokenizer = T5Tokenizer.from_pretrained(checkpoint)
base_model = T5ForConditionalGeneration.from_pretrained(checkpoint, device_map='auto', torch_dtype=torch.float32)

#Function to Read .txt File and return its Text
def file_text(filepath):
    with open(filepath) as f:
        text = f.read().replace("\n", '')
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
        return text, len(text)

# Function to retrieve text from Wikipedia URL
def wiki_text(url):
    response = requests.get(url)
    soup = bs.BeautifulSoup(response.text, 'html.parser')
    paragraphs = soup.find_all('p')
    article_text = ""
    for p in paragraphs:
        article_text += p.text
    return article_text

# LLM pipeline- using summarization pipeline
def llm_pipeline(filepath):
    input_text, input_length = pdf_file_preprocessing(filepath)
    pipe_sum = pipeline(
        'summarization',
        model=base_model,
        tokenizer=tokenizer,
        max_length=input_length//8, 
        min_length=25)
    result = pipe_sum(input_text)
    result = result[0]['summary_text']
    return result


def llm_pipeline_txt(filepath):
    input_text, input_length = file_text(filepath)
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

    choice = st.sidebar.selectbox("Select your choice", ["Type your Text (or Copy-Paste)", "Load from .txt file", "Load from .pdf file"])

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
                    result = text_summary(input_text)
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
                    summary = llm_pipeline_txt(filepath)
                    st.info("Summarization")
                    st.success(summary)                   
         

    elif choice == "Load from .pdf file":
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

