from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = ChatOllama(model="llama3.1:8b", temperature=0.7)

clarification_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a clarification agent. When a user gives you a vague prompt,
your job is to identify the 3 most important missing pieces of information.
Ask exactly 3 short, clear questions — numbered 1, 2, 3.
Do not answer the prompt. Only ask the questions."""),
    ("human", "{user_prompt}")
])

clarification_chain = clarification_prompt | llm | StrOutputParser()

vague_prompt = "i want to work on an assignment for my english class"

print("=== VAGUE PROMPT ===")
print(vague_prompt)
print("\n=== CLARIFYING QUESTIONS ===")

questions = clarification_chain.invoke({"user_prompt": vague_prompt})
print(questions)