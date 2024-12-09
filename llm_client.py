# llm_client.py

import openai
from config import LLM_API_KEY
from logger import log_message

openai.api_key = LLM_API_KEY


def query_llm(prompt):
    """
    Send a prompt to the LLM and return the response.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a trading assistant."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=150,
            n=1,
            stop=None,
            temperature=0.5,
        )
        answer = response.choices[0].message["content"].strip()
        return answer
    except openai.error.OpenAIError as e:
        log_message("ERROR", f"OpenAI API Error: {e}")
        return None
