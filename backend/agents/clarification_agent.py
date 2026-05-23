from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from utils.prompt_loader import load_prompt

llm = ChatOllama(model="llama3.1:8b", temperature=0.7)

system_prompt = load_prompt("clarification")

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "{user_prompt}")
])

chain = prompt | llm | StrOutputParser()

def get_clarifying_questions(user_prompt: str) -> str:
    return chain.invoke({"user_prompt": user_prompt})