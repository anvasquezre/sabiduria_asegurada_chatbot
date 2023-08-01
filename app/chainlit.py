
import chainlit as cl
from agent_utils import ChatBOT


@cl.on_chat_start
def start():
    agent = ChatBOT()
    cl.user_session.set("agent", agent)


@cl.on_message
async def main(message):
    agent = cl.user_session.get("agent")  # type: AgentExecutor
    res = await agent.achat(message, callbacks=[cl.AsyncLangchainCallbackHandler(stream_final_answer=True)])

    await cl.Message(content=res).send()