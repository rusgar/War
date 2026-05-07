# src/sections/render_filtered_data_section.py

import streamlit as st


def render_filtered_data_section(df, df_original):
    st.subheader("🔎 Datos Filtrados")
    st.caption(f"{len(df):,} registros mostrados de {len(df_original):,} totales")

    cols_display = [
        "name",
        "date_of_event",
        "age",
        "gender",
        "citizenship",
        "event_location_region",
        "type_of_injury",
        "killed_by",
    ]
    available = [c for c in cols_display if c in df.columns]

    st.dataframe(
        df[available].reset_index(drop=True),
        use_container_width=True,
        height=350,
    )

    st.download_button(
        label="⬇️ Descargar datos filtrados (CSV)",
        data=df[available].to_csv(index=False).encode("utf-8"),
        file_name="fatalities_filtered.csv",
        mime="text/csv",
    )
    