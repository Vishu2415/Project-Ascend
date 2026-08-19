# DuckDuckGo based web search ke liye DDGS import kar rahe hain.
from ddgs import DDGS

# LangChain ka tool decorator import kar rahe hain.
from langchain_core.tools import tool


# Ye tool internet par web search karega.
@tool
def search_web(query: str) -> str:
    """
    Search the web for current information and return relevant search results.
    """

    # Search results ko store karne ke liye list create kar rahe hain.
    results = []

    # DDGS search client create kar rahe hain.
    search_client = DDGS()

    # User ki query ke basis par web search kar rahe hain.
    search_results = search_client.text(
        query,
        max_results=5
    )

    # Har search result ko process kar rahe hain.
    for result in search_results:

        # Result se required information extract kar rahe hain.
        title = result.get(
            "title",
            ""
        )

        href = result.get(
            "href",
            ""
        )

        body = result.get(
            "body",
            ""
        )

        # Result ko readable format me convert kar rahe hain.
        results.append(
            f"Title: {title}\n"
            f"URL: {href}\n"
            f"Snippet: {body}"
        )

    # Agar search se koi result nahi mila.
    if not results:

        return "No search results found."

    # Saare results ko ek single string me combine karke return kar rahe hain.
    return "\n\n".join(
        results
    )