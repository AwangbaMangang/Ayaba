document.addEventListener('DOMContentLoaded', () => {
    // Elements
    const langSelect = document.getElementById('lang-select');
    const searchInput = document.getElementById('wiki-search');
    const fetchBtn = document.getElementById('fetch-btn');
    const translateBtn = document.getElementById('translate-btn');
    const articleTitle = document.getElementById('article-title');
    const wikiLink = document.getElementById('wiki-link');
    const englishContent = document.getElementById('english-content');
    const meeteiContent = document.getElementById('meetei-content');
    const loadingFetch = document.getElementById('loading-fetch');
    const loadingTranslate = document.getElementById('loading-translate');
    const progressInfo = document.getElementById('progress-info');

    // Event listeners
    fetchBtn.addEventListener('click', fetchWikipediaArticle);
    translateBtn.addEventListener('click', translateArticle);
    searchInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') fetchWikipediaArticle();
    });

    // Fetch Wikipedia article
    async function fetchWikipediaArticle() {
        const title = searchInput.value.trim();
        const lang = langSelect.value;
        
        if (!title) {
            alert('Please enter a Wikipedia article title');
            return;
        }
        
        // Clear previous content
        articleTitle.textContent = '';
        wikiLink.href = '';
        wikiLink.textContent = '';
        englishContent.innerHTML = '';
        meeteiContent.innerHTML = '';
        progressInfo.textContent = '';
        
        // Show loading
        loadingFetch.style.display = 'flex';
        
        try {
            const response = await fetch(`/fetch_wikipedia?title=${encodeURIComponent(title)}&lang=${lang}`);
            const data = await response.json();
            
            if (data.error) {
                alert(`Error: ${data.error}`);
                if (data.options) {
                    alert("Did you mean: " + data.options.join(", "));
                }
            } else {
                // Display article info
                articleTitle.textContent = data.title;
                wikiLink.href = data.url;
                wikiLink.textContent = 'View on Wikipedia';
                
                // Display content
                englishContent.textContent = data.content;
            }
        } catch (error) {
            console.error('Error fetching Wikipedia article:', error);
            alert('Failed to fetch Wikipedia article. Please try again.');
        } finally {
            loadingFetch.style.display = 'none';
        }
    }

    // Translate article to Meetei Mayek
    async function translateArticle() {
        const content = englishContent.textContent;
        
        if (!content) {
            alert('No content to translate. Please fetch an article first.');
            return;
        }
        
        // Clear previous translation
        meeteiContent.innerHTML = '';
        progressInfo.textContent = '';
        
        // Show loading
        loadingTranslate.style.display = 'flex';
        translateBtn.disabled = true;
        
        try {
            // Split content into chunks
            const chunks = splitTextIntoChunks(content, 500);
            progressInfo.textContent = `Translating 0/${chunks.length} chunks...`;
            
            let fullTranslation = '';
            
            for (let i = 0; i < chunks.length; i++) {
                progressInfo.textContent = `Translating ${i+1}/${chunks.length} chunks...`;
                
                const response = await fetch('/translate', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ text: chunks[i] })
                });
                
                const data = await response.json();
                
                if (data.error) {
                    throw new Error(data.error);
                }
                
                fullTranslation += data.translation + '\n\n';
                meeteiContent.textContent = fullTranslation;
                
                // Scroll to bottom
                meeteiContent.scrollTop = meeteiContent.scrollHeight;
                
                // Small delay between chunks to avoid rate limiting
                await new Promise(resolve => setTimeout(resolve, 300));
            }
            
            progressInfo.textContent = `Translation completed! ${chunks.length} chunks translated`;
        } catch (error) {
            console.error('Translation error:', error);
            progressInfo.textContent = 'Error: ' + error.message;
        } finally {
            loadingTranslate.style.display = 'none';
            translateBtn.disabled = false;
        }
    }

    // Helper function to split text into chunks
    function splitTextIntoChunks(text, maxChunkSize) {
        const chunks = [];
        let index = 0;
        
        while (index < text.length) {
            let chunkEnd = index + maxChunkSize;
            
            // Try to split at paragraph boundary
            if (chunkEnd < text.length) {
                const nextNewline = text.indexOf('\n\n', chunkEnd);
                if (nextNewline !== -1 && nextNewline > index) {
                    chunkEnd = nextNewline + 2; // Include the two newlines
                }
            }
            
            chunks.push(text.substring(index, chunkEnd));
            index = chunkEnd;
        }
        
        return chunks;
    }
});
