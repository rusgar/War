import pandas as pd
import plotly.express as px
from src.charts.constants import PALETTE
from src.logger.get_chart_logger import get_chart_logger
from src.logger.log_chart_rendered import log_chart_rendered

def render_chart_top_locations():
    logger = get_chart_logger()
    
    try:
        # 1. Load Data
        df = pd.read_csv('data/fatalities.csv')
        
        # 2. Identify Location Column (using your logic)
        district_candidates = ['district', 'distrito', 'region', 'location', 'area', 
                               'governorate', 'province', 'admin_region', 'city']
        
        found_col = next((c for c in district_candidates if c in df.columns), None)
        
        if not found_col:
            logger.error("No location/district column found in dataset.")
            return

        # 3. Process Data for Top 15 Locations
        location_counts = (
            df.groupby(found_col)
            .size()
            .reset_index(name='fatalities')
            .sort_values('fatalities', ascending=False)
            .head(15)
        )

        # 4. Create Plotly Figure
        fig = px.bar(
            location_counts,
            x='fatalities',
            y=found_col,
            orientation='h',
            title=f"Top 15 Locations by Fatalities ({found_col.capitalize()})",
            labels={'fatalities': 'Number of Fatalities', found_col: 'Location'},
            color='fatalities',
            color_continuous_scale=PALETTE  # Using your project's custom palette
        )

        # Improve layout
        fig.update_layout(
            yaxis={'categoryorder': 'total ascending'},
            xaxis_title="Total Fatalities",
            yaxis_title=None,
            template="plotly_dark",
            margin=dict(l=100, r=20, t=60, b=40)
        )

        # 5. Show and Log
        fig.show()
        log_chart_rendered("top_locations")
        logger.info(f"Successfully rendered top locations chart using column: {found_col}")

    except Exception as e:
        logger.error(f"Failed to render top locations chart: {str(e)}")

if __name__ == "__main__":
    render_chart_top_locations()