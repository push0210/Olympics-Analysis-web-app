import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import scipy

import plotly.figure_factory as ff
import preprocessor, helper
df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')
df = preprocessor.preprocess(df, region_df)
st.sidebar.title("Olympics Analysis")
user_menu = st.sidebar.radio(
    'Select an option', ("Medal Tally", "Overall Analysis", "Country wise Analysis", "Athlete wise Analysis")
)


if user_menu == 'Medal Tally':
    st.sidebar.header("Medal Tally")
    years, country = helper.country_year_list(df)

    selected_year = st.sidebar.selectbox("Select Year", years)
    selected_country = st.sidebar.selectbox("Select Country", country)

    medal_tally = helper.fetch_medal_tally(df, selected_year, selected_country)
    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title("Overall tally")
    if selected_year != 'Overall' and selected_country == 'Overall':
        st.title("Medal Tally in " + str(selected_year)+" Olympics")
    if selected_year == 'Overall' and selected_country != 'Overall':
        st.title(selected_country + " Overall performance")
    if selected_year != 'Overall' and selected_country != 'Overall':
        st.title(selected_country+"performance in " + str(selected_year)+" Olympics")
    st.table(medal_tally)

if user_menu == "Overall Analysis":
    editions = df['Year'].unique().shape[0]-1
    Cities = df['City'].unique().shape[0]
    Sports = df['Sport'].unique().shape[0]
    Events = df['Event'].unique().shape[0]
    Athletes = df['Name'].unique().shape[0]
    Nations = df['region'].unique().shape[0]
    st.title("Top Statistics")
    col1,col2,col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)
    with col2:
        st.header("Hosts")
        st.title(Cities)
    with col3:
        st.header("Sports")
        st.title(Sports)

    col1,col2,col3 = st.columns(3)
    with col1:
        st.header("Events")
        st.title(Events)
    with col2:
        st.header("Nations")
        st.title(Nations)
    with col3:
        st.header("Athletes")
        st.title(Athletes)

    # nations_over_time=helper.data_over_time(df, 'region')
    # fig = px.line(nations_over_time, x='Edition', y='No. of countries')
    # st.title("Participating Nations over the years")
    # st.plotly_chart(fig)
    #
    # events_over_time = helper.data_over_time(df, 'Event')
    # fig = px.line(events_over_time, x='Edition', y='Event')
    # st.title("Events over the years")
    # st.plotly_chart(fig)

    # athlete_over_time = helper.data_over_time(df, 'Name')
    # fig = px.line(events_over_time, x='Edition', y='Name')
    # st.title("Events over the years")
    # st.plotly_chart(fig)
    st.title("No. of Events over time(Every Sport)")
    fig,ax = plt.subplots(figsize=(30, 30))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    ax = sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'),
                annot=True)
    st.pyplot(fig)

    # st.title("Most Successful Athletes")
    sport_list=df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')
    selected_sport = st.selectbox('Select a sport', sport_list)
    # x = helper.most_successful(df,selected_sport)
    # st.table(x)

if user_menu == "Country wise Analysis":
    st.sidebar.title('Country wise Analysis')
    country_ = df.dropna(subset='region')
    country_list = country_['region'].unique().tolist()
    country_list.sort()

    selected_country = st.sidebar.selectbox('Select a country', country_list)
    country_df = helper.yearwise_medal_tally(df, selected_country)
    fig = px.line(country_df, x='Year', y='Medal')
    st.title(selected_country+" Medal Tally over the years")
    st.plotly_chart(fig)

    st.title(selected_country + " Excels in the following sports")
    pt = helper.country_event_heatmap(df, selected_country)
    fig, ax = plt.subplots(figsize=(30, 30))
    ax = sns.heatmap(pt, annot=True)
    st.pyplot(fig)

    # st.title("Top 10 Athletes " + selected_country)
    # Top10_df = helper.most_successful(df,selected_country)
    # st.table(Top10_df)

if user_menu == "Athlete wise Analysis":

    # athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    # x1 = athlete_df['Age'].dropna()
    # x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    # x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    # x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()
    #
    # fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],
    #                          show_hist=False, show_rug=False)
    # fig.update_layout(autosize=False,width=1000,height=600)
    # st.title("Distribution of Age")
    # st.plotly_chart(fig)
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')
    selected_sport = st.selectbox('Select a sport', sport_list)
    st.title("Height vs Weight")
    temp_df = helper.weight_v_height(df, selected_sport)
    fig, ax = plt.subplots(figsize=(30, 30))
    ax = sns.scatterplot(x=temp_df['Weight'], y=temp_df['Height'], hue=temp_df['Medal'],style=temp_df['Sex'],s=100)
    st.pyplot(fig)


    st.title("Men vs Women")
    final = helper.men_vs_women(df)
    fig = px.line(final,x='Year',y=['Male','Female'])
    st.plotly_chart(fig)





