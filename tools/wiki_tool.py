from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from typing import Type
from langchain_core.tools import tool

class WikiTool(WikipediaQueryRun):
    name: str = "wikipedia_search"
    description: str = "Поиск информации в Википедии для уроков"
    
    @tool
    def _run(
        self, query: str, run_manager=None, top_k_results: int = 1
    ) -> str:
        """Полезен для поиска объяснений тем по IT и AI"""
        api_wrapper = WikipediaAPIWrapper(top_k_results=top_k_results)
        result = api_wrapper.run(query)
        return f"📖 **Википедия**: {result[:500]}...\n🔗 [Читать полностью](https://ru.wikipedia.org/wiki/{query.replace(' ', '_')})"
