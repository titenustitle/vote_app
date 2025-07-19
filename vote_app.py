import streamlit as st
import pandas as pd
import json
import os

# File to store persistent vote data
VOTE_FILE = "votes.json"

# Set wide layout
st.set_page_config(layout="wide")

# --- Language Toggle ---
language = st.selectbox("Language / ভাষা", ["English", "বাংলা"])

# --- Labels ---
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

# --- Load Votes from File ---
def load_votes():
    if os.path.exists(VOTE_FILE):
        with open(VOTE_FILE, "r") as f:
            return json.load(f)
    else:
        return {"BNP": 0, "Jamaat": 0, "NCP": 0}

# --- Save Votes to File ---
def save_votes(votes):
    with open(VOTE_FILE, "w") as f:
        json.dump(votes, f)

# Load votes at app start
votes = load_votes()

# --- UI Layout ---
st.markdown(f"<h2 style='text-align: center;'>{labels['title']}</h2>", unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)

# --- BNP ---
with c1:
    st.markdown(f"<h4>{labels['bnp']}</h4>", unsafe_allow_html=True)
    if st.button(labels["vote_bnp"]):
        votes["BNP"] += 1
        save_votes(votes)
        st.toast(labels["thank_you"], icon="🗳️")

# --- Jamaat ---
with c2:
    st.markdown(f"<h4>{labels['jamaat']}</h4>", unsafe_allow_html=True)
    if st.button(labels["vote_jamaat"]):
        votes["Jamaat"] += 1
        save_votes(votes)
        st.toast(labels["thank_you"], icon="🗳️")

# --- NCP ---
with c3:
    st.markdown(f"<h4>{labels['ncp']}</h4>", unsafe_allow_html=True)
    if st.button(labels["vote_ncp"]):
        votes["NCP"] += 1
        save_votes(votes)
        st.toast(labels["thank_you"], icon="🗳️")

# --- Display Live Vote Count ---
st.divider()
st.subheader(f"📊 {labels['live_vote']}")

for party, count in votes.items():
    st.write(f"✅ {party}: {count} votes")

# --- Chart ---
df = pd.DataFrame({"Party": list(votes.keys()), "Votes": list(votes.values())})
st.bar_chart(df.set_index("Party"))

# --- Optional Styling ---
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
button[data-testid="baseButton"] {
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)
