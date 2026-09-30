import os
import time
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env")

client = genai.Client(api_key=api_key)


def analyze_research(question, verification):
    """
    Analyze verified research and identify meaningful insights.
    """

    prompt = f"""
You are the Analyst Agent of ResearchOps.

Your job is to analyze a verified research report and transform
the verified information into useful, structured insights.

RESEARCH QUESTION:
{question}

VERIFICATION REPORT:
{verification}

Analyze the information and produce:

1. KEY FINDINGS
   - The most important verified findings.

2. MARKET / INDUSTRY TRENDS
   - Important patterns or growth trends.

3. OPPORTUNITIES
   - Opportunities supported by the evidence.

4. CHALLENGES / RISKS
   - Important challenges or risks supported by the evidence.

5. IMPORTANT NUMBERS
   - Extract significant numerical information.

6. RESEARCH GAPS
   - Information that is missing, uncertain, or needs further research.

7. EXECUTIVE INSIGHT
   - Give a concise overall interpretation based ONLY on the
     verified evidence.

IMPORTANT RULES:

- Do not invent facts.
- Do not introduce unsupported statistics.
- Clearly distinguish verified information from uncertainty.
- If the evidence is insufficient for a conclusion, say so.
- Do not treat low-confidence information as established fact.

Return the result as:

ANALYSIS REPORT

KEY FINDINGS
...

MARKET / INDUSTRY TRENDS
...

OPPORTUNITIES
...

CHALLENGES / RISKS
...

IMPORTANT NUMBERS
...

RESEARCH GAPS
...

EXECUTIVE INSIGHT
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

    from researcher import search_web
    from extractor import extract_facts
    from verifier import verify_evidence

    question = input("\nResearch question: ")

    print("\n" + "=" * 60)
    print("RESEARCHOPS — ANALYSIS PIPELINE")
    print("=" * 60)

    # STEP 1 — Research
    print("\n[1/4] Searching the web...")

    sources = search_web(question, max_results=5)

    if not sources:
        print("No research sources found.")
        exit()

    print(f"Found {len(sources)} sources.")

    # STEP 2 — Extraction
    print("\n[2/4] Extracting evidence...")

    evidence = extract_facts(
        question,
        sources
    )

    print("Evidence extracted successfully.")

    # STEP 3 — Verification
    print("\n[3/4] Verifying evidence...")

    verification = verify_evidence(
        question,
        evidence
    )

    print("Evidence verified successfully.")

    # STEP 4 — Analysis
    print("\n[4/4] Analyzing verified research...")

    analysis = analyze_research(
        question,
        verification
    )

    print("\n" + "=" * 60)
    print("RESEARCHOPS — ANALYSIS REPORT")
    print("=" * 60)

    print(analysis)

    print("\n" + "=" * 60)
    print("Analysis pipeline complete.")
    print("=" * 60)