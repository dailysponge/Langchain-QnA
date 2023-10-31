from llama_index import LLMPredictor, PromptHelper, ServiceContext, StorageContext, load_index_from_storage
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv
from prompt.prompt import QA_PROMPT
from util.generate_nodes import generate_document_from_url
from util.index_setting import create_index, update_index
from util.generate_answer import generate_answer
from constants import AGENT_LLM, EMBEDDING_LLM
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
load_dotenv()

app = Flask(__name__)
CORS(app)


max_input_size = 4096
num_output = 256
prompt_helper = PromptHelper(
    max_input_size, num_output, chunk_size_limit=1024)

service_context = ServiceContext.from_defaults(
    llm=AGENT_LLM, embed_model=EMBEDDING_LLM
)


@app.route('/')
def index():
    # Tracks the number of storage index
    folder_path = f"./storage"
    return os.listdir(folder_path)


@app.route("/question", methods=["POST"])
def ask_question():
    question = request.json["question"]
    try:
        # retrieve storage context
        folder_path = f"./storage"
        if len(os.listdir(folder_path)) == 0:
            documents = generate_document_from_url(
                ['https://www.google.com/'])
            # create index
            index = create_index(service_context, documents)
        else:
            storage_context = StorageContext.from_defaults(
                persist_dir=f"./storage")
            index = load_index_from_storage(
                storage_context, service_context=service_context)
        reply = generate_answer(index, QA_PROMPT, question)
    except Exception as e:
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "data": {
                    "error": str(e),
                },
                "message": "An error occurred while querying index."
            }
        ), 500

    return jsonify(
        {
            "code": 200,
            "data": {
                "reply": reply.response,
            },
            "message": "Success"
        }
    )


@app.route("/train", methods=["PATCH"])
def edit_index():
    try:
        # Retrieve index
        storage_context = StorageContext.from_defaults(
            persist_dir="./storage")
        index = load_index_from_storage(
            storage_context, service_context=service_context)

        document_type = request.json["document_type"]

        if document_type == "url":
            urls = request.json['urls']
            index = update_index(index, urls=urls)

        elif document_type == "pdf":
            pdf = request.json['pdf']
            index = update_index(index, pdf=pdf)

    except Exception as e:
        print("Error", e)
        return jsonify(
            {
                "code": 500,
                "data": {
                    "error": str(e),
                },
                "message": "An error occurred while updating index"
            }
        ), 500

    return jsonify(
        {
            "code": 200,
            "message": "Success"
        }
    )


if __name__ == '__main__':
    app.run(port=int(os.environ.get('PORT', 8080)), debug=True, host='0.0.0.0')
