import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout='wide',page_title='StartUp Analysis')

df = pd.read_csv("startup_cleaned.csv")
df["date"] = pd.to_datetime(df["date"],errors="coerce")
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month

def load_startup_analysis():
    st.title("Startup Analysis")


def load_overall_analysis():
    st.title('Overall Analysis')

    # total invested amount
    total = round(df['amount'].sum())
    # max amount infused in a startup
    max_funding = df.groupby('startup')['amount'].max().sort_values(ascending=False).head(1).values[0]
    # avg ticket size
    avg_funding = df.groupby('startup')['amount'].sum().mean()
    # total funded startups
    num_startups = df['startup'].nunique()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric('Total', str(total) + ' Cr')
    with col2:
        st.metric('Max', str(max_funding) + ' Cr')

    with col3:
        st.metric('Avg', str(round(avg_funding)) + ' Cr')

    with col4:
        st.metric('Funded Startups', num_startups)

    st.header('MoM graph')
    selected_option = st.selectbox('Select Type', ['Total', 'Count'])
    if selected_option == 'Total':
        temp_df = df.groupby(['year', 'month'])['amount'].sum().reset_index()
    else:
        temp_df = df.groupby(['year', 'month'])['amount'].count().reset_index()

    temp_df['x_axis'] = temp_df['month'].astype('str') + '-' + temp_df['year'].astype('str')

    fig3, ax3 = plt.subplots()
    ax3.plot(temp_df['x_axis'], temp_df['amount'] )

    st.pyplot(fig3)

    st.header("Sector analysis")
    selected_option1 = st.selectbox('Select Type', ['Sector Analysis Total', 'Sector Analysis Count'])
    if selected_option1 == "Sector Analysis Total":
        Sector = df.groupby("vertical")["amount"].sum().sort_values(ascending=False).head()
    else:
        Sector = df.groupby("vertical")["amount"].count().sort_values(ascending=False).head()

    st.subheader('Sector Analysis ')
    fig1, ax1 = plt.subplots(figsize=(8, 8))
    ax1.pie(Sector, labels=Sector.index, autopct="%0.01f%%", startangle=90, counterclock=False)

    st.pyplot(fig1)

    type = df["round"].value_counts().head(7)
    st.header("Type of Funding")
    fig, ax = plt.subplots()
    ax.bar(type.index, type.values)
    plt.xticks(rotation=90, fontsize=10)
    st.pyplot(fig)

    df['city'] = df['city'].replace({'Bangalore': 'Bengaluru'})
    city = df.groupby("city")["amount"].sum().sort_values(ascending=False).head(7)
    fig, ax = plt.subplots()
    ax.bar(city.index, city.values)
    plt.xticks(rotation=90, fontsize=10)
    st.pyplot(fig)

def load_investor_details(investor):
    st.title(investor)
    last5_df = df[df['investors'].str.contains(investor)].head()[
        ['date', 'startup', 'vertical', 'city', 'round', 'amount']]
    st.subheader('Most Recent Investments')
    st.dataframe(last5_df)

    col1, col2  = st.columns(2)
    with col1:
        # biggest investments
        big_series = df[df['investors'].str.contains(investor)].groupby('startup')['amount'].sum().sort_values(
            ascending=False).head()
        st.subheader('Biggest Investments')
        fig, ax = plt.subplots()
        ax.bar(big_series.index, big_series.values)

        st.pyplot(fig)

    with col2:
        verical_series = df[df['investors'].str.contains(investor)].groupby('vertical')['amount'].sum()

        st.subheader('Sectors invested in')
        fig1, ax1 = plt.subplots(figsize=(10, 10))
        ax1.pie(verical_series, labels=verical_series.index, autopct="%0.01f%%",startangle=90, counterclock=False)

        st.pyplot(fig1)

    col3 , col4 = st.columns(2)

    with col3 :
        city_series = df[df['investors'].str.contains(investor)].groupby('city')['amount'].sum()

        st.subheader('City invested in')
        fig1, ax1 = plt.subplots(figsize=(10, 10))
        ax1.pie(city_series, labels=city_series.index, autopct="%0.01f%%", startangle=90, counterclock=False)

        st.pyplot(fig1)

    with col4 :
        city_series = df[df['investors'].str.contains(investor)].groupby('round')['amount'].sum()

        st.subheader('Round invested in')
        fig1, ax1 = plt.subplots(figsize=(10, 10))
        ax1.pie(city_series, labels=city_series.index, autopct="%0.01f%%", startangle=90, counterclock=False)

        st.pyplot(fig1)

    df['year'] = df['date'].dt.year
    year_series = df[df['investors'].str.contains(investor)].groupby('year')['amount'].sum()

    st.subheader('YoY Investment')
    fig2, ax2 = plt.subplots()
    ax2.plot(year_series.index, year_series.values)

    st.pyplot(fig2)


st.sidebar.title('Startup Funding Analysis')

option = st.sidebar.selectbox('Select One',['Overall Analysis','StartUp','Investor'])

if option == 'Overall Analysis':
    load_overall_analysis()

elif option == 'StartUp':
    st.sidebar.selectbox('Select StartUp',sorted(df['startup'].unique().tolist()))
    btn1 = st.sidebar.button('Find StartUp Details')
    if btn1:
        load_startup_analysis()

else:
    selected_investor = st.sidebar.selectbox('Select StartUp',sorted(set(df['investors'].str.split(',').sum())))
    btn2 = st.sidebar.button('Find Investor Details')
    if btn2:
        load_investor_details(selected_investor)


