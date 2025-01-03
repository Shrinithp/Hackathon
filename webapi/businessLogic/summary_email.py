from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
 
class MailSummarizer:
    def __init__(self, model="gpt-4o-mini", temperature=0.2):
        # Initialize the LLM
        self.llm = ChatOpenAI(
            model=model,
            temperature=temperature
        )
 
        # Define the prompt template for summarizing mail content
        mail_summary_prompt_template = """
        You are an expert at summarizing content. 
        Summarize below content.
 
        content: {mail}
 
        Please return only the summary of the content:
        """
 
        # Set up the prompt with the mail input variable
        self.mail_summary_prompt = PromptTemplate(
            input_variables=["mail"],
            template=mail_summary_prompt_template,
        )
 
        # Create the LLMChain
        self.mail_summary_llm_chain = LLMChain(llm=self.llm, prompt=self.mail_summary_prompt)
 
    def summarize(self, mail: str) -> str:
        # Run the summarization chain with the input mail
        result = self.mail_summary_llm_chain.run({"mail": mail})
        # Return the summarized result
        return result.strip()
 
# Example usage:
# mail = "Your long email content goes here"
# summarizer = MailSummarizer()
# summary = summarizer.summarize(mail)
# print(summary)