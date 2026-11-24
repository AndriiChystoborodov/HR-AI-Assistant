from datetime import date
from email.mime import message
from pyexpat.errors import messages
from unittest import result
from dotenv import load_dotenv
import os
from langchain_openrouter import ChatOpenRouter
from langchain.agents import create_agent
from langchain.tools import tool
from security.pii import mask, unmask
from holiday_api import fetch_holidays

load_dotenv(dotenv_path=".env")


# ---------------------------
# Step 1: Placeholder tools
# ---------------------------


@tool
def get_open_holiday_info(valid_from: str, valid_to: str) -> str:
    """Retrieve public holiday information for Switzerland for a date range (YYYY-MM-DD to YYYY-MM-DD)."""
    holidays = fetch_holidays(
        country_iso="CH",
        language_iso="EN",
        valid_from=valid_from,
        valid_to=valid_to,
        subdivision_code="CH-BS",
    )

    if not holidays:
        return f"No public holidays found in Switzerland from {valid_from} to {valid_to}."

    entries = "; ".join(f"{h['name']} ({h['start_date']})" for h in holidays)
    return f"Public holiday(s) in Basel-Stadt (CH-BS) from {valid_from} to {valid_to}: {entries}."
# ---------------------------
# Step 2: Preprocessing
# ---------------------------

def mask_pii(question: str) -> str:
    masked_text, token_map = mask(question)
    return masked_text, token_map

# //TODO demasking


# ---------------------------
# Step 3: Load handbook
# ---------------------------

def load_handbook() -> str:
     base_dir = os.path.dirname(os.path.abspath(__file__))
     file_path = os.path.join(base_dir, "data", "handbook.md")

     with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

# ---------------------------
# Step 4: Load system prompt
# ---------------------------

def load_system_prompt() -> str:
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, "prompts", "system_prompt.md")
    with open(file_path, "r", encoding="utf-8") as f:
        prompt = f.read()

    today = date.today().strftime("%Y-%m-%d")
    prompt = prompt.replace("__TODAY__", today)
    prompt = prompt.replace("__HANDBOOK__", load_handbook())

    return prompt

# ---------------------------
# Step 5: Build LLM agent
# ---------------------------

def build_agent():
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise ValueError("OPENROUTER_API_KEY is missing.")

    model = ChatOpenRouter(
        model="anthropic/claude-sonnet-4-5",
        api_key=api_key,
        temperature=0
    )
    agent = create_agent(
        model=model,
        tools=[get_open_holiday_info],
        system_prompt=load_system_prompt()
    )
    return agent

# ---------------------------
# Step 6: Main flow
# ---------------------------

def run_main_flow(user_question: str, debug: bool = False) -> str:

    #user 

    # 1. Mask personal data
    masked_question, token_map = mask_pii(user_question)

    if debug:
        print(f"\n[DEBUG]: Original question: {user_question}")
        print(f"[DEBUG]: Masked question: {masked_question}")
        print(f"[DEBUG]: Token map: {token_map}\n")

    # 3. Load handbook context
    handbook = load_handbook()

    # 3. Build agent
    agent = build_agent()

    # 3. Invoke with user question only
    result = agent.invoke(
        {
            "messages": [
                {"role": "user", "content": masked_question}
            ]
        }
    )

    messages = result["messages"]

    tool_used = any(msg.__class__.__name__ == "ToolMessage" for msg in messages)

    if debug:
        if tool_used:
            print("\n[DEBUG]: Open Holidazy API tool was called)\n")
        else:
            print("\n[DEBUG]: Answer was generated using only the handbook context and LLM capabilities\n")


    message = result["messages"][-1].content
    return unmask(message, token_map)

# ---------------------------
# Step 7: Test run
# ---------------------------

if __name__ == "__main__":
    question = "what is my expense limit ?"
    answer = run_main_flow(question)
    print(answer)