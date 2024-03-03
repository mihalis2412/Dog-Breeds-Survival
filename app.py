#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
from lifelines import KaplanMeierFitter
import plotly.graph_objects as go
import streamlit as st

# Predefined color palette
color_palette = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']

def interactive_kaplan_meier_plot(df):
    # Create a dictionary to store DataFrames for each unique breed
    breed_dfs = {}
    # Iterate through each unique breed
    for breed in df['Breed'].unique():
        # Filter the DataFrame for the current breed
        breed_dfs[breed] = df[df['Breed'] == breed].copy()

    # Create a KaplanMeierFitter object
    kmf = KaplanMeierFitter()

    # Initialize the figure
    fig = go.Figure()

    # Allow user to search for breeds dynamically
    main_breed = st.selectbox('Select Main Breed: ', list(breed_dfs.keys()), key='main_breed_input')

    # Assign a color to the main breed
    main_breed_color = color_palette[0]

    # Fit Kaplan-Meier curve for the selected main breed
    main_breed_df = breed_dfs[main_breed]
    kmf.fit(main_breed_df['lifespan'], event_observed=main_breed_df['event'])

    # Estimate median survival time
    median_survival_time = kmf.median_survival_time_

    # Plot Kaplan-Meier curve for the selected main breed with confidence intervals
    fig.add_trace(go.Scatter(x=kmf.timeline, y=kmf.survival_function_.values.flatten(), mode='lines', name=main_breed, line=dict(color=main_breed_color)))
    fig.add_trace(go.Scatter(x=kmf.timeline, y=kmf.confidence_interval_survival_function_.iloc[:, 0], mode='lines', line=dict(color=main_breed_color, dash='dash'), name=f'{main_breed} CI (Lower)', showlegend=True))
    fig.add_trace(go.Scatter(x=kmf.timeline, y=kmf.confidence_interval_survival_function_.iloc[:, 1], mode='lines', line=dict(color=main_breed_color, dash='dash'), name=f'{main_breed} CI (Upper)', showlegend=True))

    # Allow user to select breed to compare with (optional)
    compare_breeds = [breed for breed in breed_dfs.keys() if breed != main_breed]
    compare_breed = st.selectbox('Select Breed to Compare With (leave empty to skip comparison): ', ['', *compare_breeds], key='compare_breed_input')

    # If breed to compare with is provided, add its Kaplan-Meier curve as well
    if compare_breed:
        # Assign a color to the breed to compare with
        compare_breed_color = color_palette[1]

        # Fit Kaplan-Meier curve for the selected breed to compare with
        compare_breed_df = breed_dfs[compare_breed]
        kmf.fit(compare_breed_df['lifespan'], event_observed=compare_breed_df['event'])

        # Plot Kaplan-Meier curve for the selected breed to compare with with confidence intervals
        fig.add_trace(go.Scatter(x=kmf.timeline, y=kmf.survival_function_.values.flatten(), mode='lines', name=compare_breed, line=dict(color=compare_breed_color)))
        fig.add_trace(go.Scatter(x=kmf.timeline, y=kmf.confidence_interval_survival_function_.iloc[:, 0], mode='lines', line=dict(color=compare_breed_color, dash='dash'), name=f'{compare_breed} CI (Lower)', showlegend=True))
        fig.add_trace(go.Scatter(x=kmf.timeline, y=kmf.confidence_interval_survival_function_.iloc[:, 1], mode='lines', line=dict(color=compare_breed_color, dash='dash'), name=f'{compare_breed} CI (Upper)', showlegend=True))

    # Set the size of the plot
    fig.update_layout(width=1000, height=600)

    # Display the plot
    st.plotly_chart(fig, key='plotly_chart_input', use_container_width=True)

    # Display the DataFrame
    st.subheader("Median Survival and Survival Probabilities:")
    survival_data = []
    for breed_name, breed_df in breed_dfs.items():
        kmf.fit(breed_df['lifespan'], event_observed=breed_df['event'])
        median_survival = kmf.median_survival_time_
        survival_at_5_years = kmf.predict(5)
        survival_at_10_years = kmf.predict(10)
        survival_at_15_years = kmf.predict(15)
        survival_data.append([breed_name, median_survival, survival_at_5_years, survival_at_10_years, survival_at_15_years])

    survival_df = pd.DataFrame(survival_data, columns=['Breed', 'Median Survival (Years)', 'Survival Prob at 5 Years', 'Survival Prob at 10 Years', 'Survival Prob at 15 Years'])

    # Sort DataFrame by median survival in descending order
    survival_df = survival_df.sort_values(by='Median Survival (Years)', ascending=False)

    # Display the sorted DataFrame
    st.dataframe(survival_df, height=400)

# Read the CSV file into a Pandas DataFrame
df = pd.read_csv("FinalBreeds.csv")

# Call the function to generate the interactive Kaplan-Meier plot and display the survival matrix
interactive_kaplan_meier_plot(df)

