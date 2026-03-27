from pathlib import Path
from agno.agent import Agent
from agno.models.openai import OpenAIResponses
from agno.tools.coding import CodingTools

WORKSPACE = Path(__file__).parent.joinpath("workspace")
WORKSPACE.mkdir(parents=True, exist_ok=True)

agent = Agent(
    name="Gcode",
    model=OpenAIResponses(id="gpt-5.2"),
    instructions=(
        "You are a coding agent. Write clean, well-documented code. "
        "Always save your work to files and test by running them."
    ),
    tools=[CodingTools(base_dir=WORKSPACE, all=True)],
    markdown=True,
)

agent.print_response(
    "Write a Fibonacci function, save it to fib.py, and run it to verify",
    stream=True,
)