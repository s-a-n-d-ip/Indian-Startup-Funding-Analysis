import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(layout="wide",page_title="Startup Funding Analysis")

df=pd.read_csv("cleaned_startup_funding.csv")
df['date']=pd.to_datetime(df['date'],errors='coerce',dayfirst=True)
df['year']=df['date'].dt.year.astype('Int32')

@st.cache_data
def build_similarity(df):

    temp = df.copy()

    temp = temp.dropna(
        subset=['investors','vertical']
    )

    temp['investors'] = (
        temp['investors']
        .str.split(',')
    )

    temp = temp.explode(
        'investors'
    )

    temp['investors'] = (
        temp['investors']
        .str.strip()
    )

    pivot = pd.crosstab(
        temp['investors'],
        temp['vertical']
    )

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
    
    



