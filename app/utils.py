import re
import wikipedia
from config import Config

def clean_wikipedia_text(text):
    """Clean Wikipedia content by removing citations and section headers"""
    # Remove citations like [1], [2-5], etc.
    text = re.sub(r'\[\d+\]', '', text)
    text = re.sub(r'\[\d+-\d+\]', '', text)
    
    # Remove section headers
    text = re.sub(r'==.*?==+', '', text)
    
    # Remove edit markers
    text = text.replace('[edit]', '')
    
    # Remove multiple newlines
    text = re.sub(r'\n\s*\n', '\n\n', text)
    
    return text.strip()

def chunk_text(text, max_length=Config.TRANSLATION_CHUNK_SIZE):
    """Split text into chunks while preserving paragraphs"""
    paragraphs = text.split('\n')
    chunks = []
    current_chunk = ""
    
    for para in paragraphs:
        # If paragraph is too big, split into sentences
        if len(para) > max_length:
            sentences = re.split(r'(?<=[.!?]) +', para)
            for sentence in sentences:
                if len(current_chunk) + len(sentence) < max_length:
                    current_chunk += sentence + " "
                else:
                    if current_chunk:
                        chunks.append(current_chunk.strip())
                    current_chunk = sentence + " "
        else:
            if len(current_chunk) + len(para) < max_length:
                current_chunk += para + "\n"
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = para + "\n"
    
    if current_chunk:
        chunks.append(current_chunk.strip())
    
    return chunks

def fetch_wikipedia_article(title):
    try:
        page = wikipedia.page(title)
        return {
            "title": page.title,
            "content": clean_wikipedia_text(page.content),
            "url": page.url,
            "summary": page.summary
        }
    except wikipedia.exceptions.PageError:
        return {"error": "Page not found"}
    except wikipedia.exceptions.DisambiguationError as e:
        return {"error": "Disambiguation page", "options": e.options}
    except Exception as e:
        return {"error": str(e)}
