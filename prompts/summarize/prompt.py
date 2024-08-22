from typing import List
from langchain.prompts import PromptTemplate
from langchain.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain.schema import AIMessage, HumanMessage, SystemMessage

# Convert the schema object to a string
BASE_TEMPLATE = """
[BEFORE EXECUTING ACTION]
{action}

[RESULT OF ACTION]
{result}

[INSTRUCTION]
Using above [THOUGHTS], [ACTION], and [RESULT OF ACTION], please evaluate and learn from the event.

[SUGGESTED NEXT STEPS]
Based on the evaluation, suggest any next steps or actions to take.

[SUMMARY FOR USER]
Provide a summary of the event, including key learnings and any suggested next steps.
"""


SCHEMA_TEMPLATE = """
[RULE]
Your response must be provided exclusively in the JSON format outlined below, without any exceptions. 
Any additional text, explanations, or apologies outside of the JSON structure will not be accepted. 
Please ensure the response adheres to the specified format and can be successfully parsed by Python's json.loads function.

Strictly adhere to this JSON RESPONSE FORMAT for your response:
Failure to comply with this format will result in an invalid response. 
Please ensure your output strictly follows JSON RESPONSE FORMAT.

[JSON RESPONSE FORMAT]
{{
    "observation": "Summarize what was observed in [RECENT EPISODES] and the current context.",
    "thoughts": {{
        "task": "Description of the current task derived from [YOUR TASK]",
        "knowledge": "Summarize key points from [RELATED KNOWLEDGE] relevant to the task",
        "past_events": "Summarize key points from [RELATED PAST EPISODES] relevant to the task",
        "idea": "The idea or approach to take based on the task and context",
        "reasoning": "The reasoning behind the chosen idea or approach",
        "criticism": "Constructive self-criticism or reflections on the chosen approach",
        "summary": "A summary of the thought process leading to the action"
    }},
    "action": {{
        "tool_name": "Name of the tool chosen to execute the action from [TOOLS]",
        "args": {{
            "arg_name_1": "value_1",
            "arg_name_2": "value_2",
            ...
        }}
    }},
    "result": {{
        "outcome": "Describe the result of the action executed",
        "success": "True or False based on the success of the action",
        "details": "Any additional details or output from the action"
    }},
    "next_steps": {{
        "suggestion": "Any suggested next actions or steps based on the evaluation of the event"
    }},
    "summary_for_user": "A concise summary of the event, the learnings, and any next steps suggested"
}}
"""

def get_template() -> PromptTemplate:
    template = BASE_TEMPLATE
    prompt_template = PromptTemplate(
        input_variables=["thoughts", "action", "result"], template=template
    )
    return prompt_template


def get_chat_templatez() -> ChatPromptTemplate:
    messages = []
    messages.append(SystemMessagePromptTemplate.from_template(BASE_TEMPLATE))
    return ChatPromptTemplate.from_messages(messages)
