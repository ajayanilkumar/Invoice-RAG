from qachain import InvBotCreator
from config import *
import streamlit as st
from streamlit_chat import message
st.session_state.clicked=True
@st.cache_resource(show_spinner=True)
def create_invbot():
    invbotcreator = InvBotCreator()
    invbot = invbotcreator.create_invbot()
    return invbot
invbot = create_invbot()

def infer_invbot(prompt):
    model_out = invbot(prompt)
    answer = model_out['result']
    return answer

def display_conversation(history):
    for i in range(len(history["assistant"])):
        message(history["user"][i], is_user=True, key=str(i) + "_user")
        message(history["assistant"][i],key=str(i))

def main():

    st.title("Chat with your Invoice")
    st.subheader("A bot created using Langchain 🦜 to make your invoice management process easier")

    user_input = st.text_input("Enter your query")

    if "assistant" not in st.session_state:
        st.session_state["assistant"] = ["I am ready to help you"]
    if "user" not in st.session_state:
        st.session_state["user"] = ["Hey there!"]
                
    if st.session_state.clicked:
        if st.button("Answer"):

            answer = infer_invbot({'query': user_input})
            st.session_state["user"].append(user_input)
            st.session_state["assistant"].append(answer)

            if st.session_state["assistant"]:
                display_conversation(st.session_state)

if __name__ == "__main__":
    main()
    
    