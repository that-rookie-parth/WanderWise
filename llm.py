from langchain_core.runnables import RunnablePassthrough
from typing import Dict
from langchain.memory import ChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import AIMessage
from langchain_core.messages import HumanMessage
import logging
from logging.handlers import SysLogHandler

from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from langchain.chains import ConversationChain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.memory import ChatMessageHistory, ConversationSummaryBufferMemory
from langchain.prompts.chat import (
    AIMessagePromptTemplate,
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
)
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableBranch, RunnablePassthrough
from langchain_openai import ChatOpenAI

from db_utils import pinecone
from dotenv import load_dotenv
load_dotenv()
import os
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    openai_api_key=OPENAI_API_KEY,
    temperature=0.2,
)

demo_ephemeral_chat_history = ChatMessageHistory()

# k is the number of chunks to retrieve
retriever = pinecone.as_retriever(
    search_type="similarity_score_threshold",
    search_kwargs={'score_threshold': 0.7, 'k': 10}
)


question_answering_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Answer the user's questions based on the below context:\n\n{context}",
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

document_chain = create_stuff_documents_chain(llm, question_answering_prompt)


def parse_retriever_input(params: Dict):
    return params["messages"][-1].content


retrieval_chain_with_only_answer = (
    RunnablePassthrough.assign(context=parse_retriever_input | retriever).
    assign(answer=document_chain)
)


def askQuery(
    destination,
    interest,
    transportation,
    extra,
    days
):
    query = f"Create an itinerary for {destination} taking into account the following preferences: Interests - {interest}, Transportation - {transportation}, Travel Duration - {days}, Additional Preference - {extra}. Create the itineray in markdown format and remember to not consider any additional preference if they are not related to travel or the provided destination"

    response = retrieval_chain_with_only_answer.invoke(
        {
            "messages": [
                HumanMessage(
                    content=query
                )
            ]
        }
    )
    return response["answer"]
    # return response