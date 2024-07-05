# Importing everything necessary
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI

import requests
import re

# Get the API key from the .env file
import os
from dotenv import load_dotenv

load_dotenv()
os.environ["LANGCHAIN_TRACING_V2"] = "True"


# Defining the data extractor function
def data_extractor(link):
    html_doc = requests.get(link).text
    regex = re.compile("<title>(.*?)</title>", re.IGNORECASE | re.DOTALL)
    return regex.search(html_doc).group(1)


# Get the genres and moods according to the user browsing history
def song_retrieve(links):
    titles = []
    for i in links:
        titles.append(data_extractor(i))
    # Define a prompt
    with open("prompt_v3.txt", "r") as f:
        prompt_template = f.read()
        prompt = PromptTemplate(
            input_variables=["links", "titles"], template=prompt_template
        )

    # Load the chain
    llm = ChatGoogleGenerativeAI(temperature=0, model="gemini-pro")
    chain = prompt | llm | StrOutputParser()

    # Run the chain
    return chain.invoke({"links": links, "titles": titles})
