import json
from langchain.vectorstores import Chroma
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from uuid import uuid4
import os
from langchain.embeddings.openai import OpenAIEmbeddings
from bs4 import BeautifulSoup
 
class MailGrouper:
 
    persist_directory = "init_group_persist_directory"
    collection_name = "init_mail_group_collection"
   
    model="gpt-4o-mini"
    temperature=0.3
    max_tokens=None
 
 
   
    def __init__(self, email_data):
        self.documents = [self.clean_html(item["body"]) for item in email_data] 
        self.ids = [str(item["id"]) for item in email_data] 
        self.metadatas = [{"source": "mail", "id": str(item["id"])} for item in email_data]
        
        self.embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))
        # Initialize vector store
        self.init_group_vectorstore = self._initialize_vectorstore()
 
        # Add texts to vector store
        self.init_group_vectorstore.add_texts(self.documents, self.metadatas, self.ids)
 
        # if "OPENAI_API_KEY" not in os.environ:
        #     os.environ["OPENAI_API_KEY"] = self.key

    @staticmethod
    def clean_html(html_text):
        """
        Remove HTML elements from the given text.
        """
        soup = BeautifulSoup(html_text, "html.parser")
        return soup.get_text()
 
    def _initialize_vectorstore(self):
        try:
            # Check if the vector store collection exists
            vectorstore = Chroma(
                collection_name=self.collection_name,
                embedding_function=self.embeddings,
                persist_directory=self.persist_directory
            )
        
            # vectorstore.reset_collection()
        
            # Return a new or cleaned vectorstore
            return vectorstore
        except Exception as e:
            raise RuntimeError(f"Error initializing vectorstore: {e}")
    
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
 
    def _group_all_mail(self):
        final_result_dicts = []
        try:
            for i, document in enumerate(self.documents, start=1):
                query = document
                score_results = self._retrieve_from_chroma(query, score_threshold=0.4)
 
                result_dicts = []
                for doc in score_results:
                    result_dicts.append({
                        "id": doc.metadata.get("id"),
                        "page_content": doc.page_content,
                        "group_name": i,
                    })
                    final_result_dicts.append({
                        "id": doc.metadata.get("id"),
                        "page_content": doc.page_content,
                        "group_name": i,
                    })
 
                doc_ids = [item["id"] for item in result_dicts]
                self.init_group_vectorstore.delete(ids=doc_ids)
 
                for doc in score_results:
                    if doc.page_content in self.documents:
                        self.documents.remove(doc.page_content)
            return final_result_dicts
        except Exception as e:
            raise RuntimeError(f"Error grouping all mail: {e}")
 
    def _group_id_content(self, grouped_mail_data):
        try:
            grouped_content = {}
            grouped_id = {}
 
            for item in grouped_mail_data:
                group_name = item["group_name"]
                page_content = item["page_content"]
                id = item["id"]
 
                if group_name not in grouped_content:
                    grouped_content[group_name] = []
                grouped_content[group_name].append(page_content)
 
                if group_name not in grouped_id:
                    grouped_id[group_name] = []
                grouped_id[group_name].append(id)
 
            return grouped_content, grouped_id
        except Exception as e:
            raise RuntimeError(f"Error grouping ID and content: {e}")
 
    def _group_info(self, grouped_content, grouped_id):
        try:
            llm = ChatOpenAI(
                model=self.model,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
            )
 
            mail_info_prompt_template = """
            You are an AI assistant specialized in identifying similarities in emails and assigning a group name along with a description that explains the reasoning behind the grouping.
 
            Emails: {mails}
 
            Please return only the group name and description as a dictionary.
            example output:
            "group_name": "Promotional Offers",
            "description": "This group includes emails that promote special offers, discounts, or rewards, encouraging the recipient to take immediate action."
            """
 
            mail_info_prompt = PromptTemplate(
                input_variables=["mails"],
                template=mail_info_prompt_template,
            )
 
            mail_info_llm_chain = LLMChain(llm=llm, prompt=mail_info_prompt)
 
            mail_groups_with_info = []
            for group, contents in grouped_content.items():
                result = mail_info_llm_chain.run({"mails": contents})
                name_group_data = json.loads(result)
 
                group_data = {
                    "group_name": name_group_data["group_name"],
                    "description": name_group_data["description"],
                    "ids": grouped_id[group]
                }
                mail_groups_with_info.append(group_data)
 
            return mail_groups_with_info
        except Exception as e:
            raise RuntimeError(f"Error grouping info: {e}")
 
    def run(self):
        try:
            grouped_mails = self._group_all_mail()
            grouped_contents, grouped_ids = self._group_id_content(grouped_mails)
            final_output = self._group_info(grouped_contents, grouped_ids)
            return final_output
        except Exception as e:
            raise RuntimeError(f"Error running MailGrouper: {e}")
 
# Usage Example
# grouper = MailGrouper(documents)
# output = grouper.run()
# print(output)