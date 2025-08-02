from flask import Blueprint, render_template, request, jsonify
from flask_caching import cache
from flask_limiter import limiter
from app.translator import translator
from app.utils import fetch_wikipedia_article, chunk_text
from config import Config

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/translate', methods=['POST'])
@limiter.limit(Config.RATE_LIMIT)
@cache.cached(timeout=3600, query_string=True)
def translate_text():
    text = request.json.get('text', '')
    if not text:
        return jsonify({"error": "No text provided"}), 400
    
    try:
        # Translate in chunks
        chunks = chunk_text(text)
        translations = []
        
        for chunk in chunks:
            translated = translator.translate(chunk)
            translations.append(translated)
        
        return jsonify({
            "translation": "\n\n".join(translations),
            "chunk_count": len(chunks)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp.route('/fetch_wikipedia', methods=['GET'])
@limiter.limit(Config.RATE_LIMIT)
def fetch_wikipedia():
    title = request.args.get('title')
    lang = request.args.get('lang', 'en')
    
    if not title:
        return jsonify({"error": "No title provided"}), 400
    
    # Set Wikipedia language
    wikipedia.set_lang(lang)
    
    # Fetch article
    result = fetch_wikipedia_article(title)
    
    if 'error' in result:
        return jsonify(result), 404 if result['error'] == "Page not found" else 400
    
    return jsonify(result)

@bp.route('/supported_languages', methods=['GET'])
def supported_languages():
    """List supported Wikipedia languages"""
    return jsonify({
        "languages": [
            {"code": "en", "name": "English"},
            {"code": "hi", "name": "Hindi"},
            {"code": "bn", "name": "Bengali"},
            # Add more languages as needed
        ]
    })
