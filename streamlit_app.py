import altair as alt
import numpy as np
import pandas as pd
import streamlit as st
from subnetwork import get_data
"""
# Welcome to Miner Dashboard (alpha)

"""

data = get_data()
if data:
    df = pd.DataFrame.from_dict(data, orient='index')
    df.reset_index(inplace=True)
    df.rename(columns={'index': 'Miner UID'}, inplace=True)
    st.dataframe(df,  hide_index=True)
    # for key, value in data.items():
    #     st.subheader(f"{key}")
    #     for subkey, subvalue in value.items():
    #         st.text(f"{subkey}: {subvalue}")
else:
    st.write("No data available.")