import requests
import streamlit as st

# ==============================================================================
# PAGE CONFIGURATION
# ==============================================================================
st.set_page_config(
    page_title="CampusAI",
    page_icon="🎓",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ==============================================================================
# MODERN CUSTOM CSS
# ==============================================================================
st.markdown("""
<style>
/* Modern Fluid Dark Background */
.stApp {
    background: radial-gradient(circle at 0% 0%, rgba(99, 102, 241, 0.12) 0%, transparent 35%),
                radial-gradient(circle at 100% 100%, rgba(139, 92, 246, 0.1) 0%, transparent 40%),
                #0b0f19;
    color: #f1f5f9;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
}

/* Hide Default UI elements cleanly */
#MainMenu, footer, header {
    visibility: hidden;
    display: none !important;
}

/* Main Content Container */
.block-container {
    max-width: 720px;
    padding-top: 3rem;
    padding-bottom: 5rem;
}

/* Clean Header Section */
.brand-container {
    text-align: center;
    margin-bottom: 2.5rem;
}

.brand-icon {
    font-size: 3rem;
    background: linear-gradient(135deg, #818cf8, #c084fc);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.5rem;
    display: inline-block;
}

.brand-title {
    font-size: 2.5rem;
    font-weight: 800;
    letter-spacing: -0.025em;
    margin: 0;
    background: linear-gradient(to right, #ffffff, #cbd5e1);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.brand-subtitle {
    font-size: 1rem;
    color: #94a3b8;
    margin-top: 0.5rem;
    margin-bottom: 1rem;
    font-weight: 400;
}

/* Status Badge */
.status-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    background: rgba(16, 185, 129, 0.06);
    border: 1px solid rgba(16, 185, 129, 0.15);
    padding: 0.35rem 0.85rem;
    border-radius: 100px;
    color: #34d399;
    font-size: 0.8rem;
    font-weight: 600;
    letter-spacing: 0.025em;
}

.status-dot {
    width: 6px;
    height: 6px;
    background-color: #34d399;
    border-radius: 50%;
    box-shadow: 0 0 12px #34d399;
}

/* Glassmorphic App Cards */
.ui-card {
    background: rgba(17, 24, 39, 0.7);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 20px;
    padding: 2rem;
    box-shadow: 0 20px 40px -15px rgba(0, 0, 0, 0.5);
    margin-bottom: 1.5rem;
}

.card-title {
    font-size: 1.25rem;
    font-weight: 700;
    color: #ffffff;
    margin-top: 0;
    margin-bottom: 0.25rem;
}

.card-subtitle {
    font-size: 0.9rem;
    color: #64748b;
    margin-bottom: 1.5rem;
}

/* Native Textarea Styling Overrides */
div[data-baseweb="textarea"] {
    background-color: rgba(15, 23, 42, 0.6) !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-radius: 14px !important;
    transition: all 0.2s ease !important;
}

div[data-baseweb="textarea"]:focus-within {
    border-color: #6366f1 !important;
    box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.15) !important;
}

/* Text color changed to an easily readable vibrant purple */
textarea {
    color: #6366f1 !important;
    font-size: 0.95rem !important;
}

/* Placeholder styling color adjusted for readability */
textarea::placeholder {
    color: #64748b !important;
}

/* Suggestion Pills / Tokens */
.suggestion-heading {
    font-size: 0.85rem;
    font-weight: 600;
    color: #475569;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-top: 1.5rem;
    margin-bottom: 0.75rem;
}

.suggestion-pill {
    background: rgba(30, 41, 59, 0.4);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 12px;
    padding: 0.75rem 1rem;
    margin-bottom: 0.5rem;
    color: #cbd5e1;
    font-size: 0.88rem;
    transition: all 0.2s ease;
    cursor: pointer;
}

.suggestion-pill:hover {
    background: rgba(99, 102, 241, 0.08);
    border-color: rgba(99, 102, 241, 0.3);
    color: #ffffff;
    transform: translateY(-1px);
}

/* Primary Accent Action Button */
.stButton > button {
    width: 100%;
    height: 3rem;
    background: linear-gradient(90deg, #5046e5, #6366f1);
    color: #ffffff !important;
    border: none !important;
    border-radius: 14px !important;
    font-size: 0.95rem !important;
    font-weight: 600 !important;
    box-shadow: 0 10px 25px -5px rgba(79, 70, 229, 0.4) !important;
    transition: all 0.2s ease !important;
    margin-top: 1rem;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 15px 30px -5px rgba(79, 70, 229, 0.5) !important;
    background: linear-gradient(90deg, #4f46e5, #4f46e5);
}

.stButton > button:active {
    transform: translateY(0);
}

/* Output Display Cards */
.output-card {
    background: rgba(15, 23, 42, 0.8);
    border-radius: 16px;
    padding: 1.5rem;
    border: 1px solid rgba(255, 255, 255, 0.06);
    margin-top: 1.5rem;
}

.output-heading {
    font-size: 0.9rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 0.75rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.heading-ans { color: #818cf8; }
.heading-src { color: #94a3b8; }

.source-item {
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.04);
    border-radius: 8px;
    padding: 0.5rem 0.75rem;
    margin-top: 0.5rem;
    font-size: 0.85rem;
    color: #94a3b8;
}
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# HEADER COMPONENT
# ==============================================================================
st.markdown(
    '<div class="brand-container">'
    '<div class="brand-icon">🎓</div>'
    '<div class="brand-title">CampusAI</div>'
    '<div class="brand-subtitle">Your intelligent college information assistant</div>'
    '<div class="status-badge"><span class="status-dot"></span>AI Assistant Online</div>'
    '</div>', 
    unsafe_allow_html=True
)

# ==============================================================================
# INPUT FORM CARD
# ==============================================================================
st.markdown(
    '<div class="ui-card">'
    '<div class="card-title">💬 Ask CampusAI</div>'
    '<div class="card-subtitle">Get quick answers from the official college document.</div>',
    unsafe_allow_html=True
)

question = st.text_area(
    "Your question",
    placeholder="Ask anything about the college...\n\nExample: What departments are available?",
    height=120,
    label_visibility="collapsed"
)

# Suggestion Grid
st.markdown('<div class="suggestion-heading">✨ Try asking</div>', unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    st.markdown('<div class="suggestion-pill">🏫 What AI and DS course list ?</div>', unsafe_allow_html=True)
    st.markdown('<div class="suggestion-pill">📚 What courses are availoable?</div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="suggestion-pill">🎯 What programme are available?</div>', unsafe_allow_html=True)
    st.markdown('<div class="suggestion-pill">👨‍🏫 Tell me about the lab course name.</div>', unsafe_allow_html=True)

ask_button = st.button("🚀 Ask CampusAI")
st.markdown('</div>', unsafe_allow_html=True)

# ==============================================================================
# CORE BACKEND LOGIC
# ==============================================================================
if ask_button:
    if not question.strip():
        st.warning("⚠️ Please enter a question first.")
    else:
        with st.spinner("🔎 Searching the college knowledge base..."):
            try:
                response = requests.post(
                    "http://127.0.0.1:5000/ask",
                    json={"question": question},
                    timeout=60
                )

                if response.status_code == 200:
                    result = response.json()

                    # Display Answer
                    st.markdown(
                        '<div class="output-card">'
                        '<div class="output-heading heading-ans">🤖 CampusAI Answer</div>',
                        unsafe_allow_html=True
                    )

                    st.write(result["answer"])
                    st.markdown('</div>', unsafe_allow_html=True)

                    # Display Sources
                    st.markdown(
                        '<div class="output-card">'
                        '<div class="output-heading heading-src">📚 Information Sources</div>',
                        unsafe_allow_html=True
                    )

                    for page in result.get("sources", []):
                        st.markdown(
                            f'<div class="source-item">📄 College Document — Page {page}</div>',
                            unsafe_allow_html=True
                        )

                    st.markdown('</div>', unsafe_allow_html=True)

                else:
                    try:
                        error_message = response.json().get(
                            "error",
                            "Something went wrong."
                        )
                    except Exception:
                        error_message = "Something went wrong with the backend."

                    st.error(f"❌ {error_message}")

            except requests.exceptions.ConnectionError:
                st.error("🔴 Cannot connect to the Flask backend.")
                st.info(
                    "Make sure your Flask app.py is running on "
                    "http://127.0.0.1:5000"
                )

            except Exception as e:
                st.error(f"❌ An unexpected error occurred: {str(e)}")