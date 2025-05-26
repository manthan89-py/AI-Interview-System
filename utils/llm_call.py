from litellm import completion
import os
import json

LLM_MODEL = os.environ.get("LLM_MODEL", "mistral/mistral-large-latest")


def get_response_from_llm(prompt):
    """
    Calls the LLM and returns the response.

    Args:
        prompt (str): The string to prompt the LLM with.

    Returns:
        str: The response from the LLM.
    """
    response = completion(
        model=LLM_MODEL,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content


def parse_json_response(response):
    # Parse the JSON response
    try:
        response = response.strip("```json")
        response = response.strip("```")
        return json.loads(response)
    except json.JSONDecodeError:
        return None
