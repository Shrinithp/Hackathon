# for new user custom group
 
import os
from bs4 import BeautifulSoup
from langchain.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
 
class UserCustomGrouping:
    key = "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"
    persist_directory = "new_group_directory"
    collection_name = "new_group_collection"
 
    def __init__(self, email_data):
 
        self.documents = [self.clean_html(item["body"]) for item in email_data] 
        self.ids = [str(item["id"]) for item in email_data] 
        self.metadatas = [{"source": "mail", "id": str(item["id"])} for item in email_data]
 
        self.embeddings = OpenAIEmbeddings(openai_api_key=self.key)
        self.new_group_vectorstore = self._initialize_vectorstore()
 
        # Add texts to vector store
        self.new_group_vectorstore.add_texts(self.documents, self.metadatas, self.ids)
 
        if "OPENAI_API_KEY" not in os.environ:
            os.environ["OPENAI_API_KEY"] = self.key
    @staticmethod
    def clean_html(html_text):
        """
        Remove HTML elements from the given text.
        """
        soup = BeautifulSoup(html_text, "html.parser")
        return soup.get_text()
    
    def _initialize_vectorstore(self):
        try:
            return Chroma(
                collection_name=self.collection_name,
                embedding_function=self.embeddings,
                persist_directory=self.persist_directory
            )
        except Exception as e:
            raise RuntimeError(f"Error initializing vectorstore: {e}")
 
    # def initialize_vectorstore(self):
    #     """
    #     Initializes the Chroma vector store.
    #     """
    #     try:
    #         self.new_group_vectorstore = Chroma(
    #             collection_name=self.collection_name,
    #             embedding_function=self.embedding_function,
    #             persist_directory=self.persist_directory
    #         )
    #     except Exception as e:
    #         raise RuntimeError(f"Error initializing Chroma vector store: {e}")
 
    # def add_texts(self, documents, metadatas, ids):
 
    #     if not self.new_group_vectorstore:
    #         raise RuntimeError("Vector store not initialized. Call 'initialize_vectorstore()' first.")
       
    #     try:
    #         self.new_group_vectorstore.add_texts(documents, metadatas, ids)
    #     except Exception as e:
    #         raise RuntimeError(f"Error adding texts to Chroma vector store: {e}")
   
    def _retrieve_from_chroma(self, query, top_k=None, score_threshold=None):
        try:
            max_results = top_k if top_k is not None else self.init_group_vectorstore._collection.count()
            docs = self.init_group_vectorstore.similarity_search_with_score(query, k=max_results)
            print(docs)
            results = []
            if top_k is not None:
                results = [doc for doc, score in docs]
            scored_results = []
            if score_threshold is not None:
                for doc, score in docs:
                    if score <= score_threshold:
                        scored_results.append(doc)
                results = scored_results
            return results
            # if score_threshold is not None:
            #     docs = [doc for doc, score in docs if score <= score_threshold]
            # return [doc for doc, _ in docs]
        except Exception as e:
            raise RuntimeError(f"Error retrieving from Chroma: {e}")
 
 
    def retrieve_results(self, query, score_threshold=0.4):
 
        if not self.new_group_vectorstore:
            raise RuntimeError("Vector store not initialized. Call 'initialize_vectorstore()' first.")
       
        try:
            # Perform similarity search
            score_results = self._retrieve_from_chroma(query, score_threshold=0.4)
            # Extract IDs from results
            id_list = [doc.metadata.get("id") for doc in score_results]
            return id_list
        except Exception as e:
            raise RuntimeError(f"Error retrieving results from Chroma vector store: {e}")
 
    def run(self, query, score_threshold=0.4):
 
        return self.retrieve_results(query, score_threshold)