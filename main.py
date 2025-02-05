import os
from decouple import config
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI


def main():
    os.environ['GOOGLE_API_KEY'] = config('GOOGLE_API_KEY')
    llm = ChatGoogleGenerativeAI(
        model='gemini-1.5-flash',
        temperature=0.1
    )
    messages = ChatPromptTemplate(
        [
            SystemMessagePromptTemplate.from_template(
               "Você é um tradutor especialista e poliglota. Traduza as frases do usuário do {original_idiom} para o {target_idiom} de forma fidedigna."
            ),
            HumanMessage(content="Olá, como vai? Estou testando a inteligência artificial."),
        ]
    )
    prompt = messages.format_messages(original_idiom="português", target_idiom="italiano")
    print(prompt)

    response = llm.invoke(prompt)
    print(response.content)


if __name__ == '__main__':
    main()
