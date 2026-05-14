"""
Database module - SQLite setup, schema creation, and helper utilities
Uses sqlite3 directly (no ORM) to stay lightweight on low-RAM machines
"""

import sqlite3
import os
from werkzeug.security import generate_password_hash
from flask import current_app, g


def get_db():
    """Get database connection, stored on Flask's g object for request lifetime."""
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE_PATH'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row  # Return dict-like rows
    return g.db


def close_db(e=None):
    """Close database connection at end of request."""
    db = g.pop('db', None)
    if db is not None:
        db.close()


def init_db():
    """Create all tables if they don't exist."""
    db_path = current_app.config['DATABASE_PATH']
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # --- Users table ---
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            college TEXT,
            year TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # --- Admin table ---
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS admins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # --- Resumes metadata table (no file stored permanently) ---
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS resumes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            filename TEXT NOT NULL,
            ats_score INTEGER,
            word_count INTEGER,
            skills_found TEXT,          -- JSON string
            missing_keywords TEXT,      -- JSON string
            weak_verbs_found TEXT,      -- JSON string
            suggestions TEXT,           -- JSON string
            uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    ''')

    # --- DSA Resources table ---
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS dsa_resources (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,         -- 'topic', 'youtube', 'platform', 'book'
            title TEXT NOT NULL,
            description TEXT,
            url TEXT,
            difficulty TEXT,                -- 'beginner', 'intermediate', 'advanced'
            order_index INTEGER DEFAULT 0,
            is_active INTEGER DEFAULT 1,
            added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # --- Suggestions / Tips table ---
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS suggestions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,         -- 'resume', 'interview', 'career', 'dsa'
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            is_active INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # --- Chat history (lightweight, per session) ---
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            role TEXT NOT NULL,             -- 'user' or 'assistant'
            message TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    ''')

    conn.commit()
    conn.close()
    _seed_dsa_resources(db_path)


def seed_admin():
    """Create default admin account if it doesn't exist."""
    from config import Config
    db_path = current_app.config['DATABASE_PATH']
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('SELECT id FROM admins WHERE email = ?', (Config.ADMIN_DEFAULT_EMAIL,))
    if not cursor.fetchone():
        cursor.execute(
            'INSERT INTO admins (email, password_hash) VALUES (?, ?)',
            (Config.ADMIN_DEFAULT_EMAIL, generate_password_hash(Config.ADMIN_DEFAULT_PASSWORD))
        )
        conn.commit()
    conn.close()


def query_db(query, args=(), one=False):
    """Execute a SELECT query and return results."""
    db = get_db()
    cur = db.execute(query, args)
    rv = cur.fetchall()
    return (rv[0] if rv else None) if one else rv


def execute_db(query, args=()):
    """Execute INSERT/UPDATE/DELETE and commit."""
    db = get_db()
    cur = db.execute(query, args)
    db.commit()
    return cur.lastrowid


def _seed_dsa_resources(db_path):
    """Seed default DSA resources if table is empty."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM dsa_resources')
    count = cursor.fetchone()[0]

    if count == 0:
        resources = [
            # Topics - Beginner
            ('topic', 'Arrays & Strings', 'Foundation of coding interviews. Master traversal, sliding window, two pointers.', 'https://leetcode.com/tag/array/', 'beginner', 1),
            ('topic', 'Linked Lists', 'Singly, doubly, circular lists. Reversal, cycle detection, merge operations.', 'https://leetcode.com/tag/linked-list/', 'beginner', 2),
            ('topic', 'Stacks & Queues', 'LIFO/FIFO structures. Monotonic stacks, BFS queues, deques.', 'https://leetcode.com/tag/stack/', 'beginner', 3),
            ('topic', 'Recursion & Backtracking', 'Tree of choices. Subsets, permutations, N-Queens, Sudoku solver.', 'https://leetcode.com/tag/backtracking/', 'intermediate', 4),
            ('topic', 'Trees & BST', 'Binary trees, BST operations, tree DP, LCA, diameter problems.', 'https://leetcode.com/tag/tree/', 'intermediate', 5),
            ('topic', 'Graphs & BFS/DFS', 'Grid problems, topological sort, Dijkstra, Union-Find, cycle detection.', 'https://leetcode.com/tag/graph/', 'intermediate', 6),
            ('topic', 'Dynamic Programming', 'Memoization vs tabulation. 0/1 knapsack, LCS, LIS, coin change.', 'https://leetcode.com/tag/dynamic-programming/', 'advanced', 7),
            ('topic', 'Heaps & Priority Queue', 'Min/max heaps. Top-K problems, median finder, merge K lists.', 'https://leetcode.com/tag/heap-priority-queue/', 'intermediate', 8),
            ('topic', 'Binary Search', 'Search on answer technique, rotated arrays, matrix search.', 'https://leetcode.com/tag/binary-search/', 'intermediate', 9),
            ('topic', 'Sorting Algorithms', 'Merge sort, quick sort, counting sort, custom comparators.', 'https://en.wikipedia.org/wiki/Sorting_algorithm', 'beginner', 10),
            # YouTube channels
            ('youtube', 'NeetCode', 'Best structured DSA explanations with visual animations. 150-problem roadmap.', 'https://youtube.com/@NeetCode', 'intermediate', 1),
            ('youtube', 'Abdul Bari', 'Deep algorithm theory with proofs. Perfect for university exam prep.', 'https://youtube.com/@abdul_bari', 'intermediate', 2),
            ('youtube', 'William Fiset', 'Graph algorithms, advanced data structures in depth.', 'https://youtube.com/@WilliamFiset-videos', 'advanced', 3),
            ('youtube', 'Striver (takeUForward)', 'SDE Sheet walkthrough, comprehensive placement prep.', 'https://youtube.com/@takeUforward', 'intermediate', 4),
            ('youtube', 'Aditya Verma (DP Series)', 'Best DP series on YouTube. Pattern-based approach to DP.', 'https://youtube.com/@adityaverma', 'intermediate', 5),
            ('youtube', 'CS Dojo', 'Beginner-friendly, clear explanations of fundamentals.', 'https://youtube.com/@CSDojo', 'beginner', 6),
            # Platforms
            ('platform', 'LeetCode', 'Industry standard. 2000+ problems. Company-tagged questions. Contest platform.', 'https://leetcode.com', 'intermediate', 1),
            ('platform', 'Codeforces', 'Competitive programming. Rated contests every week. Improves speed.', 'https://codeforces.com', 'advanced', 2),
            ('platform', 'GeeksForGeeks', 'Theory + practice. Company-specific interview questions. Articles.', 'https://geeksforgeeks.org', 'beginner', 3),
            ('platform', 'HackerRank', 'Good for beginners. Domain-based certifications. Coding interviews.', 'https://hackerrank.com', 'beginner', 4),
            ('platform', 'Coding Ninjas', 'Structured courses + problems. Topic-wise learning path.', 'https://codingninjas.com', 'beginner', 5),
            ('platform', 'InterviewBit', 'Company interview preparation. Timed problems. Scaler community.', 'https://interviewbit.com', 'intermediate', 6),
        ]
        cursor.executemany(
            'INSERT INTO dsa_resources (category, title, description, url, difficulty, order_index) VALUES (?,?,?,?,?,?)',
            resources
        )
        conn.commit()
    conn.close()
