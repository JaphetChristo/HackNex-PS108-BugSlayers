import json

from groq import Groq

from app.config import GROQ_API_KEY, MODEL_NAME
from app.prompts import SYSTEM_PROMPT
from app.models import AgentResponse


client = Groq(api_key=GROQ_API_KEY)


def analyze_question(user_question, dataset_schema, metadata=""):

    user_prompt = f"""
User question:
{user_question}

Dataset schema:
{dataset_schema}

Dataset metadata:
{metadata}

Analyze whether the question can be answered using the available dataset.

Return ONLY valid JSON.
"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ],
        response_format={
            "type": "json_object"
        }
    )

    result_text = response.choices[0].message.content

    try:
        result = json.loads(result_text)

        validated_result = AgentResponse.model_validate(result)

        return validated_result

    except Exception as e:
        print("Validation error:", e)
        return None