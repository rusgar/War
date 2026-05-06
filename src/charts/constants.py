# src/charts/constants.py

import logging

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from src.logger import log_chart_rendered, get_chart_logger

PALETTE = {
    "Palestinian": "#04FF04",
    "Israeli": "#FC0000",
    "Foreign": "#FF009D",
    "Jordanian": "#0053EC",
    "American": "#FBFF00",
}

VIVID_COLORS = ["#FF006E", "#00D4FF", "#3A86FF", "#FB5607", "#FFBE0B"]

MONTHS_ES = ["Ene", "Feb", "Mar", "Abr", "May", "Jun",
            "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]