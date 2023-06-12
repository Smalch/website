import streamlit as st
import requests
from streamlit_chat import message
from time import sleep

url = "http://34.149.30.111"

def setup_history(history):
    for id, line in enumerate(history):
        message(line, is_user=id%2==0, key=str(id))


def last_answer():
    while True:

        print('last_answer')
        sleep(10)
        response = requests.post(
            f"{url}/last_answer/"
        )
        print(response)
        sleep(10)


        if response.status_code == 200:
            if response.json() != "None":
                print(response)
                print(response.json())
                return response.json()
        sleep(3)

def main():
    st.set_page_config(page_title='LLM Demo', page_icon=':robot_face:')
    st.title("LLM Demo")
    st.markdown("## A demo of the Chat model by Artem")
    st.header("Chat with the model")
    # placeholder = st.empty()
    # with placeholder.form(key = 'my_form', clear_on_submit=False):





    if "history" not in st.session_state:
        st.session_state.history = []
    if "question" not in st.session_state:
        st.session_state.question = ''

    input = st.text_input('Ask a question', key='question', value=st.session_state.question)

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
                        f"{url}/upload_pdf/",
                        files={"file": pdf_docs},
                    )


    if input:
        setup_history(st.session_state.history)
        message(input, is_user=True, key=str(len(st.session_state.history)))
        st.session_state.history.append(input)
        st.session_state.question = ''
        with st.spinner('Processing'):
            try:
                response = requests.post(
                    f"{url}/qa_from_files/",
                    json={"query": input},
                )
                if response.status_code != 200:
                    answer = last_answer()
                else:
                    answer = response.json()
            except:
                answer = last_answer()
        print(answer)
        st.session_state.history.append(answer)
        message(answer, key=str(len(st.session_state.history)))

if __name__ == "__main__":
    main()