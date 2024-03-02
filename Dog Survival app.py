#!/usr/bin/env python
# coding: utf-8

# In[5]:


import streamlit as st
from lifelines import KaplanMeierFitter
import plotly.graph_objects as go
import pandas as pd

# Read the CSV file into a Pandas DataFrame
df = pd.read_csv("Breeds.csv")

# Assuming 'df' is your DataFrame containing the 'lifespan' column
kmf = KaplanMeierFitter()
kmf.fit(df['lifespan'], event_observed=df['event'])

# Initialize the figure
fig = go.Figure()

# Add Kaplan-Meier curve
fig.add_trace(go.Scatter(x=kmf.timeline, y=kmf.survival_function_.iloc[:, 0], mode='lines', name='Kaplan-Meier Estimate'))

# Add median survival time
median_survival_time = kmf.median_survival_time_
fig.add_trace(go.Scatter(x=[median_survival_time], y=[0.5], mode='markers', marker=dict(color='red', size=13), name='Median Survival Time'))

# Update layout
fig.update_layout(title='Interactive Kaplan-Meier Plot of Dog Breeds',
                  xaxis_title='Years',
                  yaxis_title='Survival Probability',
                  xaxis=dict(range=[0, 20]))  # Extend x-axis limits

# Display the plot using Streamlit
st.plotly_chart(fig)


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




