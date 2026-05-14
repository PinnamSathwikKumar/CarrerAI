# ⚡ CareerAI — AI-Powered Career Assistant for CSE Students

> A full-stack web platform that helps Computer Science students optimize their resumes, get AI career guidance, follow structured DSA roadmaps, and prepare for placements — all for free.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Flask](https://img.shields.io/badge/Flask-3.0-green)
![SQLite](https://img.shields.io/badge/Database-SQLite-orange)
![License](https://img.shields.io/badge/License-MIT-purple)

---

## 📸 Features

| Feature                  | Description                                                                                      |
| ------------------------ | ------------------------------------------------------------------------------------------------ |
| 📄 **ATS Resume Scorer** | Upload PDF/DOCX → instant ATS score (0-100) with keyword, verb, formatting, and contact analysis |
| 🤖 **AI Career Chatbot** | Keyword-based + optional OpenAI GPT career advisor for DSA, SQL, Python, ML roadmaps             |
| 🗺️ **DSA Roadmap**       | Topic-wise learning path, YouTube channels, practice platforms, daily plan                       |
| 📊 **User Dashboard**    | Score history, stats, quick actions, career tips                                                 |
| 🛡️ **Admin Panel**       | Manage DSA resources, view resume metadata, user stats, score distribution                       |

---

## 🗂️ Project Structure

```
career_ai/
│
├── app.py                  # Flask app factory & entry point
├── config.py               # All configuration, env vars, ATS keywords
├── requirements.txt        # Python dependencies
├── Procfile                # Gunicorn deployment command
├── runtime.txt             # Python version for hosting
├── .env.example            # Environment variable template
├── .gitignore
├── README.md
│
├── database/
│   ├── __init__.py
│   └── db.py               # SQLite init, schema, query helpers, seed data
│
├── routes/
│   ├── __init__.py
│   ├── auth.py             # Register, login, logout (user + admin)
│   ├── user.py             # Dashboard, resume upload, chat, DSA roadmap
│   ├── admin.py            # Admin dashboard, resource/suggestion management
│   └── api.py              # JSON endpoints for AJAX (chat, stats)
│
├── utils/
│   ├── __init__.py
│   ├── resume_parser.py    # PDF + DOCX text extraction
│   ├── ats_scorer.py       # 5-category ATS scoring engine
│   └── chatbot.py          # Keyword-based chatbot + OpenAI fallback
│
├── templates/
│   ├── base.html           # Base layout with navbar, flash messages, footer
│   ├── index.html          # Landing page
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html      # User dashboard
│   ├── resume_upload.html  # Upload form + history
│   ├── resume_result.html  # ATS score breakdown + suggestions
│   ├── chat.html           # Chat interface
│   ├── dsa_roadmap.html    # Tabbed roadmap page
│   ├── profile.html
│   └── admin/
│       ├── login.html
│       ├── dashboard.html
│       ├── resources.html
│       ├── edit_resource.html
│       ├── users.html
│       └── suggestions.html
│
└── static/
    ├── css/
    │   └── style.css       # Full dark-mode design system
    ├── js/
    │   ├── main.js         # Global UI (nav, flash, animations, markdown)
    │   ├── chat.js         # Chat send/receive/render
    │   └── resume.js       # Drag-drop upload, validation, loading
    └── uploads/            # Temporary upload directory (files deleted after analysis)
```

---

## 🚀 Quick Start (Local Development)

### Prerequisites

- Python 3.9+
- pip

### 1. Clone & Setup

```bash
git clone https://github.com/yourusername/career-ai.git
cd career_ai

# Create virtual environment
python -m venv venv
source venv/bin/activate      # Linux/Mac
venv\Scripts\activate         # Windows

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
```

Edit `.env`:

```env
SECRET_KEY=your-strong-secret-key-here
FLASK_DEBUG=True
ADMIN_EMAIL=admin@careerAI.com
ADMIN_PASSWORD=YourStrongPassword
# Optional: Add OpenAI key for GPT chatbot
# OPENAI_API_KEY=sk-...
```

### 3. Run

```bash
python app.py
```

Visit: **http://localhost:5000**

The database is auto-created on first run with seed DSA resources and the default admin account.

---

## 🔐 Default Credentials

| Role  | Email              | Password  |
| ----- | ------------------ | --------- |
| Admin | admin@careerAI.com | Admin@123 |

> **⚠️ Change these immediately** before any production deployment via the `.env` file.

---

## 🤖 AI Chatbot Modes

### Mode 1: Keyword-Based (Default, Free)

Works out of the box with no API keys. Covers:

- DSA roadmap, Python, SQL, System Design, AI/ML
- Resume tips, internship strategies
- Interview preparation

### Mode 2: OpenAI GPT-3.5 (Optional)

Set `OPENAI_API_KEY` in `.env` for more natural, context-aware responses.
Estimated cost: ~$0.002 per conversation (very cheap).

```env
OPENAI_API_KEY=sk-your-key-here
```

---

## 📊 ATS Scoring Breakdown

| Category     | Points  | What's Checked                     |
| ------------ | ------- | ---------------------------------- |
| Keywords     | 40      | 60+ tech skills, tools, frameworks |
| Action Verbs | 20      | Strong vs weak verb detection      |
| Formatting   | 20      | Headers, bullets, dates, structure |
| Length       | 10      | Optimal word count (300-700 words) |
| Contact Info | 10      | Email, phone, LinkedIn, GitHub     |
| **Total**    | **100** |                                    |

**Grades:** A (85+) • B (70+) • C (55+) • D (40+) • F (<40)

---

## 🌐 Deployment

### Option 1: Render (Recommended — Free Tier)

1. Push code to GitHub
2. Go to [render.com](https://render.com) → New Web Service
3. Connect GitHub repo
4. Settings:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
   - **Instance:** Free
5. Add environment variables under **Environment** tab:
   ```
   SECRET_KEY = <generate a strong key>
   ADMIN_EMAIL = your-admin@email.com
   ADMIN_PASSWORD = StrongPassword123
   OPENAI_API_KEY = (optional)
   ```
6. Deploy → your app is live!

> **Note:** Render free tier spins down after 15 minutes of inactivity. First request after sleep takes ~30 seconds.

---

### Option 2: Railway

1. Install Railway CLI: `npm i -g @railway/cli`
2. ```bash
   railway login
   railway init
   railway up
   ```
3. Set env vars:
   ```bash
   railway variables set SECRET_KEY=your-key
   railway variables set ADMIN_PASSWORD=StrongPass
   ```
4. Railway auto-detects `Procfile` and deploys.

> Railway gives $5 free credit/month which covers low-traffic apps.

---

### Option 3: PythonAnywhere (Free Tier)

1. Create account at [pythonanywhere.com](https://www.pythonanywhere.com)
2. Open a **Bash console** and:
   ```bash
   git clone https://github.com/yourusername/career-ai.git
   cd career_ai
   pip3 install --user -r requirements.txt
   ```
3. Go to **Web** tab → Add a new web app → Manual configuration → Python 3.11
4. Set **Source code:** `/home/yourusername/career_ai`
5. Edit the WSGI config file:
   ```python
   import sys
   sys.path.insert(0, '/home/yourusername/career_ai')
   from app import app as application
   ```
6. In **Web** → **Environment variables**: add your `.env` values
7. Hit **Reload**

> PythonAnywhere free tier: 1 web app, limited CPU seconds/day — perfect for personal projects.

---

### Option 4: Local Network (i3 Laptop / LAN)

Run the app accessible on your local network:

```bash
python app.py
# or
flask run --host=0.0.0.0 --port=5000
```

Access from other devices: `http://<your-ip>:5000`

---

## 🗄️ Database Tables

```sql
users          -- Student accounts
admins         -- Admin accounts
resumes        -- Resume metadata + ATS scores (no file stored)
dsa_resources  -- DSA topics, YouTube channels, platforms
suggestions    -- Career tips/suggestions
chat_history   -- Per-user chat messages
```

---

## 🔒 Security Features

- ✅ Passwords hashed with Werkzeug (PBKDF2-SHA256)
- ✅ Session-based authentication (Flask sessions)
- ✅ File type validation (whitelist: PDF, DOCX only)
- ✅ Max file size: 5 MB
- ✅ Secure filename (werkzeug `secure_filename`)
- ✅ Uploaded files deleted immediately after analysis
- ✅ Admin routes protected by separate session key
- ✅ SQL injection prevention via parameterized queries
- ✅ CSRF protection via same-site cookie policy

---

## ⚡ Performance (Low-RAM Optimizations)

- SQLite — zero-config, no separate server process
- No heavy ORM (raw `sqlite3` module)
- `pdfplumber` reads page-by-page (low memory)
- Files deleted immediately after processing
- Gunicorn with 2 sync workers (configurable via `Procfile`)
- No in-memory caching needed (SQLite is fast for this scale)

---

## 🛠️ Tech Stack

| Layer        | Technology                                 |
| ------------ | ------------------------------------------ |
| Backend      | Python 3.11 + Flask 3.0                    |
| Database     | SQLite (via Python sqlite3)                |
| PDF Parsing  | pdfplumber + PyPDF2 fallback               |
| DOCX Parsing | python-docx                                |
| AI           | Keyword engine + OpenAI GPT-3.5 (optional) |
| Frontend     | Vanilla HTML, CSS, JavaScript              |
| Fonts        | Space Grotesk + JetBrains Mono             |
| Deployment   | Gunicorn + Render/Railway/PythonAnywhere   |

---

## 📝 Development Notes

### Adding New Chat Topics

Edit `utils/chatbot.py` → `CAREER_KB` dictionary:

```python
'your_topic': {
    'keywords': ['keyword1', 'keyword2'],
    'response': """Your markdown response here"""
}
```

### Adding New ATS Keywords

Edit `config.py` → `TECH_KEYWORDS` list.

### Adding DSA Resources via Admin Panel

Login at `/admin/login` → Resources → Add Resource

---

## 🤝 Contributing

1. Fork the repo
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit: `git commit -m 'Add amazing feature'`
4. Push: `git push origin feature/amazing-feature`
5. Open a Pull Request

---

## 📄 License

MIT License — free to use, modify, and distribute.

---

## 💬 Support

- Open an issue on GitHub
- Email: pinnamsathwikkumar@gmail.com

---

_Built with ❤️ for CSE students aiming for their dream jobs._
