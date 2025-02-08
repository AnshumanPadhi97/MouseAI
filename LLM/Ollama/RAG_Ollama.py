from langchain_community.document_loaders import PDFPlumberLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_ollama import OllamaEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import OllamaLLM

import Settings.constants as constants


EMBEDDING_MODEL = OllamaEmbeddings(model=constants.EMBED_LLM_MODEL)
DOCUMENT_VECTOR_DB = InMemoryVectorStore(EMBEDDING_MODEL)
LANGUAGE_MODEL = OllamaLLM(model=constants.TEXT_LLM_MODEL)


def clear_memory():
    InMemoryVectorStore.delete(None)


def rag_generate_answer(messages, user_query):

    if len(DOCUMENT_VECTOR_DB.store) == 0:
        return "No documents has been processed"

    conversation_history = "\n\n".join(
        [f"{msg['role']}: {msg['content']}" for msg in messages]
    )

    context_documents = DOCUMENT_VECTOR_DB.similarity_search(user_query)
    context_text = "\n\n".join([doc.page_content for doc in context_documents])

    combined_context = conversation_history + "\n\n" + context_text

    conversation_prompt = ChatPromptTemplate.from_template(
        constants.PROMPT_TEMPLATE)

    response_chain = conversation_prompt | LANGUAGE_MODEL
    llm_response = response_chain.invoke(
        {"user_query": user_query, "document_context": combined_context})

    return llm_response


def rag_process_document(file_paths):
    try:
        documents = []
        for file_path in file_paths:
            loader = PDFPlumberLoader(file_path)
            documents.extend(loader.load())
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            add_start_index=True
        )
        split_documents = text_splitter.split_documents(documents)
        DOCUMENT_VECTOR_DB.add_documents(split_documents)
        return True

    except Exception as e:
        return False
