import streamlit as st
from database import get_ranking_desc, set_ranking_desc, re_score_all

st.title("Update Ranking Description")

current_ranking_desc = get_ranking_desc()
ranking_input = st.text_area("Set Ranking Description", value=current_ranking_desc, height=200)
if st.button("Update Ranking Description"):
    set_ranking_desc(ranking_input)
    re_score_all(ranking_input)
    st.success("Ranking description updated and all leads re-scored.")
