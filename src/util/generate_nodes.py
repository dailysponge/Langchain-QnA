from llama_index import download_loader, Document
from llama_index import SimpleWebPageReader
from llama_index.node_parser import SimpleNodeParser
from bs4 import BeautifulSoup
from io import BytesIO
import PyPDF2
import requests
from dotenv import load_dotenv

load_dotenv()


# Convert URL into Nodes using SimpleWebPageReader Loader


def generate_document_from_url(urls):
    documents = SimpleWebPageReader(html_to_text=True).load_data(urls)
    return documents

# Convert Documents into Nodes


def generate_nodes_from_document(document):
    parser = SimpleNodeParser()
    nodes = parser.get_nodes_from_documents(document)
    return nodes

# Convert HTML file into Text Chunks using Custom HTML loader


def convert_html_to_text_chunks(file_path):
    with open(file_path, 'r') as file:
        html_content = file.read()
        soup = BeautifulSoup(html_content, 'html.parser')

        text_chunks = []
        for element in soup.find_all(text=True):
            text = element.strip()
            if text:
                text_chunks.append(text)

        return text_chunks

# Convert HTML URL into Text Chunks using Custom URL loader


def convert_url_to_text_chunks(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        text_content = soup.get_text()
        cleaned_text = ' '.join(text_content.split())
        return cleaned_text
    except requests.exceptions.RequestException as e:
        print('Error:', e)
    except Exception as e:
        print('An error occurred:', e)


# Convert PDF into Text Chunks using Custom PDF loader
def convert_pdf_to_text(file_path):
    try:
        with open(file_path, 'rb') as file:
            text = extract_pdf_content(file)
        return text
    except Exception as e:
        print('An error occurred:', e)


def convert_pdf_url_to_nodes(file_url, file_name):
    # Download the file
    response = requests.get(file_url)
    pdf_content = BytesIO(response.content)
    pdf_text = extract_pdf_content(pdf_content)
    document = Document(doc_id=file_name, text=pdf_text)
    nodes = generate_nodes_from_document([document])

    return nodes


def extract_pdf_content(source):
    pdf_reader = PyPDF2.PdfReader(source)
    text = ''
    for page_number in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_number]
        text += page.extract_text()
    return text
