
import streamlit as st
import pandas as pd

TRAIT_MULTIPLIERS = {
    "None": 1.0,
    "Bruiser": 1.8,
    "Invoker": 2.0,
    "Heavenly": 2.2,
    "Fated": 1.3,
    "Reaper": 1.5,
    "Dryad": 1.4,
    "Mythic": 1.6,
    "Dragonlord": 1.7
}

st.title("🧠 TFT Power Model Evaluator")

level = st.slider("Level", 1, 10, 6)
star3_units = st.number_input("Number of 3★ Units", min_value=0, step=1)
star2_units = st.number_input("Number of 2★ Units", min_value=0, step=1)
items = st.number_input("Number of Completed Items", min_value=0, step=1)

selected_traits = st.multiselect(
    "Select Active Traits (up to 3)",
    options=list(TRAIT_MULTIPLIERS.keys()),
    default=["Heavenly"]
)

augment_score = st.slider("Augment Strength Score (1–5)", 1, 5, 3)
trait_score = sum(TRAIT_MULTIPLIERS.get(trait, 1.0) for trait in selected_traits)

power_score = (
    3 * star3_units +
    2 * star2_units +
    1 * items +
    0.4 * level +
    1.5 * trait_score +
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
    st.write(f"Trait Score × 1.5 = {1.5 * trait_score:.2f}")
    st.write(f"Augment Score × 0.5 = {0.5 * augment_score}")
    for trait in selected_traits:
        st.write(f" - {trait} weight: {TRAIT_MULTIPLIERS[trait]}")

@st.cache_data
def load_comps():
    return pd.read_csv("meta_comps.csv")

comps_df = load_comps()
matching_comps = comps_df[comps_df['Core Traits'].apply(
    lambda traits: any(t in traits for t in selected_traits)
)]

st.subheader("🔍 Suggested Meta Comps Based on Your Traits:")
if not matching_comps.empty:
    st.dataframe(matching_comps)
else:
    st.write("No matching comps found. Try different traits.")
