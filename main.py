import os
from langchain.agents import Tool
from langchain_community.tools import DuckDuckGoSearchRun
from crewai import Crew,Agent,Task,Process,LLM
llm = LLM(model="groq/llama-3.3-70b-specdec", )
task_values = []
from crewai.tools import tool


os.environ["GROQ_API_KEY"] = "Your_groq_api_key"

@tool("DUCKDUCKGoSEARCH")
def my_simple_tool(query: str) -> str:
    """THIS TOOL SEARCH ON THE WEB FOR YOU TAKING A QUERY AS AN INPUT"""
    # Tool logic here
    duckduckgo_search = DuckDuckGoSearchRun()

    result = duckduckgo_search.invoke(query)

    return result


researcher = Agent(
    role="Content researcher",
    goal="Plan engaging and factually accurate content on {topic}",
    backstory="You're working on planning a blog article "
              "about the topic: {topic}."
              "You collect information that helps the "
              "audience learn something "
              "and make informed decisions. "
              "Your work is the basis for "
              "the Content Writer to write an article on this topic.",
    llm=llm,        
    allow_delegation=False,
    tools=[my_simple_tool],
	verbose=True
)

writer = Agent(
    role="Content Writer",
    goal="Write insightful and factually accurate "
         "opinion piece about the topic: {topic}",
    backstory="You're working on a writing "
              "a new opinion piece about the topic: {topic}. "
              "You base your writing on the work of "
              "the Content researcher, who provides an outline "
              "and relevant context about the topic. "
              "You follow the main objectives and "
              "direction of the outline, "
              "as provide by the Content Planner. "
              "You also provide objective and impartial insights "
              "and back them up with information "
              "provide by the Content researcher. "
              "You acknowledge in your opinion piece "
              "when your statements are opinions "
              "as opposed to objective statements.",
    llm=llm,
    allow_delegation=False,
    verbose=True
)

research = Task(
    description=(
        "1. Prioritize the latest trends, key players, "
            "and noteworthy news on {topic}.\n"
        "2. Identify the target audience, considering "
            "their interests and pain points.\n"
        "3. Develop a detailed content outline including "
            "an introduction, key points, and a call to action.\n"
        "4. Include SEO keywords and relevant data or sources."
    ),
    expected_output="A comprehensive content plan document "
        "with an outline, audience analysis, "
        "SEO keywords, and resources ,maximum of 2 or 3 paragraph length ",
    agent=planner,
)
write = Task(
    description=(
        "1. Use the content plan to craft a compelling "
            "blog post on {topic}.\n"
        "2. Incorporate SEO keywords naturally.\n"
		"3. Sections/Subtitles are properly named "
            "in an engaging manner.\n"
        "4. Ensure the post is structured with an "
            "engaging introduction, insightful body, "
            "and a summarizing conclusion.\n"
        "5. Proofread for grammatical errors and "
            "alignment with the brand's voice.\n"
    ),
    expected_output="A well-written blog post "
        "in markdown format, ready for publication, "
        "each section should have 2 or 3 paragraphs.",
    agent=writer,
)
crew = Crew(
    agents=[researcher, writer],
    tasks=[research, write],
    process=Process.sequential,
    verbose=True,
    telemetry=False
)
result = crew.kickoff(inputs={"topic": "Artificial Intelligence"})
print(result)
