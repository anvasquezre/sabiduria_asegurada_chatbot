from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.chat_models import ChatOpenAI
from langchain.agents import Tool, AgentOutputParser, AgentExecutor,LLMSingleActionAgent,AgentOutputParser
from langchain.prompts import StringPromptTemplate
from langchain import LLMChain
from typing import List, Optional, Union
from langchain.schema import AgentAction, AgentFinish, OutputParserException
import re
import config
from langchain.callbacks.streaming_stdout_final_only import (
    FinalStreamingStdOutCallbackHandler,
)
from langchain.tools import DuckDuckGoSearchRun , DuckDuckGoSearchResults
from data_utils import connect_db, aconnect_db

class CustomOutputParser(AgentOutputParser):

    def parse(self, llm_output: str) -> Union[AgentAction, AgentFinish]:
        # Check if agent should finish
        if "Final Answer:" in llm_output:
            return AgentFinish(
                # Return values is generally always a dictionary with a single `output` key
                # It is not recommended to try anything else at the moment :)
                return_values={"output": llm_output.split("Final Answer:")[-1].strip()},
                log=llm_output,
            )
        # Parse out the action and action input
        regex = r"Action\s*\d*\s*:(.*?)\nAction\s*\d*\s*Input\s*\d*\s*:[\s]*(.*)"
        match = re.search(regex, llm_output, re.DOTALL)
        if not match:
            raise OutputParserException(f"Could not parse LLM output: `{llm_output}`")
        action = match.group(1).strip()
        action_input = match.group(2)
        # Return the action and action input
        return AgentAction(tool=action, tool_input=action_input.strip(" ").strip('"'), log=llm_output)

# Set up a prompt template
class CustomPromptTemplate(StringPromptTemplate):
    """ Creates a custom prompt template for the agent

    Args:
        StringPromptTemplate (_type_): String template

    Returns:
        StringPromptTemplate: PromptTemplateClass
    """    
    # The template to use
    template: str
    # The list of tools available
    tools: List[Tool]

    def format(self, **kwargs) -> str:
        # Get the intermediate steps (AgentAction, Observation tuples)
        # Format them in a particular way
        intermediate_steps = kwargs.pop("intermediate_steps")
        thoughts = ""
        for action, observation in intermediate_steps:
            thoughts += action.log
            thoughts += f"\nObservation: {observation}\nThought: "
        # Set the agent_scratchpad variable to that value
        kwargs["agent_scratchpad"] = thoughts
        # Create a tools variable from the list of tools provided
        kwargs["tools"] = "\n".join([f"{tool.name}: {tool.description}" for tool in self.tools])
        # Create a list of tool names for the tools provided
        kwargs["tool_names"] = ", ".join([tool.name for tool in self.tools])
        return self.template.format(**kwargs)


def get_chat_template():
    openai_template="""Eres un agente comercial de polizas de la empresa QuePlan. Eres encargado de responder las preguntas de los clientes sobre las polizas de la empresa.
            Si no sabes la respuesta, simplemente di que no lo sabes, no trates de inventar una respuesta.
            Crea una respuesta con la suficiente información para que el usuario pueda entender la respuesta. No te limites a responder con un 'Sí' o un 'No', ni por extenso ni abreviado.
            
            Utilizaras el siguiente contexto para responder la pregunta del usuario.
            {context}"""
    human_template="{question}"
    system_message_prompt = SystemMessagePromptTemplate.from_template(openai_template)
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)


    CHAT_PROMPT = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )
    return CHAT_PROMPT

# Set up the base template
def get_agent_template():
    template = """Eres Sabiduria Asegurada,un agente comercial de polizas de la empresa QuePlan, lastimosamente no sabes nada de informacion y dependes unicamente de las herramientas que te proporciona la empresa. No sabes nada de nada y si la herramienta no proporciona responde cordialmente que no sabes.
    Eres encargado de responder las preguntas de los clientes sobre las polizas de la empresa.
    Si no sabes la respuesta, simplemente di que no lo sabes, no trates de inventar una respuesta.
    Crea una respuesta con la suficiente información para que el usuario pueda entender la respuesta. No te limites a responder con un 'Sí' o un 'No', ni por extenso ni abreviado.
            
    Como agente tienes acceso a las siguientes herramientas:

    {tools}

    Utiliza unicamente el siguiente formato para tus respuestas:

    Question: La pregunta que te hace el usuario
    Thought: Piensa y razona como proceder para resolver la pregunta
    Action: La mejor accion a realizar. Debe ser unicamente una de las siguientes [{tool_names}]
    Action Input: Con base en la accion, que input necesita la accion para ejecutarse
    Observation: El resultado de la accion
    ... (Este ciclo de Thought/Action/Action Input/Observation se puede repetir N veces hasta encontrar la respuesta final) 

    Cuando encuentres la respuesta final, responde al usuario UNICAMENTE UNICAMENTE UNICAMENTE con la siguiente estructura:
    Thought: Creo que se la respuesta final
    Final Answer: La respuesta final que le daras al usuario. Empieza a responder la pregunta del usuario: Responde siempre de forma profesional y educada. Extiendete lo necesario
    para una respuesta de calidad. SIEMPRE RESPONDE CON LA MAYOR CANTIDAD DE INFORMACION POSIBLE.


    Historial de conversacion anterior:
    {history}

    Question: {input}
    {agent_scratchpad}"""
    
    AGENT_TEMPLATE = template
    
    return AGENT_TEMPLATE

def custom_filter_chain(question:str, 
                        db = connect_db(config.COLLECTION_SUMMARY)
                        ) -> str:
    docs = db.similarity_search(question, k = 1)
    most_likely_doc = docs[0].metadata['source']
    content = docs[0].page_content
    return most_likely_doc , content

async def acustom_filter_chain(question:str, 
                        db = aconnect_db(config.COLLECTION_SUMMARY)
                        ) -> str:
    docs = await db.asimilarity_search(question, k = 1)
    most_likely_doc = docs[0].metadata['source']
    content = docs[0].page_content
    return most_likely_doc, content

def get_llm(model_name:str= config.OPENAI_MODEL) -> ChatOpenAI:
    llm = ChatOpenAI(temperature=0,
                     model_name=model_name, 
                     max_tokens=4_000,
                     streaming=True, 
                     #callbacks=[FinalStreamingStdOutCallbackHandler()],
                     openai_api_key=config.OPENAI_API_KEY) # 4_000 max tokens in the request, 16k model to avoid context loss
    return llm

def custom_qa(question:str, 
              db = connect_db(config.COLLECTION_CHUNKS),
              llm = get_llm(),
              prompt = get_chat_template()
              ) -> dict[str,str,str]:
    response_dict = {}
    likely_doc , content = custom_filter_chain(question)
    docs = db.similarity_search(question, k = 10, filter={"source":likely_doc})
    # Stuffing the content in a single window
    doc_list = [doc.page_content for doc in docs]
    doc_list.append(content)
    chat_prompt_openai= prompt.format_prompt(question=question, context="\n".join(doc_list)).to_messages()
    response = llm(chat_prompt_openai)
    response_dict['response'] = response
    response_dict['docs'] = docs
    response_dict['chat_prompt_openai'] = chat_prompt_openai
    return response_dict


def get_tools(qa_type:int = 0) -> List[Tool]:
    
    def duck_duck_wrapper(query):
        search = DuckDuckGoSearchResults()
        search_results = search.run(f"{query}")
        return search_results 
    
    async def aduck_duck_wrapper(query):
        search = DuckDuckGoSearchResults()
        search_results = await search.run(f"{query}")
        return search_results 
    
    # Directly answer the question
    def qa_tool(question:str) -> str:
        response_dict = custom_qa(question)
        response = response_dict['response']
        return response.content

    db = connect_db(config.COLLECTION_CHUNKS)
    def qa_tool2(question:str) -> str:
        likely_doc, content = custom_filter_chain(question)
        docs = db.similarity_search(question, k = 6, filter={"source":likely_doc})
        docs_list = [doc.page_content for doc in docs]
        docs_list.append(content)
        context="\n".join(docs_list)
        return context
    
    adb = aconnect_db(config.COLLECTION_CHUNKS)
    async def aqa_tool2(question:str) -> str:
        likely_doc, content = await acustom_filter_chain(question)
        docs = await adb.asimilarity_search(question, k = 6, filter={"source":likely_doc})
        docs_list = [doc.page_content for doc in docs]
        docs_list.append(content)
        context=  "\n".join(docs_list)
        return context
    
    if qa_type == 0:
        qa_tool_func = qa_tool2
    else:
        qa_tool_func = qa_tool
    
    tools = [
        # Tool(
        #     name = "Web Search",
        #     func=aduck_duck_wrapper,
        #     description="useful for when you need to answer questions about current events, news or the current state of the world. Do not use it when asked about policies, in that case, use the policy search tool",
        # ),
        Tool(
            name = "Policy Search",
            func=qa_tool2,
            description="useful for when you need to answer questions about an specific policy, in that case, use the policy search tool",
            coroutine=aqa_tool2
        ),
    ]

    return tools

def get_agent_prompt() -> str:
    prompt = CustomPromptTemplate(
        template=get_agent_template(),
        tools=get_tools(),
        # This omits the `agent_scratchpad`, `tools`, and `tool_names` variables because those are generated dynamically
        # This includes the `intermediate_steps` variable because that is needed
        input_variables=["input", "intermediate_steps","history"]
    )
    return prompt


def get_output_parser() -> CustomOutputParser:
    return CustomOutputParser()


def create_agent():

    prompt = get_agent_prompt()
    output_parser = get_output_parser()
    llm = get_llm()
    llm_chain = LLMChain(llm=llm, prompt=prompt)
    tools = get_tools()
    tool_names = [tool.name for tool in tools]
    agent = LLMSingleActionAgent(
        llm_chain=llm_chain,
        output_parser=output_parser,
        stop=["\nObservation:"],
        allowed_tools=tool_names
    )
    agent_executor = AgentExecutor.from_agent_and_tools(agent=agent, 
                                                        tools=tools, 
                                                        verbose=False,
                                                        handle_parsing_errors=True)
    return agent_executor

class ChatBOT():
    chat_history = []
    answer = ""
    db_query  = ""
    db_response = ""
    
    def __init__(self):
        self.agent = create_agent()
        self.db_summary = connect_db(config.COLLECTION_SUMMARY)
        self.db_chunks = connect_db(config.COLLECTION_CHUNKS)
        
    def get_related_docs(self):
        self.db_response = custom_filter_chain(self.db_query)
        return self.db_response
    
    def clr_history(self):
        self.chat_history = []
        
    def chat(self, query, **kwargs):
        self.db_query = query
        question = {f'history': {'\n'.join(self.chat_history)}, 'input': f"{self.db_query}"}
        self.answer = self.agent.run(question, **kwargs)
        self.chat_history.append(f"Human: {question['input']}, AI: {self.answer}")
        return self.answer , self.chat_history, self.get_related_docs()
    
    async def achat(self, query, **kwargs):
        self.db_query = query
        question = {f'history': {'\n'.join(self.chat_history)}, 'input': f"{self.db_query}"}
        self.answer = await self.agent.arun(question, **kwargs)
        self.chat_history.append(f"Human: {question['input']}, AI: {self.answer}")
        self.get_related_docs()
        return self.answer