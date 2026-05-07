import streamlit as st


def render_header_section():
    st.title("📊 Conflict Fatalities Dashboard")
    st.caption(
        "Fuente: B'Tselem · Israeli Information Center for Human Rights · 2000–2023"
    )
    st.markdown("---")