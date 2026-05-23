from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from utils.prompt_loader import load_prompt

llm = ChatOllama(model="llama3.1:8b", temperature=0.3)

system_prompt = load_prompt("reconstruction")

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", """Original prompt: {original_prompt}

Clarifying questions that were asked:
{questions}

User's answers:
{answers}

Now reconstruct the ideal prompt.""")
])

chain = prompt | llm | StrOutputParser()

def reconstruct_prompt(original_prompt: str, questions: str, answers: str) -> str:
    return chain.invoke({
        "original_prompt": original_prompt,
        "questions": questions,
        "answers": answers
    })