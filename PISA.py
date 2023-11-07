import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Dashboard Bullying", page_icon="📈", layout="wide")

st.header("Dashboard Bullying")
st.write("This is a streamlit page of Dashboard Bullying by PISA")

PISAdata = pd.read_parquet('data/cleaned_bully_data.parquet')
PISAdata['GRADE'] = PISAdata['GRADE'].astype(str)

country = st.selectbox("Country", PISAdata['COUNTRY_CODE'].unique().tolist())

filtered_country = PISAdata.query(f"`COUNTRY_CODE` == '{country}'")
length = len(filtered_country)
filtered_country['physical_bullied'] = (filtered_country['Tookaway_destroy_things_in1years'] + filtered_country['Hit_pushed_in1years']) / 2
filtered_country['verbal_bullied'] = (filtered_country['Made_fun_of_in1years'] + filtered_country['Thretened_in1years'] + filtered_country['Spread_bad_rumor_in1years']) / 3
filtered_country['social_bullied'] = filtered_country['Ostracized_in1years']
physical_bullied_percentage = round((len(filtered_country[filtered_country['physical_bullied'] > 1]) / length) * 100)
verbal_bullied_percentage = round((len(filtered_country[filtered_country['verbal_bullied'] > 1]) / length) * 100)
social_bullied_percentage = round((len(filtered_country[filtered_country['social_bullied'] > 1]) / length) * 100)
st.subheader("Percentage of Bullying (by Type)")
col1, col2, col3 = st.columns(3)
col1.metric("Physical", f"{physical_bullied_percentage}%")
col2.metric("Verbal", f"{verbal_bullied_percentage}%")
col3.metric("Social", f"{social_bullied_percentage}%")



fig_col1, fig_col2 = st.columns(2)

with fig_col1:
    df1 = pd.DataFrame({'Percentage of bullied': filtered_country[filtered_country["bullied"] == True].groupby(['GENDER', 'bullied']).size() * 100 / len(filtered_country[filtered_country["bullied"] == True])}).reset_index()
    df1['Percentage of bullied'] = df1['Percentage of bullied'].round(decimals=2)
    fig1 = px.pie(
        df1, values='Percentage of bullied', names=["Female", "Male"], title='Percentage of Bullied by Gender',
        labels={'GENDER':'Percentage of bullied', 'bullied':'bully'}
    )
    fig1.update_traces(textinfo='percent+label')
    st.plotly_chart(fig1)
    
with fig_col2:
    df2 = pd.DataFrame({'Percentage of bullied': filtered_country[filtered_country["bullied"] == True].groupby(['GRADE', 'bullied']).size() * 100 / len(filtered_country[filtered_country["bullied"] == True])}).reset_index()
    df2['Percentage of bullied'] = df2['Percentage of bullied'].round(decimals=2)
    fig2 = px.bar(df2, x="GRADE", y="Percentage of bullied",
                hover_data=['Percentage of bullied'], labels={'GRADE':'Grade'})
    fig2.update_yaxes(range=[0,100])
    st.plotly_chart(fig2)


df3 = PISAdata.groupby(['COUNTRY_CODE', 'bullied'])['bullied'].count().rename("Percentage of bullied").groupby(level = 0).transform(lambda x: x/x.sum()).reset_index()
df3 = df3.query('bullied == True')
fig3 = px.choropleth(df3, locations="COUNTRY_CODE",
                    color="Percentage of bullied", # lifeExp is a column of gapminder
                    hover_name="COUNTRY_CODE", # column to add to hover information
                    color_continuous_scale=px.colors.sequential.Blues)
st.plotly_chart(fig3, use_container_width=True)