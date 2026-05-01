from langchain_ollama import OllamaLLM

llm = OllamaLLM(model="llama3:8b")
response = llm.invoke("Say hello")
print(response)