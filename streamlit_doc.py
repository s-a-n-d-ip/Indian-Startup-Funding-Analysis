import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout="wide",page_title="Startup Funding Analysis")

df=pd.read_csv("cleaned_startup_funding.csv")

def load_investors_details(selected_investor):
    st.title(selected_investor)
    recent_data=df[df['investors'].str.contains(selected_investor,regex=False,na=False)][['date','startup','vertical','round','amount']].head(5)
    st.subheader("Recent Investments")
    st.dataframe(recent_data)
    col1,col2=st.columns(2)
    with col1:
        biggest_investment=df[df['investors'].str.contains(selected_investor,regex=False,na=False)].groupby('startup')['amount'].sum().sort_values(ascending=False).head(5)
        fig,ax=plt.subplots()
        ax.bar(biggest_investment.index,biggest_investment.values)
        st.subheader("Biggest Investments")
        plt.xticks(rotation=45)
        st.pyplot(fig)


st.sidebar.header("Startup Funding Analysis")
selected_sector=st.sidebar.selectbox("Select One",['Overall Analysis','Startups','Investors'])

if selected_sector=='Overall Analysis':
    st.title("Overall Analysis")

elif selected_sector=='Startups':
    st.sidebar.selectbox("Select Startup",sorted(df['startup'].unique().tolist()))
    btn1=st.sidebar.button("Show Startup Details")
    st.title("Startup Analysis")
    
else:
    selected_investor=st.sidebar.selectbox("Select Investor",sorted(df['investors'].dropna().str.split(',').explode().str.strip().unique()))
    btn2=st.sidebar.button("Show Investor Details")
    if btn2:
        load_investors_details(selected_investor)
    
    



