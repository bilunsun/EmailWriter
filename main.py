import streamlit as st
import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


# Configure the OpenAI API
def initialize_openai() -> OpenAI:
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def rewrite_professional_email(
    client: OpenAI,
    original_email: str,
    tone: str,
) -> tuple[str, str]:
    prompt = f"""
Please rewrite this email maintaining the same core message but improving its professionalism.
Generate an appropriate subject line as well.

Original Email:
{original_email}

Desired Tone: {tone}

Format your response as follows:
Subject: [Your generated subject line]
[Rest of the email with greeting, body, and signature]

If the sender's name was not provided, default to "Sean".
    """

    response = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}], model="gpt-4o-mini"
    )

    # Split the response into subject and body
    content = response.choices[0].message.content
    lines = content.split("\n", 2)  # Split into max 3 parts
    subject = lines[0].replace("Subject:", "").strip()
    body = lines[-1].strip()

    return subject, body


st.title("Professional Email Rewriter")

# Initialize OpenAI
client = initialize_openai()

# Input fields
original_email = st.text_area("Paste your email here:", height=100)
tone = st.selectbox(
    "Select desired tone:",
    [
        "Friendly but Professional",
        "Formal",
        "Casual Professional",
        "Direct and Concise",
    ],
)
if st.button("Rewrite Email"):
    if original_email:
        with st.spinner("Rewriting your email..."):
            subject, email_text = rewrite_professional_email(
                client, original_email, tone
            )
            st.markdown("### Improved Version:")
            st.text_input("Subject:", value=subject)
            edited_email = st.text_area(
                "Edit your improved email:", value=email_text, height=300
            )
    else:
        st.error("Please paste an email to rewrite.")
