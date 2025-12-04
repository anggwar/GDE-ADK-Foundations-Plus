from google.adk.agents.llm_agent import Agent

BASIC_INSTRUCTION = """
You are a grandmother telling a folklore story.
Just tell the plot of the story in a simple, factual way.
"""

root_agent = Agent(
    model='gemini-3-pro-preview',
    name='root_agent',
    description='A simple folklore bot.',
    instruction=BASIC_INSTRUCTION,
)
