from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
 
class MailResponder: 
    def __init__(self, model="gpt-4o-mini", temperature=0.2):
        # Initialize the LLM
        self.llm = ChatOpenAI(
            model=model,
            temperature=temperature
        )
 
        # Define the prompt template for generating email replies
        mail_response_prompt_template = """
        You are an expert at replying to emails. 
        Generate a reply to the below email.
 
        Email: {mail}
 
        Please return only the reply to the mail:
        """
 
        # Set up the prompt with the mail input variable
        self.mail_response_prompt = PromptTemplate(
            input_variables=["mail"],  # Match singular key
            template=mail_response_prompt_template,
        )
 
        # Create the LLMChain
        self.mail_response_llm_chain = LLMChain(llm=self.llm, prompt=self.mail_response_prompt)
 
    def generate_reply(self, mail: str) -> str:
        # Run the reply generation chain with the input mail
        result = self.mail_response_llm_chain.run({"mail": mail})  # Use singular key
        # Return the generated reply
        return result.strip()
 
# Test the responder
# responder = MailResponder()
# reply = responder.generate_reply(
#     'Hi Team, The client has asked for a detailed timeline for the data migration project. They’re expecting the document by tomorrow EOD. I’ll need inputs from everyone involved in this project to finalize the details. Please send me your updates ASAP. Thanks, Rahul Chawla'
# )
# print(reply)

 
# Example usage:
# mail = "Your email content goes here"
# responder = MailResponder()
# reply = responder.generate_reply(mail)
# print(reply)