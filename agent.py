from typing import Annotated, Sequence
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph import END, StateGraph, MessagesState
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

class AgentState(MessagesState):
    """Состояние агента HermesEduBot"""
    pass

def create_hermes_agent(tools):
    """Создает ReAct агента для HermesEduBot"""
    
    # LLM с русским языком
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.1,
        api_key=os.getenv("OPENAI_API_KEY")
    )
    
    llm_with_tools = llm.bind_tools(tools)
    
    # Системный промпт для образования
    system_prompt = """
    Ты HermesEduBot - AI-ассистент Hermes IT-School. Помогаешь учителям готовить уроки по IT и AI.
    
    Твои возможности:
    - Объясняешь сложные темы простым языком для школьников
    - Находишь актуальные видеоуроки на YouTube
    - Даешь ссылки на Википедию с кратким описанием
    - Предлагаешь практические задания
    
    Всегда отвечай структурировано:
    1. Краткое объяснение
    2. Основные примеры
    3. Полезные ресурсы
    4. Практическое задание
    
    Форматируй ответ markdown.
    """
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="messages"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])
    
    def call_model(state: AgentState):
        chain = prompt | llm_with_tools
        response = chain.invoke(state)
        return {"messages": [response]}
    
    # Граф агента
    workflow = StateGraph(state_schema=AgentState)
    workflow.add_node("agent", call_model)
    workflow.add_node("tools", ToolNode(tools))
    
    workflow.set_entry_point("agent")
    workflow.add_conditional_edges(
        "agent",
        tools_condition,
        {
            "tools": "tools",
            END: END
        }
    )
    workflow.add_edge("tools", "agent")
    
    return workflow.compile()
