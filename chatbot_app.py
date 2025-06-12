from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
import streamlit as st


template ="""
hey, I will give input. you will rewrite everthing exactly same. can you do it? if you do just reply "I will do it."
"""

model = OllamaLLM(model="qwen2:1.5b")

prompt = ChatPromptTemplate.from_template(template)

result = model.invoke(input="hello world")
print(result)
def convert_to_latex(text):
    return f"\\text{{{text}}}"

st.title("Chatbot with LaTeX Output")

user_input = st.text_input("Enter your text:")

if user_input:
    result = model.invoke(input=user_input)
    latex_result = convert_to_latex(result)
    st.write("LaTeX Output:")
    st.latex(latex_result)