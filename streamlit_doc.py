import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(layout="wide",page_title="Startup Funding Analysis")

df=pd.read_csv("cleaned_startup_funding.csv")
df['date']=pd.to_datetime(df['date'],errors='coerce',dayfirst=True)
df['year']=df['date'].dt.year.astype('Int32')
df['month']=df['date'].dt.month

# Build investor similarity matrix
# Cache result to avoid recomputation
@st.cache_data
def build_similarity(df):

    temp = df.copy()
    temp = temp.dropna(subset=['investors','vertical'])
    temp['investors'] = (temp['investors'].str.split(','))
    temp = temp.explode('investors')
    temp['investors'] = (temp['investors'].str.strip())
    pivot = pd.crosstab(temp['investors'],temp['vertical'])
    sim = cosine_similarity(
        pivot
    )
    similarity_df = pd.DataFrame(
        sim,
        index=pivot.index,
        columns=pivot.index
    )
    return similarity_df
similarity_df = build_similarity(df)

# Get similar investors (top N)
def get_similar_investors(
        investor_name,
        n=5):

    if investor_name not in similarity_df.index:

        return None

    similar = (
        similarity_df
        .loc[investor_name]
        .sort_values(
            ascending=False
        )
        .iloc[1:n+1]
    )

    return similar

# Load investor details
def load_investors_details(selected_investor):
    st.title(selected_investor)
    investor_df = df[
        df['investors']
        .str.contains(
            selected_investor,
            regex=False,
            na=False
        )
    ]
    recent_data=investor_df[['date','startup','vertical','round','amount']].head(5)
    st.subheader("Recent Investments")
    st.dataframe(recent_data)
    col1,col2=st.columns(2)
    with col1:
        biggest_investment=investor_df.groupby('startup')['amount'].sum().sort_values(ascending=False).head(5)
        fig,ax=plt.subplots()
        ax.bar(biggest_investment.index,biggest_investment.values)
        st.subheader("Biggest Investments")
        plt.xticks(rotation=45)
        st.pyplot(fig)
    with col2:
        vertical_series=investor_df.groupby('vertical')['amount'].sum()
        fig1,ax1=plt.subplots()
        ax1.pie(vertical_series,labels=vertical_series.index,autopct='%1.1f%%')
        st.subheader("Sectors invested in")
        st.pyplot(fig1)

    st.subheader("Yearly Investments Trend")
    year_series=investor_df.groupby('year')['amount'].sum()
    fig2,ax2=plt.subplots()
    ax2.plot(year_series.index,year_series.values)
    st.pyplot(fig2)

    st.subheader("Similar Investors")

    similar = get_similar_investors(
        selected_investor
    )

    if similar is not None:

        similar_df = (
            similar.reset_index()
            .rename(columns={'index':'Investor',selected_investor:'Similarity Score'})
        )

        similar_df.index += 1
        similar_df.index.name='Rank'

        similar_df['Similarity Score'] = (similar_df['Similarity Score'].mul(100).round(2).astype(str)+ '%')

        st.dataframe(
            similar_df,
            use_container_width=True
        )

# Load startup details for the selected startup
def load_Startups_details(selected_startup):
    st.title(selected_startup)
    st.subheader("Startup Details")
    info=df[df['startup'].str.contains(selected_startup,regex=False,na=False)][['vertical','subvertical','city']]
    st.dataframe(info)
    st.subheader("Investment Details")
    invest=df[df['startup'].str.contains(selected_startup,regex=False,na=False)][['investors','round','amount','year']]
    st.dataframe(invest)

# Load overall analysis    
def load_Overall_Analysis():
    st.title("Overall Analysis")
    # total invested amount
    total=round(df['amount'].sum())
    st.subheader("Total Invested Amount in India")
    st.metric("Total",str(total)+' Cr')

    # highest invested amount
    hi=df.groupby('startup')['amount'].sum().sort_values(ascending=False).head(5)
    hi = hi.rename('amount (Cr)')
    st.subheader("Top 5 highest invested startups")
    st.dataframe(hi)

    # yearwise investment trend graph
    year_series=df.groupby('year')['amount'].sum()
    fig3,ax3=plt.subplots()
    ax3.plot(year_series.index,year_series.values)
    st.subheader("Yearwise Investment Trend")
    st.pyplot(fig3)

    # top 5 sectors
    top = df.groupby('vertical')['amount'].sum().sort_values(ascending=False).head(5)
    fig, ax = plt.subplots(figsize=(6,3.5))
    # Create the bar chart
    ax.bar(top.index, top.values, color='#1f77b4')
    # Customise labels and titles
    ax.set_title("Top 5 Sectors by Total Investment", fontsize=14)
    ax.set_ylabel("Total Amount (in Cr)", fontsize=8)
    ax.set_xlabel("Vertical / Sector", fontsize=8)
    # Rotate the vertical names so they don't overlap
    plt.xticks(rotation=45, ha='right') 
    st.pyplot(fig)

    #Month on month investment trend
    st.subheader("Month on Month Investment Trend")
    temp = df.groupby(['year', 'month'])['amount'].sum().reset_index(name='amount')
    temp = temp.dropna(subset=['year', 'month'])
    # FIX: Force year and month to be integers (.astype(int)) to remove the decimal '.0'
    temp['date_obj'] = pd.to_datetime(temp['year'].astype(int).astype(str) + '-' + temp['month'].astype(int).astype(str) + '-01')
    temp = temp.sort_values('date_obj')
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(temp['date_obj'], temp['amount'], marker='o', linewidth=2)
    ax.set_xlabel('Date', fontsize=12)
    ax.set_ylabel('Amount (in Cr)', fontsize=12)
    fig.autofmt_xdate()
    st.pyplot(fig)

st.sidebar.header("Startup Funding Analysis")
selected_option=st.sidebar.selectbox("Select One",['Overall Analysis','Startups','Investors'])

if selected_option=='Overall Analysis':
        load_Overall_Analysis()
    

elif selected_option=='Startups':
    selected_startup=st.sidebar.selectbox("Select Startup",sorted(df['startup'].unique().tolist()))
    btn1=st.sidebar.button("Show Startup Details")
    if btn1:
        load_Startups_details(selected_startup)
    
    
else:
    selected_investor=st.sidebar.selectbox("Select Investor",sorted(df['investors'].dropna().str.split(',').explode().str.strip().unique()))
    btn2=st.sidebar.button("Show Investor Details")
    if btn2:
        load_investors_details(selected_investor)
    
    



