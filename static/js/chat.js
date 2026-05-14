/* ===================================================
   CareerAI — chat.js
   Handles chat UI: message sending, rendering,
   typing indicators, markdown, auto-scroll
   =================================================== */

const chatMessages  = document.getElementById('chatMessages');
const chatInput     = document.getElementById('chatInput');
const sendBtn       = document.getElementById('sendBtn');
const typingIndicator = document.getElementById('typingIndicator');

// ─── Send Message ────────────────────────────────────
async function sendMessage() {
  const text = chatInput.value.trim();
  if (!text) return;

  // Disable input while processing
  setInputState(false);

  // Add user message to UI
  appendMessage('user', text);
  chatInput.value = '';
  autoResize(chatInput);

  // Show typing animation
  showTyping(true);

  try {
    const res = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: text }),
    });

    if (!res.ok) throw new Error('Server error: ' + res.status);

    const data = await res.json();
    showTyping(false);
    appendMessage('bot', data.response);
  } catch (err) {
    showTyping(false);
    appendMessage('bot', '⚠️ Sorry, something went wrong. Please try again.');
    console.error('Chat error:', err);
  } finally {
    setInputState(true);
    chatInput.focus();
  }
}

// ─── Send Quick Topic Message ────────────────────────
function sendQuickMessage(text) {
  chatInput.value = text;
  sendMessage();
}

// ─── Clear Chat History ──────────────────────────────
async function clearChat() {
  if (!confirm('Clear your entire chat history?')) return;
  try {
    await fetch('/api/chat/clear', { method: 'POST' });
    chatMessages.innerHTML = `
      <div class="message bot-message">
        <div class="msg-avatar">🤖</div>
        <div class="msg-bubble">
          Chat cleared! 🧹 How can I help you today?<br><br>
          Try asking: <em>"Give me a DSA roadmap for placements"</em>
        </div>
      </div>`;
  } catch (err) {
    alert('Could not clear chat. Please try again.');
  }
}

// ─── Append Message to Chat ──────────────────────────
function appendMessage(role, text) {
  const isBot = role === 'bot';
  const div = document.createElement('div');
  div.className = `message ${isBot ? 'bot-message' : 'user-message'}`;

  const avatar = document.createElement('div');
  avatar.className = 'msg-avatar';
  avatar.textContent = isBot ? '🤖' : '👤';

  const bubble = document.createElement('div');
  bubble.className = 'msg-bubble';

  if (isBot) {
    // Render markdown for bot messages
    bubble.innerHTML = window.CareerAI
      ? window.CareerAI.renderMarkdown(text)
      : text;
  } else {
    bubble.textContent = text;
  }

  div.appendChild(avatar);
  div.appendChild(bubble);
  chatMessages.appendChild(div);
  scrollToBottom();

  // Fade-in effect
  div.style.opacity = '0';
  div.style.transform = 'translateY(10px)';
  requestAnimationFrame(() => {
    div.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
    div.style.opacity = '1';
    div.style.transform = 'none';
  });
}

// ─── Typing Indicator ───────────────────────────────
function showTyping(show) {
  if (!typingIndicator) return;
  typingIndicator.classList.toggle('hidden', !show);
  if (show) scrollToBottom();
}

// ─── Scroll Chat to Bottom ───────────────────────────
function scrollToBottom() {
  if (chatMessages) {
    chatMessages.scrollTo({ top: chatMessages.scrollHeight, behavior: 'smooth' });
  }
}

// ─── Input State Toggle ──────────────────────────────
function setInputState(enabled) {
  if (chatInput) chatInput.disabled = !enabled;
  if (sendBtn)   sendBtn.disabled  = !enabled;
}

// ─── Handle Enter Key ────────────────────────────────
function handleChatKey(e) {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    sendMessage();
  }
}

// ─── Auto-resize Textarea ────────────────────────────
function autoResize(el) {
  el.style.height = 'auto';
  el.style.height = Math.min(el.scrollHeight, 160) + 'px';
}

// ─── Init ────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  // Scroll to bottom on load (to show latest messages)
  scrollToBottom();

  // Apply markdown to pre-loaded history messages
  document.querySelectorAll('.bot-message .msg-bubble').forEach(bubble => {
    const raw = bubble.textContent.trim();
    if (raw && window.CareerAI) {
      bubble.innerHTML = window.CareerAI.renderMarkdown(raw);
    }
  });

  // Focus input
  if (chatInput) chatInput.focus();
});
