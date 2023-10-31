# create index
from llama_index import GPTVectorStoreIndex, Document
from util.generate_nodes import convert_url_to_text_chunks, generate_nodes_from_document, convert_pdf_url_to_nodes
from dotenv import load_dotenv

load_dotenv()


def create_index(service_context, documents):
    index = GPTVectorStoreIndex([], service_context=service_context)
    for doc in documents:
        index.insert(doc)
    # index.insert_nodes(nodes)

    # Save the index for future use
    index.storage_context.persist(persist_dir="./storage")
    return index


def update_index(index, urls=None, pdf=None):
    node_list = []

    # Convert urls into nodes via Document injection
    if urls:
        for url in urls:
            url_content = convert_url_to_text_chunks(url)
            document = Document(text=url_content, doc_id=url)
            nodes = generate_nodes_from_document([document])
            node_list += [node for node in nodes]
    if pdf:
        file_url = pdf['file_url']
        file_name = pdf['file_name']
        nodes = convert_pdf_url_to_nodes(file_url, file_name)
        node_list += [node for node in nodes]

    index.insert_nodes(node_list)
    index.storage_context.persist()
    return index
