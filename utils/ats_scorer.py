"""
ATS Scoring Engine
Analyzes resume text and produces an ATS-style score with detailed feedback.
No external AI API required - uses keyword matching, heuristics, and NLP rules.
"""

import re
import json
from config import Config


def score_resume(text: str) -> dict:
    """
    Main scoring function. Returns a comprehensive analysis dict.
    Score breakdown:
      - Keyword coverage    : 40 points
      - Action verbs        : 20 points
      - Formatting signals  : 20 points
      - Length/density      : 10 points
      - Contact info        : 10 points
    Total: 100 points
    """
    text_lower = text.lower()
    result = {}

    # 1. Keyword analysis (40 pts)
    keyword_data = _analyze_keywords(text_lower)
    result.update(keyword_data)

    # 2. Action verb analysis (20 pts)
    verb_data = _analyze_action_verbs(text_lower)
    result.update(verb_data)

    # 3. Formatting signals (20 pts)
    format_data = _analyze_formatting(text)
    result.update(format_data)

    # 4. Length / density (10 pts)
    length_data = _analyze_length(text)
    result.update(length_data)

    # 5. Contact info (10 pts)
    contact_data = _analyze_contact(text)
    result.update(contact_data)

    # Total score
    total = (
        result.get('keyword_score', 0) +
        result.get('verb_score', 0) +
        result.get('format_score', 0) +
        result.get('length_score', 0) +
        result.get('contact_score', 0)
    )
    result['total_score'] = min(total, 100)
    result['grade'] = _score_to_grade(result['total_score'])
    result['suggestions'] = _generate_suggestions(result)
    result['skills_found'] = json.dumps(result.get('matched_keywords', []))
    result['missing_keywords'] = json.dumps(result.get('top_missing', []))
    result['weak_verbs_found'] = json.dumps(result.get('weak_verbs', []))

    return result


def _analyze_keywords(text_lower: str) -> dict:
    """Check how many tech keywords appear in resume."""
    all_keywords = [k.lower() for k in Config.TECH_KEYWORDS]
    matched = [kw for kw in all_keywords if kw in text_lower]
    missing = [kw for kw in all_keywords if kw not in text_lower]

    # Score: each keyword worth up to 40 pts total
    coverage = len(matched) / max(len(all_keywords), 1)
    score = min(int(coverage * 80), 40)   # scale to 40 max

    # Top 10 missing keywords that are most impactful
    priority_missing = [kw for kw in [
        'python', 'sql', 'git', 'data structures', 'algorithms',
        'machine learning', 'system design', 'api', 'docker', 'aws',
        'react', 'javascript', 'linux', 'agile', 'communication'
    ] if kw not in text_lower][:10]

    return {
        'matched_keywords': matched[:20],      # Show top 20 matched
        'keyword_count': len(matched),
        'total_keywords': len(all_keywords),
        'top_missing': priority_missing,
        'keyword_score': score,
    }


def _analyze_action_verbs(text_lower: str) -> dict:
    """Check for strong vs weak action verbs."""
    strong = Config.STRONG_ACTION_VERBS
    weak = Config.WEAK_ACTION_VERBS

    found_strong = [v for v in strong if v in text_lower]
    found_weak = [v for v in weak if v in text_lower]

    # Score: reward strong, penalize weak
    strong_score = min(len(found_strong) * 2, 18)
    weak_penalty = len(found_weak) * 3
    score = max(strong_score - weak_penalty, 0)
    score = min(score, 20)

    verb_suggestions = []
    if found_weak:
        verb_suggestions.append(f"Replace weak phrases ({', '.join(found_weak[:3])}) with action verbs")
    if len(found_strong) < 4:
        verb_suggestions.append("Add more strong action verbs: developed, optimized, architected, deployed")

    return {
        'strong_verbs': found_strong,
        'weak_verbs': found_weak,
        'verb_score': score,
        'verb_suggestions': verb_suggestions,
    }


def _analyze_formatting(text: str) -> dict:
    """
    Infer formatting quality from text signals.
    Looks for consistent structure indicators.
    """
    score = 0
    issues = []

    # Check for section headers (ALL CAPS or Title Case patterns)
    caps_headers = len(re.findall(r'\n[A-Z][A-Z ]{3,}\n', text))
    if caps_headers >= 2:
        score += 5
    else:
        issues.append("Use clear section headers (EDUCATION, EXPERIENCE, SKILLS)")

    # Check for bullet points (•, -, *, ▪)
    bullets = len(re.findall(r'[\•\-\*\▪\➤]', text))
    if bullets >= 3:
        score += 5
    else:
        issues.append("Add bullet points to describe experience and achievements")

    # Check for dates (year patterns)
    dates = len(re.findall(r'\b(19|20)\d{2}\b', text))
    if dates >= 2:
        score += 5
    else:
        issues.append("Include dates for education and work experience")

    # Penalize very long lines (wall-of-text)
    lines = text.split('\n')
    long_lines = sum(1 for l in lines if len(l) > 200)
    if long_lines == 0:
        score += 5
    else:
        issues.append("Break up long paragraphs into concise bullet points")

    return {
        'format_score': min(score, 20),
        'format_issues': issues,
    }


def _analyze_length(text: str) -> dict:
    """Optimal resume length: 300-700 words."""
    words = len(text.split())
    score = 0
    issue = None

    if 300 <= words <= 700:
        score = 10
    elif words < 300:
        score = 5
        issue = f"Resume is too short ({words} words). Add more detail to your experience and skills."
    elif 700 < words <= 900:
        score = 8
        issue = f"Resume is slightly long ({words} words). Consider trimming older experience."
    else:
        score = 5
        issue = f"Resume is too long ({words} words). Recruiters prefer 1-page resumes. Keep it under 700 words."

    return {
        'word_count': words,
        'length_score': score,
        'length_issue': issue,
    }


def _analyze_contact(text: str) -> dict:
    """Check for contact information completeness."""
    score = 0
    missing = []

    has_email = bool(re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text))
    has_phone = bool(re.search(r'(\+?\d[\d\s\-]{8,})', text))
    has_linkedin = 'linkedin' in text.lower()
    has_github = 'github' in text.lower()

    if has_email:
        score += 3
    else:
        missing.append('email address')
    if has_phone:
        score += 3
    else:
        missing.append('phone number')
    if has_linkedin:
        score += 2
    else:
        missing.append('LinkedIn profile URL')
    if has_github:
        score += 2
    else:
        missing.append('GitHub profile URL')

    return {
        'contact_score': score,
        'contact_missing': missing,
        'has_email': has_email,
        'has_phone': has_phone,
        'has_linkedin': has_linkedin,
        'has_github': has_github,
    }


def _score_to_grade(score: int) -> dict:
    """Convert numeric score to letter grade and feedback."""
    if score >= 85:
        return {'letter': 'A', 'label': 'Excellent', 'color': '#00ff88'}
    elif score >= 70:
        return {'letter': 'B', 'label': 'Good', 'color': '#00d4ff'}
    elif score >= 55:
        return {'letter': 'C', 'label': 'Average', 'color': '#ffd700'}
    elif score >= 40:
        return {'letter': 'D', 'label': 'Below Average', 'color': '#ff8c00'}
    else:
        return {'letter': 'F', 'label': 'Needs Work', 'color': '#ff4444'}


def _generate_suggestions(result: dict) -> list:
    """Compile all improvement suggestions into a prioritized list."""
    suggestions = []

    # Contact suggestions
    for item in result.get('contact_missing', []):
        suggestions.append({
            'priority': 'high',
            'icon': '📞',
            'title': f'Add {item}',
            'detail': f'Include your {item} at the top of the resume for recruiters to contact you.'
        })

    # Keyword suggestions
    missing = result.get('top_missing', [])
    if missing:
        suggestions.append({
            'priority': 'high',
            'icon': '🔑',
            'title': 'Add missing technical keywords',
            'detail': f"Add relevant skills: {', '.join(missing[:6])}. Tailor keywords to the job description."
        })

    # Verb suggestions
    for s in result.get('verb_suggestions', []):
        suggestions.append({
            'priority': 'medium',
            'icon': '💪',
            'title': 'Strengthen action verbs',
            'detail': s
        })

    # Formatting
    for issue in result.get('format_issues', []):
        suggestions.append({
            'priority': 'medium',
            'icon': '📋',
            'title': 'Improve formatting',
            'detail': issue
        })

    # Length
    if result.get('length_issue'):
        suggestions.append({
            'priority': 'low',
            'icon': '📏',
            'title': 'Adjust resume length',
            'detail': result['length_issue']
        })

    # GitHub / LinkedIn
    if not result.get('has_github'):
        suggestions.append({
            'priority': 'medium',
            'icon': '🐙',
            'title': 'Add GitHub profile',
            'detail': 'Include your GitHub URL to showcase projects. Upload at least 3-5 projects with READMEs.'
        })
    if not result.get('has_linkedin'):
        suggestions.append({
            'priority': 'medium',
            'icon': '💼',
            'title': 'Add LinkedIn profile',
            'detail': 'LinkedIn is checked by 90% of recruiters. Add your profile URL to the resume.'
        })

    return suggestions
