
import time
from flask import session
import openai
import os
from langchain.vectorstores import Chroma
from typing import List, Tuple
import re
import ast
import html
from load_config import LoadConfig

APPCFG = LoadConfig()


class ChatBot:


    @staticmethod
    def respond(chatbot: List, message: str, data_type: str = "Process for RAG", temperature: float = 0.0) -> Tuple:
        """
        Generate a response to a user query using document retrieval and language model completion.
        """
        if data_type == "Preprocessed doc":
            directory = APPCFG.persist_directory
        elif data_type == "Process for RAG":
            # Correct directory without extra 'chroma' in the path
            user_id = session.get('user')
            directory = os.path.join(APPCFG.custom_persist_directory, user_id)
            print(f"Using directory for vector database: {directory}")
        else:
            chatbot.append((message, "Welcome to Demo Bot. No file was uploaded. Please first upload your files using the 'upload' button."))
            return "", chatbot, None

        if not os.path.exists(directory):
            print(f"Directory not found: {directory}")
            chatbot.append((message, "No relevant documents found in the vector store."))
            return "", chatbot, None

        vectordb = Chroma(persist_directory=directory, embedding_function=APPCFG.embedding_model)

        docs = vectordb.similarity_search(message, k=APPCFG.k)
        if not docs:
            print(f"No documents found in vector store at: {directory}")
            chatbot.append((message, "No relevant documents found in the vector store."))
            return "", chatbot, None

        print("Documents found:", docs)
        
        question = "# User new question:\n" + message
        retrieved_content = ChatBot.clean_references(docs)
        chat_history = "\n".join([f"[{q}, {a}]" for q, a in chatbot[-APPCFG.number_of_q_a_pairs:]])
        chat_history_formatted = f"# Chat history:\n{chat_history}\n\n"
        print("Chat History:", chat_history_formatted)
        prompt = f"{chat_history_formatted}{retrieved_content}{question}"
        
        response = openai.ChatCompletion.create(
            messages=[
                {"role": "system", "content": APPCFG.llm_system_role},
                {"role": "user", "content": prompt}
            ],
            model="gpt-4",
            temperature=temperature
        )
        
        chatbot.append((message, response["choices"][0]["message"]["content"]))
        
        return "", chatbot, retrieved_content


    @staticmethod
    def clean_references(documents: List) -> str:

        server_url = "http://localhost:8000"
        documents = [str(x)+"\n\n" for x in documents]
        markdown_documents = ""
        counter = 1
        for doc in documents:
            # Extract content and metadata
            content, metadata = re.match(
                r"page_content=(.*?)( metadata=\{.*\})", doc).groups()
            metadata = metadata.split('=', 1)[1]
            metadata_dict = ast.literal_eval(metadata)

            # Decode newlines and other escape sequences
            content = bytes(content, "utf-8").decode("unicode_escape")

            # Replace escaped newlines with actual newlines
            content = re.sub(r'\\n', '\n', content)
            # Remove special tokens
            content = re.sub(r'\s*<EOS>\s*<pad>\s*', ' ', content)
            # Remove any remaining multiple spaces
            content = re.sub(r'\s+', ' ', content).strip()

            # Decode HTML entities
            content = html.unescape(content)

            # Replace incorrect unicode characters with correct ones
            content = content.encode('latin1').decode('utf-8', 'ignore')

            # Remove or replace special characters and mathematical symbols
            # This step may need to be customized based on the specific symbols in your documents
            content = re.sub(r'â', '-', content)
            content = re.sub(r'â', '∈', content)
            content = re.sub(r'Ã', '×', content)
            content = re.sub(r'ï¬', 'fi', content)
            content = re.sub(r'â', '∈', content)
            content = re.sub(r'Â·', '·', content)
            content = re.sub(r'ï¬', 'fl', content)

            pdf_url = f"{server_url}/{os.path.basename(metadata_dict['source'])}"

            # Append cleaned content to the markdown string with two newlines between documents
            markdown_documents += f"# Reference {counter}:\n" + content + "\n\n" + \
                f"Source: {os.path.basename(metadata_dict['source'])}" + " | " +\
                f"Page number: {str(metadata_dict['page'])}" + " | "  "\n\n"
            counter += 1

        return markdown_documents