document.addEventListener('DOMContentLoaded', () => {
    const feedContainer = document.getElementById('feed');
    const loadingState = document.getElementById('loading');
    const navLinks = document.querySelectorAll('.nav-links a');
    
    // Q&A Modal Elements
    const modal = document.getElementById('qa-modal');
    const closeModalBtn = document.getElementById('close-modal');
    const qaSubmitBtn = document.getElementById('qa-submit');
    const qaInput = document.getElementById('qa-input');
    const qaHistory = document.getElementById('qa-history');
    
    let currentArticleId = null;

    // Initialize Markdown parsing options
    marked.setOptions({
        gfm: true,
        breaks: true,
        headerIds: false
    });

    const fetchArticles = async (niche = 'all') => {
        try {
            loadingState.classList.remove('hidden');
            feedContainer.classList.add('hidden');
            feedContainer.innerHTML = '';
            
            const url = niche === 'all' ? '/api/articles' : `/api/articles?niche=${encodeURIComponent(niche)}`;
            const response = await fetch(url);
            const articles = await response.json();
            
            loadingState.classList.add('hidden');
            
            if (articles.length === 0) {
                feedContainer.innerHTML = '<p style="text-align: center; color: var(--text-secondary);">No reporting available for this niche currently. Agents are scanning...</p>';
            } else {
                articles.forEach((article, index) => {
                    const card = document.createElement('article');
                    card.className = 'article-card';
                    card.style.animationDelay = `${index * 0.15}s`;
                    
                    const date = new Date(article.published_at).toLocaleDateString();
                    
                    card.innerHTML = `
                        <div class="meta-info">
                            <span>${article.niche} &bull; ${date}</span>
                            <button class="btn-interrogate" data-id="${article.id}" data-title="${article.headline}">
                                <svg width="16" height="16" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"></path></svg>
                                Interrogate AI
                            </button>
                        </div>
                        <h2 class="article-title">${article.headline}</h2>
                        <h3 class="article-subtitle">${article.subheadline}</h3>
                        <div class="article-body">
                            ${marked.parse(article.body_markdown)}
                        </div>
                        <div class="reporting-process-panel">
                            <h4>
                                <svg width="16" height="16" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"></path></svg>
                                Reporting Process
                            </h4>
                            <p>This article was generated through:</p>
                            <ul>
                                <li>${article.sources_analyzed || 1} data sources dynamically analyzed</li>
                                <li>${article.overlapping_signals_merged || 0} overlapping signals consolidated</li>
                                <li>Structured fact sheet extracted and verified</li>
                                <li>Editorial synthesis applied securely via The Sentinel Style Guide</li>
                            </ul>
                            <button class="fact-transparency-toggle" onclick="this.nextElementSibling.classList.toggle('open')">View reporting notes &amp; facts</button>
                            <div class="fact-transparency-content">
                                <p><strong>Key Entities:</strong> ${article.fact_sheet?.key_entities?.join(', ') || 'N/A'}</p>
                                <p style="margin-top: 0.5rem;"><strong>Timeline:</strong> ${article.fact_sheet?.timeline_events?.join(' &rarr; ') || 'N/A'}</p>
                                <p style="margin-top: 0.5rem;"><strong>Core Claims:</strong></p>
                                <ul>
                                    ${(article.fact_sheet?.core_claims || ['N/A']).map(c => `<li>${c}</li>`).join('')}
                                </ul>
                            </div>
                        </div>
                    `;
                    feedContainer.appendChild(card);
                });
            }
            feedContainer.classList.remove('hidden');
            attachInterrogateListeners();
            
        } catch (error) {
            console.error('Error fetching articles:', error);
            loadingState.innerHTML = '<p>Error syncing with agents. Please refresh.</p>';
        }
    };

    const attachInterrogateListeners = () => {
        const buttons = document.querySelectorAll('.btn-interrogate');
        buttons.forEach(btn => {
            btn.addEventListener('click', (e) => {
                currentArticleId = e.currentTarget.getAttribute('data-id');
                const title = e.currentTarget.getAttribute('data-title');
                
                // Set modal title
                document.querySelector('.modal-header h2').innerText = `Interrogate: ${title}`;
                
                // Clear chat history
                qaHistory.innerHTML = '';
                qaInput.value = '';
                
                // Show modal
                modal.classList.add('active');
            });
        });
    };

    const handleChatSubmit = async () => {
        const question = qaInput.value.trim();
        if (!question || !currentArticleId) return;

        // Display user question
        appendChatBubble(question, 'user');
        qaInput.value = '';

        // Add loading bubble for bot
        const botLoading = appendChatBubble('Synthesizing answer...', 'bot', true);

        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ article_id: currentArticleId, question })
            });
            const data = await response.json();
            
            // Replace loading bubble with real answer
            botLoading.innerText = data.response;
            botLoading.classList.remove('loading-bubble');
            
        } catch (error) {
            botLoading.innerText = "Connection lost to Research Agent. Try again.";
        }
    };

    const appendChatBubble = (text, sender, isLoading = false) => {
        const bubble = document.createElement('div');
        bubble.className = `chat-bubble ${sender}`;
        if (isLoading) bubble.classList.add('loading-bubble');
        bubble.innerText = text;
        qaHistory.appendChild(bubble);
        
        // Auto scroll
        document.querySelector('.modal-body').scrollTop = document.querySelector('.modal-body').scrollHeight;
        
        return bubble;
    };

    // Event Listeners for Chat
    qaSubmitBtn.addEventListener('click', handleChatSubmit);
    qaInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') handleChatSubmit();
    });

    document.querySelectorAll('.qa-quick-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            qaInput.value = e.target.innerText;
            handleChatSubmit();
        });
    });

    closeModalBtn.addEventListener('click', () => {
        modal.classList.remove('active');
        currentArticleId = null;
    });
    
    // Close modal gently if clicking outside
    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            modal.classList.remove('active');
        }
    });

    // Navigation Filtering
    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            
            // Update active state
            navLinks.forEach(l => l.classList.remove('active'));
            e.currentTarget.classList.add('active');
            
            const niche = e.currentTarget.getAttribute('data-niche');
            fetchArticles(niche);
        });
    });

    // Initial Load
    fetchArticles();
});
