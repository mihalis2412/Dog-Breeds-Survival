#!/usr/bin/env python
# coding: utf-8

# In[5]:


import streamlit as st
from lifelines import KaplanMeierFitter
import plotly.graph_objects as go
import pandas as pd

# Read the CSV file into a Pandas DataFrame
df = pd.read_csv("Breeds.csv")

# Assuming 'df' is your DataFrame containing the 'lifespan' and 'event' columns

# Create KaplanMeierFitter object
kmf = KaplanMeierFitter()

# Initialize the figure
fig = go.Figure()

# Create color map for breeds
color_map = {
    'Labrador Retriever': 'blue',
    'German Shepherd': 'red',
    'Golden Retriever': 'green'
    # Add more colors and breeds as needed
}

# Iterate through each breed
for breed in df['Breed'].unique():
    # Filter dataframe for the current breed
    breed_df = df[df['Breed'] == breed]
    # Fit Kaplan-Meier curve for the current breed
    kmf.fit(breed_df['lifespan'], event_observed=breed_df['event'])
    # Add Kaplan-Meier curve for the current breed
    fig.add_trace(go.Scatter(x=kmf.timeline, y=kmf.survival_function_[1], mode='lines', name=breed, line=dict(color=color_map.get(breed, 'black'))))

# Update layout
fig.update_layout(title='Interactive Kaplan-Meier Plot of Dog Breeds',
                  xaxis_title='Years',
                  yaxis_title='Survival Probability')

# Display the plot using Streamlit
st.plotly_chart(fig)

# Allow user to select breed
selected_breed = st.selectbox('Select Breed:', df['Breed'].unique())
st.write(f"Selected Breed: {selected_breed}")

# Show median survival time for selected breed
selected_breed_df = df[df['Breed'] == selected_breed]
kmf.fit(selected_breed_df['lifespan'], event_observed=selected_breed_df['event'])
median_survival_time = kmf.median_survival_time_
st.write(f"Median Survival Time for {selected_breed}: {median_survival_time} years")


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




