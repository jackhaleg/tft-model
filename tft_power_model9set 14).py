
import streamlit as st
import pandas as pd
import os

TRAIT_MULTIPLIERS = {
    "BoomBot": 1.9,
    "Cybernetic": 1.6,
    "CyberBoss": 2.0,
    "Techie": 1.7,
    "Strategist": 1.6,
    "Bastion": 1.5,
    "Bruiser": 1.8,
    "Marksman": 1.7,
    "Executioner": 1.6,
    "Rapidfire": 1.5,
    "Slayer": 1.6,
    "Sentinel": 1.5,
    "Arcanist": 1.8,
    "Support": 1.4
}

def calculate_synergy_bonus(trait_counts):
    bonus = 0
    for trait, count in trait_counts.items():
        if count >= 2:
            multiplier = TRAIT_MULTIPLIERS.get(trait, 1.0)
            bonus += multiplier * (count ** 0.8)
    return round(bonus, 2)

st.title("🧠 TFT Set 14 (Cyber City) Power Model + Synergy Evaluator")

level = st.slider("Level", 1, 10, 6)
star3_units = st.number_input("Number of 3★ Units", min_value=0, step=1)
star2_units = st.number_input("Number of 2★ Units", min_value=0, step=1)
items = st.number_input("Number of Completed Items", min_value=0, step=1)

st.markdown("### 🧩 Enter Trait Counts From Your Team (Set 14 only)")
trait_counts = {}
for trait in TRAIT_MULTIPLIERS:
    count = st.number_input(f"{trait} count", min_value=0, step=1, key=trait)
    if count > 0:
        trait_counts[trait] = count

synergy_bonus = calculate_synergy_bonus(trait_counts)
augment_score = st.slider("Augment Strength Score (1–5)", 1, 5, 3)

power_score = (
    3 * star3_units +
    2 * star2_units +
    1 * items +
    0.4 * level +
    1.5 * synergy_bonus +
    0.5 * augment_score
)

if power_score < 15:
    zone = "🔴 Weak - Consider rolling or stabilizing"
elif power_score < 25:
    zone = "🟡 Average - Scout and consider streaking or egoing"
else:
    zone = "🟢 Strong - Push tempo or econ up"

st.markdown(f"### Power Score: `{power_score:.1f}`")
st.markdown(f"### Status: **{zone}**")

with st.expander("Show Score Breakdown"):
    st.write(f"3★ Units × 3 = {3 * star3_units}")
    st.write(f"2★ Units × 2 = {2 * star2_units}")
    st.write(f"Items × 1 = {items}")
    st.write(f"Level × 0.4 = {0.4 * level}")
    st.write(f"Synergy Bonus × 1.5 = {1.5 * synergy_bonus}")
    st.write(f"Augment Score × 0.5 = {0.5 * augment_score}")
    for trait, count in trait_counts.items():
        st.write(f" - {trait}: {count} units")

@st.cache_data
def load_comps():
    path = os.path.join(os.path.dirname(__file__), "meta_comps.csv")
    return pd.read_csv(path)

comps_df = load_comps()
matching_comps = comps_df[comps_df['Core Traits'].apply(
    lambda traits: any(t in traits for t in trait_counts.keys())
)]

# Champion role table
st.markdown("### 🧙 Champion Role Categories (Set 14 - Cyber City)")
st.markdown("""
| Role         | Description                                      | Example Champions           |
|--------------|--------------------------------------------------|-----------------------------|
| **Tank**     | Durable frontline units                          | Sejuani, Thresh, Shen       |
| **Carry**    | Primary item holders and damage sources          | Zeri, Aphelios, Samira      |
| **Support**  | Utility casters that shield, heal, or CC         | Janna, Lulu, Bard           |
| **Assassin** | Dive burst units targeting backline              | Qiyana, Talon, Katarina     |
| **Flex**     | Can pivot into multiple comps or roles           | Ekko, Mordekaiser, Urgot    |
""")

st.subheader("🔍 Suggested Meta Comps Based on Your Traits:")
if not matching_comps.empty:
    st.dataframe(matching_comps)
else:
    st.write("No matching comps found. Try different traits.")
