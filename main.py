from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.prompts import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
    MessagesPlaceholder
)
import streamlit as st
from streamlit_chat import message
from utils import *
from streamlit_option_menu import option_menu
def assistant():
    st.subheader("RBI Chatbot")

    if 'responses' not in st.session_state:
        st.session_state['responses'] = ["How can I assist you?"]

    if 'requests' not in st.session_state:
        st.session_state['requests'] = []

    llm = ChatOpenAI(model_name="gpt-3.5-turbo", openai_api_key="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")

    if 'buffer_memory' not in st.session_state:
                st.session_state.buffer_memory=ConversationBufferWindowMemory(k=3,return_messages=True)


    system_msg_template = SystemMessagePromptTemplate.from_template(template="""You have been trained on guidelines and faq from bank guidelines.Given the context , Answer the question as truthfully as possible using the provided context, 
    and if the answer is not contained within the text below, say 'Try again with different Question'""")


    human_msg_template = HumanMessagePromptTemplate.from_template(template="{input}")

    prompt_template = ChatPromptTemplate.from_messages([system_msg_template, MessagesPlaceholder(variable_name="history"), human_msg_template])

    conversation = ConversationChain(memory=st.session_state.buffer_memory, prompt=prompt_template, llm=llm, verbose=True)




    # container for chat history
    response_container = st.container()
    # container for text box
    textcontainer = st.container()
    st.write("                                  Tip: To search for a different topic , please click New chat button")
    col1, col2, col3,col4,col5 = st.columns(5)
    
    with col3:
        if st.button("New Chat"):
            st.session_state['responses'] = ["How can I assist you?"]
            st.session_state['requests'] = []
            st.rerun()
    with textcontainer:
        query = st.text_input("Query: ", key="input")
        if query:
            with st.spinner("typing..."):
                conversation_string = get_conversation_string()
                # st.code(conversation_string)
                refined_query = query_refiner(conversation_string, query)
                st.subheader("Refined Query:")
                st.write(refined_query)
                context = find_match(refined_query)
                # print(context)  
                response = conversation.predict(input=f"Context:\n {context} \n\n Query:\n{query}")
            st.session_state.requests.append(query)
            st.session_state.responses.append(response) 
    with response_container:
        if st.session_state['responses']:

            for i in range(len(st.session_state['responses'])):
                message(st.session_state['responses'][i],key=str(i))
                if i < len(st.session_state['requests']):
                    message(st.session_state["requests"][i], is_user=True,key=str(i)+ '_user')
                    
                    
def home():
    st.title("Welcome to RBI assistant🤖")
    st.subheader("How to Use Chatbot?")

with st.sidebar:
    nav = option_menu("RBI Insights Bot", ["Home", "Assistant"], 
        icons=['house', 'signpost-split'], 
        menu_icon="sunrise", 
        default_index=0,
        styles={ 
        "@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500&display=swap')"
        "container": {"font-family": "Montserrat"},
        "nav-link": { "fony-size":"25px","--hover-color": "#FF4B4B"},
        }
        )
    
    
if nav == "Home":
    home()
elif nav == "Assistant":
    assistant()
          