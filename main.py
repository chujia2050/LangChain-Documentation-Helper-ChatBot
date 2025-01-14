from dotenv import load_dotenv
load_dotenv()

from backend.core import run_llm
import streamlit as st
from streamlit_chat import message

from PIL import Image
import requests
from io import BytesIO

def create_sources_string(source_urls):
    if not source_urls:
        return ""
    sources_list = list(source_urls)
    sources_list.sort()
    sources_string = "sources:\n"
    for i, source in enumerate(sources_list):
        sources_string += f"{i+1}. {source}\n"
    return sources_string

# Add this function to get a profile picture
def get_profile_picture(email):
    # This uses Gravatar to get a profile picture based on email
    # You can replace this with a different service or use a default image
    gravatar_url = f"https://www.gravatar.com/avatar/{hash(email)}?d=identicon&s=200"
    response = requests.get(gravatar_url)
    img = Image.open(BytesIO(response.content))
    return img


st.sidebar.title("User Profile")

# You can replace these with actual user data
user_name = "John Doe"
user_email = "john.doe@example.com"

profile_pic = get_profile_picture(user_email)
st.sidebar.image(profile_pic, width=150)
st.sidebar.write(f"**Name:** {user_name}")
st.sidebar.write(f"**Email:** {user_email}")

st.header("LangChain🦜🔗 Documentation Helper ChatBot")

if (
    "chat_answers_history" not in st.session_state
    and "user_prompt_history" not in st.session_state
    and "chat_history" not in st.session_state
):
    st.session_state["chat_answers_history"] = []
    st.session_state["user_prompt_history"] = []
    st.session_state["chat_history"] = []

prompt = st.text_input("Prompt", placeholder="Enter your message here...")

if prompt:
    with st.spinner("Generating response.."):
        generated_response = run_llm(query=prompt, chat_history=st.session_state["chat_history"])
        sources = set(
            [doc.metadata["source"] for doc in generated_response["source_documents"]]
        )

        formatted_response = (
            f"{generated_response['result']} \n\n {create_sources_string(sources)}"
        )

        st.session_state["user_prompt_history"].append(prompt)
        st.session_state["chat_answers_history"].append(formatted_response)
        st.session_state["chat_history"].append(("human", prompt))
        st.session_state["chat_history"].append(
            ("ai", generated_response["result"]))

if st.session_state["chat_answers_history"]:
    for generated_response, user_query in zip(
        st.session_state["chat_answers_history"],
        st.session_state["user_prompt_history"],
    ):
        message(user_query, is_user=True)
        message(generated_response)

# Add a footer
st.markdown("---")
st.markdown("Powered by LangChain and Streamlit")