
import streamlit as st

from src.stats.compute_descriptive_stats import compute_descriptive_stats
from src.stats.export_stats_to_json import export_stats_to_json


def render_stats_section(df_filtrado):
    st.subheader("📊 Estadísticas Descriptivas")

    try:
        stats = compute_descriptive_stats(df_filtrado)

        col_s1, col_s2, col_s3 = st.columns(3)

        with col_s1:
            st.metric("Edad media", f"{stats['age_stats']['mean']:.1f}")

        with col_s2:
            st.metric("Edad mediana", f"{stats['age_stats']['median']:.1f}")

        with col_s3:
            st.metric("% Menores", f"{stats['pct_minors']:.1f}%")

        if st.button("💾 Exportar estadísticas a JSON"):
            path = export_stats_to_json(stats)
            st.success(f"Guardado en: {path}")

    except NotImplementedError:
        st.info("⚙️ feature/pipeline: compute_descriptive_stats pendiente")


