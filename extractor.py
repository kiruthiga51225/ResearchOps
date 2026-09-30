import os
import time
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env")

client = genai.Client(api_key=api_key)


def extract_facts(question, sources):
    """Extract useful evidence from real research sources."""

    source_text = ""

    for i, source in enumerate(sources, start=1):
        source_text += f"""
SOURCE {i}
Title: {source.get("title", "")}
URL: {source.get("url", "")}
Snippet: {source.get("snippet", "")}
"""


    prompt = f"""
You are the Extractor Agent of ResearchOps.

Research question:
{question}

Below are web research results:

{source_text}

Extract only information that is supported by these sources.

For every important finding, provide:

FACT:
SOURCE:
URL:
RELEVANCE:

Do not invent facts.
Do not add information that is not present in the sources.

Return the result under:

EXTRACTED EVIDENCE
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

                print(
                    f"\nGemini temporarily unavailable. "
                    f"Retrying... ({attempt + 1}/2)"
                )

                time.sleep(5)

            else:
                raise e


if __name__ == "__main__":

    from researcher import search_web

    question = input("\nResearch question: ")

    print("\nSearching the web...")

    sources = search_web(question, max_results=5)

    if not sources:
        print("No research sources found.")
        exit()

    print(f"Found {len(sources)} sources.")

    print("\nExtracting evidence...")

    evidence = extract_facts(question, sources)

    print("\n" + "=" * 60)
    print("RESEARCHOPS — EXTRACTED EVIDENCE")
    print("=" * 60)

    print(evidence)

    print("\n" + "=" * 60)
    print("Extraction complete.")
    print("=" * 60)