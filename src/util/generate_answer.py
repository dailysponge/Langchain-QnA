import re


def generate_answer(index, QA_PROMPT, question):
    # Regex pattern for URL with .gov.sg domain
    pattern = r'(https?://[^\s]*\.gov\.sg[^\s]*)'
    query_str = question
    response = index.as_query_engine(
        text_qa_template=QA_PROMPT).query(query_str)
    # score = response.source_nodes[0].score
    return response


def get_bulleted_strings(source_set):
    bulleted_list = ["• " + source for source in source_set]
    formatted_list = "\n".join(bulleted_list)
    return formatted_list
