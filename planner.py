import os
from dotenv import load_dotenv
from google import genai

# Load API key
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env")

# Connect to Gemini
client = genai.Client(api_key=api_key)


def create_research_plan(question):
    """
    Creates a structured research plan from the user's question.
    """

    prompt = f"""
You are the Planner Agent of ResearchOps.

Break this research question into a practical research plan:

RESEARCH QUESTION:
{question}

Return:

RESEARCH OBJECTIVE:
...

RESEARCH QUESTIONS:
1. ...
2. ...
3. ...
4. ...
5. ...

INFORMATION TO COLLECT:
- ...
- ...
- ...

SOURCE TYPES:
- ...
- ...
- ...

EXPECTED OUTPUT:
...
"""

    for attempt in range(3):

        try:
            response = client.models.generate_content(
                model="gemini-3.5-flash-lite",
                contents=prompt
            )

            return response.text

        except Exception as e:

            if "503" in str(e) and attempt < 2:
                import time
                print(f"\nGemini temporarily unavailable. Retrying... ({attempt + 1}/2)")
                time.sleep(5)

            else:
                raise e

# Test the Planner Agent
if __name__ == "__main__":

    question = input("\nEnter your research question: ")

    if not question.strip():
        print("Please enter a research question.")
    else:
        print("\n" + "=" * 60)
        print("RESEARCHOPS — PLANNER AGENT")
        print("=" * 60)

        plan = create_research_plan(question)

        print("\n" + plan)

        print("\n" + "=" * 60)
        print("Planning complete.")
        print("=" * 60)