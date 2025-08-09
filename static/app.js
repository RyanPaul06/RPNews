// RPNews Enhanced - Frontend JavaScript with Open Source LLM Support

let currentData = null;
let currentView = 'briefing';
let currentFilter = 'all';

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    loadBriefing();
    setupNavigation();
    setupFilters();
});

function setupNavigation() {
    document.querySelectorAll('.nav-tab').forEach(tab => {
        tab.addEventListener('click', function() {
            // Update active tab
            document.querySelectorAll('.nav-tab').forEach(t => t.classList.remove('active'));
            this.classList.add('active');
            
            // Switch view
            currentView = this.dataset.view;
            if (currentData || currentView === 'reading-list') {
                displayContent();
            }
        });
    });
    
    // Handle reading list button
    document.querySelector('[data-view="reading-list"]').addEventListener('click', function() {
        currentView = 'reading-list';
        // Update nav tabs
        document.querySelectorAll('.nav-tab').forEach(t => t.classList.remove('active'));
        displayContent();
    });
}

function setupFilters() {
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            
            currentFilter = this.dataset.filter;
            if (currentData) {
                displayContent();
            }
        });
    });
}

async function loadBriefing() {
    try {
        showLoading();
        const response = await fetch('/api/morning-briefing');
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        
        currentData = await response.json();
        console.log('Briefing data loaded:', currentData);
        displayContent();
    } catch (error) {
        console.error('Error loading briefing:', error);
        showError(error.message);
    }
}

async function loadReadingList() {
    try {
        showLoading();
        const response = await fetch('/api/reading-list');
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        
        const readingListData = await response.json();
        console.log('Reading list loaded:', readingListData);
        return readingListData;
    } catch (error) {
        console.error('Error loading reading list:', error);
        showError(error.message);
        return null;
    }
}

async function refreshNews() {
    const refreshIcon = document.getElementById('refresh-icon');
    refreshIcon.style.animation = 'spin 1s linear infinite';
    
    try {
        // Trigger collection
        const response = await fetch('/api/collect', { method: 'POST' });
        
        if (!response.ok) {
            throw new Error(`Collection failed: ${response.statusText}`);
        }
        
        // Wait a moment then reload
        setTimeout(async () => {
            if (currentView === 'reading-list') {
                await displayContent(); // Will reload reading list
            } else {
                await loadBriefing();
            }
            refreshIcon.style.animation = 'none';
        }, 5000);
    } catch (error) {
        console.error('Error refreshing:', error);
        refreshIcon.style.animation = 'none';
        alert('Refresh failed: ' + error.message);
    }
}

async function markAsRead(articleId, element) {
    try {
        const response = await fetch(`/api/articles/${articleId}/read`, { method: 'POST' });
        
        if (!response.ok) {
            throw new Error(`Failed to toggle read status: ${response.statusText}`);
        }
        
        const result = await response.json();
        const card = element.closest('.article-card');
        const btn = element.closest('.article-card').querySelector('.read-btn');
        
        if (result.isRead) {
            card.classList.add('read');
            btn.classList.add('read');
            btn.innerHTML = '✓';
            btn.title = 'Mark as unread';
        } else {
            card.classList.remove('read');
            btn.classList.remove('read');
            btn.innerHTML = '○';
            btn.title = 'Mark as read';
        }
    } catch (error) {
        console.error('Error toggling read status:', error);
        alert('Failed to toggle read status: ' + error.message);
    }
}

async function toggleStar(articleId, element) {
    try {
        const card = element.closest('.article-card');
        const isStarred = card.classList.contains('starred');
        
        const response = await fetch(`/api/articles/${articleId}/star`, { 
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ starred: !isStarred })
        });
        
        if (!response.ok) {
            throw new Error(`Failed to toggle star: ${response.statusText}`);
        }
        
        const result = await response.json();
        
        if (result.isStarred) {
            card.classList.add('starred');
            element.innerHTML = '★';
            element.classList.add('starred');
        } else {
            card.classList.remove('starred');
            element.innerHTML = '☆';
            element.classList.remove('starred');
        }
    } catch (error) {
        console.error('Error toggling star:', error);
        alert('Failed to toggle star: ' + error.message);
    }
}

async function passArticle(articleId, element) {
    try {
        const response = await fetch(`/api/articles/${articleId}/pass`, { method: 'POST' });
        
        if (!response.ok) {
            throw new Error(`Failed to pass article: ${response.statusText}`);
        }
        
        // Remove the article card with animation
        const card = element.closest('.article-card');
        card.style.opacity = '0';
        card.style.transform = 'translateX(-100px)';
        
        setTimeout(() => {
            card.remove();
            // Update stats if needed
            updateStatsBar();
        }, 300);
        
    } catch (error) {
        console.error('Error passing article:', error);
        alert('Failed to pass article: ' + error.message);
    }
}

function openArticle(url, summaryElement) {
    // Mark the summary as clicked (visual feedback)
    if (summaryElement) {
        summaryElement.style.background = 'linear-gradient(135deg, #e8ecff, #d4e3ff)';
    }
    
    // Open article in new tab
    window.open(url, '_blank', 'noopener,noreferrer');
}

function showLoading() {
    document.getElementById('loading').style.display = 'block';
    document.getElementById('content').style.display = 'none';
}

function hideLoading() {
    document.getElementById('loading').style.display = 'none';
    document.getElementById('content').style.display = 'block';
}

function showError(message = 'Unknown error occurred') {
    hideLoading();
    document.getElementById('news-content').innerHTML = `
        <div class="empty-state">
            <div class="empty-state-icon">⚠️</div>
            <h3>Unable to load news</h3>
            <p>Error: ${message}</p>
            <p>Please try refreshing or check back in a few minutes.</p>
        </div>
    `;
}

async function displayContent() {
    hideLoading();
    
    // Handle reading list view
    if (currentView === 'reading-list') {
        const readingListData = await loadReadingList();
        if (!readingListData) return;
        
        document.getElementById('briefing-date').textContent = 'Reading List';
        document.getElementById('daily-overview').style.display = 'none';
        
        // Update stats for reading list
        const statsBar = document.getElementById('stats-bar');
        const highPriorityCount = readingListData.articles.filter(a => a.priority === 'high').length;
        
        statsBar.innerHTML = `
            <div class="stat-item">
                <div class="stat-number">${readingListData.count}</div>
                <div class="stat-label">Unread Articles</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">${highPriorityCount}</div>
                <div class="stat-label">High Priority</div>
            </div>
        `;
        
        const contentDiv = document.getElementById('news-content');
        if (readingListData.articles.length === 0) {
            contentDiv.innerHTML = '<div class="empty-state"><div class="empty-state-icon">📖</div><h3>All caught up!</h3><p>You\'ve read all available articles. Check back later for new updates.</p></div>';
        } else {
            const filteredArticles = applyFilters(readingListData.articles);
            contentDiv.innerHTML = `
                <div class="articles-grid">
                    ${filteredArticles.map(article => createArticleCard(article, true)).join('')}
                </div>
            `;
        }
        return;
    }
    
    if (!currentData || !currentData.briefing) {
        showError('No briefing data available');
        return;
    }

    // Update header
    document.getElementById('briefing-date').textContent = currentData.date || 'Today';
    
    // Show daily overview if available
    const overviewDiv = document.getElementById('daily-overview');
    const overviewText = document.getElementById('overview-text');
    if (currentData.daily_overview && currentView === 'briefing') {
        overviewText.textContent = currentData.daily_overview;
        overviewDiv.style.display = 'block';
    } else {
        overviewDiv.style.display = 'none';
    }
    
    // Update stats
    updateStatsBar();
    
    // Display articles
    const contentDiv = document.getElementById('news-content');
    contentDiv.className = 'fade-in';
    
    try {
        if (currentView === 'briefing') {
            contentDiv.innerHTML = displayAllCategories();
        } else if (currentView === 'starred') {
            contentDiv.innerHTML = displayStarredArticles();
        } else {
            contentDiv.innerHTML = displaySingleCategory(currentView);
        }
    } catch (error) {
        console.error('Error displaying content:', error);
        showError('Failed to display articles: ' + error.message);
    }
}

function updateStatsBar() {
    const statsBar = document.getElementById('stats-bar');
    
    if (currentView === 'briefing') {
        const totalArticles = currentData.total_articles || 0;
        const aiCount = currentData.briefing.ai?.length || 0;
        const financeCount = currentData.briefing.finance?.length || 0;
        const politicsCount = currentData.briefing.politics?.length || 0;
        const highPriorityCount = currentData.high_priority_count || 0;
        
        statsBar.innerHTML = `
            <div class="stat-item">
                <div class="stat-number">${totalArticles}</div>
                <div class="stat-label">Total Articles</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">${highPriorityCount}</div>
                <div class="stat-label">High Priority</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">${aiCount}</div>
                <div class="stat-label">AI & Tech</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">${financeCount}</div>
                <div class="stat-label">Finance</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">${politicsCount}</div>
                <div class="stat-label">Politics</div>
            </div>
        `;
    } else {
        const categoryData = getCurrentCategoryData();
        const highPriorityCount = categoryData.filter(a => a.priority === 'high').length;
        const unreadCount = categoryData.filter(a => !a.isRead).length;
        
        statsBar.innerHTML = `
            <div class="stat-item">
                <div class="stat-number">${categoryData.length}</div>
                <div class="stat-label">Articles</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">${highPriorityCount}</div>
                <div class="stat-label">High Priority</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">${unreadCount}</div>
                <div class="stat-label">Unread</div>
            </div>
        `;
    }
}

function getCurrentCategoryData() {
    if (currentView === 'starred') {
        return getAllArticles().filter(a => a.isStarred);
    } else if (currentView === 'reading-list') {
        return getAllArticles().filter(a => !a.isRead);
    } else if (currentView !== 'briefing') {
        return currentData.briefing[currentView] || [];
    }
    return [];
}

function getAllArticles() {
    const allArticles = [];
    ['ai', 'finance', 'politics'].forEach(category => {
        if (currentData.briefing[category]) {
            allArticles.push(...currentData.briefing[category]);
        }
    });
    return allArticles;
}

function applyFilters(articles) {
    let filtered = [...articles];
    
    if (currentFilter === 'high') {
        filtered = filtered.filter(a => a.priority === 'high');
    } else if (currentFilter === 'unread') {
        filtered = filtered.filter(a => !a.isRead);
    }
    
    return filtered;
}

function displayAllCategories() {
    let html = '';
    
    const categories = [
        { key: 'ai', title: 'AI & Technology', icon: 'AI' },
        { key: 'finance', title: 'Finance & Markets', icon: 'FIN' },
        { key: 'politics', title: 'Politics & Policy', icon: 'POL' }
    ];

    categories.forEach(category => {
        const articles = applyFilters(currentData.briefing[category.key] || []);
        if (articles.length > 0) {
            const highPriorityCount = articles.filter(a => a.priority === 'high').length;
            const unreadCount = articles.filter(a => !a.isRead).length;
            
            html += `
                <div class="category-section">
                    <div class="category-header">
                        <span class="category-icon">${category.icon}</span>
                        <h2 class="category-title">${category.title}</h2>
                        <div class="category-stats">
                            ${highPriorityCount > 0 ? `<span class="category-count" style="background: #ff6b6b;">${highPriorityCount} high priority</span>` : ''}
                            <span class="category-count">${articles.length} articles</span>
                            ${unreadCount > 0 ? `<span class="category-count" style="background: #48dbfb;">${unreadCount} unread</span>` : ''}
                        </div>
                    </div>
                    <div class="articles-grid">
                        ${articles.map(article => createArticleCard(article)).join('')}
                    </div>
                </div>
            `;
        }
    });

    return html || '<div class="empty-state"><div class="empty-state-icon">∅</div><h3>No articles match current filters</h3><p>Try adjusting your filters or refresh to collect the latest news.</p></div>';
}

function displaySingleCategory(categoryKey) {
    const articles = applyFilters(currentData.briefing[categoryKey] || []);
    
    if (articles.length === 0) {
        return '<div class="empty-state"><div class="empty-state-icon">∅</div><h3>No articles match current filters</h3><p>Try adjusting your filters or refresh to collect the latest news.</p></div>';
    }

    return `
        <div class="articles-grid">
            ${articles.map(article => createArticleCard(article)).join('')}
        </div>
    `;
}

function displayStarredArticles() {
    const starredArticles = applyFilters(getAllArticles().filter(a => a.isStarred));
    
    if (starredArticles.length === 0) {
        return '<div class="empty-state"><div class="empty-state-icon">⭐</div><h3>No starred articles yet</h3><p>Star articles you find interesting to save them for later reading.</p></div>';
    }

    return `
        <div class="starred-section">
            <div class="articles-grid">
                ${starredArticles.map(article => createArticleCard(article)).join('')}
            </div>
        </div>
    `;
}

function createArticleCard(article, showPassButton = false) {
    const tags = article.tags || [];
    const tagsHtml = tags.map(tag => `<span class="tag">${escapeHtml(tag)}</span>`).join('');
    const readClass = article.isRead ? 'read' : '';
    const starredClass = article.isStarred ? 'starred' : '';
    const readIcon = article.isRead ? '✓' : '○';
    const starIcon = article.isStarred ? '★' : '☆';
    const readBtnClass = article.isRead ? 'read' : '';
    const starBtnClass = article.isStarred ? 'starred' : '';
    const readTitle = article.isRead ? 'Mark as unread' : 'Mark as read';
    
    // Create action buttons
    let actionButtons = `
        <button class="action-btn read-btn ${readBtnClass}" 
                onclick="markAsRead('${escapeHtml(article.id)}', this)" 
                title="${readTitle}">
            ${readIcon}
        </button>
        <button class="action-btn star-btn ${starBtnClass}" 
                onclick="toggleStar('${escapeHtml(article.id)}', this)" 
                title="Star article">
            ${starIcon}
        </button>
    `;
    
    // Add pass button for reading list and main briefing
    if (showPassButton || currentView === 'briefing') {
        actionButtons += `
            <button class="action-btn pass-btn" 
                    onclick="passArticle('${escapeHtml(article.id)}', this)" 
                    title="Pass/dismiss article">
                ✕
            </button>
        `;
    }
    
    return `
        <article class="article-card ${readClass} ${starredClass}">
            <div class="article-actions">
                ${actionButtons}
            </div>
            <div class="priority-badge priority-${article.priority || 'medium'}">${article.priority || 'medium'}</div>
            
            <div class="article-header">
                <div class="article-meta">
                    <span class="article-source">${escapeHtml(article.source)}</span>
                    <div class="article-time-info">
                        <span>${escapeHtml(article.timeAgo)}</span>
                        <span class="reading-time">${article.readingTime || 2}min read</span>
                    </div>
                </div>
                <h3 class="article-title" onclick="openArticle('${escapeHtml(article.url)}', this)">
                    ${escapeHtml(article.title)}
                </h3>
            </div>
            
            <div class="article-content">
                ${article.aiSummary ? `
                    <div class="article-summary" onclick="openArticle('${escapeHtml(article.url)}', this)" title="Click to read full article">
                        ${escapeHtml(article.aiSummary)}
                    </div>
                ` : ''}
                <p class="article-excerpt">${escapeHtml(article.excerpt)}</p>
                ${tagsHtml ? `<div class="article-tags">${tagsHtml}</div>` : ''}
            </div>
        </article>
    `;
}

function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
