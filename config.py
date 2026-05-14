"""
Configuration module - loads settings from environment variables
Supports .env file via python-dotenv
"""

import os
from dotenv import load_dotenv

load_dotenv()  # Load .env file if present

class Config:
    # --- Core ---
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production-xyz123')
    DEBUG = os.environ.get('FLASK_DEBUG', 'False') == 'True'

    # --- Database ---
    DATABASE_PATH = os.environ.get('DATABASE_PATH', 'database/career_ai.db')

    # --- File Upload ---
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'static', 'uploads')
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5 MB max upload size
    ALLOWED_EXTENSIONS = {'pdf', 'docx', 'doc'}

    # --- AI / OpenAI (optional) ---
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', '')
    USE_AI_CHATBOT = bool(os.environ.get('OPENAI_API_KEY', ''))  # Falls back to keyword logic if not set

    # --- Admin ---
    ADMIN_DEFAULT_EMAIL = os.environ.get('ADMIN_EMAIL', 'admin@careerAI.com').lower()
    ADMIN_DEFAULT_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'Admin@123')

    # --- Session ---
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'

    # --- ATS Scoring ---
    # Tech keywords used for ATS analysis
    TECH_KEYWORDS = [
        # Languages
        'python', 'java', 'javascript', 'c++', 'c#', 'typescript', 'go', 'rust', 'kotlin', 'swift',
        'r', 'scala', 'php', 'ruby', 'dart', 'matlab',
        # Web
        'html', 'css', 'react', 'angular', 'vue', 'nodejs', 'flask', 'django', 'fastapi', 'express',
        'bootstrap', 'tailwind', 'next.js', 'nuxt',
        # Data / AI / ML
        'machine learning', 'deep learning', 'nlp', 'computer vision', 'tensorflow', 'pytorch',
        'keras', 'scikit-learn', 'pandas', 'numpy', 'matplotlib', 'seaborn', 'opencv',
        'data science', 'data analysis', 'data visualization', 'statistics',
        # Databases
        'sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'sqlite', 'oracle', 'cassandra',
        'elasticsearch', 'firebase',
        # Cloud / DevOps
        'aws', 'gcp', 'azure', 'docker', 'kubernetes', 'ci/cd', 'git', 'github', 'gitlab',
        'linux', 'bash', 'terraform', 'ansible', 'jenkins',
        # DSA / CS Fundamentals
        'data structures', 'algorithms', 'dynamic programming', 'graph algorithms', 'sorting',
        'searching', 'trees', 'linked list', 'stack', 'queue', 'hash map', 'recursion',
        # Soft Skills
        'communication', 'teamwork', 'leadership', 'problem solving', 'critical thinking',
        'time management', 'collaboration', 'agile', 'scrum',
        # System Design
        'system design', 'microservices', 'api', 'rest', 'graphql', 'websocket', 'message queue',
        'load balancing', 'caching', 'scalability', 'distributed systems',
    ]

    STRONG_ACTION_VERBS = [
        'developed', 'built', 'designed', 'implemented', 'optimized', 'automated', 'deployed',
        'architected', 'engineered', 'created', 'improved', 'increased', 'reduced', 'led',
        'managed', 'delivered', 'launched', 'integrated', 'migrated', 'scaled', 'streamlined',
        'collaborated', 'mentored', 'researched', 'analyzed', 'published', 'achieved',
    ]

    WEAK_ACTION_VERBS = [
        'worked', 'helped', 'assisted', 'did', 'made', 'used', 'tried', 'participated',
        'involved', 'part of', 'responsible for', 'duties included',
    ]
