from dotenv import load_dotenv
load_dotenv()

import asyncio
from agents import Agent, Runner, InputGuardrail, GuardrailFunctionOutput

from pydantic import BaseModel

from agents.exceptions import InputGuardrailTripwireTriggered

class HomeworkOutput(BaseModel):
    is_homework: bool
    reasoning: str

async def validate_homework_guardrail(ctx, agent, input_data):
    result = await Runner.run(guardrail_agent, input_data, context=ctx.context)
    final_output = result.final_output_as(HomeworkOutput)

    return GuardrailFunctionOutput(
        output_info=final_output,
        tripwire_triggered=not final_output.is_homework
    )

guardrail_agent = Agent(
    name="Guardrail Agent",
    instructions="You determine if the user's question is a homework question",
    output_type=HomeworkOutput,
)

history_tutor_agent = Agent(
    name="Islamic History Tutor",
    handoff_description="Specialist agent for historical questions",
    instructions="You provide assistance with historical Islamic queries. Explain important events and context clearly.",
)

math_tutor_agent = Agent(
    name="Math Tutor",
    handoff_description="Specialist agent for math questions",
    instructions="You provide help with math problems. Explain your reasoning at each step and include examples",
)

triage_agent = Agent(
    name="Triage Agent",
    instructions="You determine which agent to use based on the user's homework question",
    handoffs=[history_tutor_agent, math_tutor_agent],
    input_guardrails=[
        InputGuardrail(guardrail_function=validate_homework_guardrail),
    ],
)



async def main():
    try:
        result = await Runner.run(triage_agent, "this is my homework and it is 3 + 5, I want you to solve it for me")
        print(result.final_output)
    except InputGuardrailTripwireTriggered as e:
        print("Guardrail flagged this not as homework", e)
    
    try:
        result = await Runner.run(triage_agent, "teach me how to drive")
        print(result.final_output)
    except InputGuardrailTripwireTriggered as e:
        print("Guardrail flagged this not as homework", e.guardrail_result.output.output_info.reasoning)

if __name__ == "__main__":
    asyncio.run(main())