
import streamlit as st
import pandas as pd
import os

TRAIT_MULTIPLIERS = {
    "Anima Squad": 1.8,
    "BoomBots": 1.9,
    "Cybernetic": 1.6,
    "Cyberboss": 2.0,
    "Cypher": 1.7,
    "Divinicorp": 1.7,
    "Exotech": 1.8,
    "Executioner": 1.6,
    "Rapidfire": 1.5,
    "Slayer": 1.6,
    "Strategist": 1.6,
    "Techie": 1.7,
    "Bastion": 1.5,
    "Bruiser": 1.8,
    "Marksman": 1.7
}

def calculate_synergy_bonus(counts):
    bonus = 0
    for t, c in counts.items():
        if c >= 2:
            bonus += TRAIT_MULTIPLIERS[t] * (c ** 0.8)
    return round(bonus, 2)

st.title("🧠 TFT Set 14 (Cyber City) Power + Synergy Evaluator")

level = st.slider("Level", 1, 10, 6)
s3 = st.number_input("3★ Units", min_value=0, step=1)
s2 = st.number_input("2★ Units", min_value=0, step=1)
items = st.number_input("Completed Items", min_value=0, step=1)

st.markdown("### Enter Trait Counts (for live Set 14)")
counts = {}
for trait in TRAIT_MULTIPLIERS:
    c = st.number_input(f"{trait} count", 0, 10, 0, key=trait)
    if c > 0:
        counts[trait] = c

synergy = calculate_synergy_bonus(counts)
augment = st.slider("Augment Score (1–5)", 1, 5, 3)

power = 3*s3 + 2*s2 + items + 0.4*level + 1.5*synergy + 0.5*augment
zone = "🔴 Weak" if power < 15 else "🟡 Average" if power < 25 else "🟢 Strong"

st.markdown(f"**Power Score:** `{power:.1f}` — **{zone}**")
with st.expander("Score Breakdown"):
    st.write(f"3★ units = {3*s3}")
    st.write(f"2★ units = {2*s2}")
    st.write(f"Items = {items}")
    st.write(f"Level = {0.4*level:.1f}")
    st.write(f"Synergy bonus = {1.5*synergy:.2f}")
    st.write(f"Augment = {0.5*augment}")
    st.write("Trait counts:", counts.items())

@st.cache_data
def load_comps():
    return pd.read_csv(os.path.join(os.path.dirname(__file__), "meta_comps.csv"))

df = load_comps()
matches = df[df['Core Traits'].apply(
    lambda t: any(tr in t for tr in counts.keys())
)]
st.subheader("🔍 Suggested Meta Comps")
st.dataframe(matches if not matches.empty else "No comps match traits entered.")
