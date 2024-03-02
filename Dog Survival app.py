#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
import pandas as pd
from lifelines import KaplanMeierFitter
import plotly.graph_objects as go

# Read the CSV file into a Pandas DataFrame
df = pd.read_csv("Breeds.csv")

# Create a dictionary to store DataFrames for each unique breed
breed_dfs = {}
# Iterate through each unique breed
for breed in df['Breed'].unique():
    # Filter the DataFrame for the current breed
    breed_dfs[breed] = df[df['Breed'] == breed].copy()

# Create a KaplanMeierFitter object
kmf = KaplanMeierFitter()

# Initialize Streamlit app
st.title('Interactive Kaplan-Meier Plot of Dog Breeds')

# Allow user to select breed
selected_breed = st.selectbox('Select Breed:', list(breed_dfs.keys()))

# Fit Kaplan-Meier curve for the selected breed
selected_breed_df = breed_dfs[selected_breed]
kmf.fit(selected_breed_df['lifespan'], event_observed=selected_breed_df['event'])

# Initialize the figure
fig = go.Figure()

# Add Kaplan-Meier curve for the selected breed
fig.add_trace(go.Scatter(x=kmf.timeline, y=kmf.survival_function_[kmf.event_observed].values, mode='lines', name=selected_breed))

# Update layout
fig.update_layout(title=f'Kaplan-Meier Plot for {selected_breed}',
                  xaxis_title='Years',
                  yaxis_title='Survival Probability')

# Display the plot using Streamlit
st.plotly_chart(fig)

