import streamlit as st
from PIL import Image
import pandas as pd
import requests
from io import BytesIO

# Set wide layout
st.set_page_config(layout="wide")

# --- Language Toggle ---
language = st.selectbox("Language / ভাষা", ["English", "বাংলা"])

# Labels
labels = {
    "title": "Voter Table | ভোট দিন" if language == "বাংলা" else "Voter Table | Vote Now",
    "bnp": "বিএনপি" if language == "বাংলা" else "BNP",
    "jamaat": "জামায়াতে ইসলামী" if language == "বাংলা" else "Jamaat e Islami",
    "ncp": "এনসিপি" if language == "বাংলা" else "NCP",
    "vote_bnp": "ভোট দিন বিএনপি" if language == "বাংলা" else "Vote BNP",
    "vote_jamaat": "ভোট দিন জামায়াতে ইসলামী" if language == "বাংলা" else "Vote Jamaat e Islami",
    "vote_ncp": "ভোট দিন এনসিপি" if language == "বাংলা" else "Vote NCP",
    "thank_you": "ভোট দেওয়ার জন্য ধন্যবাদ!" if language == "বাংলা" else "Thank you for voting!",
    "live_vote": "বর্তমান ভোটের হিসাব" if language == "বাংলা" else "Live Vote Count"
}

# Title
st.markdown(f"<h2 style='text-align: center;'>{labels['title']}</h2>", unsafe_allow_html=True)

# Initialize vote counts in session state
if "votes" not in st.session_state:
    st.session_state.votes = {"BNP": 0, "Jamaat": 0, "NCP": 0}

# --- Image Paths ---
bnp_img_path = "https://upload.wikimedia.org/wikipedia/en/f/f0/Bangladesh_Nationalist_Party_logo.jpeg"
jamaat_img_path = "https://upload.wikimedia.org/wikipedia/commons/0/04/Bangladesh_Jamaat-e-_Islami_Logo_%28cropped%29.png"
ncp_img_path = "https://upload.wikimedia.org/wikipedia/en/0/0d/NCP_LOGO.png"
IMAGE_SIZE = (150, 150)

# --- Load Images (Support URLs) ---
def load_image(path_or_url):
    try:
        if path_or_url.startswith("http://") or path_or_url.startswith("https://"):
            response = requests.get(path_or_url)
            response.raise_for_status()
            img = Image.open(BytesIO(response.content)).convert("RGBA").resize(IMAGE_SIZE)
        else:
            img = Image.open(path_or_url).convert("RGBA").resize(IMAGE_SIZE)
        return img
    except Exception as e:
        st.error(f"Error loading image: {e}")
        return None

# --- Layout: 3 Columns ---
c1, c2, c3 = st.columns(3)

# --- BNP ---
with c1:
    st.markdown(f"<h4>{labels['bnp']}</h4>", unsafe_allow_html=True)
    img = load_image(bnp_img_path)
    if img:
        st.image(img, use_container_width=True)
    if st.button(labels["vote_bnp"], key="vote_bnp"):
        st.session_state.votes["BNP"] += 1
        st.toast(labels["thank_you"], icon="🗳️")

# --- Jamaat e Islami ---
with c2:
    st.markdown(f"<h4>{labels['jamaat']}</h4>", unsafe_allow_html=True)
    img = load_image(jamaat_img_path)
    if img:
        st.image(img, use_container_width=True)
    if st.button(labels["vote_jamaat"], key="vote_jamaat"):
        st.session_state.votes["Jamaat"] += 1
        st.toast(labels["thank_you"], icon="🗳️")

# --- NCP ---
with c3:
    st.markdown(f"<h4>{labels['ncp']}</h4>", unsafe_allow_html=True)
    img = load_image(ncp_img_path)
    if img:
        st.image(img, use_container_width=True)
    if st.button(labels["vote_ncp"], key="vote_ncp"):
        st.session_state.votes["NCP"] += 1
        st.toast(labels["thank_you"], icon="🗳️")

# --- Live Vote Count ---
st.divider()
st.subheader(f"📊 {labels['live_vote']}")

# Table view
for party, votes in st.session_state.votes.items():
    st.write(f"✅ {party}: {votes} votes")

# --- Bar Chart ---
df = pd.DataFrame({
    "Party": list(st.session_state.votes.keys()),
    "Votes": list(st.session_state.votes.values())
})
st.bar_chart(df.set_index("Party"))

# --- CSS Styling ---
st.markdown("""
<style>
html, body, [class*="css"]  {
    font-size: 15px !important;
}

h1, h2, h3, h4 {
    font-size: 18px !important;
    margin-bottom: 10px;
    text-align: center;
}

/* Custom vote button colors */
button[data-testid="baseButton"][aria-label="Vote BNP"] {
    background-color: #3498db !important;
    color: white !important;
}
button[data-testid="baseButton"][aria-label="Vote Jamaat e Islami"] {
    background-color: #2ecc71 !important;
    color: white !important;
}
button[data-testid="baseButton"][aria-label="Vote NCP"] {
    background-color: #e74c3c !important;
    color: white !important;
}

/* Mobile responsiveness */
@media only screen and (max-width: 600px) {
    .block-container {
        padding: 0.5rem 0.5rem !important;
    }
    button[kind="secondary"] {
        font-size: 16px !important;
    }
}
</style>
""", unsafe_allow_html=True)
