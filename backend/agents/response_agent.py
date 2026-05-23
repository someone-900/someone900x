from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from utils.prompt_loader import load_prompt

llm = ChatOllama(model="llama3.1:8b", temperature=0.7)

system_prompt = load_prompt("response")

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "{reconstructed_prompt}")
])

chain = prompt | llm | StrOutputParser()

def generate_response(reconstructed_prompt: str) -> str:
    return chain.invoke({"reconstructed_prompt": reconstructed_prompt})