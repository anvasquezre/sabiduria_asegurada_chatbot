
import chainlit as cl
from agent_utils import ChatBOT
from chainlit.server import app
from pydantic import BaseModel
from data_utils import save_feedback
import json
import re

@cl.on_chat_start
async def start():
    agent = ChatBOT()
    cl.user_session.set("agent", agent)
    await cl.Message(content="""
                     Hola 👋, soy un agente de búsqueda de información de polizas de Seguro.
                     Escribe una pregunta para poder ayudarte 🤗👋""").send()

@cl.action_callback("👍")
async def on_action(action):
    agent = cl.user_session.get("agent")
    question = agent.db_query
    ans = agent.answer
    feedback = {"question": question,"answer": ans ,"feedback": "Positive"}
    save_feedback(feedback)
    await cl.Message(content=f"Gracias por tu calificacion 👍").send()

    
@cl.action_callback("👎")
async def on_action(action):
    # [TODO] Save the feedback in a database
    agent = cl.user_session.get("agent")
    question = agent.db_query
    ans = agent.answer
    feedback = {"question": question,"answer": ans ,"feedback": "Negative"}
    save_feedback(feedback)
    await cl.Message(content=f"""
                     Gracias por tu calificacion.
                     Tu feedback nos ayudará a mejorar nuestra atencion al cliente""").send()

@cl.on_message
async def main(message):
    agent = cl.user_session.get("agent")  # type: AgentExecutor
    res = await agent.achat(
        message,
        callbacks=[cl.AsyncLangchainCallbackHandler()]
        )
    await cl.Message(content=res).send()
    
    pattern = r"([A-za-z]{3}\d{3,15})"
    pattern_found = re.findall(pattern, res)
    
    if pattern_found:
        element_list = []
        for source in pattern_found:
            element_list.append(cl.File(name=f"{source.upper()}.pdf",
                                       display="inline",
                                       path=f"./docs/{source.upper()}.pdf")) 
        await cl.Message(content="La respuesta anterior tuvo en cuenta las siguientes fuentes 📔",
                        elements=element_list).send()
    actions = [
        cl.Action(name="👍", value="👍", description="Click me!"),
        cl.Action(name="👎", value="👎", description="Click me!"),
    ]

    await cl.Message(content="Califica esta respuesta", actions=actions).send()

    


# Custom endopoint for testing purposes


class Message(BaseModel):
    message: str
    story: str | None = None
    
@app.post("/test/")
async def test(request: Message):
    agent = ChatBOT()
    agent.db_query = request.message
    source, cont = await agent.aget_related_docs(k=10)
    ans = "Mock up answer for testing purposes"
    response = {"answer": ans,"source": source, "title": cont}
    return json.dumps(response)