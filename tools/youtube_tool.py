from langchain_core.tools import tool
from ytsearchpython import VideosSearch

@tool
def search_youtube(query: str) -> str:
    """Поиск образовательных видео на YouTube"""
    videosSearch = VideosSearch(query + " урок", limit=3)
    results = videosSearch.result()['result']
    
    if not results:
        return "❌ Видео не найдены"
    
    video_links = []
    for video in results:
        title = video['title'][:60]
        link = f"https://www.youtube.com/watch?v={video['id']}"
        video_links.append(f"• [{title}]({link})")
    
    return f"🎥 **Рекомендуемые видео**:\n" + "\n".join(video_links)
