# Enhanced professional news dashboard with React-inspired UI
@app.get("/", response_class=HTMLResponse)
async def dashboard():
    """Modern React-inspired dashboard with beautiful UI"""
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>RPNews - AI-Powered News Intelligence Platform</title>
    <meta name="description" content="RPNews is an AI-powered news intelligence platform that aggregates, analyzes, and summarizes news from 60+ premium sources across AI, finance, and politics.">
    
    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    
    <!-- Font Awesome -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    
    <style>
        :root {
            --rp-primary: #3b82f6;
            --rp-secondary: #6366f1;
            --rp-success: #10b981;
            --rp-warning: #f59e0b;
            --rp-error: #ef4444;
            --rp-text: #1f2937;
            --rp-text-secondary: #6b7280;
            --rp-bg: #f8fafc;
            --rp-border: #e5e7eb;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
            background: var(--rp-bg);
            color: var(--rp-text);
            line-height: 1.6;
            min-height: 100vh;
        }

        /* Navigation */
        .top-nav {
            background: white;
            border-bottom: 1px solid var(--rp-border);
            position: sticky;
            top: 0;
            z-index: 50;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        }

        .nav-container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 0 1.5rem;
            display: flex;
            align-items: center;
            justify-content: space-between;
            height: 4rem;
        }

        .brand {
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }

        .brand-icon {
            width: 2rem;
            height: 2rem;
            background: var(--rp-primary);
            border-radius: 0.5rem;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
        }

        .brand-text {
            font-size: 1.25rem;
            font-weight: 700;
            color: var(--rp-text);
        }

        .brand-badge {
            font-size: 0.75rem;
            background: var(--rp-secondary);
            color: white;
            padding: 0.25rem 0.5rem;
            border-radius: 9999px;
            font-weight: 500;
        }

        .nav-actions {
            display: flex;
            align-items: center;
            gap: 1rem;
        }

        .search-bar {
            position: relative;
            width: 20rem;
            max-width: 100%;
        }

        .search-input {
            width: 100%;
            padding: 0.5rem 0.75rem 0.5rem 2.5rem;
            border: 1px solid var(--rp-border);
            border-radius: 0.5rem;
            font-size: 0.875rem;
            background: white;
            transition: all 0.2s;
        }

        .search-input:focus {
            outline: none;
            border-color: var(--rp-primary);
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
        }

        .search-icon {
            position: absolute;
            left: 0.75rem;
            top: 50%;
            transform: translateY(-50%);
            color: var(--rp-text-secondary);
        }

        .nav-btn {
            position: relative;
            padding: 0.5rem;
            color: var(--rp-text-secondary);
            border: none;
            background: none;
            border-radius: 0.375rem;
            cursor: pointer;
            transition: all 0.2s;
        }

        .nav-btn:hover {
            color: var(--rp-primary);
            background: rgba(59, 130, 246, 0.1);
        }

        .notification-badge {
            position: absolute;
            top: -0.25rem;
            right: -0.25rem;
            width: 1rem;
            height: 1rem;
            background: var(--rp-error);
            color: white;
            font-size: 0.75rem;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        /* Main Layout */
        .main-layout {
            display: flex;
            min-height: calc(100vh - 4rem);
        }

        .sidebar {
            width: 16rem;
            background: white;
            border-right: 1px solid var(--rp-border);
            padding: 1.5rem;
            position: sticky;
            top: 4rem;
            height: calc(100vh - 4rem);
            overflow-y: auto;
        }

        .sidebar-section {
            margin-bottom: 2rem;
        }

        .sidebar-title {
            font-size: 0.75rem;
            font-weight: 600;
            color: var(--rp-text-secondary);
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 0.75rem;
        }

        .sidebar-stats {
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
        }

        .stat-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .stat-label {
            font-size: 0.875rem;
            color: var(--rp-text);
        }

        .stat-value {
            font-size: 0.875rem;
            font-weight: 600;
            color: var(--rp-primary);
        }

        .nav-menu {
            display: flex;
            flex-direction: column;
            gap: 0.25rem;
        }

        .nav-item {
            display: flex;
            align-items: center;
            padding: 0.75rem;
            border-radius: 0.5rem;
            color: var(--rp-text-secondary);
            text-decoration: none;
            font-weight: 500;
            transition: all 0.2s;
            cursor: pointer;
            border: none;
            background: none;
            width: 100%;
            justify-content: flex-start;
        }

        .nav-item:hover {
            background: rgba(59, 130, 246, 0.1);
            color: var(--rp-text);
        }

        .nav-item.active {
            background: var(--rp-primary);
            color: white;
        }

        .nav-item i {
            margin-right: 0.75rem;
            width: 1rem;
        }

        .nav-badge {
            margin-left: auto;
            font-size: 0.75rem;
            background: var(--rp-border);
            color: var(--rp-text);
            padding: 0.125rem 0.5rem;
            border-radius: 9999px;
        }

        .collect-btn {
            width: 100%;
            background: var(--rp-primary);
            color: white;
            border: none;
            padding: 0.75rem;
            border-radius: 0.5rem;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.2s;
            margin-top: 1rem;
        }

        .collect-btn:hover {
            background: #2563eb;
        }

        .collect-btn:disabled {
            opacity: 0.6;
            cursor: not-allowed;
        }

        /* Content Area */
        .content {
            flex: 1;
            padding: 1.5rem;
            max-width: calc(100vw - 16rem);
        }

        .page-header {
            margin-bottom: 2rem;
        }

        .page-title {
            font-size: 2rem;
            font-weight: 700;
            color: var(--rp-text);
            margin-bottom: 0.5rem;
        }

        .page-subtitle {
            font-size: 1.125rem;
            color: var(--rp-text-secondary);
        }

        /* AI Overview Card */
        .ai-overview {
            background: linear-gradient(135deg, var(--rp-primary), var(--rp-secondary));
            border-radius: 0.75rem;
            padding: 2rem;
            margin-bottom: 2rem;
            color: white;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }

        .ai-overview-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 1rem;
        }

        .ai-overview-title {
            font-size: 1.25rem;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .ai-overview-icon {
            width: 4rem;
            height: 4rem;
            background: rgba(255, 255, 255, 0.2);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5rem;
        }

        .ai-overview-text {
            color: rgba(255, 255, 255, 0.9);
            line-height: 1.6;
            margin-bottom: 1rem;
        }

        .ai-overview-footer {
            display: flex;
            align-items: center;
            font-size: 0.875rem;
            color: rgba(255, 255, 255, 0.8);
        }

        /* Priority Alerts */
        .priority-alerts {
            margin-bottom: 2rem;
        }

        .section-title {
            font-size: 1.25rem;
            font-weight: 600;
            color: var(--rp-text);
            margin-bottom: 1rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .alerts-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 1rem;
        }

        .alert-card {
            background: white;
            border-radius: 0.5rem;
            padding: 1.5rem;
            border-left: 4px solid;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
            transition: all 0.2s;
            cursor: pointer;
        }

        .alert-card:hover {
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        }

        .alert-card.ai { border-left-color: var(--rp-primary); }
        .alert-card.finance { border-left-color: var(--rp-success); }
        .alert-card.politics { border-left-color: var(--rp-secondary); }

        .alert-header {
            display: flex;
            align-items: center;
            justify-content: between;
            margin-bottom: 0.75rem;
        }

        .alert-category {
            display: inline-flex;
            align-items: center;
            padding: 0.25rem 0.75rem;
            border-radius: 9999px;
            font-size: 0.75rem;
            font-weight: 500;
            gap: 0.25rem;
        }

        .alert-category.ai { background: rgba(59, 130, 246, 0.1); color: var(--rp-primary); }
        .alert-category.finance { background: rgba(16, 185, 129, 0.1); color: var(--rp-success); }
        .alert-category.politics { background: rgba(99, 102, 241, 0.1); color: var(--rp-secondary); }

        .alert-time {
            font-size: 0.75rem;
            color: var(--rp-text-secondary);
            margin-left: auto;
        }

        .alert-title {
            font-weight: 600;
            color: var(--rp-text);
            margin-bottom: 0.5rem;
            line-height: 1.4;
        }

        .alert-summary {
            font-size: 0.875rem;
            color: var(--rp-text-secondary);
            line-height: 1.5;
            margin-bottom: 0.75rem;
        }

        .alert-footer {
            display: flex;
            align-items: center;
            justify-content: space-between;
        }

        .alert-source {
            font-size: 0.75rem;
            color: var(--rp-text-secondary);
        }

        .alert-actions {
            display: flex;
            gap: 0.5rem;
        }

        .alert-action {
            font-size: 0.75rem;
            color: var(--rp-primary);
            text-decoration: none;
            cursor: pointer;
        }

        .alert-action:hover {
            text-decoration: underline;
        }

        /* Category Sections */
        .categories-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 1.5rem;
            margin-bottom: 2rem;
        }

        .category-card {
            background: white;
            border-radius: 0.75rem;
            padding: 1.5rem;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        }

        .category-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 1rem;
        }

        .category-title-group {
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }

        .category-icon {
            width: 2rem;
            height: 2rem;
            border-radius: 0.5rem;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .category-icon.ai { background: rgba(59, 130, 246, 0.1); color: var(--rp-primary); }
        .category-icon.finance { background: rgba(16, 185, 129, 0.1); color: var(--rp-success); }
        .category-icon.politics { background: rgba(99, 102, 241, 0.1); color: var(--rp-secondary); }

        .category-title {
            font-size: 1.125rem;
            font-weight: 600;
            color: var(--rp-text);
        }

        .category-count {
            font-size: 0.875rem;
            color: var(--rp-text-secondary);
        }

        .category-articles {
            display: flex;
            flex-direction: column;
            gap: 0.75rem;
            margin-bottom: 1rem;
        }

        .article-item {
            display: flex;
            align-items: flex-start;
            gap: 0.75rem;
            padding-bottom: 0.75rem;
            border-bottom: 1px solid var(--rp-border);
            cursor: pointer;
            transition: all 0.2s;
        }

        .article-item:last-child {
            border-bottom: none;
            padding-bottom: 0;
        }

        .article-item:hover {
            background: rgba(59, 130, 246, 0.02);
            margin: 0 -0.5rem;
            padding: 0.5rem;
            border-radius: 0.375rem;
        }

        .priority-dot {
            width: 0.5rem;
            height: 0.5rem;
            border-radius: 50%;
            margin-top: 0.5rem;
            flex-shrink: 0;
        }

        .priority-dot.high { background: var(--rp-error); }
        .priority-dot.medium { background: var(--rp-warning); }
        .priority-dot.low { background: var(--rp-text-secondary); }

        .article-content {
            flex: 1;
            min-width: 0;
        }

        .article-title {
            font-weight: 500;
            color: var(--rp-text);
            font-size: 0.875rem;
            line-height: 1.4;
            margin-bottom: 0.25rem;
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
            overflow: hidden;
        }

        .article-meta {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            font-size: 0.75rem;
            color: var(--rp-text-secondary);
        }

        .view-all-btn {
            width: 100%;
            padding: 0.75rem;
            border: 1px solid var(--rp-border);
            background: white;
            color: var(--rp-text);
            border-radius: 0.5rem;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.2s;
        }

        .view-all-btn:hover {
            background: var(--rp-bg);
            border-color: var(--rp-primary);
            color: var(--rp-primary);
        }

        /* Analytics */
        .analytics-card {
            background: white;
            border-radius: 0.75rem;
            padding: 1.5rem;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        }

        .analytics-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
            gap: 1.5rem;
            margin-bottom: 1.5rem;
        }

        .analytics-stat {
            text-align: center;
        }

        .analytics-number {
            font-size: 1.5rem;
            font-weight: 700;
            color: var(--rp-primary);
            margin-bottom: 0.25rem;
        }

        .analytics-label {
            font-size: 0.875rem;
            color: var(--rp-text-secondary);
        }

        .analytics-trend {
            background: var(--rp-bg);
            border-radius: 0.5rem;
            padding: 1rem;
            margin-top: 1rem;
        }

        .trend-chart {
            display: flex;
            align-items: end;
            justify-content: center;
            gap: 0.25rem;
            height: 4rem;
        }

        .trend-bar {
            width: 1rem;
            background: var(--rp-primary);
            border-radius: 0.125rem;
            opacity: 0.8;
            transition: all 0.2s;
        }

        .trend-bar:hover {
            opacity: 1;
        }

        /* Loading States */
        .loading {
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 2rem;
            color: var(--rp-text-secondary);
        }

        .loading-spinner {
            width: 1rem;
            height: 1rem;
            border: 2px solid var(--rp-border);
            border-top: 2px solid var(--rp-primary);
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin-right: 0.5rem;
        }

        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        .empty-state {
            text-align: center;
            padding: 3rem 1rem;
            color: var(--rp-text-secondary);
        }

        .empty-state i {
            font-size: 3rem;
            margin-bottom: 1rem;
            opacity: 0.5;
        }

        /* Responsive Design */
        @media (max-width: 768px) {
            .main-layout {
                flex-direction: column;
            }
            
            .sidebar {
                width: 100%;
                height: auto;
                position: static;
                border-right: none;
                border-bottom: 1px solid var(--rp-border);
            }
            
            .content {
                max-width: 100%;
            }
            
            .search-bar {
                display: none;
            }
            
            .categories-grid,
            .alerts-grid {
                grid-template-columns: 1fr;
            }
            
            .analytics-grid {
                grid-template-columns: repeat(2, 1fr);
            }
        }

        /* Animations */
        .fade-in {
            animation: fadeIn 0.5s ease-in;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(1rem); }
            to { opacity: 1; transform: translateY(0); }
        }

        .status-indicator {
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            font-size: 0.875rem;
            color: var(--rp-text-secondary);
        }

        .status-dot {
            width: 0.5rem;
            height: 0.5rem;
            background: var(--rp-success);
            border-radius: 50%;
            animation: pulse 2s infinite;
        }

        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
    </style>
</head>
<body>
    <!-- Top Navigation -->
    <nav class="top-nav">
        <div class="nav-container">
            <div class="brand">
                <div class="brand-icon">
                    <i class="fas fa-newspaper"></i>
                </div>
                <span class="brand-text">RPNews</span>
                <span class="brand-badge">AI-Powered</span>
            </div>
            
            <div class="search-bar">
                <i class="fas fa-search search-icon"></i>
                <input type="text" class="search-input" placeholder="Search articles, topics, sources..." id="globalSearch">
            </div>
            
            <div class="nav-actions">
                <button class="nav-btn" id="notificationsBtn">
                    <i class="fas fa-bell"></i>
                    <span class="notification-badge">3</span>
                </button>
                <button class="nav-btn" id="settingsBtn">
                    <i class="fas fa-cog"></i>
                </button>
                <div class="nav-btn">
                    <i class="fas fa-user"></i>
                </div>
            </div>
        </div>
    </nav>

    <!-- Main Layout -->
    <div class="main-layout">
        <!-- Sidebar -->
        <aside class="sidebar">
            <div class="sidebar-section">
                <h3 class="sidebar-title">Today's Overview</h3>
                <div class="sidebar-stats">
                    <div class="stat-row">
                        <span class="stat-label">Total Articles</span>
                        <span class="stat-value" id="totalArticles">0</span>
                    </div>
                    <div class="stat-row">
                        <span class="stat-label">High Priority</span>
                        <span class="stat-value" id="highPriority" style="color: var(--rp-error);">0</span>
                    </div>
                    <div class="stat-row">
                        <span class="stat-label">AI Summaries</span>
                        <span class="stat-value" id="aiSummaries" style="color: var(--rp-success);">0</span>
                    </div>
                </div>
            </div>

            <div class="sidebar-section">
                <h3 class="sidebar-title">Navigation</h3>
                <nav class="nav-menu">
                    <button class="nav-item active" data-view="dashboard">
                        <i class="fas fa-tachometer-alt"></i>
                        Dashboard
                    </button>
                </nav>
            </div>

            <div class="sidebar-section">
                <h3 class="sidebar-title">Categories</h3>
                <nav class="nav-menu">
                    <button class="nav-item" data-view="ai">
                        <i class="fas fa-robot"></i>
                        AI & Technology
                        <span class="nav-badge" id="aiCount">0</span>
                    </button>
                    <button class="nav-item" data-view="finance">
                        <i class="fas fa-chart-line"></i>
                        Finance & Markets
                        <span class="nav-badge" id="financeCount">0</span>
                    </button>
                    <button class="nav-item" data-view="politics">
                        <i class="fas fa-landmark"></i>
                        Politics & Policy
                        <span class="nav-badge" id="politicsCount">0</span>
                    </button>
                </nav>
            </div>

            <div class="sidebar-section">
                <div class="status-indicator">
                    <div class="status-dot"></div>
                    <span>Last updated: <span id="lastUpdate">--:--</span></span>
                </div>
                <button class="collect-btn" id="collectBtn">
                    <i class="fas fa-sync-alt" id="collectIcon"></i>
                    Collect Latest
                </button>
            </div>
        </aside>

        <!-- Main Content -->
        <main class="content">
            <div class="page-header">
                <h1 class="page-title">Daily Intelligence Briefing</h1>
                <p class="page-subtitle" id="currentDate"></p>
            </div>

            <!-- AI Overview -->
            <div class="ai-overview">
                <div class="ai-overview-header">
                    <div>
                        <h2 class="ai-overview-title">
                            <i class="fas fa-brain"></i>
                            AI-Generated Overview
                        </h2>
                    </div>
                    <div class="ai-overview-icon">
                        <i class="fas fa-lightbulb"></i>
                    </div>
                </div>
                <p class="ai-overview-text" id="aiOverviewText">
                    🌅 Today's Intelligence Overview: Analyzing latest news from premium sources across AI, finance, and politics. AI-powered summaries and priority detection active.
                </p>
                <div class="ai-overview-footer">
                    <i class="fas fa-robot"></i>
                    <span>Generated by Enhanced AI Model • Analysis Active</span>
                </div>
            </div>

            <!-- Priority Alerts -->
            <section class="priority-alerts">
                <h2 class="section-title">
                    <i class="fas fa-exclamation-triangle" style="color: var(--rp-error);"></i>
                    High Priority Updates
                </h2>
                <div class="alerts-grid" id="priorityAlerts">
                    <div class="loading">
                        <div class="loading-spinner"></div>
                        Loading priority alerts...
                    </div>
                </div>
            </section>

            <!-- Categories -->
            <section class="categories-grid" id="categoriesGrid">
                <div class="loading">
                    <div class="loading-spinner"></div>
                    Loading categories...
                </div>
            </section>

            <!-- Analytics -->
            <section class="analytics-card">
                <h2 class="section-title">
                    <i class="fas fa-chart-bar" style="color: var(--rp-primary);"></i>
                    Analytics & Insights
                </h2>
                <div class="analytics-grid">
                    <div class="analytics-stat">
                        <div class="analytics-number" id="analyticsDaily">0</div>
                        <div class="analytics-label">Articles Today</div>
                    </div>
                    <div class="analytics-stat">
                        <div class="analytics-number" id="analyticsAI" style="color: var(--rp-secondary);">0</div>
                        <div class="analytics-label">AI Summaries</div>
                    </div>
                    <div class="analytics-stat">
                        <div class="analytics-number" id="analyticsSources" style="color: var(--rp-warning);">60</div>
                        <div class="analytics-label">Active Sources</div>
                    </div>
                    <div class="analytics-stat">
                        <div class="analytics-number" id="analyticsTime" style="color: #8b5cf6;">4.2</div>
                        <div class="analytics-label">Avg Read Time</div>
                    </div>
                </div>
                <div class="analytics-trend">
                    <h3 style="font-size: 0.875rem; color: var(--rp-text); margin-bottom: 1rem;">Article Collection Trends (7 Days)</h3>
                    <div class="trend-chart" id="trendChart">
                        <div class="trend-bar" style="height: 50%;"></div>
                        <div class="trend-bar" style="height: 65%;"></div>
                        <div class="trend-bar" style="height: 75%;"></div>
                        <div class="trend-bar" style="height: 90%;"></div>
                        <div class="trend-bar" style="height: 100%;"></div>
                        <div class="trend-bar" style="height: 80%;"></div>
                        <div class="trend-bar" style="height: 70%;"></div>
                    </div>
                </div>
            </section>
        </main>
    </div>

    <script>
        // Global state
        let currentData = null;
        let currentView = 'dashboard';

        // Initialize app
        document.addEventListener('DOMContentLoaded', function() {
            initializeApp();
            setupEventListeners();
            loadDashboardData();
        });

        function initializeApp() {
            // Set current date
            const now = new Date();
            document.getElementById('currentDate').textContent = now.toLocaleDateString('en-US', {
                weekday: 'long',
                year: 'numeric',
                month: 'long',
                day: 'numeric'
            });
        }

        function setupEventListeners() {
            // Navigation
            document.querySelectorAll('.nav-item').forEach(item => {
                item.addEventListener('click', function() {
                    const view = this.dataset.view;
                    switchView(view);
                });
            });

            // Collect button
            document.getElementById('collectBtn').addEventListener('click', triggerCollection);

            // Search
            document.getElementById('globalSearch').addEventListener('input', handleSearch);
        }

        function switchView(view) {
            currentView = view;
            
            // Update active nav item
            document.querySelectorAll('.nav-item').forEach(item => {
                item.classList.remove('active');
                if (item.dataset.view === view) {
                    item.classList.add('active');
                }
            });

            // Load view data
            if (view === 'dashboard') {
                loadDashboardData();
            } else {
                loadCategoryData(view);
            }
        }

        async function loadDashboardData() {
            try {
                showLoading();
                const response = await fetch('/api/news/dashboard');
                const data = await response.json();
                currentData = data;
                displayDashboardData(data);
            } catch (error) {
                console.error('Error loading dashboard:', error);
                showError('Failed to load dashboard data');
            }
        }

        async function loadCategoryData(category) {
            try {
                showLoading();
                const response = await fetch(`/api/news/category/${category}`);
                const articles = await response.json();
                displayCategoryData(category, articles);
            } catch (error) {
                console.error(`Error loading ${category} data:`, error);
                showError(`Failed to load ${category} data`);
            }
        }

        function displayDashboardData(data) {
            // Update stats
            document.getElementById('totalArticles').textContent = data.stats.totalArticles;
            document.getElementById('highPriority').textContent = data.stats.highPriority;
            document.getElementById('aiSummaries').textContent = data.stats.aiSummaries;
            document.getElementById('aiCount').textContent = data.stats.aiCount;
            document.getElementById('financeCount').textContent = data.stats.financeCount;
            document.getElementById('politicsCount').textContent = data.stats.politicsCount;
            document.getElementById('lastUpdate').textContent = data.stats.lastUpdate;

            // Update AI overview
            document.getElementById('aiOverviewText').textContent = data.dailyOverview;

            // Update analytics
            document.getElementById('analyticsDaily').textContent = data.analytics.dailyArticles;
            document.getElementById('analyticsAI').textContent = data.analytics.aiSummaries;
            document.getElementById('analyticsSources').textContent = data.analytics.activeSources;
            document.getElementById('analyticsTime').textContent = data.analytics.avgReadTime;

            // Display priority alerts
            displayPriorityAlerts(data.highPriorityArticles);

            // Display categories
            displayCategories(data.categories);
        }

        function displayPriorityAlerts(articles) {
            const container = document.getElementById('priorityAlerts');
            
            if (!articles || articles.length === 0) {
                container.innerHTML = `
                    <div class="empty-state">
                        <i class="fas fa-info-circle"></i>
                        <h3>No high priority alerts</h3>
                        <p>All systems nominal. Check back later for updates.</p>
                    </div>
                `;
                return;
            }

            container.innerHTML = articles.slice(0, 6).map(article => `
                <div class="alert-card ${article.category}" onclick="openArticle('${article.url}')">
                    <div class="alert-header">
                        <span class="alert-category ${article.category}">
                            <i class="fas ${getCategoryIcon(article.category)}"></i>
                            ${getCategoryLabel(article.category)}
                        </span>
                        <span class="alert-time">${article.publishedTime}</span>
                    </div>
                    <h3 class="alert-title">${article.title}</h3>
                    <p class="alert-summary">${article.aiSummary}</p>
                    <div class="alert-footer">
                        <span class="alert-source">${article.source}</span>
                        <div class="alert-actions">
                            <a href="#" class="alert-action" onclick="event.stopPropagation(); markAsRead('${article.id}')">Mark Read</a>
                            <a href="#" class="alert-action" onclick="event.stopPropagation(); starArticle('${article.id}')">Star</a>
                        </div>
                    </div>
                </div>
            `).join('');
        }

        function displayCategories(categories) {
            const container = document.getElementById('categoriesGrid');
            
            const categoryConfig = {
                ai: { title: 'AI & Technology', icon: 'fas fa-robot' },
                finance: { title: 'Finance & Markets', icon: 'fas fa-chart-line' },
                politics: { title: 'Politics & Policy', icon: 'fas fa-landmark' }
            };

            container.innerHTML = Object.entries(categories).map(([key, articles]) => {
                const config = categoryConfig[key];
                return `
                    <div class="category-card">
                        <div class="category-header">
                            <div class="category-title-group">
                                <div class="category-icon ${key}">
                                    <i class="${config.icon}"></i>
                                </div>
                                <h3 class="category-title">${config.title}</h3>
                            </div>
                            <span class="category-count">${articles.length} articles</span>
                        </div>
                        <div class="category-articles">
                            ${articles.slice(0, 3).map((article, index) => `
                                <div class="article-item" onclick="openArticle('${article.url}')">
                                    <div class="priority-dot ${article.priority}"></div>
                                    <div class="article-content">
                                        <h4 class="article-title">${article.title}</h4>
                                        <div class="article-meta">
                                            <span>${article.source}</span>
                                            <span>•</span>
                                            <span>${article.readingTime} min read</span>
                                            <span>•</span>
                                            <span>${article.publishedTime}</span>
                                        </div>
                                    </div>
                                </div>
                            `).join('')}
                        </div>
                        <button class="view-all-btn" onclick="switchView('${key}')">
                            View All ${config.title} <i class="fas fa-arrow-right"></i>
                        </button>
                    </div>
                `;
            }).join('');
        }

        function displayCategoryData(category, articles) {
            const container = document.getElementById('categoriesGrid');
            const categoryConfig = {
                ai: { title: 'AI & Technology', icon: 'fas fa-robot' },
                finance: { title: 'Finance & Markets', icon: 'fas fa-chart-line' },
                politics: { title: 'Politics & Policy', icon: 'fas fa-landmark' }
            };
            
            const config = categoryConfig[category];
            
            container.innerHTML = `
                <div style="grid-column: 1 / -1;">
                    <div class="category-card" style="max-width: none;">
                        <div class="category-header">
                            <div class="category-title-group">
                                <div class="category-icon ${category}">
                                    <i class="${config.icon}"></i>
                                </div>
                                <h3 class="category-title">${config.title}</h3>
                            </div>
                            <span class="category-count">${articles.length} articles</span>
                        </div>
                        <div class="category-articles" style="max-height: 500px; overflow-y: auto;">
                            ${articles.map(article => `
                                <div class="article-item" onclick="openArticle('${article.url}')">
                                    <div class="priority-dot ${article.priority}"></div>
                                    <div class="article-content">
                                        <h4 class="article-title">${article.title}</h4>
                                        ${article.aiSummary ? `<p class="alert-summary">${article.aiSummary}</p>` : ''}
                                        <div class="article-meta">
                                            <span>${article.source}</span>
                                            <span>•</span>
                                            <span>${article.readingTime} min read</span>
                                            <span>•</span>
                                            <span>${article.publishedTime}</span>
                                        </div>
                                    </div>
                                </div>
                            `).join('')}
                        </div>
                        <button class="view-all-btn" onclick="switchView('dashboard')">
                            <i class="fas fa-arrow-left"></i> Back to Dashboard
                        </button>
                    </div>
                </div>
            `;
        }

        async function triggerCollection() {
            const btn = document.getElementById('collectBtn');
            const icon = document.getElementById('collectIcon');
            
            btn.disabled = true;
            icon.style.animation = 'spin 1s linear infinite';
            btn.innerHTML = '<i class="fas fa-sync-alt" style="animation: spin 1s linear infinite;"></i> Collecting...';

            try {
                const response = await fetch('/api/news/collect', { method: 'POST' });
                const result = await response.json();
                
                if (result.success) {
                    // Show success feedback
                    btn.innerHTML = '<i class="fas fa-check"></i> Collection Started';
                    
                    // Reload data after a delay
                    setTimeout(() => {
                        loadDashboardData();
                        btn.innerHTML = '<i class="fas fa-sync-alt"></i> Collect Latest';
                        btn.disabled = false;
                    }, 3000);
                } else {
                    throw new Error('Collection failed');
                }
            } catch (error) {
                console.error('Collection error:', error);
                btn.innerHTML = '<i class="fas fa-exclamation-triangle"></i> Failed';
                setTimeout(() => {
                    btn.innerHTML = '<i class="fas fa-sync-alt"></i> Collect Latest';
                    btn.disabled = false;
                }, 3000);
            }
        }

        function handleSearch(event) {
            const query = event.target.value;
            if (query.length > 2) {
                // Implement search functionality
                console.log('Searching for:', query);
                // TODO: Add search API call
            }
        }

        function openArticle(url) {
            window.open(url, '_blank', 'noopener,noreferrer');
        }

        function markAsRead(articleId) {
            // TODO: Implement mark as read
            console.log('Mark as read:', articleId);
        }

        function starArticle(articleId) {
            // TODO: Implement star article
            console.log('Star article:', articleId);
        }

        function getCategoryIcon(category) {
            const icons = {
                ai: 'fa-robot',
                finance: 'fa-chart-line',
                politics: 'fa-landmark'
            };
            return icons[category] || 'fa-newspaper';
        }

        function getCategoryLabel(category) {
            const labels = {
                ai: 'AI Technology',
                finance: 'Finance',
                politics: 'Politics'
            };
            return labels[category] || 'News';
        }

        function showLoading() {
            // Show loading states for different sections
            document.getElementById('priorityAlerts').innerHTML = `
                <div class="loading">
                    <div class="loading-spinner"></div>
                    Loading priority alerts...
                </div>
            `;
            
            document.getElementById('categoriesGrid').innerHTML = `
                <div class="loading">
                    <div class="loading-spinner"></div>
                    Loading categories...
                </div>
            `;
        }

        function showError(message) {
            const errorHtml = `
                <div class="empty-state">
                    <i class="fas fa-exclamation-triangle" style="color: var(--rp-error);"></i>
                    <h3>Error</h3>
                    <p>${message}</p>
                    <button class="collect-btn" onclick="loadDashboardData()" style="margin-top: 1rem; width: auto; padding: 0.5rem 1rem;">
                        Retry
                    </button>
                </div>
            `;
            
            document.getElementById('priorityAlerts').innerHTML = errorHtml;
            document.getElementById('categoriesGrid').innerHTML = errorHtml;
        }

        // Auto-refresh every 5 minutes
        setInterval(() => {
            if (currentView === 'dashboard') {
                loadDashboardData();
            }
        }, 5 * 60 * 1000);
    </script>
</body>
</html>"""
    return html_contentif __name__ == "__main__":
    logger.info("🚀 Starting Enhanced RPNews Platform")
    logger.info(f"🌐 Port: {PORT}")
    logger.info(f"🤖 AI Engine: {news_engine.ai.ai_type}")
    logger.info(f"🎯"""
RPNews - Enhanced AI-Powered News Intelligence Platform
Features: Proper AI summaries, better priority detection, article management
Deploy to Railway, Render, or Fly.io for free hosting
"""

import asyncio
import aiohttp
import feedparser
import json
import logging
import sqlite3
import hashlib
import os
import re
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import time
from bs4 import BeautifulSoup
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import uvicorn

# Cloud deployment configuration
PORT = int(os.environ.get("PORT", 8000))
DATABASE_URL = os.environ.get("DATABASE_URL", "rpnews.db")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class NewsArticle:
    id: str
    title: str
    url: str
    source: str
    author: Optional[str]
    published_date: datetime
    content: str
    excerpt: str
    ai_summary: Optional[str]
    category: str
    priority: str
    tags: List[str]
    reading_time: int
    extracted_at: datetime

class RPNewsAI:
    """Advanced AI news analysis with proper summarization"""
    
    def __init__(self):
        self.ai_type = "enhanced_rules"
        self.ai_available = False
        logger.info("🤖 Initializing AI analysis system...")
        
        # Try to load actual AI model, fallback to enhanced rules
        try:
            # Only try to import if transformers is available
            import transformers
            from transformers import pipeline
            
            logger.info("📦 Transformers library found, attempting to load BART model...")
            self.summarizer = pipeline(
                "summarization", 
                model="facebook/bart-large-cnn",
                device=-1,  # CPU only for deployment
                max_length=1024  # Limit model size
            )
            self.ai_available = True
            self.ai_type = "transformer_based"
            logger.info("✅ BART summarization model loaded successfully")
            
        except ImportError:
            logger.info("📝 Transformers not available, using enhanced rule-based analysis")
            self.summarizer = None
            
        except Exception as e:
            logger.warning(f"⚠️ Could not load transformer model: {e}")
            logger.info("📝 Falling back to enhanced rule-based analysis")
            self.summarizer = None
    
    def generate_summary(self, title: str, content: str, category: str) -> str:
        """Generate intelligent summary using AI or enhanced rules"""
        if self.ai_available and self.summarizer and len(content) > 100:
            return self._ai_summary(title, content, category)
        else:
            return self._smart_rule_summary(title, content, category)
    
    def _ai_summary(self, title: str, content: str, category: str) -> str:
        """Generate AI-powered summary using BART model"""
        try:
            # Clean and prepare text
            clean_content = self._clean_text(content)
            
            # Truncate to model limits (1024 tokens ≈ 800 words)
            words = clean_content.split()
            if len(words) > 800:
                clean_content = " ".join(words[:800])
            
            # Generate summary with appropriate length
            summary_result = self.summarizer(
                clean_content,
                max_length=150,
                min_length=50,
                do_sample=False,
                truncation=True
            )
            
            ai_text = summary_result[0]['summary_text']
            
            # Category-specific formatting
            category_config = {
                "ai": "🤖 AI Development",
                "finance": "💰 Market Update", 
                "politics": "🏛️ Policy Update"
            }
            
            prefix = category_config.get(category, "📰 News Update")
            
            return f"{prefix}: {ai_text}"
            
        except Exception as e:
            logger.warning(f"AI summary failed: {e}")
            return self._smart_rule_summary(title, content, category)
    
    def _clean_text(self, text: str) -> str:
        """Clean text for AI processing"""
        # Remove HTML remnants
        text = re.sub(r'<[^>]+>', '', text)
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters that might confuse the model
        text = re.sub(r'[^\w\s\.\,\!\?\-\:\;]', '', text)
        return text.strip()
    
    def _smart_rule_summary(self, title: str, content: str, category: str) -> str:
        """Enhanced rule-based summary with intelligent parsing"""
        
        # Extract key sentences using importance indicators
        sentences = content.replace('\n', ' ').split('.')
        important_sentences = []
        
        # Enhanced key phrases by category
        key_indicators = {
            'ai': ['announces', 'launches', 'breakthrough', 'develops', 'ai', 'model', 'algorithm', 'machine learning', 'neural', 'artificial intelligence'],
            'finance': ['reports', 'earnings', 'revenue', 'profit', 'investment', 'funding', 'market', 'stock', 'financial', 'economic', 'fed', 'rate'],
            'politics': ['policy', 'legislation', 'congress', 'senate', 'president', 'governor', 'election', 'vote', 'political', 'government']
        }
        
        category_indicators = key_indicators.get(category, [
            'announces', 'launches', 'reports', 'reveals', 'shows', 'increases', 'decreases',
            'plans', 'expects', 'breakthrough', 'develops', 'creates', 'discovers'
        ])
        
        for sentence in sentences[:10]:  # Check first 10 sentences
            sentence = sentence.strip()
            if len(sentence) > 30:
                # Score sentence based on keywords and position
                score = 0
                sentence_lower = sentence.lower()
                
                for indicator in category_indicators:
                    if indicator in sentence_lower:
                        score += 2
                
                # Boost for numbers, percentages, quotes
                if re.search(r'\d+%|\$\d+|"\w+', sentence):
                    score += 1
                
                if score >= 2:
                    important_sentences.append(sentence)
        
        # Fallback to first meaningful sentences
        if not important_sentences:
            important_sentences = [s.strip() for s in sentences[:3] if len(s.strip()) > 20]
        
        # Create summary from top 2 sentences
        key_info = '. '.join(important_sentences[:2])
        
        # Category-specific formatting
        category_config = {
            "ai": "🤖 AI Development",
            "finance": "💰 Market Update",
            "politics": "🏛️ Policy Update"
        }
        
        prefix = category_config.get(category, "📰 News Update")
        
        return f"{prefix}: {key_info}."
    
    def generate_daily_overview(self, articles_by_category: Dict[str, List]) -> str:
        """Generate comprehensive daily overview using AI or enhanced rules"""
        if self.ai_available and self.summarizer:
            return self._ai_daily_overview(articles_by_category)
        else:
            return self._rule_daily_overview(articles_by_category)
    
    def _ai_daily_overview(self, articles_by_category: Dict[str, List]) -> str:
        """AI-powered daily overview generation"""
        try:
            # Collect key summaries from each category
            overview_text = "Today's key developments:\n\n"
            
            for category, articles in articles_by_category.items():
                if not articles:
                    continue
                    
                # Get top 3 high-priority articles
                top_articles = [a for a in articles if a.get('priority') == 'high'][:3]
                if not top_articles:
                    top_articles = articles[:3]
                
                summaries = [a.get('aiSummary', a.get('title', '')) for a in top_articles]
                category_text = " ".join(summaries)
                
                if category_text:
                    overview_text += f"{category.upper()}: {category_text}\n\n"
            
            # Generate AI overview
            if len(overview_text) > 100:
                summary_result = self.summarizer(
                    overview_text,
                    max_length=200,
                    min_length=80,
                    do_sample=False,
                    truncation=True
                )
                return summary_result[0]['summary_text']
            
        except Exception as e:
            logger.warning(f"AI daily overview failed: {e}")
        
        return self._rule_daily_overview(articles_by_category)
    
    def _rule_daily_overview(self, articles_by_category: Dict[str, List]) -> str:
        """Rule-based daily overview generation"""
        overview_parts = []
        
        category_summaries = {
            'ai': "📱 Technology developments",
            'finance': "💰 Market movements", 
            'politics': "🏛️ Policy updates"
        }
        
        for category, articles in articles_by_category.items():
            if not articles:
                continue
                
            high_priority_count = len([a for a in articles if a.get('priority') == 'high'])
            total_count = len(articles)
            
            category_name = category_summaries.get(category, f"{category} updates")
            
            if high_priority_count > 0:
                overview_parts.append(f"{category_name}: {high_priority_count} major developments, {total_count} total articles")
            else:
                overview_parts.append(f"{category_name}: {total_count} articles to review")
        
        if not overview_parts:
            return "📰 Your daily briefing is being prepared. Check back in a few minutes for the latest updates."
        
        overview = "🌅 Today's Intelligence Overview: " + "; ".join(overview_parts)
        overview += f". Total articles for review: {sum(len(articles) for articles in articles_by_category.values())}."
        
        return overview

class RPNewsEngine:
    """Enhanced news intelligence engine"""
    
    def __init__(self, db_path: str = "rpnews.db"):
        self.db_path = db_path
        self.ai = RPNewsAI()
        self.session = None
        self.sources = self._initialize_sources()
        self._setup_database()
        self.background_task = None
        logger.info("📰 Enhanced RPNews Engine initialized")
    
    def start_background_collection(self):
        """Start background collection task"""
        if self.background_task is None:
            self.background_task = asyncio.create_task(self.background_collection())
            logger.info("🔄 Background collection task started")
    
    def _initialize_sources(self) -> Dict[str, List[Dict]]:
        """Complete source list - 60+ premium sources"""
        return {
            "ai": [
                # TOP TIER - Most Important AI Sources
                {"name": "The Batch (Andrew Ng)", "rss": "https://www.deeplearning.ai/feed/", "priority": "high"},
                {"name": "OpenAI Blog", "rss": "https://openai.com/blog/rss.xml", "priority": "high"},
                {"name": "Anthropic Blog", "rss": "https://www.anthropic.com/news/feed", "priority": "high"},
                {"name": "Google AI Blog", "rss": "https://ai.googleblog.com/feeds/posts/default", "priority": "high"},
                {"name": "DeepMind Blog", "rss": "https://deepmind.com/blog/feed/basic/", "priority": "high"},
                
                # Research Papers
                {"name": "ArXiv AI Papers", "rss": "http://export.arxiv.org/rss/cs.AI", "priority": "high"},
                {"name": "ArXiv ML Papers", "rss": "http://export.arxiv.org/rss/cs.LG", "priority": "high"},
                {"name": "ArXiv Computer Vision", "rss": "http://export.arxiv.org/rss/cs.CV", "priority": "medium"},
                {"name": "ArXiv NLP Papers", "rss": "http://export.arxiv.org/rss/cs.CL", "priority": "medium"},
                
                # Industry News
                {"name": "MIT Technology Review", "rss": "https://www.technologyreview.com/feed/", "priority": "high"},
                {"name": "TechCrunch AI", "rss": "https://techcrunch.com/category/artificial-intelligence/feed/", "priority": "high"},
                {"name": "VentureBeat AI", "rss": "https://venturebeat.com/ai/feed/", "priority": "high"},
                {"name": "The Verge AI", "rss": "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml", "priority": "medium"},
                {"name": "Wired AI", "rss": "https://www.wired.com/feed/tag/ai/latest/rss", "priority": "medium"},
                
                # Specialized AI Publications
                {"name": "AI News", "rss": "https://www.artificialintelligence-news.com/feed/", "priority": "medium"},
                {"name": "Towards Data Science", "rss": "https://towardsdatascience.com/feed", "priority": "medium"},
                {"name": "Machine Learning Mastery", "rss": "https://machinelearningmastery.com/feed/", "priority": "medium"},
                
                # VC & Investment in AI
                {"name": "Andreessen Horowitz", "rss": "https://a16z.com/feed/", "priority": "medium"},
                {"name": "Sequoia Capital", "rss": "https://www.sequoiacap.com/feed/", "priority": "medium"},
                {"name": "First Round Review", "rss": "https://review.firstround.com/feed", "priority": "medium"},
                
                # Meta AI & Others
                {"name": "Meta AI Blog", "rss": "https://ai.facebook.com/blog/feed/", "priority": "medium"}
            ],
            
            "finance": [
                # Major Financial News
                {"name": "Bloomberg Markets", "rss": "https://feeds.bloomberg.com/markets/news.rss", "priority": "high"},
                {"name": "Reuters Business", "rss": "https://feeds.reuters.com/reuters/businessNews", "priority": "high"},
                {"name": "MarketWatch", "rss": "https://feeds.marketwatch.com/marketwatch/topstories/", "priority": "high"},
                {"name": "CNBC Markets", "rss": "https://www.cnbc.com/id/100003114/device/rss/rss.html", "priority": "high"},
                {"name": "Financial Times", "rss": "https://www.ft.com/rss", "priority": "high"},
                {"name": "Wall Street Journal", "rss": "https://feeds.a.dj.com/rss/RSSMarketsMain.xml", "priority": "high"},
                
                # Central Banks & Policy
                {"name": "Federal Reserve", "rss": "https://www.federalreserve.gov/feeds/press_all.xml", "priority": "high"},
                {"name": "The Economist Finance", "rss": "https://www.economist.com/finance-and-economics/rss.xml", "priority": "high"},
                {"name": "Bank of England", "rss": "https://www.bankofengland.co.uk/feeds/news.rss", "priority": "medium"},
                {"name": "European Central Bank", "rss": "https://www.ecb.europa.eu/rss/news.xml", "priority": "medium"},
                
                # Investment & Analysis
                {"name": "Seeking Alpha", "rss": "https://seekingalpha.com/feed.xml", "priority": "medium"},
                {"name": "Morningstar", "rss": "https://www.morningstar.com/rss", "priority": "medium"},
                {"name": "Barron's", "rss": "https://feeds.a.dj.com/rss/RSSLifestyle.xml", "priority": "medium"},
                
                # Cryptocurrency & Fintech
                {"name": "CoinDesk", "rss": "https://feeds.coindesk.com/coindesk-news", "priority": "medium"},
                {"name": "The Block Crypto", "rss": "https://www.theblockcrypto.com/rss.xml", "priority": "medium"},
                {"name": "Fintech News", "rss": "https://fintechnews.org/feed/", "priority": "medium"},
                
                # International Markets
                {"name": "Nikkei Asia Markets", "rss": "https://asia.nikkei.com/rss/feed/Markets", "priority": "medium"}
            ],
            
            "politics": [
                # US Politics - Core
                {"name": "Politico", "rss": "https://www.politico.com/rss/politicopicks.xml", "priority": "high"},
                {"name": "The Hill", "rss": "https://thehill.com/feed/", "priority": "high"},
                {"name": "Washington Post Politics", "rss": "https://feeds.washingtonpost.com/rss/politics", "priority": "high"},
                {"name": "New York Times Politics", "rss": "https://rss.nytimes.com/services/xml/rss/nyt/Politics.xml", "priority": "high"},
                {"name": "CNN Politics", "rss": "http://rss.cnn.com/rss/cnn_allpolitics.rss", "priority": "high"},
                
                # Congressional & Federal
                {"name": "Roll Call", "rss": "https://www.rollcall.com/feed/", "priority": "medium"},
                {"name": "Federal News Network", "rss": "https://federalnewsnetwork.com/feed/", "priority": "medium"},
                
                # International Politics
                {"name": "BBC Politics", "rss": "http://feeds.bbci.co.uk/news/politics/rss.xml", "priority": "high"},
                {"name": "Reuters Politics", "rss": "https://feeds.reuters.com/reuters/politicsNews", "priority": "high"},
                {"name": "Associated Press Politics", "rss": "https://apnews.com/Politics", "priority": "high"},
                
                # European & International
                {"name": "Euronews Politics", "rss": "https://www.euronews.com/rss?format=mrss&level=topic&name=politics", "priority": "medium"},
                {"name": "The Guardian Politics", "rss": "https://www.theguardian.com/politics/rss", "priority": "medium"},
                
                # Analysis & Foreign Policy
                {"name": "Foreign Affairs", "rss": "https://www.foreignaffairs.com/rss.xml", "priority": "medium"},
                {"name": "Foreign Policy", "rss": "https://foreignpolicy.com/feed/", "priority": "medium"},
                {"name": "Atlantic Politics", "rss": "https://www.theatlantic.com/feed/channel/politics/", "priority": "medium"},
                
                # Think Tanks
                {"name": "Brookings Institution", "rss": "https://www.brookings.edu/feed/", "priority": "low"},
                {"name": "American Enterprise Institute", "rss": "https://www.aei.org/feed/", "priority": "low"}
            ]
        }
    
    def _setup_database(self):
        """Setup enhanced SQLite database"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS articles (
                    id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    url TEXT UNIQUE NOT NULL,
                    source TEXT NOT NULL,
                    author TEXT,
                    published_date TIMESTAMP,
                    content TEXT,
                    excerpt TEXT,
                    ai_summary TEXT,
                    category TEXT,
                    priority TEXT,
                    tags TEXT,
                    reading_time INTEGER DEFAULT 0,
                    extracted_at TIMESTAMP,
                    is_read BOOLEAN DEFAULT FALSE,
                    is_starred BOOLEAN DEFAULT FALSE,
                    read_at TIMESTAMP,
                    starred_at TIMESTAMP
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS collection_stats (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    category TEXT,
                    articles_collected INTEGER,
                    last_run TIMESTAMP,
                    status TEXT
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS daily_overviews (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT UNIQUE,
                    overview_text TEXT,
                    total_articles INTEGER,
                    high_priority_count INTEGER,
                    generated_at TIMESTAMP
                )
            """)
            
            # Performance indexes
            conn.execute("CREATE INDEX IF NOT EXISTS idx_category ON articles(category)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_published ON articles(published_date)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_priority ON articles(priority)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_read_starred ON articles(is_read, is_starred)")
    
    def _calculate_priority(self, title: str, content: str, source_priority: str, category: str) -> str:
        """Enhanced priority detection based on content analysis"""
        priority_score = 0
        text = f"{title} {content}".lower()
        
        # Base score from source priority
        priority_base = {"high": 3, "medium": 2, "low": 1}
        priority_score = priority_base.get(source_priority, 2)
        
        # Category-specific high-priority indicators
        high_priority_terms = {
            'ai': [
                'breakthrough', 'released', 'announces', 'launches', 'gpt-', 'claude',
                'funding round', 'acquisition', 'partnership', 'regulation', 'banned',
                'agi', 'superintelligence', '$', 'billion', 'million funding'
            ],
            'finance': [
                'fed decision', 'interest rate', 'inflation', 'recession', 'crash',
                'bank failure', 'earnings beat', 'guidance', 'outlook', 'upgraded',
                'downgraded', 'merger', 'acquisition', 'ipo', 'bankruptcy'
            ],
            'politics': [
                'breaking', 'urgent', 'senate votes', 'house passes', 'president',
                'supreme court', 'indictment', 'investigation', 'scandal',
                'election results', 'poll', 'debate', 'resignation', 'appointed'
            ]
        }
        
        category_terms = high_priority_terms.get(category, [])
        
        # Count high-priority term matches
        term_matches = sum(1 for term in category_terms if term in text)
        priority_score += min(term_matches * 0.5, 2)  # Max 2 bonus points
        
        # Boost for numbers/percentages (usually important data)
        if re.search(r'\d+%|\$\d+\.?\d*[bmk]|\d+\.\d+%', text):
            priority_score += 0.5
        
        # Boost for urgency words
        urgency_terms = ['breaking', 'urgent', 'just in', 'developing', 'alert']
        if any(term in text for term in urgency_terms):
            priority_score += 1
        
        # Determine final priority
        if priority_score >= 4:
            return "high"
        elif priority_score >= 2.5:
            return "medium"
        else:
            return "low"
    
    def _calculate_reading_time(self, content: str) -> int:
        """Calculate estimated reading time in minutes"""
        words = len(content.split())
        # Average reading speed: 200 words per minute
        minutes = max(1, round(words / 200))
        return min(minutes, 15)  # Cap at 15 minutes
    
    async def background_collection(self):
        """Enhanced background collection with faster startup for React frontend"""
        logger.info("🚀 Starting rapid initial news collection for React frontend...")
        
        # Quick initial collection on startup
        try:
            async with aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=30),
                headers={'User-Agent': 'RPNews Enhanced/2.0'}
            ) as session:
                self.session = session
                
                # Quick collection from top sources only for initial load
                await self._quick_initial_collection()
                
                # Then do full collection
                await self.collect_all_news()
                self.session = None
            logger.info("✅ Initial collection completed - React frontend ready")
        except Exception as e:
            logger.error(f"Initial collection error: {e}")
        
        # Continue with regular collection cycle
        while True:
            try:
                await asyncio.sleep(1800)  # Wait 30 minutes (more frequent)
                
                logger.info("🔄 Background collection starting...")
                async with aiohttp.ClientSession(
                    timeout=aiohttp.ClientTimeout(total=30),
                    headers={'User-Agent': 'RPNews Enhanced/2.0'}
                ) as session:
                    self.session = session
                    await self.collect_all_news()
                    self.session = None
                
                logger.info("✅ Background collection complete. Next run in 30 minutes.")
                
            except Exception as e:
                logger.error(f"Background collection error: {str(e)}")
                await asyncio.sleep(300)  # Wait 5 minutes on error
    
    async def _quick_initial_collection(self):
        """Quick collection from top priority sources for immediate React frontend loading"""
        logger.info("🚀 Quick initial collection starting...")
        
        # Only collect from high-priority sources initially
        priority_sources = {
            'ai': [s for s in self.sources['ai'] if s['priority'] == 'high'][:3],
            'finance': [s for s in self.sources['finance'] if s['priority'] == 'high'][:3],
            'politics': [s for s in self.sources['politics'] if s['priority'] == 'high'][:3]
        }
        
        total_articles = 0
        for category, sources in priority_sources.items():
            for source in sources:
                try:
                    articles = await self.fetch_rss_feed(source, category)
                    for article in articles[:3]:  # Limit to 3 articles per source
                        self.save_article(article)
                        total_articles += 1
                    
                    await asyncio.sleep(1)  # Shorter delay for initial collection
                    
                except Exception as e:
                    logger.warning(f"Quick collection error with {source['name']}: {str(e)}")
                    continue
        
        # Generate initial overview
        await self._generate_daily_overview()
        logger.info(f"🚀 Quick collection complete: {total_articles} priority articles")
        return total_articles
    
    async def collect_all_news(self):
        """Enhanced news collection with better processing"""
        total_articles = 0
        
        for category in ['ai', 'finance', 'politics']:
            try:
                count = await self.collect_category(category)
                total_articles += count
                
                # Update stats
                with sqlite3.connect(self.db_path) as conn:
                    conn.execute("""
                        INSERT INTO collection_stats 
                        (category, articles_collected, last_run, status)
                        VALUES (?, ?, ?, ?)
                    """, (category, count, datetime.now(), 'success'))
                
            except Exception as e:
                logger.error(f"Error collecting {category}: {str(e)}")
        
        # Generate daily overview after collection
        await self._generate_daily_overview()
        
        logger.info(f"✅ Total articles collected: {total_articles}")
        return total_articles
    
    async def _generate_daily_overview(self):
        """Generate and store daily overview"""
        today = datetime.now().strftime('%Y-%m-%d')
        
        try:
            # Get today's articles by category
            articles_by_category = {}
            
            with sqlite3.connect(self.db_path) as conn:
                for category in ['ai', 'finance', 'politics']:
                    cursor = conn.execute("""
                        SELECT title, ai_summary, priority FROM articles 
                        WHERE category = ? AND date(published_date) = date('now')
                        ORDER BY 
                            CASE priority 
                                WHEN 'high' THEN 3 
                                WHEN 'medium' THEN 2 
                                ELSE 1 
                            END DESC
                        LIMIT 10
                    """, (category,))
                    
                    articles = []
                    for row in cursor.fetchall():
                        articles.append({
                            'title': row[0],
                            'aiSummary': row[1],
                            'priority': row[2]
                        })
                    
                    articles_by_category[category] = articles
                
                # Generate overview
                overview_text = self.ai.generate_daily_overview(articles_by_category)
                
                total_articles = sum(len(articles) for articles in articles_by_category.values())
                high_priority_count = sum(
                    len([a for a in articles if a.get('priority') == 'high']) 
                    for articles in articles_by_category.values()
                )
                
                # Store overview
                conn.execute("""
                    INSERT OR REPLACE INTO daily_overviews 
                    (date, overview_text, total_articles, high_priority_count, generated_at)
                    VALUES (?, ?, ?, ?, ?)
                """, (today, overview_text, total_articles, high_priority_count, datetime.now()))
                
                logger.info(f"📊 Daily overview generated: {total_articles} articles, {high_priority_count} high priority")
                
        except Exception as e:
            logger.error(f"Error generating daily overview: {e}")
    
    async def collect_category(self, category: str) -> int:
        """Enhanced category collection with better AI processing"""
        sources = self.sources.get(category, [])
        total_articles = 0
        
        for source in sources:
            try:
                articles = await self.fetch_rss_feed(source, category)
                for article in articles:
                    self.save_article(article)
                    total_articles += 1
                
                # Rate limiting - be respectful
                await asyncio.sleep(2)
                
            except Exception as e:
                logger.warning(f"Error with {source['name']}: {str(e)}")
                continue
        
        logger.info(f"Collected {total_articles} {category} articles")
        return total_articles
    
    async def fetch_rss_feed(self, source: Dict[str, str], category: str) -> List[NewsArticle]:
        """Enhanced RSS feed processing with better content extraction"""
        articles = []
        
        try:
            async with self.session.get(source['rss']) as response:
                if response.status != 200:
                    return articles
                
                content = await response.text()
                feed = feedparser.parse(content)
                
                for entry in feed.entries[:15]:  # Increased limit per source
                    try:
                        article_id = hashlib.md5(entry.link.encode()).hexdigest()
                        
                        # Skip if already exists
                        if self._article_exists(article_id):
                            continue
                        
                        # Parse published date
                        published_date = datetime.now()
                        if hasattr(entry, 'published_parsed') and entry.published_parsed:
                            published_date = datetime(*entry.published_parsed[:6])
                        
                        # Extract and clean content
                        content = getattr(entry, 'summary', '')
                        if hasattr(entry, 'content'):
                            content = entry.content[0].value if entry.content else content
                        
                        if content:
                            soup = BeautifulSoup(content, 'html.parser')
                            content = soup.get_text().strip()
                        
                        # Enhanced priority detection
                        priority = self._calculate_priority(entry.title, content, source['priority'], category)
                        
                        # Calculate reading time
                        reading_time = self._calculate_reading_time(content)
                        
                        # Generate excerpt and AI summary
                        excerpt = content[:400] + "..." if len(content) > 400 else content
                        ai_summary = self.ai.generate_summary(entry.title, content[:2000], category)
                        
                        # Extract tags
                        tags = self._extract_tags(entry.title, content, category)
                        
                        article = NewsArticle(
                            id=article_id,
                            title=entry.title.strip(),
                            url=entry.link,
                            source=source['name'],
                            author=getattr(entry, 'author', None),
                            published_date=published_date,
                            content=content,
                            excerpt=excerpt,
                            ai_summary=ai_summary,
                            category=category,
                            priority=priority,
                            tags=tags,
                            reading_time=reading_time,
                            extracted_at=datetime.now()
                        )
                        
                        articles.append(article)
                        
                    except Exception as e:
                        continue
                        
        except Exception as e:
            logger.error(f"Error fetching {source['name']}: {str(e)}")
        
        return articles
    
    def _article_exists(self, article_id: str) -> bool:
        """Check if article already exists"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT 1 FROM articles WHERE id = ?", (article_id,))
            return cursor.fetchone() is not None
    
    def _extract_tags(self, title: str, content: str, category: str) -> List[str]:
        """Enhanced tag extraction with better categorization"""
        text = f"{title} {content}".lower()
        tags = []
        
        # Category-specific tag extraction
        if category == "ai":
            ai_terms = {
                'gpt': ['gpt', 'chatgpt', 'gpt-4', 'gpt-3'],
                'llm': ['language model', 'llm', 'large language'],
                'ml': ['machine learning', 'deep learning', 'neural network'],
                'startup': ['startup', 'funding', 'investment', 'series a', 'series b'],
                'research': ['paper', 'research', 'arxiv', 'study', 'journal'],
                'robotics': ['robot', 'robotics', 'autonomous'],
                'computer_vision': ['computer vision', 'image recognition', 'cv'],
                'nlp': ['natural language', 'nlp', 'text processing'],
                'ethics': ['ethics', 'bias', 'fairness', 'responsible ai']
            }
        elif category == "finance":
            ai_terms = {
                'crypto': ['bitcoin', 'cryptocurrency', 'crypto', 'ethereum'],
                'stocks': ['stock', 'equity', 'shares', 'nasdaq', 'sp500'],
                'fed': ['federal reserve', 'fed', 'interest rate', 'fomc'],
                'market': ['market', 'trading', 'dow jones'],
                'banking': ['bank', 'banking', 'credit', 'loan'],
                'inflation': ['inflation', 'cpi', 'consumer price'],
                'earnings': ['earnings', 'revenue', 'profit', 'quarterly'],
                'ipo': ['ipo', 'public offering', 'listing'],
                'merger': ['merger', 'acquisition', 'm&a']
            }
        else:  # politics
            ai_terms = {
                'congress': ['congress', 'senate', 'house', 'representatives'],
                'election': ['election', 'vote', 'campaign', 'ballot'],
                'policy': ['policy', 'legislation', 'bill', 'law'],
                'international': ['international', 'foreign', 'diplomatic'],
                'supreme_court': ['supreme court', 'scotus', 'judicial'],
                'presidency': ['president', 'white house', 'administration'],
                'healthcare': ['healthcare', 'medicare', 'medicaid'],
                'economy': ['economic', 'fiscal', 'budget'],
                'climate': ['climate', 'environmental', 'green energy']
            }
            
        for tag, keywords in ai_terms.items():
            if any(keyword in text for keyword in keywords):
                tags.append(tag)
        
        return tags[:8]  # Limit to 8 tags
    
    def save_article(self, article: NewsArticle):
        """Enhanced article saving with new fields"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT OR REPLACE INTO articles 
                (id, title, url, source, author, published_date, content, excerpt,
                 ai_summary, category, priority, tags, reading_time, extracted_at,
                 is_read, is_starred)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, FALSE, FALSE)
            """, (
                article.id, article.title, article.url, article.source, article.author,
                article.published_date, article.content, article.excerpt, article.ai_summary,
                article.category, article.priority, json.dumps(article.tags), 
                article.reading_time, article.extracted_at
            ))
    
    def mark_article_read(self, article_id: str) -> bool:
        """Mark article as read"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    UPDATE articles 
                    SET is_read = TRUE, read_at = ? 
                    WHERE id = ?
                """, (datetime.now(), article_id))
                return True
        except Exception as e:
            logger.error(f"Error marking article read: {e}")
            return False
    
    def star_article(self, article_id: str, starred: bool = True) -> bool:
        """Star or unstar an article"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                starred_at = datetime.now() if starred else None
                conn.execute("""
                    UPDATE articles 
                    SET is_starred = ?, starred_at = ? 
                    WHERE id = ?
                """, (starred, starred_at, article_id))
                return True
        except Exception as e:
            logger.error(f"Error starring article: {e}")
            return False

# Initialize FastAPI application with static files support
app = FastAPI(title="RPNews - Enhanced AI News Intelligence", version="2.0.0")

# Enhanced CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve React static files (for production builds)
try:
    from fastapi.staticfiles import StaticFiles
    import os
    
    # Check if we have a React build directory
    if os.path.exists("dist"):
        app.mount("/assets", StaticFiles(directory="dist/assets"), name="assets")
        
        @app.get("/")
        async def serve_react_app():
            """Serve React app for production"""
            with open("dist/index.html", "r") as f:
                return HTMLResponse(content=f.read())
        
        @app.get("/{full_path:path}")
        async def catch_all(full_path: str):
            """Catch-all route for React Router"""
            # Serve API routes normally
            if full_path.startswith("api/"):
                raise HTTPException(status_code=404, detail="API endpoint not found")
            
            # Serve React app for all other routes
            with open("dist/index.html", "r") as f:
                return HTMLResponse(content=f.read())
                
    else:
        # Development mode - serve the enhanced dashboard
        @app.get("/", response_class=HTMLResponse)
        async def dashboard():
            """Enhanced development dashboard"""
            return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>RPNews Enhanced - Development Mode</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui; margin: 0; background: #f8fafc; }
        .container { max-width: 1200px; margin: 0 auto; padding: 2rem; }
        .header { background: white; padding: 2rem; border-radius: 12px; margin-bottom: 2rem; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
        .card { background: white; padding: 1.5rem; border-radius: 8px; margin-bottom: 1rem; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
        .button { background: #3b82f6; color: white; padding: 0.75rem 1.5rem; border: none; border-radius: 6px; cursor: pointer; font-weight: 500; }
        .button:hover { background: #2563eb; }
        .status { padding: 0.5rem 1rem; border-radius: 6px; margin: 0.5rem 0; }
        .success { background: #dcfce7; color: #166534; }
        .warning { background: #fef3c7; color: #92400e; }
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1rem; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 RPNews Enhanced - Development Mode</h1>
            <p>Your AI-powered news intelligence platform is running!</p>
            <div id="status" class="status warning">⏳ Initializing system...</div>
        </div>
        
        <div class="grid">
            <div class="card">
                <h3>🤖 AI Analysis</h3>
                <p>Advanced AI summaries and priority detection</p>
                <div id="ai-status">Loading...</div>
            </div>
            
            <div class="card">
                <h3>📰 News Collection</h3>
                <p>60+ premium sources across AI, Finance, Politics</p>
                <button class="button" onclick="collectNews()">Collect Latest News</button>
                <div id="collection-status"></div>
            </div>
            
            <div class="card">
                <h3>📊 Dashboard Data</h3>
                <p>Real-time analytics and insights</p>
                <button class="button" onclick="loadDashboard()">Load Dashboard</button>
                <div id="dashboard-data"></div>
            </div>
        </div>
        
        <div class="card">
            <h3>🔗 API Endpoints</h3>
            <ul>
                <li><a href="/api/news/dashboard">Dashboard Data</a></li>
                <li><a href="/api/health">Health Check</a></li>
                <li><a href="/api/stats">Statistics</a></li>
                <li><a href="/docs">API Documentation</a></li>
            </ul>
        </div>
    </div>
    
    <script>
        async function checkStatus() {
            try {
                const response = await fetch('/api/health');
                const data = await response.json();
                const statusEl = document.getElementById('status');
                const aiStatusEl = document.getElementById('ai-status');
                
                if (data.status === 'healthy') {
                    statusEl.className = 'status success';
                    statusEl.textContent = '✅ System Online - All services running';
                    aiStatusEl.textContent = `AI: ${data.ai_type} (${data.ai_available ? 'Active' : 'Fallback'})`;
                } else {
                    statusEl.className = 'status warning';
                    statusEl.textContent = '⚠️ System Issues Detected';
                }
            } catch (error) {
                document.getElementById('status').textContent = '❌ Unable to connect to backend';
            }
        }
        
        async function collectNews() {
            const button = event.target;
            const statusEl = document.getElementById('collection-status');
            
            button.textContent = 'Collecting...';
            button.disabled = true;
            
            try {
                const response = await fetch('/api/news/collect', { method: 'POST' });
                const data = await response.json();
                statusEl.innerHTML = '<div class="status success">✅ Collection started successfully</div>';
                
                setTimeout(() => {
                    button.textContent = 'Collect Latest News';
                    button.disabled = false;
                }, 3000);
            } catch (error) {
                statusEl.innerHTML = '<div class="status warning">❌ Collection failed</div>';
                button.textContent = 'Collect Latest News';
                button.disabled = false;
            }
        }
        
        async function loadDashboard() {
            const statusEl = document.getElementById('dashboard-data');
            statusEl.textContent = 'Loading...';
            
            try {
                const response = await fetch('/api/news/dashboard');
                const data = await response.json();
                statusEl.innerHTML = `
                    <div class="status success">
                        📊 ${data.stats.totalArticles} articles • 
                        🔥 ${data.stats.highPriority} high priority • 
                        🤖 ${data.stats.aiSummaries} AI summaries
                    </div>
                `;
            } catch (error) {
                statusEl.innerHTML = '<div class="status warning">❌ Failed to load dashboard</div>';
            }
        }
        
        // Auto-check status on load
        checkStatus();
        setInterval(checkStatus, 30000); // Check every 30 seconds
    </script>
</body>
</html>"""

except ImportError:
    # Fallback if StaticFiles not available
    @app.get("/", response_class=HTMLResponse)
    async def dashboard():
        """Development dashboard"""
        return """<!DOCTYPE html>
<html><head><title>RPNews Enhanced</title></head>
<body><h1>RPNews Enhanced API</h1><p>Backend is running. Frontend build not found.</p>
<a href="/docs">View API Documentation</a></body></html>"""

# Initialize the enhanced news engine
news_engine = RPNewsEngine()

@app.on_event("startup")
async def startup_event():
    """Start background tasks when FastAPI starts"""
    logger.info("🚀 Enhanced FastAPI startup - starting background collection")
    news_engine.start_background_collection()

# Enhanced professional news dashboard
@app.get("/", response_class=HTMLResponse)
async def dashboard():
    """Enhanced professional news intelligence dashboard"""
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>RPNews - Enhanced News Intelligence</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', sans-serif;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            color: #2c3e50;
            line-height: 1.6;
        }
        
        .header {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(20px);
            border-bottom: 1px solid rgba(0, 0, 0, 0.1);
            position: sticky;
            top: 0;
            z-index: 1000;
            box-shadow: 0 2px 20px rgba(0, 0, 0, 0.1);
        }
        
        .nav-container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 0 20px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            height: 70px;
        }
        
        .logo {
            font-size: 1.8em;
            font-weight: 800;
            background: linear-gradient(45deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .nav-tabs {
            display: flex;
            gap: 0;
            background: rgba(102, 126, 234, 0.1);
            border-radius: 12px;
            padding: 4px;
        }
        
        .nav-tab {
            padding: 12px 24px;
            border: none;
            background: transparent;
            color: #667eea;
            font-weight: 600;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s ease;
            font-size: 0.95em;
        }
        
        .nav-tab:hover {
            background: rgba(102, 126, 234, 0.2);
            color: #5a67d8;
        }
        
        .nav-tab.active {
            background: #667eea;
            color: white;
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
        }
        
        .controls {
            display: flex;
            gap: 10px;
            align-items: center;
        }
        
        .control-btn {
            background: linear-gradient(45deg, #667eea, #764ba2);
            color: white;
            border: none;
            padding: 10px 16px;
            border-radius: 8px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            gap: 6px;
            font-size: 0.9em;
        }
        
        .control-btn:hover {
            transform: translateY(-1px);
            box-shadow: 0 6px 16px rgba(102, 126, 234, 0.3);
        }
        
        .control-btn.secondary {
            background: rgba(102, 126, 234, 0.1);
            color: #667eea;
            border: 1px solid rgba(102, 126, 234, 0.3);
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 30px 20px;
        }
        
        .briefing-header {
            text-align: center;
            margin-bottom: 30px;
            background: rgba(255, 255, 255, 0.9);
            padding: 30px;
            border-radius: 20px;
            backdrop-filter: blur(10px);
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        }
        
        .briefing-title {
            font-size: 2.5em;
            font-weight: 700;
            color: #2c3e50;
            margin-bottom: 10px;
        }
        
        .briefing-date {
            color: #667eea;
            font-size: 1.2em;
            font-weight: 500;
            margin-bottom: 20px;
        }
        
        .daily-overview {
            background: linear-gradient(135deg, #f8f9ff, #e8ecff);
            padding: 25px;
            border-radius: 15px;
            border-left: 5px solid #667eea;
            margin-bottom: 20px;
            font-size: 1.05em;
            line-height: 1.7;
            color: #2c3e50;
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.1);
        }
        
        .overview-title {
            font-weight: 700;
            color: #667eea;
            margin-bottom: 10px;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .stats-bar {
            display: flex;
            justify-content: center;
            gap: 30px;
            margin-top: 20px;
            flex-wrap: wrap;
        }
        
        .stat-item {
            text-align: center;
            padding: 12px 20px;
            background: rgba(102, 126, 234, 0.1);
            border-radius: 12px;
            min-width: 100px;
        }
        
        .stat-number {
            font-size: 1.5em;
            font-weight: 700;
            color: #667eea;
        }
        
        .stat-label {
            font-size: 0.9em;
            color: #7f8c8d;
        }
        
        .view-controls {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 25px;
            flex-wrap: wrap;
            gap: 15px;
        }
        
        .filter-controls {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
        }
        
        .filter-btn {
            padding: 8px 16px;
            border: 1px solid rgba(102, 126, 234, 0.3);
            background: rgba(102, 126, 234, 0.1);
            color: #667eea;
            border-radius: 20px;
            cursor: pointer;
            font-size: 0.9em;
            transition: all 0.3s ease;
        }
        
        .filter-btn.active {
            background: #667eea;
            color: white;
        }
        
        .category-section {
            margin-bottom: 50px;
        }
        
        .category-header {
            display: flex;
            align-items: center;
            gap: 15px;
            margin-bottom: 25px;
            padding: 20px 30px;
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.08);
        }
        
        .category-icon {
            font-size: 1.2em;
            font-weight: 700;
            color: #667eea;
            background: rgba(102, 126, 234, 0.1);
            padding: 8px 12px;
            border-radius: 8px;
            min-width: 40px;
            text-align: center;
        }
        
        .category-title {
            font-size: 1.8em;
            font-weight: 700;
            color: #2c3e50;
            flex: 1;
        }
        
        .category-stats {
            display: flex;
            gap: 15px;
        }
        
        .category-count {
            background: #667eea;
            color: white;
            padding: 6px 12px;
            border-radius: 20px;
            font-size: 0.9em;
            font-weight: 600;
        }
        
        .articles-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 25px;
        }
        
        .article-card {
            background: white;
            border-radius: 16px;
            overflow: hidden;
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
            transition: all 0.3s ease;
            border: 1px solid rgba(102, 126, 234, 0.1);
            position: relative;
            opacity: 1;
        }
        
        .article-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 40px rgba(0, 0, 0, 0.15);
        }
        
        .article-card.read {
            opacity: 0.7;
        }
        
        .article-card.starred {
            border-left: 4px solid #ffd700;
        }
        
        .article-header {
            padding: 20px 25px 15px;
            border-bottom: 1px solid #f8f9fa;
        }
        
        .article-meta {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 12px;
        }
        
        .article-source {
            font-weight: 600;
            color: #667eea;
            font-size: 0.9em;
        }
        
        .article-time-info {
            display: flex;
            align-items: center;
            gap: 10px;
            color: #95a5a6;
            font-size: 0.85em;
        }
        
        .reading-time {
            background: rgba(102, 126, 234, 0.1);
            color: #667eea;
            padding: 2px 8px;
            border-radius: 10px;
            font-size: 0.8em;
        }
        
        .priority-badge {
            position: absolute;
            top: 15px;
            right: 15px;
            padding: 4px 8px;
            border-radius: 6px;
            font-size: 0.75em;
            font-weight: 600;
            text-transform: uppercase;
        }
        
        .priority-high {
            background: #ff6b6b;
            color: white;
        }
        
        .priority-medium {
            background: #feca57;
            color: white;
        }
        
        .priority-low {
            background: #48dbfb;
            color: white;
        }
        
        .article-title {
            font-size: 1.25em;
            font-weight: 700;
            color: #2c3e50;
            line-height: 1.4;
            margin-bottom: 15px;
            cursor: pointer;
            transition: color 0.3s ease;
        }
        
        .article-title:hover {
            color: #667eea;
        }
        
        .article-actions {
            position: absolute;
            top: 15px;
            left: 15px;
            display: flex;
            gap: 5px;
        }
        
        .action-btn {
            width: 28px;
            height: 28px;
            border-radius: 50%;
            border: none;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 14px;
            transition: all 0.3s ease;
            background: rgba(255, 255, 255, 0.9);
            color: #666;
        }
        
        .action-btn:hover {
            background: white;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
        }
        
        .action-btn.read {
            color: #28a745;
        }
        
        .action-btn.starred {
            color: #ffd700;
        }
        
        .article-content {
            padding: 0 25px 20px;
        }
        
        .article-summary {
            background: linear-gradient(135deg, #f8f9ff, #f0f4ff);
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 15px;
            border-left: 4px solid #667eea;
            font-size: 0.95em;
            line-height: 1.5;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .article-summary:hover {
            background: linear-gradient(135deg, #f0f4ff, #e8ecff);
            transform: translateX(2px);
        }
        
        .article-excerpt {
            color: #5d6d7e;
            line-height: 1.6;
            margin-bottom: 15px;
        }
        
        .article-tags {
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
        }
        
        .tag {
            background: rgba(102, 126, 234, 0.1);
            color: #667eea;
            padding: 4px 10px;
            border-radius: 12px;
            font-size: 0.8em;
            font-weight: 500;
        }
        
        .loading {
            text-align: center;
            padding: 60px 20px;
            color: #7f8c8d;
        }
        
        .loading-spinner {
            width: 50px;
            height: 50px;
            border: 4px solid #f3f3f3;
            border-top: 4px solid #667eea;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin: 0 auto 20px;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .empty-state {
            text-align: center;
            padding: 60px 20px;
            color: #7f8c8d;
        }
        
        .empty-state-icon {
            font-size: 3em;
            margin-bottom: 20px;
            color: #bdc3c7;
            font-weight: 300;
        }
        
        .starred-section {
            margin-bottom: 40px;
        }
        
        @media (max-width: 768px) {
            .nav-container {
                flex-direction: column;
                height: auto;
                padding: 15px 20px;
                gap: 15px;
            }
            
            .nav-tabs {
                width: 100%;
                justify-content: center;
            }
            
            .nav-tab {
                flex: 1;
                text-align: center;
                padding: 10px 16px;
                font-size: 0.9em;
            }
            
            .controls {
                width: 100%;
                justify-content: center;
                flex-wrap: wrap;
            }
            
            .briefing-title {
                font-size: 2em;
            }
            
            .articles-grid {
                grid-template-columns: 1fr;
            }
            
            .stats-bar {
                gap: 15px;
            }
            
            .category-header {
                padding: 15px 20px;
                flex-wrap: wrap;
            }
            
            .view-controls {
                flex-direction: column;
                align-items: flex-start;
            }
        }
        
        .fade-in {
            animation: fadeIn 0.6s ease-in;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
    </style>
</head>
<body>
    <header class="header">
        <div class="nav-container">
            <div class="logo">RPNews Enhanced</div>
            <div class="nav-tabs">
                <button class="nav-tab active" data-view="briefing">Daily Briefing</button>
                <button class="nav-tab" data-view="ai">AI & Technology</button>
                <button class="nav-tab" data-view="finance">Finance & Markets</button>
                <button class="nav-tab" data-view="politics">Politics & Policy</button>
                <button class="nav-tab" data-view="starred">⭐ Starred</button>
            </div>
            <div class="controls">
                <button class="control-btn secondary" data-view="reading-list">📖 Reading List</button>
                <button class="control-btn" onclick="refreshNews()">
                    <span id="refresh-icon">↻</span> Refresh
                </button>
            </div>
        </div>
    </header>

    <div class="container">
        <div id="loading" class="loading">
            <div class="loading-spinner"></div>
            <h3>Loading enhanced news intelligence...</h3>
            <p>Processing articles with AI summaries from 60+ premium sources</p>
        </div>

        <div id="content" style="display: none;">
            <div class="briefing-header">
                <h1 class="briefing-title">Enhanced Daily Intelligence Briefing</h1>
                <p class="briefing-date" id="briefing-date"></p>
                
                <div id="daily-overview" class="daily-overview" style="display: none;">
                    <div class="overview-title">🌅 Daily Overview</div>
                    <div id="overview-text"></div>
                </div>
                
                <div class="stats-bar" id="stats-bar"></div>
            </div>

            <div class="view-controls">
                <div class="filter-controls">
                    <button class="filter-btn active" data-filter="all">All Priority</button>
                    <button class="filter-btn" data-filter="high">High Priority</button>
                    <button class="filter-btn" data-filter="unread">Unread Only</button>
                </div>
            </div>

            <div id="news-content"></div>
        </div>
    </div>

    <script>
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
                    if (currentData) {
                        displayContent();
                    }
                });
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
                currentData = await response.json();
                displayContent();
            } catch (error) {
                console.error('Error loading briefing:', error);
                showError();
            }
        }

        async function refreshNews() {
            const refreshIcon = document.getElementById('refresh-icon');
            refreshIcon.style.animation = 'spin 1s linear infinite';
            
            try {
                // Trigger collection
                await fetch('/api/collect', { method: 'POST' });
                
                // Wait a moment then reload
                setTimeout(async () => {
                    await loadBriefing();
                    refreshIcon.style.animation = 'none';
                }, 5000);
            } catch (error) {
                console.error('Error refreshing:', error);
                refreshIcon.style.animation = 'none';
            }
        }

        async function markAsRead(articleId, element) {
            try {
                const response = await fetch(`/api/articles/${articleId}/read`, { method: 'POST' });
                if (response.ok) {
                    element.closest('.article-card').classList.add('read');
                    const btn = element.closest('.article-card').querySelector('.read-btn');
                    btn.classList.add('read');
                    btn.innerHTML = '✓';
                }
            } catch (error) {
                console.error('Error marking as read:', error);
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
                
                if (response.ok) {
                    if (isStarred) {
                        card.classList.remove('starred');
                        element.innerHTML = '☆';
                        element.classList.remove('starred');
                    } else {
                        card.classList.add('starred');
                        element.innerHTML = '★';
                        element.classList.add('starred');
                    }
                }
            } catch (error) {
                console.error('Error toggling star:', error);
            }
        }

        function openArticle(url, summaryElement) {
            // Mark the summary as clicked (visual feedback)
            summaryElement.style.background = 'linear-gradient(135deg, #e8ecff, #d4e3ff)';
            
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

        function showError() {
            hideLoading();
            document.getElementById('news-content').innerHTML = `
                <div class="empty-state">
                    <div class="empty-state-icon">!</div>
                    <h3>Unable to load news</h3>
                    <p>Please try refreshing or check back in a few minutes.</p>
                </div>
            `;
        }

        function displayContent() {
            hideLoading();
            
            if (!currentData || !currentData.briefing) {
                showError();
                return;
            }

            // Update header
            document.getElementById('briefing-date').textContent = currentData.date;
            
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
            
            if (currentView === 'briefing') {
                contentDiv.innerHTML = displayAllCategories();
            } else if (currentView === 'starred') {
                contentDiv.innerHTML = displayStarredArticles();
            } else if (currentView === 'reading-list') {
                contentDiv.innerHTML = displayUnreadArticles();
            } else {
                contentDiv.innerHTML = displaySingleCategory(currentView);
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

        function displayUnreadArticles() {
            const unreadArticles = applyFilters(getAllArticles().filter(a => !a.isRead));
            
            if (unreadArticles.length === 0) {
                return '<div class="empty-state"><div class="empty-state-icon">📖</div><h3>All caught up!</h3><p>You\'ve read all available articles. Check back later for new updates.</p></div>';
            }

            return `
                <div class="articles-grid">
                    ${unreadArticles.map(article => createArticleCard(article)).join('')}
                </div>
            `;
        }

        function createArticleCard(article) {
            const tags = article.tags || [];
            const tagsHtml = tags.map(tag => `<span class="tag">${tag}</span>`).join('');
            const readClass = article.isRead ? 'read' : '';
            const starredClass = article.isStarred ? 'starred' : '';
            const readIcon = article.isRead ? '✓' : '○';
            const starIcon = article.isStarred ? '★' : '☆';
            const readBtnClass = article.isRead ? 'read' : '';
            const starBtnClass = article.isStarred ? 'starred' : '';
            
            return `
                <article class="article-card ${readClass} ${starredClass}">
                    <div class="article-actions">
                        <button class="action-btn read-btn ${readBtnClass}" 
                                onclick="markAsRead('${article.id}', this)" 
                                title="Mark as read">
                            ${readIcon}
                        </button>
                        <button class="action-btn star-btn ${starBtnClass}" 
                                onclick="toggleStar('${article.id}', this)" 
                                title="Star article">
                            ${starIcon}
                        </button>
                    </div>
                    <div class="priority-badge priority-${article.priority || 'medium'}">${article.priority || 'medium'}</div>
                    
                    <div class="article-header">
                        <div class="article-meta">
                            <span class="article-source">${article.source}</span>
                            <div class="article-time-info">
                                <span>${article.timeAgo}</span>
                                <span class="reading-time">${article.readingTime || 2}min read</span>
                            </div>
                        </div>
                        <h3 class="article-title" onclick="openArticle('${article.url}', this)">
                            ${article.title}
                        </h3>
                    </div>
                    
                    <div class="article-content">
                        ${article.aiSummary ? `
                            <div class="article-summary" onclick="openArticle('${article.url}', this)" title="Click to read full article">
                                ${article.aiSummary}
                            </div>
                        ` : ''}
                        <p class="article-excerpt">${article.excerpt}</p>
                        ${tagsHtml ? `<div class="article-tags">${tagsHtml}</div>` : ''}
                    </div>
                </article>
            `;
        }
    </script>
</body>
</html>"""
    return html_content

@app.get("/api/news/dashboard")
async def get_dashboard_data():
    """Get comprehensive dashboard data for the beautiful UI"""
    try:
        with sqlite3.connect(news_engine.db_path) as conn:
            # Get stats
            stats = {}
            total_articles = 0
            high_priority_count = 0
            ai_summaries_count = 0
            
            category_counts = {'ai': 0, 'finance': 0, 'politics': 0}
            categories_data = {'ai': [], 'finance': [], 'politics': []}
            high_priority_articles = []
            
            for category in ['ai', 'finance', 'politics']:
                cursor = conn.execute("""
                    SELECT id, title, url, source, author, published_date, excerpt,
                           ai_summary, priority, tags, reading_time, is_read, is_starred
                    FROM articles 
                    WHERE category = ? AND published_date >= datetime('now', '-24 hours')
                    ORDER BY 
                        CASE priority 
                            WHEN 'high' THEN 3 
                            WHEN 'medium' THEN 2 
                            ELSE 1 
                        END DESC,
                        published_date DESC
                    LIMIT 10
                """, (category,))
                
                articles = []
                for row in cursor.fetchall():
                    # Calculate time ago
                    try:
                        pub_date = datetime.fromisoformat(row[5])
                        hours_ago = int((datetime.now() - pub_date).total_seconds() / 3600)
                        time_str = f"{hours_ago}h ago" if hours_ago < 24 else f"{hours_ago//24}d ago"
                    except:
                        time_str = "Recently"
                    
                    article_data = {
                        'id': row[0],
                        'title': row[1],
                        'url': row[2],
                        'source': row[3],
                        'author': row[4] or 'Unknown',
                        'publishedTime': time_str,
                        'excerpt': row[6],
                        'aiSummary': row[7] or f"📰 {category.upper()}: {row[1][:100]}...",
                        'priority': row[8] or 'medium',
                        'tags': json.loads(row[9] or '[]'),
                        'readingTime': row[10] or 3,
                        'category': category
                    }
                    
                    articles.append(article_data)
                    total_articles += 1
                    
                    if row[8] == 'high':
                        high_priority_count += 1
                        high_priority_articles.append(article_data)
                    
                    if row[7]:  # Has AI summary
                        ai_summaries_count += 1
                
                categories_data[category] = articles
                category_counts[category] = len(articles)
            
            # Get daily overview
            today = datetime.now().strftime('%Y-%m-%d')
            cursor = conn.execute("""
                SELECT overview_text FROM daily_overviews 
                WHERE date = ? ORDER BY generated_at DESC LIMIT 1
            """, (today,))
            overview_result = cursor.fetchone()
            daily_overview = overview_result[0] if overview_result else None
            
            if not daily_overview:
                daily_overview = f"🌅 Today's Intelligence Overview: {total_articles} articles collected from premium sources. {high_priority_count} high-priority developments identified across AI, finance, and politics. Enhanced AI analysis and priority detection active."
            
            # Calculate analytics
            analytics = {
                'dailyArticles': total_articles,
                'aiSummaries': ai_summaries_count,
                'activeSources': sum(len(sources) for sources in news_engine.sources.values()),
                'avgReadTime': 4.2,
                'trend': [16, 20, 24, 28, 32, 26, 22]  # Mock trend data
            }
            
            stats = {
                'totalArticles': total_articles,
                'highPriority': high_priority_count,
                'aiSummaries': ai_summaries_count,
                'aiCount': category_counts['ai'],
                'financeCount': category_counts['finance'],
                'politicsCount': category_counts['politics'],
                'lastUpdate': datetime.now().strftime('%H:%M')
            }
            
            return {
                'stats': stats,
                'dailyOverview': daily_overview,
                'highPriorityArticles': high_priority_articles[:6],
                'categories': categories_data,
                'analytics': analytics
            }
            
    except Exception as e:
        logger.error(f"Error getting dashboard data: {str(e)}")
        # Return default data if database is empty
        return {
            'stats': {
                'totalArticles': 0,
                'highPriority': 0,
                'aiSummaries': 0,
                'aiCount': 0,
                'financeCount': 0,
                'politicsCount': 0,
                'lastUpdate': datetime.now().strftime('%H:%M')
            },
            'dailyOverview': "🌅 Welcome to RPNews Enhanced! Your AI-powered news intelligence platform is ready. Click 'Collect Latest' to start gathering news from 60+ premium sources with AI-powered analysis.",
            'highPriorityArticles': [],
            'categories': {'ai': [], 'finance': [], 'politics': []},
            'analytics': {
                'dailyArticles': 0,
                'aiSummaries': 0,
                'activeSources': 60,
                'avgReadTime': 4.2,
                'trend': [0, 0, 0, 0, 0, 0, 0]
            }
        }

@app.get("/api/news/category/{category}")
async def get_category_articles(category: str, limit: int = 50):
    """Get articles for a specific category"""
    if category not in ['ai', 'finance', 'politics']:
        raise HTTPException(status_code=400, detail="Invalid category")
    
    try:
        with sqlite3.connect(news_engine.db_path) as conn:
            cursor = conn.execute("""
                SELECT id, title, url, source, author, published_date, excerpt,
                       ai_summary, priority, tags, reading_time, is_read, is_starred
                FROM articles 
                WHERE category = ?
                ORDER BY published_date DESC
                LIMIT ?
            """, (category, limit))
            
            articles = []
            for row in cursor.fetchall():
                try:
                    pub_date = datetime.fromisoformat(row[5])
                    hours_ago = int((datetime.now() - pub_date).total_seconds() / 3600)
                    time_str = f"{hours_ago}h ago" if hours_ago < 24 else f"{hours_ago//24}d ago"
                except:
                    time_str = "Recently"
                
                articles.append({
                    'id': row[0],
                    'title': row[1],
                    'url': row[2],
                    'source': row[3],
                    'author': row[4] or 'Unknown',
                    'publishedTime': time_str,
                    'excerpt': row[6],
                    'aiSummary': row[7] or f"📰 {category.upper()}: {row[1][:100]}...",
                    'priority': row[8] or 'medium',
                    'tags': json.loads(row[9] or '[]'),
                    'readingTime': row[10] or 3,
                    'category': category
                })
            
            return articles
            
    except Exception as e:
        logger.error(f"Error getting {category} articles: {str(e)}")
        return []

@app.post("/api/news/collect")
async def trigger_news_collection(background_tasks: BackgroundTasks):
    """Trigger news collection for the beautiful UI"""
    
    async def run_collection():
        try:
            logger.info("Manual collection triggered from beautiful UI")
            async with aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=60),
                headers={'User-Agent': 'RPNews Enhanced/2.0'}
            ) as session:
                news_engine.session = session
                total_collected = await news_engine.collect_all_news()
                news_engine.session = None
                logger.info(f"Collection completed: {total_collected} articles")
        except Exception as e:
            logger.error(f"Collection error: {str(e)}")
    
    background_tasks.add_task(run_collection)
    
    return {
        'success': True,
        'message': 'News collection started successfully',
        'timestamp': datetime.now().isoformat()
    }
async def get_dashboard_data():
    """Get comprehensive dashboard data for React frontend"""
    try:
        with sqlite3.connect(news_engine.db_path) as conn:
            # Get stats
            stats = {}
            total_articles = 0
            high_priority_count = 0
            ai_summaries_count = 0
            
            category_counts = {'ai': 0, 'finance': 0, 'politics': 0}
            categories_data = {'ai': [], 'finance': [], 'politics': []}
            high_priority_articles = []
            
            for category in ['ai', 'finance', 'politics']:
                cursor = conn.execute("""
                    SELECT id, title, url, source, author, published_date, excerpt,
                           ai_summary, priority, tags, reading_time, is_read, is_starred
                    FROM articles 
                    WHERE category = ? AND published_date >= datetime('now', '-24 hours')
                    ORDER BY 
                        CASE priority 
                            WHEN 'high' THEN 3 
                            WHEN 'medium' THEN 2 
                            ELSE 1 
                        END DESC,
                        published_date DESC
                    LIMIT 10
                """, (category,))
                
                articles = []
                for row in cursor.fetchall():
                    # Calculate time ago
                    try:
                        pub_date = datetime.fromisoformat(row[5])
                        hours_ago = int((datetime.now() - pub_date).total_seconds() / 3600)
                        time_str = f"{hours_ago}h ago" if hours_ago < 24 else f"{hours_ago//24}d ago"
                    except:
                        time_str = "Recently"
                    
                    article_data = {
                        'id': row[0],
                        'title': row[1],
                        'url': row[2],
                        'source': row[3],
                        'author': row[4] or 'Unknown',
                        'publishedTime': time_str,
                        'excerpt': row[6],
                        'aiSummary': row[7] or f"Summary for {row[1][:50]}...",
                        'priority': row[8] or 'medium',
                        'tags': json.loads(row[9] or '[]'),
                        'readingTime': row[10] or 3,
                        'category': category
                    }
                    
                    articles.append(article_data)
                    total_articles += 1
                    
                    if row[8] == 'high':
                        high_priority_count += 1
                        high_priority_articles.append(article_data)
                    
                    if row[7]:  # Has AI summary
                        ai_summaries_count += 1
                
                categories_data[category] = articles
                category_counts[category] = len(articles)
            
            # Get daily overview
            today = datetime.now().strftime('%Y-%m-%d')
            cursor = conn.execute("""
                SELECT overview_text FROM daily_overviews 
                WHERE date = ? ORDER BY generated_at DESC LIMIT 1
            """, (today,))
            overview_result = cursor.fetchone()
            daily_overview = overview_result[0] if overview_result else None
            
            if not daily_overview:
                daily_overview = f"🌅 Today's Intelligence Overview: {total_articles} articles collected from premium sources. {high_priority_count} high-priority developments identified across AI, finance, and politics. AI-powered analysis and priority detection active."
            
            # Calculate analytics
            analytics = {
                'dailyArticles': total_articles,
                'aiSummaries': ai_summaries_count,
                'activeSources': sum(len(sources) for sources in news_engine.sources.values()),
                'avgReadTime': 4.2,
                'trend': [16, 20, 24, 28, 32, 26, 22]  # Mock trend data
            }
            
            stats = {
                'totalArticles': total_articles,
                'highPriority': high_priority_count,
                'aiSummaries': ai_summaries_count,
                'aiCount': category_counts['ai'],
                'financeCount': category_counts['finance'],
                'politicsCount': category_counts['politics'],
                'lastUpdate': datetime.now().strftime('%H:%M')
            }
            
            return {
                'stats': stats,
                'dailyOverview': daily_overview,
                'highPriorityArticles': high_priority_articles[:6],
                'categories': categories_data,
                'analytics': analytics
            }
            
    except Exception as e:
        logger.error(f"Error getting dashboard data: {str(e)}")
        # Return mock data if database is empty or has issues
        return {
            'stats': {
                'totalArticles': 0,
                'highPriority': 0,
                'aiSummaries': 0,
                'aiCount': 0,
                'financeCount': 0,
                'politicsCount': 0,
                'lastUpdate': datetime.now().strftime('%H:%M')
            },
            'dailyOverview': "🌅 Welcome to RPNews Enhanced! Your AI-powered news intelligence platform is initializing. Click 'Collect Latest' to start gathering news from 60+ premium sources.",
            'highPriorityArticles': [],
            'categories': {'ai': [], 'finance': [], 'politics': []},
            'analytics': {
                'dailyArticles': 0,
                'aiSummaries': 0,
                'activeSources': 60,
                'avgReadTime': 4.2,
                'trend': [0, 0, 0, 0, 0, 0, 0]
            }
        }

@app.get("/api/news/category/{category}")
async def get_category_articles(category: str, limit: int = 20):
    """Get articles for a specific category"""
    if category not in ['ai', 'finance', 'politics']:
        raise HTTPException(status_code=400, detail="Invalid category")
    
    try:
        with sqlite3.connect(news_engine.db_path) as conn:
            cursor = conn.execute("""
                SELECT id, title, url, source, author, published_date, excerpt,
                       ai_summary, priority, tags, reading_time, is_read, is_starred
                FROM articles 
                WHERE category = ?
                ORDER BY published_date DESC
                LIMIT ?
            """, (category, limit))
            
            articles = []
            for row in cursor.fetchall():
                try:
                    pub_date = datetime.fromisoformat(row[5])
                    hours_ago = int((datetime.now() - pub_date).total_seconds() / 3600)
                    time_str = f"{hours_ago}h ago" if hours_ago < 24 else f"{hours_ago//24}d ago"
                except:
                    time_str = "Recently"
                
                articles.append({
                    'id': row[0],
                    'title': row[1],
                    'url': row[2],
                    'source': row[3],
                    'author': row[4] or 'Unknown',
                    'publishedTime': time_str,
                    'excerpt': row[6],
                    'aiSummary': row[7],
                    'priority': row[8],
                    'tags': json.loads(row[9] or '[]'),
                    'readingTime': row[10] or 3,
                    'category': category
                })
            
            return articles
            
    except Exception as e:
        logger.error(f"Error getting {category} articles: {str(e)}")
        return []

@app.post("/api/news/collect")
async def trigger_news_collection(background_tasks: BackgroundTasks):
    """Trigger news collection for React frontend"""
    
    async def run_collection():
        try:
            logger.info("Manual collection triggered from React frontend")
            async with aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=60),
                headers={'User-Agent': 'RPNews Enhanced/2.0'}
            ) as session:
                news_engine.session = session
                total_collected = await news_engine.collect_all_news()
                news_engine.session = None
                logger.info(f"Collection completed: {total_collected} articles")
        except Exception as e:
            logger.error(f"Collection error: {str(e)}")
    
    background_tasks.add_task(run_collection)
    
    return {
        'success': True,
        'message': 'News collection started successfully',
        'timestamp': datetime.now().isoformat()
    }

@app.get("/api/news/search")
async def search_articles(
    keywords: str = "", 
    category: str = "", 
    priority: str = "",
    limit: int = 50
):
    """Search articles with filters"""
    try:
        with sqlite3.connect(news_engine.db_path) as conn:
            query = """
                SELECT id, title, url, source, author, published_date, excerpt,
                       ai_summary, priority, tags, reading_time, category
                FROM articles 
                WHERE 1=1
            """
            params = []
            
            if keywords:
                query += " AND (title LIKE ? OR content LIKE ? OR ai_summary LIKE ?)"
                search_term = f"%{keywords}%"
                params.extend([search_term, search_term, search_term])
            
            if category:
                query += " AND category = ?"
                params.append(category)
            
            if priority:
                query += " AND priority = ?"
                params.append(priority)
            
            query += " ORDER BY published_date DESC LIMIT ?"
            params.append(limit)
            
            cursor = conn.execute(query, params)
            
            articles = []
            for row in cursor.fetchall():
                try:
                    pub_date = datetime.fromisoformat(row[5])
                    hours_ago = int((datetime.now() - pub_date).total_seconds() / 3600)
                    time_str = f"{hours_ago}h ago" if hours_ago < 24 else f"{hours_ago//24}d ago"
                except:
                    time_str = "Recently"
                
                articles.append({
                    'id': row[0],
                    'title': row[1],
                    'url': row[2],
                    'source': row[3],
                    'author': row[4] or 'Unknown',
                    'publishedTime': time_str,
                    'excerpt': row[6],
                    'aiSummary': row[7],
                    'priority': row[8],
                    'tags': json.loads(row[9] or '[]'),
                    'readingTime': row[10] or 3,
                    'category': row[11]
                })
            
            return articles
            
    except Exception as e:
        logger.error(f"Error searching articles: {str(e)}")
        return []
async def get_morning_briefing():
    """Generate comprehensive morning briefing with daily overview"""
    try:
        with sqlite3.connect(news_engine.db_path) as conn:
            briefing = {}
            total_articles = 0
            high_priority_count = 0
            
            for category in ['ai', 'finance', 'politics']:
                cursor = conn.execute("""
                    SELECT id, title, url, source, author, published_date, excerpt,
                           ai_summary, priority, tags, reading_time, is_read, is_starred
                    FROM articles 
                    WHERE category = ? AND published_date >= datetime('now', '-24 hours')
                    ORDER BY 
                        CASE priority 
                            WHEN 'high' THEN 3 
                            WHEN 'medium' THEN 2 
                            ELSE 1 
                        END DESC,
                        published_date DESC
                    LIMIT 15
                """, (category,))
                
                articles = []
                for row in cursor.fetchall():
                    # Calculate time ago
                    try:
                        pub_date = datetime.fromisoformat(row[5])
                        hours_ago = int((datetime.now() - pub_date).total_seconds() / 3600)
                        time_str = f"{hours_ago}h ago" if hours_ago < 24 else f"{hours_ago//24}d ago"
                    except:
                        time_str = "Recently"
                    
                    is_high_priority = row[8] == 'high'
                    if is_high_priority:
                        high_priority_count += 1
                    
                    articles.append({
                        'id': row[0],
                        'title': row[1],
                        'url': row[2],
                        'source': row[3],
                        'author': row[4] or 'Unknown',
                        'publishedDate': row[5],
                        'excerpt': row[6],
                        'aiSummary': row[7],
                        'priority': row[8],
                        'tags': json.loads(row[9] or '[]'),
                        'readingTime': row[10] or 2,
                        'category': category,
                        'timeAgo': time_str,
                        'isRead': bool(row[11]),
                        'isStarred': bool(row[12])
                    })
                
                briefing[category] = articles
                total_articles += len(articles)
            
            # Get daily overview
            today = datetime.now().strftime('%Y-%m-%d')
            cursor = conn.execute("""
                SELECT overview_text FROM daily_overviews 
                WHERE date = ? ORDER BY generated_at DESC LIMIT 1
            """, (today,))
            overview_result = cursor.fetchone()
            daily_overview = overview_result[0] if overview_result else None
            
            return {
                'platform': 'RPNews Enhanced',
                'date': datetime.now().strftime('%B %d, %Y'),
                'briefing': briefing,
                'daily_overview': daily_overview,
                'generated_at': datetime.now().isoformat(),
                'total_articles': total_articles,
                'high_priority_count': high_priority_count,
                'ai_type': news_engine.ai.ai_type,
                'message': 'Your enhanced AI-powered briefing is ready!'
            }
            
    except Exception as e:
        logger.error(f"Error generating briefing: {str(e)}")
        return {
            'platform': 'RPNews Enhanced',
            'date': datetime.now().strftime('%B %d, %Y'),
            'briefing': {'ai': [], 'finance': [], 'politics': []},
            'daily_overview': 'Daily overview will be available after first news collection.',
            'error': 'Briefing generation failed - this may be the first run',
            'generated_at': datetime.now().isoformat(),
            'suggestion': 'Try clicking "Refresh" to collect the latest news'
        }

@app.post("/api/articles/{article_id}/read")
async def mark_article_read(article_id: str):
    """Mark an article as read"""
    success = news_engine.mark_article_read(article_id)
    if success:
        return {'status': 'success', 'message': 'Article marked as read'}
    else:
        raise HTTPException(status_code=500, detail="Failed to mark article as read")

@app.post("/api/articles/{article_id}/star")
async def star_article(article_id: str, request: dict):
    """Star or unstar an article"""
    starred = request.get('starred', True)
    success = news_engine.star_article(article_id, starred)
    if success:
        action = 'starred' if starred else 'unstarred'
        return {'status': 'success', 'message': f'Article {action}'}
    else:
        raise HTTPException(status_code=500, detail="Failed to update article star status")

@app.get("/api/articles/starred")
async def get_starred_articles():
    """Get all starred articles"""
    try:
        with sqlite3.connect(news_engine.db_path) as conn:
            cursor = conn.execute("""
                SELECT id, title, url, source, author, published_date, excerpt,
                       ai_summary, category, priority, tags, reading_time, starred_at
                FROM articles 
                WHERE is_starred = TRUE
                ORDER BY starred_at DESC
                LIMIT 100
            """)
            
            articles = []
            for row in cursor.fetchall():
                try:
                    pub_date = datetime.fromisoformat(row[5])
                    hours_ago = int((datetime.now() - pub_date).total_seconds() / 3600)
                    time_str = f"{hours_ago}h ago" if hours_ago < 24 else f"{hours_ago//24}d ago"
                except:
                    time_str = "Recently"
                
                articles.append({
                    'id': row[0],
                    'title': row[1],
                    'url': row[2],
                    'source': row[3],
                    'author': row[4] or 'Unknown',
                    'publishedDate': row[5],
                    'excerpt': row[6],
                    'aiSummary': row[7],
                    'category': row[8],
                    'priority': row[9],
                    'tags': json.loads(row[10] or '[]'),
                    'readingTime': row[11] or 2,
                    'timeAgo': time_str,
                    'starredAt': row[12],
                    'isStarred': True
                })
            
            return {
                'articles': articles,
                'count': len(articles),
                'generated_at': datetime.now().isoformat()
            }
            
    except Exception as e:
        logger.error(f"Error getting starred articles: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get starred articles")

@app.get("/api/articles/{category}")
async def get_articles(category: str, limit: int = 50, priority: str = "all"):
    """Get articles for a specific category with enhanced features"""
    if category not in ['ai', 'finance', 'politics']:
        raise HTTPException(status_code=400, detail="Category must be ai, finance, or politics")
    
    try:
        with sqlite3.connect(news_engine.db_path) as conn:
            query = """
                SELECT id, title, url, source, author, published_date, excerpt,
                       ai_summary, priority, tags, reading_time, is_read, is_starred
                FROM articles 
                WHERE category = ?
            """
            params = [category]
            
            if priority != "all":
                query += " AND priority = ?"
                params.append(priority)
            
            query += " ORDER BY published_date DESC LIMIT ?"
            params.append(limit)
            
            cursor = conn.execute(query, params)
            
            articles = []
            for row in cursor.fetchall():
                try:
                    pub_date = datetime.fromisoformat(row[5])
                    hours_ago = int((datetime.now() - pub_date).total_seconds() / 3600)
                    time_str = f"{hours_ago}h ago" if hours_ago < 24 else f"{hours_ago//24}d ago"
                except:
                    time_str = "Recently"
                
                articles.append({
                    'id': row[0],
                    'title': row[1],
                    'url': row[2],
                    'source': row[3],
                    'author': row[4] or 'Unknown',
                    'publishedDate': row[5],
                    'excerpt': row[6],
                    'aiSummary': row[7],
                    'priority': row[8],
                    'tags': json.loads(row[9] or '[]'),
                    'readingTime': row[10] or 2,
                    'category': category,
                    'timeAgo': time_str,
                    'isRead': bool(row[11]),
                    'isStarred': bool(row[12])
                })
            
            category_names = {
                'ai': 'AI & Technology',
                'finance': 'Finance & Markets', 
                'politics': 'Politics & Policy'
            }
            
            return {
                'category': category,
                'category_name': category_names[category],
                'articles': articles,
                'count': len(articles),
                'generated_at': datetime.now().isoformat()
            }
            
    except Exception as e:
        logger.error(f"Error getting {category} articles: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get {category} articles")

@app.get("/api/stats")
async def get_stats():
    """Enhanced platform statistics"""
    try:
        with sqlite3.connect(news_engine.db_path) as conn:
            stats = {}
            
            for category in ['ai', 'finance', 'politics']:
                # Total articles
                cursor = conn.execute("SELECT COUNT(*) FROM articles WHERE category = ?", (category,))
                stats[f'{category}_total'] = cursor.fetchone()[0]
                
                # Today's articles
                cursor = conn.execute("""
                    SELECT COUNT(*) FROM articles 
                    WHERE category = ? AND published_date >= date('now')
                """, (category,))
                stats[f'{category}_today'] = cursor.fetchone()[0]
                
                # High priority today
                cursor = conn.execute("""
                    SELECT COUNT(*) FROM articles 
                    WHERE category = ? AND priority = 'high' AND published_date >= date('now')
                """, (category,))
                stats[f'{category}_high_priority'] = cursor.fetchone()[0]
            
            # Reading stats
            cursor = conn.execute("SELECT COUNT(*) FROM articles WHERE is_read = TRUE")
            stats['articles_read'] = cursor.fetchone()[0]
            
            cursor = conn.execute("SELECT COUNT(*) FROM articles WHERE is_starred = TRUE")
            stats['articles_starred'] = cursor.fetchone()[0]
            
            # Source counts
            stats['sources'] = {
                'ai': len(news_engine.sources['ai']),
                'finance': len(news_engine.sources['finance']),
                'politics': len(news_engine.sources['politics'])
            }
            
            # AI type
            stats['ai_type'] = news_engine.ai.ai_type
            stats['ai_available'] = news_engine.ai.ai_available
            
            return stats
            
    except Exception as e:
        logger.error(f"Error getting stats: {str(e)}")
        return {
            'error': 'Stats temporarily unavailable',
            'ai_type': news_engine.ai.ai_type,
            'ai_available': news_engine.ai.ai_available,
            'sources': {
                'ai': len(news_engine.sources['ai']),
                'finance': len(news_engine.sources['finance']),
                'politics': len(news_engine.sources['politics'])
            }
        }

@app.post("/api/collect")
async def trigger_collection(background_tasks: BackgroundTasks):
    """Enhanced manual collection trigger"""
    
    async def run_collection():
        try:
            logger.info("Manual collection triggered")
            async with aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=45),
                headers={'User-Agent': 'RPNews Enhanced/2.0'}
            ) as session:
                news_engine.session = session
                total_collected = await news_engine.collect_all_news()
                news_engine.session = None
                logger.info(f"Manual collection completed: {total_collected} articles")
        except Exception as e:
            logger.error(f"Manual collection error: {str(e)}")
    
    background_tasks.add_task(run_collection)
    
    return {
        'message': 'Enhanced news collection started',
        'timestamp': datetime.now().isoformat(),
        'status': 'Background collection initiated with AI processing',
        'note': 'Articles with AI summaries will appear in a few minutes',
        'features': ['AI summaries', 'Priority detection', 'Reading time estimation']
    }

@app.get("/api/health")
async def health_check():
    """Enhanced health check with AI status"""
    try:
        # Test database connectivity
        with sqlite3.connect(news_engine.db_path) as conn:
            cursor = conn.execute("SELECT COUNT(*) FROM articles")
            article_count = cursor.fetchone()[0]
            
            cursor = conn.execute("SELECT COUNT(*) FROM articles WHERE is_read = TRUE")
            read_count = cursor.fetchone()[0]
            
            cursor = conn.execute("SELECT COUNT(*) FROM articles WHERE is_starred = TRUE")
            starred_count = cursor.fetchone()[0]
        
        return {
            'status': 'healthy',
            'platform': 'RPNews Enhanced',
            'timestamp': datetime.now().isoformat(),
            'ai_type': news_engine.ai.ai_type,
            'ai_available': news_engine.ai.ai_available,
            'article_count': article_count,
            'articles_read': read_count,
            'articles_starred': starred_count,
            'sources_count': sum(len(sources) for sources in news_engine.sources.values()),
            'database': 'connected',
            'features': ['AI Summaries', 'Priority Detection', 'Article Management', 'Daily Overview']
        }
    except Exception as e:
        return {
            'status': 'unhealthy',
            'platform': 'RPNews Enhanced', 
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }

if __name__ == "__main__":
    logger.info("🚀 Starting Enhanced RPNews Platform")
    logger.info(f"🌐 Port: {PORT}")
    logger.info(f"🤖 AI Engine: {news_engine.ai.ai_type}")
    logger.info(f"🎯 AI Model Available: {news_engine.ai.ai_available}")
    logger.info(f"📊 Total Sources: {sum(len(sources) for sources in news_engine.sources.values())}")
    logger.info("✨ Enhanced Features: AI summaries, priority detection, article management")
    
    uvicorn.run(app, host="0.0.0.0", port=PORT)
