import streamlit as st
import pandas as pd

df=pd.read_csv("cleaned_startup_funding.csv")

def load_investors_details(selected_investor):
    st.title(selected_investor)
    recent_data=df[df['investors'].str.contains(selected_investor)][['date','startup','vertical','round','amount']].head(5)
    st.dataframe(recent_data)
st.sidebar.header("Startup Funding Analysis")
selected_sector=st.sidebar.selectbox("Select One",['Overall Analysis','Startups','Investors'])

if selected_sector=='Overall Analysis':
    st.title("Overall Analysis")

elif selected_sector=='Startups':
    st.sidebar.selectbox("Select Startup",sorted(df['startup'].unique().tolist()))
    btn1=st.sidebar.button("Show Startup Details")
    st.title("Startup Analysis")
    
else:
    selected_investor=st.sidebar.selectbox("Select Investor",sorted(set(df['investors'].str.split(',').sum())))
    btn2=st.sidebar.button("Show Investor Details")
    if btn2:
        load_investors_details(selected_investor)
    
    



