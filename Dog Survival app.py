#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import streamlit as st
from lifelines import KaplanMeierFitter
import plotly.graph_objects as go

def interactive_kaplan_meier_plot(df):
    # Create a dictionary to store DataFrames for each unique breed
    breed_dfs = {}
    # Iterate through each unique breed
    for breed in df['Breed'].unique():
        # Filter the DataFrame for the current breed
        breed_dfs[breed] = df[df['Breed'] == breed].copy()

    # Create a KaplanMeierFitter object
    kmf = KaplanMeierFitter()

    # Allow user to select breed
    selected_breed = st.selectbox('Select Breed:', list(breed_dfs.keys()))

    # Check if the selected breed exists in the data
    if selected_breed not in breed_dfs:
        st.write(f"Please select a breed from the list: {list(breed_dfs.keys())}")
        return

    # Fit Kaplan-Meier curve for the selected breed
    selected_breed_df = breed_dfs[selected_breed]
    kmf.fit(selected_breed_df['lifespan'], event_observed=selected_breed_df['event'])

    # Estimate median survival time
    median_survival_time = kmf.median_survival_time_
    st.write(f"Median Survival Time for {selected_breed}: {median_survival_time} years")

    # Estimate survival probabilities at specific time points
    time_points = [5, 10, 15]
    survival_probabilities = []
    for t in time_points:
        survival_probability = kmf.predict(t)
        survival_probabilities.append(survival_probability)
        st.write(f"Survival Probability at {t} years for {selected_breed}: {survival_probability}")

    # Initialize the figure
    fig = go.Figure()

    # Add Kaplan-Meier curve for the selected breed
    fig.add_trace(go.Scatter(x=kmf.timeline, y=kmf.survival_function_.values.flatten(), mode='lines', name=selected_breed))

    # Update layout
    fig.update_layout(title=f'Kaplan-Meier Plot for {selected_breed}',
                      xaxis_title='Years',
                      yaxis_title='Survival Probability')

    # Display the plot
    st.plotly_chart(fig)

# Read the CSV file into a Pandas DataFrame
df = pd.read_csv("Breeds.csv")

# Call the function to generate the interactive Kaplan-Meier plot
interactive_kaplan_meier_plot(df)

