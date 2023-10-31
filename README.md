<h1>Getting started with Langchain QnA</h1>

<h2>Pre-requisites</h2>

- Azure OpenAi API access

<h2>Installation</h2>

- download required dependencies with `python -m pip install --no-cache-dir -r requirements.txt`
- Create a `.env` file using `.env.template` file and populate OpenAI API key

<h2>Things to note</h2>

- There will be a folder called storage.

  - It holds 4 files: [`docstore.json`, `graph_store.json`, `index_store.json`, `vector_store.json`]
  - `docstore.json` contains all the metadata of the embeddings
  - `graph_store.json` contains the mappings between embedding to form relationships
  - `index_store.json` stores all the indexed embeddings for quicker search
  - `vector_store.json` stores all actual vector embedding of the data
    Creation of Index

- Adjust `persist_dir` in this line of code `StorageContext.from_defaults(persist_dir=f"./storage")` to adjust where the index files are stored.
- Adjust `folder_path` and `persist_dir` in app.py file found in this line of code `storage_context = StorageContext.from_defaults(persist_dir="./storage")` to change where the data source is coming from.

<h2>Usage</h2>

- Use the endpoint "[POST] /question" and {"question": QUESTION} in the body to get results
- Use the endpoint "[PATCH] /train" to update the database
  - For PDF files, use
    {`document_type`: `pdf`,
    `pdf`: {`file_url`: FILE_URL, `file_name`: FILE_NAME}
    }
  - For URL based files, use
    {
    `document_type`: `url`
    `urls`: []
    }
