import streamlit as st
import requests
from streamlit_chat import message
from time import sleep


def setup_history(history):
    for id, line in enumerate(history):
        message(line, is_user=id%2==0, key=str(id))

def main():
    st.set_page_config(page_title='LLM Demo', page_icon=':robot_face:')
    st.title("LLM Demo")
    st.markdown("## A demo of the Chat model by Artem")
    st.header("Chat with the model")
    input = st.text_input('Ask a question', key='question')

    if "history" not in st.session_state:
        st.session_state.history = []

    # placeholder = st.empty()
    # input_ = st.text_input("Ask a question")
    # message_history.append(input_)
    #
    # with placeholder.container():
    #     for message_ in message_history:
    #         message(message_)

    with st.sidebar:
        st.subheader('Your fiels')
        pdf_docs = st.file_uploader('Upload your file')
        if st.button('Send', key='load_files'):
            with st.spinner('Processing files'):
                if pdf_docs is not None:
                    response = requests.post(
                        "http://localhost:8000/upload_pdf/",
                        files={"file": pdf_docs},
                    )


    if input:
        setup_history(st.session_state.history)
        message(input, is_user=True, key=str(len(st.session_state.history)))
        st.session_state.history.append(input)
        with st.spinner('Processing'):
            response = requests.get(
                "http://localhost:8000/qa_from_files/",
                json={"query": input},
            )

        st.session_state.history.append(response.json())
        message(response.json(), key=str(len(st.session_state.history)))

if __name__ == "__main__":
    main()