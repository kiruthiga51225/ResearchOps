import os
import time
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env")

client = genai.Client(api_key=api_key)


def verify_evidence(question, evidence):
    """
    Verify evidence produced by the Extractor Agent.
    """

    prompt = f"""
You are the Verifier Agent of ResearchOps.

Research question:
{question}

Extracted evidence:
{evidence}

Analyze the evidence carefully.

For each important claim, determine:

1. CLAIM
2. SOURCE SUPPORT
   - Fully supported
   - Partially supported
   - Not supported
3. SOURCE QUALITY
   - High
   - Medium
   - Low
4. CONFLICT
   - Identify conflicts if present.
5. CONFIDENCE
   - High
   - Medium
   - Low
6. NEEDS MORE RESEARCH
   - Yes
   - No

Rules:
- Do not invent facts.
- Do not assume unsupported claims are true.
- Clearly identify missing information.
- Base your verification only on the supplied evidence.

Return:

VERIFICATION REPORT

CLAIM 1:
...

SOURCE SUPPORT:
...

SOURCE QUALITY:
...

CONFLICT:
...

CONFIDENCE:
...

NEEDS MORE RESEARCH:
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

                print(
                    f"\nGemini temporarily unavailable. "
                    f"Retrying... ({attempt + 1}/2)"
                )

                time.sleep(5)

            else:
                raise e


if __name__ == "__main__":

    # Import the Researcher and Extractor
    from researcher import search_web
    from extractor import extract_facts

    question = input("\nResearch question: ")

    print("\n" + "=" * 60)
    print("RESEARCHOPS — RESEARCH PIPELINE")
    print("=" * 60)

    # STEP 1 — Research
    print("\n[1/3] Searching the web...")

    sources = search_web(question, max_results=5)

    if not sources:
        print("No research sources found.")
        exit()

    print(f"Found {len(sources)} sources.")

    # STEP 2 — Extraction
    print("\n[2/3] Extracting evidence...")

    evidence = extract_facts(question, sources)

    print("Evidence extracted successfully.")

    # STEP 3 — Verification
    print("\n[3/3] Verifying evidence...")

    verification = verify_evidence(
        question,
        evidence
    )

    print("\n" + "=" * 60)
    print("VERIFICATION REPORT")
    print("=" * 60)

    print(verification)

    print("\n" + "=" * 60)
    print("Research pipeline complete.")
    print("=" * 60)