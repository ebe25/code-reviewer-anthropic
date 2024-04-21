from langchain_anthropic import ChatAnthropic
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage
from pathlib import Path

load_dotenv()
import os
import streamlit as st
import base64

#settiong build env
# os.environ["ANTHROPIC_API_KEY"] = os.getenv("ANTHROPIC_API_KEY")
# os.environ["LANGCHAIN_TRACING_V2"]= os.getenv("LANGCHAIN_TRACING_V2")
# os.environ["LANGCHAIN_API_KEY"]= os.getenv("LANGCHAIN_API_KEY")

#streamlit ui 
st.set_page_config(page_title="Chat with ebeCodes", page_icon=":flashlight:", layout="centered")
st.title("""
         Get your daily code reviews!💻 :flashlight:"""
         )

#define your input

##upload using upload care and getting back the url 
code_snippet = st.file_uploader("Upload a code snippet here")
if code_snippet is not None:
    # Read the content of the uploaded file and encode it into base64
    img_base64 = base64.b64encode(code_snippet.read()).decode("utf-8")
    st.image(f"data:image/png;base64,{img_base64}")
else:
    st.write("No code snippet uploaded.")
 
    




#prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", """
     As an expert software coding developer, your primary role is to analyze and review code snippets provided in code snippets as images. Your task is to thoroughly examine the code, assessing its efficiency, time complexity, and overall quality. After analyzing the code, provide a comprehensive summary of your findings, highlighting any areas that could be improved or optimized. """),
    ("user", "{code_snippets}")
])

output_parser = StrOutputParser()

#Paid api configuration
llm = ChatAnthropic(api_key=st.secrets["ANTHROPIC_API_KEY"],model="claude-3-opus-20240229", temperature=0.2, max_tokens=3000)


#This is basically what langchain does adds wrapper to adding multiple functionalities to an llm



chain =llm | output_parser

if code_snippet:
    messages = [
    HumanMessage(
        content=[
            {
                "type": "image_url",
                "image_url": {
                    # User codeSnippet
                    "url": f"data:image/png;base64,{img_base64}",  
                },
            },
            {"type": "text", "text": "As an expert software coding developer, your primary role is to analyze and review code snippets provided in code snippets as images. Your task is to thoroughly examine the code, assessing its efficiency, time complexity, and overall quality. After analyzing the code, provide a comprehensive summary of your findings, highlighting any areas that could be improved or optimized."},
        ]
    )
]
    response = chain.invoke(messages)
    st.write(response)
    
    

