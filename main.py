import os
from decouple import config
from langchain_core.prompts import PromptTemplate
from langchain_core.globals import set_llm_cache
from langchain_community.cache import SQLiteCache
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain.agents import create_react_agent, AgentExecutor
from langchain import hub


def main():
    os.environ['GOOGLE_API_KEY'] = config('GOOGLE_API_KEY')

    set_llm_cache(
        SQLiteCache(database_path="gemini_cache.db")
    )

    llm = ChatGoogleGenerativeAI(
        model='gemini-1.5-flash-8b',
        temperature=0.1
    )

    db = SQLDatabase.from_uri("sqlite:///students.db")
    toolkit = SQLDatabaseToolkit(
        db=db,
        llm=llm
    )
    system_message = hub.pull("hwchase17/react")

    agent = create_react_agent(
        llm=llm,
        tools=toolkit.get_tools(),
        prompt=system_message
    )
    agent_executor = AgentExecutor(
        agent=agent,
        tools=toolkit.get_tools(),
    )

    prompt = '''
    Use as ferramentas necessárias para responder questões sobre os estudantes, matérias e notas escolares. Todas as respostas devem ser geradas em português brasileiro. Perguntas: {q}
    '''
    prompt_template = PromptTemplate.from_template(prompt)
    question = input(f"O que deseja saber sobre os dados escolares?\n")

    output = agent_executor.invoke({
        'input': prompt_template.format(q=question)
    })

    print(output.get('output'))


if __name__ == '__main__':
    main()
