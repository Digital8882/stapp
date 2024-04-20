import streamlit as st
from langchain_anthropic import ChatAnthropic
from crewai import Crew, Process, Agent
import os

# Set your Anthropic API key
os.environ["ANTHROPIC_API_KEY"] = "sk-ant-api03-nYM_SEsU4dvtnC8n0SYQB2CSEySCAzIVOOL1lOlCx9s_zrwJYaC1SNSKFGzHyjsVk4xgINAtBn5PpDrOsoOoCQ-6Il51gAA"

# Create a Crew AI agent
Nutritionist = Agent(
    role='Nutritionist',
    goal=f'prescribe healthy meal plan',
    backstory=f""" you are an expert nutritionist""",
    verbose=False,
    allow_delegation=True,
    max_rpm=5,
    llm=ChatAnthropic(model="claude-3-sonnet-20240229", max_tokens=4069),
)

# Define a task for the agent
from crewai import Task

diet_task = Task(
    description=f"""a balanced diet meal plan """,
    expected_output=f"""  300 words maximum, a healthy meal plan""",
    output_file='diet_report.docx',
)

def generate_text(prompt):
    # Create a Crew AI crew
    project_crew = Crew(
        tasks=[diet_task],
        agents=[Nutritionist],
        manager_llm=ChatAnthropic(temperature=1, model="claude-3-sonnet-20240229", max_tokens=4069),
        max_rpm=4,
        process=Process.hierarchical
    )

    # Kickoff the crew and get the result
    result = project_crew.kickoff()
    return result

def main():
    st.title("Crew AI App")

    prompt = st.text_area("Enter your prompt:", height=200)

    if st.button("Generate"):
        if prompt:
            with st.spinner("Generating text..."):
                generated_text = generate_text(prompt)
                st.success(generated_text)
        else:
            st.warning("Please enter a prompt.")

if __name__ == "__main__":
    main()