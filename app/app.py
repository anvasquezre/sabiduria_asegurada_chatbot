
import chainlit as cl
from agent_utils import ChatBOT


@cl.on_chat_start
def start():
    agent = ChatBOT()
    cl.user_session.set("agent", agent)


@cl.on_message
async def main(message):
    agent = cl.user_session.get("agent")  # type: AgentExecutor
    res = await agent.achat(
        message,
        #callbacks=[cl.AsyncLangchainCallbackHandler()]
        )
    await cl.Message(content=res).send()
    # print(agent.db_response)
    # if agent.db_response:
    #     element_list = []
    #     source_list, title_list = agent.db_response[0] , agent.db_response[1]
    #     for source, title in zip(source_list, title_list):
    #         element_list.append(cl.Pdf(name=source,
    #                                    display="inline",
    #                                    path=f".{source}")) 
    #     await cl.Message(content="La respuesta anterior tuvo en cuenta las siguientes fuentes",
    #                     elements=element_list).send()
        
        