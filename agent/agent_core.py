from llm.llm_engine import call_llm
from rag.prompt_builder import build_prompt
from agent.parser import parse_output

def run_agent(session, query):

    prompt = build_prompt(
        session["issue"],
        query,
        session["steps"],
        session["current"]
    )

    output = call_llm(prompt)

    action, response = parse_output(output)

    return action, response, output