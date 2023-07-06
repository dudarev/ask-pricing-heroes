"""
Streamlit app that accepts a user's question and returns an answer using OpenAI's GPT-3.
"""

import os
import streamlit as st

from answer_questions import answer_question
from good_questions import GOOD_QUESTIONS
from sources import get_sources_markdown

# a developer may specify an OpenAI API key in `.env` file
# (see `.env.example` for an example)
try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

st.sidebar.title("Ask Pricing Heroes")
st.sidebar.markdown(
    """
    Get your questions about pricing answered based on the insights shared in the
[#Pricing_Heroes](https://podcasts.apple.com/us/podcast/pricing-heroes/id1649346598) podcast
by [Competera](https://competera.net/resources/articles).
"""
)


st.sidebar.markdown("## Settings")


def set_openai_api_key(api_key: str):
    st.session_state["OPENAI_API_KEY"] = api_key


api_key_input = st.sidebar.text_input(
    "OpenAI API Key",
    type="password",
    placeholder="Paste your OpenAI API key here (sk-...)",
    help="You can get your API key from https://platform.openai.com/account/api-keys.\n"
    "It's needed to get non-cached answers. We do not store your keys.",
    value=st.session_state.get("OPENAI_API_KEY", ""),
)
if api_key_input:
    set_openai_api_key(api_key_input)


st.sidebar.markdown(
    """
---
Based on [ask-my-texts](https://github/dudarev/ask-my-texts) project
"""
)


input = st.text_input("Question", key="question")


if "expand_examples" not in st.session_state:
    st.session_state.expand_examples = True


if st.button("Ask") or input:
    question = st.session_state.question
    with st.spinner("Requesting..."):
        open_api_key = os.environ.get("OPENAI_API_KEY") or st.session_state.get(
            "OPENAI_API_KEY", ""
        )
        answer = answer_question(question, open_api_key)
    answer_expander = st.expander("Answer", expanded=True)
    if question:
        answer_expander.write(answer["answer"])
        if answer.get("sources"):
            sources_expander = st.expander("Sources", expanded=True)
            sources_expander.write(get_sources_markdown(answer["sources"]))
    else:
        answer_expander.write("Please enter a question.")
    st.session_state.expand_examples = False


def click_example_question_button(q):
    st.session_state.update(question=q)
    st.session_state.update(expand_examples=False)


examples_expander = st.expander(
    "Example questions (cached answers)", expanded=st.session_state.expand_examples
)
for q in GOOD_QUESTIONS:
    examples_expander.button(
        q,
        on_click=click_example_question_button,
        args=(q,),
    )
