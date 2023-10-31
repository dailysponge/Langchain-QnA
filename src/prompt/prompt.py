from llama_index import QuestionAnswerPrompt
from datetime import date

current_date = date.today()

QA_PROMPT_TMPL = (

    """"You are a helpful chatbot that provides information about a certain document to users. You are given a document and a question. Your task is to answer the question using the information in the document. If you are unable to answer the question, respond with 'I don't know.'. Prioritize accuracy in your responses and your responses should directly answer the question.

Document text: '{context_str}':

Question: '{query_str}'

"""
)
QA_PROMPT = QuestionAnswerPrompt(QA_PROMPT_TMPL)
