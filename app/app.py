
import chainlit as cl
from agent_utils import ChatBOT
from chainlit.server import app
from pydantic import BaseModel
from data_utils import save_feedback
import json
import re

@cl.on_chat_start
async def start():
    """
    Handle the start of a chat session with the PolicyGuru AI agent.

    This asynchronous function is triggered at the start of a chat session. It initializes a ChatBOT instance,
    stores it in the user's session, and sends an introductory message to the user.

    """
    # Create a ChatBOT instance and store it in the user's session
    agent = ChatBOT()
    cl.user_session.set("agent", agent)
    # Send an introductory message to the user
    await cl.Message(content="""
                     Hola 👋, soy un agente de búsqueda de información de polizas de Seguro.
                     Escribe una pregunta para poder ayudarte 🤗👋""").send()

@cl.action_callback("👍")
async def on_action(action):
    """
    Handle the user's positive feedback action.

    This asynchronous function is triggered when the user provides positive feedback. It retrieves the ChatBOT instance
    from the user's session, extracts the question and answer, and saves the feedback information in the database.

    Args:
        action: The action data associated with the user's action.

    """
    # Retrieve the ChatBOT instance from the user's session
    agent = cl.user_session.get("agent")
    # Retrieve the question and answer
    question = agent.db_query
    ans = agent.answer
    # Save the feedback in the database
    feedback = {"question": question,"answer": ans ,"feedback": "Positive"}
    save_feedback(feedback)
    await cl.Message(content=f"Gracias por tu calificacion 👍").send()

    
@cl.action_callback("👎")
async def on_action(action):
    """
    Handle the user's negative feedback action.

    This asynchronous function is triggered when the user provides negative feedback. It retrieves the ChatBOT instance
    from the user's session, extracts the question and answer, and saves the feedback information in the database.

    Args:
        action: The action data associated with the user's action.

    """
    # Retrieve the ChatBOT instance from the user's session
    agent = cl.user_session.get("agent")
    # Retrieve the question and answer
    question = agent.db_query
    ans = agent.answer
    # Save the feedback in the database
    feedback = {"question": question,"answer": ans ,"feedback": "Negative"}
    save_feedback(feedback)
    await cl.Message(content=f"""
                    Gracias por tu calificacion.
                    Tu feedback nos ayudará a mejorar nuestra atencion al cliente""").send()

@cl.on_message
async def main(message):
    """
    Handle incoming messages and interaction with the PolicyGuru AI agent.

    This asynchronous function is triggered when the user sends a message. It interacts with the PolicyGuru AI agent,
    processes the agent's response, handles feedback, and sends appropriate messages to the user.

    Args:
        message: The incoming message from the user.

    """
    # Retrieve the ChatBOT instance from the user's session
    agent = cl.user_session.get("agent")  # type: AgentExecutor
    # Process the user's message and get the agent's response
    res = await agent.achat(
        message,
        callbacks=[cl.AsyncLangchainCallbackHandler()]
        )
    await cl.Message(content=res).send()
    # Checks if the response has a pattern of policy number
    pattern = r"([A-za-z]{3}\d{3,15})"
    found = re.findall(pattern, res)
    pattern_found = list(set(found))
    # If the response has a pattern of policy number, send the policy document to chat
    if pattern_found:
        element_list = []
        for source in pattern_found:
            element_list.append(cl.File(name=f"{source.upper()}.pdf",
                                       display="inline",
                                       path=f"./docs/{source.upper()}.pdf")) 
        await cl.Message(content="La respuesta anterior tuvo en cuenta las siguientes fuentes 📔",
                        elements=element_list).send()
    # Send a feedback message to the user
    actions = [
        cl.Action(name="👍", value="👍", description="Click me!"),
        cl.Action(name="👎", value="👎", description="Click me!"),
    ]

    await cl.Message(content="Califica esta respuesta", actions=actions).send()

    


# Custom endopoint for testing purposes


class Message(BaseModel):
    """
    Represents a message input for testing purposes.

    This class defines the structure of a message used for testing purposes. It includes the main `message` content
    and an optional `story` content.

    Attributes:
        message (str): The main content of the message.
        story (str | None): An optional content describing the story related to the message.

    """
    message: str
    story: str | None = None
    
@app.post("/test/")
async def test(request: Message):
    """
    Handle testing requests and return a mock response.

    This asynchronous function handles testing requests by creating a ChatBOT instance, setting the database query,
    retrieving related documents, and constructing a mock response for testing purposes.

    Args:
        request (Message): The input request containing the message for testing.

    Returns:
        str: A JSON-encoded response containing a mock answer, source information, and title.

    """
    agent = ChatBOT()
    agent.db_query = request.message
    source, cont = await agent.aget_related_docs(k=10)
    ans = "Mock up answer for testing purposes"
    response = {"answer": ans,"source": source, "title": cont}
    return json.dumps(response)