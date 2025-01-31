# Models: ~/.ollama/models

import os
from langchain_ollama import ChatOllama

BRAVO_OLLAMA_MODEL = os.getenv("BRAVO_OLLAMA_MODEL", "phi4")

llm = ChatOllama(
    model=BRAVO_OLLAMA_MODEL,
    temperature=0,
)