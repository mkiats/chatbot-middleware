from dotenv import load_dotenv
import os
import logging
from langchain_openai import AzureChatOpenAI
from langchain_openai.embeddings import AzureOpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.runnables import RunnablePassthrough, RunnableParallel

async def main(query: str) -> str:
    # ----------------- RAG Chatbot Logic -----------------
    # Load environment variables
    load_dotenv(override=True)
    try:
    # Initialize OpenAI and embeddings models
        llm = AzureChatOpenAI(
            azure_endpoint=os.environ['AZURE_OPENAI_ENDPOINT'],
            api_key=os.environ['AZURE_OPENAI_API_KEY'],
            deployment_name=os.environ['AZURE_OPENAI_DEPLOYMENT_NAME'],
            model_name=os.environ['AZURE_OPENAI_MODEL_NAME'],
            api_version=os.environ['AZURE_OPENAI_API_VERSION'],
            temperature=0
        )
        embeddings = AzureOpenAIEmbeddings(azure_endpoint=os.environ['AZURE_OPENAI_ENDPOINT'],
                                        api_key=os.environ['AZURE_OPENAI_API_KEY'],
                                        azure_deployment=os.environ['AZURE_EMBEDDING_DEPLOYMENT_NAME'],
                                        model=os.environ['AZURE_TEXT_EMBEDDING_MODEL'],
                                        )
        file_loader = PyPDFLoader('pagerank.pdf')
        page = file_loader.load_and_split()
        splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=50)
        pages = splitter.split_documents(page)
        vector_store = FAISS.from_documents(pages, embeddings)
        # Create a retriever from the vector store
        retriever = vector_store.as_retriever()
        # Define the question template
        # TODO: You can change the template according to how you want your chatbot to reply
        question_template = """
        You are a teaching assistant at NTU.
        If you don't know the answer, just say that you don't know, don't try to make up an answer.
        context:{context}
        question:{question}
        """
        # Create a prompt template from the question template
        prompt = PromptTemplate.from_template(template=question_template)
        # Create a result chain with the retriever, prompt, model, and parser
        chain = (RunnableParallel(context = retriever, question = RunnablePassthrough()) | prompt | llm | StrOutputParser())
        # ----------------------------------------------------
        return chain.invoke(query)

    except Exception as e:
        return "Error has occured"
