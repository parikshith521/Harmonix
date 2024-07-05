# Importing everything necessary
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.docstore.document import Document
from langchain_community.document_loaders import WebBaseLoader


# Get the API key from the .env file
import os
from dotenv import load_dotenv

load_dotenv()
os.environ["LANGCHAIN_TRACING_V2"] = "True"


# Defining the data extractor function
def data_extractor(link):
    loader = WebBaseLoader(link)
    docs = loader.load()
    return docs


# Define a sentiment analysis function
def sentiment(links):
    summ_data = []
    # Define the llm model and the chain
    llm = ChatGoogleGenerativeAI(temperature=0, model="gemini-pro")

    # Define prompt
    prompt_template = """Write a concise summary in less than 10 words of the following:
    "{text}"
    CONCISE SUMMARY:"""
    prompt = PromptTemplate.from_template(prompt_template)

    # Define LLM chain
    chain = prompt | llm | StrOutputParser()

    # Extract data from each of the links and summarise it
    with open("summarised_text.txt", "w") as f:
        for link in links:
            docs = data_extractor(link)
            # Summarize the data and append it to the list
            result = chain.invoke(docs)
            f.write(result)
            f.write("\n\n")
    with open("summarised_text.txt", "r") as s:
        with open("summariser_prompt.txt", "r") as f:
            prompt_template2 = f.read()
            prompt2 = PromptTemplate(
                input_variables=["input"], template=prompt_template2
            )
            chain2 = prompt2 | llm | StrOutputParser()
            return chain2.invoke(s.read())


# Get the genres and moods according to the user browsing history
def song_retrieve(links):
    # Define a prompt
    with open("prompt.txt", "r") as f:

        prompt_template = f.read()
        prompt = PromptTemplate(input_variables=["data"], template=prompt_template)

    # Load the chain
    llm = ChatGoogleGenerativeAI(temperature=0, model="gemini-pro")
    chain = prompt | llm | StrOutputParser()

    # Extract data from the link
    data = sentiment(links)

    # Run the chain
    result = chain.invoke(data)

    return result


links = [
    "https://www.youtube.com/watch?v=l6ev1lGq0B4",
    "https://www.reddit.com/r/AskReddit/comments/jdvj55/what_do_you_do_to_cheer_yourself_when_youre_sad/",
    "https://www.reddit.com/r/AskReddit/comments/3aosor/redditors_who_are_feeling_a_bit_sad_right_now/",
]

print(song_retrieve(links))
