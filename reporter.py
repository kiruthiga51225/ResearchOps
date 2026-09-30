import os
import time
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env")

client = genai.Client(api_key=api_key)


def generate_report(question, analysis):
    """
    Generate a professional final research report.
    """

    prompt = f"""
You are the Reporter Agent of ResearchOps.

Create a polished, professional research report using the
verified analysis provided below.

RESEARCH QUESTION:
{question}

ANALYSIS:
{analysis}

Create the report using this structure:

# RESEARCHOPS — RESEARCH REPORT

## 1. Executive Summary
Give a concise overview of the most important findings.

## 2. Key Findings
Present the major findings clearly.

## 3. Market / Industry Trends
Explain the important trends identified in the research.

## 4. Opportunities
List opportunities supported by the evidence.

## 5. Challenges & Risks
List important challenges and risks.

## 6. Important Numbers
Present significant statistics or numerical findings.

## 7. Research Gaps
Clearly identify uncertain or missing information.

## 8. Overall Insight
Give a concise evidence-based interpretation.

## 9. Evidence Confidence
Summarize the overall confidence level and explain why.

IMPORTANT:

- Use only information contained in the analysis.
- Do not invent statistics or facts.
- Do not present uncertain information as certain.
- Keep the report professional and easy to read.
- Use bullets and short paragraphs.
- Clearly distinguish evidence from uncertainty.
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
    from analyst import analyze_research

    question = input("\nResearch question: ")

    print("\n" + "=" * 60)
    print("RESEARCHOPS — FULL RESEARCH PIPELINE")
    print("=" * 60)

    # STEP 1 — Research
    print("\n[1/5] Searching the web...")

    sources = search_web(
        question,
        max_results=5
    )

    if not sources:
        print("No research sources found.")
        exit()

    print(f"Found {len(sources)} sources.")

    # STEP 2 — Extraction
    print("\n[2/5] Extracting evidence...")

    evidence = extract_facts(
        question,
        sources
    )

    print("Evidence extracted successfully.")

    # STEP 3 — Verification
    print("\n[3/5] Verifying evidence...")

    verification = verify_evidence(
        question,
        evidence
    )

    print("Evidence verified successfully.")

    print("\n" + "=" * 60)
    print("VERIFICATION RESULTS")
    print("=" * 60)
    print(verification)

    # STEP 4 — Analysis
    print("\n[4/5] Analyzing research...")

    analysis = analyze_research(
        question,
        verification
    )

    print("Research analyzed successfully.")

    # STEP 5 — Report
    print("\n[5/5] Generating final report...")

    report = generate_report(
        question,
        analysis
    )

    print("\n" + "=" * 60)
    print("RESEARCHOPS — FINAL REPORT")
    print("=" * 60)

    print(report)

    print("\n" + "=" * 60)
    print("FULL RESEARCH PIPELINE COMPLETE")
    print("=" * 60)