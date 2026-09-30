from ddgs import DDGS

def search_web(query, max_results=5):
    """
    Search the web and return useful sources.
    """

    results = []

    with DDGS() as ddgs:
        search_results = ddgs.text(
            query,
            max_results=max_results
        )

        for result in search_results:
            results.append({
                "title": result.get("title", ""),
                "url": result.get("href", ""),
                "snippet": result.get("body", "")
            })

    return results


if __name__ == "__main__":

    query = input("\nWhat do you want to research? ")

    print("\n" + "=" * 60)
    print("RESEARCHOPS — RESEARCHER AGENT")
    print("=" * 60)

    results = search_web(query)

    if not results:
        print("\nNo results found.")
    else:
        for i, result in enumerate(results, start=1):

            print(f"\nSOURCE {i}")
            print("-" * 40)
            print("TITLE:", result["title"])
            print("URL:", result["url"])
            print("SUMMARY:", result["snippet"])

    print("\n" + "=" * 60)
    print("Research search complete.")
    print("=" * 60)