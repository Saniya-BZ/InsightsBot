# import streamlit as st
# from streamlit_chat import message
# from utils import find_match, get_conversation_string

# st.subheader("IIIT ChatBot")

# if 'responses' not in st.session_state:
#     st.session_state['responses'] = ["How can I assist you?"]

# if 'requests' not in st.session_state:
#     st.session_state['requests'] = []

# # container for chat history
# response_container = st.container()
# # container for text box
# textcontainer = st.container()

# with textcontainer:
#     query = st.text_input("Query: ", key="input")
#     if query:
#         with st.spinner("typing..."):
#             context = find_match(query)
#             response = f"Context:\n{context}\n\nQuery:\n{query}\n\nAnswer:\n{context}"
#         st.session_state.requests.append(query)
#         st.session_state.responses.append(response)
        
# with response_container:
#     if st.session_state['responses']:
#         for i in range(len(st.session_state['responses'])):
#             message(st.session_state['responses'][i], key=str(i))
#             if i < len(st.session_state['requests']):
#                 message(st.session_state["requests"][i], is_user=True, key=str(i) + '_user')
import streamlit as st
from streamlit_chat import message
from utils import find_match, generate_response

st.subheader("IIIT ChatBot")

if 'responses' not in st.session_state:
    st.session_state['responses'] = ["How can I assist you?"]

if 'requests' not in st.session_state:
    st.session_state['requests'] = []

# container for chat history
response_container = st.container()
# container for text box
textcontainer = st.container()

with textcontainer:
    query = st.text_input("Query: ", key="input")
    if query:
        with st.spinner("typing..."):
            context = find_match(query)
            response = generate_response(f"Context:\n{context}\n\nQuery:\n{query}")
        st.session_state.requests.append(query)
        st.session_state.responses.append(response)
        
with response_container:
    if st.session_state['responses']:
        for i in range(len(st.session_state['responses'])):
            message(st.session_state['responses'][i], key=str(i))
            if i < len(st.session_state['requests']):
                message(st.session_state["requests"][i], is_user=True, key=str(i) + '_user')
