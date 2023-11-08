import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Dashboard Bullying", page_icon="📈", layout="wide")

st.header("Dashboard Bullying")
st.write("This is a streamlit page of Dashboard Bullying by GSHS")


GSHS2015 = pd.read_csv('data/IDN2015_Public_Use_national.csv')[['Q1', 'Q2', 'Q3', 'Q22', 'Q23', 'Q24', 'Q25', 'Q26', 'Q27', 'Q28','Q29', 'Q30',
                        'Q34', 'Q38', 'Q39', 'Q40', 'Q41', 'Q42', 'Q43']]
GSHS2007 = pd.read_csv('data/IOH2007_Public_Use.csv')[['Q1', 'Q2', 'Q3', 'Q13', 'Q14', 'Q15', 'Q16', 'Q17', 'Q18', 'Q19',
            'Q20', 'Q21', 'Q22', 'Q23', 'Q24','Q25', 'Q26', 'Q27', 'Q51', 'Q53', 'Q54']]

column_name_mapping_2015 = {
    'Q1':'Age_label',
    'Q2':'Gender_label',
    'Q3':'Grade_label',
    'Q22':'Physical_Attacks_Past_12_Months_label',
    'Q23':'Physical_Fight_Past_12_Months_label',
    'Q25':'Serious_Injuries_Past_12_Months_label',
    'Q26':'The_Most_Serious_Injury_Past_12_Months_label',
    'Q27':'Major_Cause_of_Injury_Past_12_Months_label',
    'Q28':'Injury_Cause_Past_12_Months_label',
    'Q29':'Bullied_Days_Past_30_Days_label',
    'Q30':'Most_Often_Bullied_Past_30_Days_label',
    'Q38':'Lonely_Frequency_Past_12_Months_label',
    'Q39':'Sleeplessness_Frequency_Past_12_Months_label',
    'Q40':'Suicide_Consideration_Past_12_Months_label',
    'Q41':'Suicide_Planning_Past_12_Months_label',
    'Q43':'Close_Friend_label'
}

column_name_mapping_2007 = {
    'Q1':'Age_label',
    'Q2':'Gender_label',
    'Q3':'Grade_label',
    'Q13':'Physical_Attacks_Past_12_Months_label',
    'Q14':'Physical_Fight_Past_12_Months_label',
    'Q15':'Serious_Injuries_Past_12_Months_label',
    'Q17':'Major_Cause_of_Injury_Past_12_Months_label',
    'Q18':'Injury_Cause_Past_12_Months_label',
    'Q19':'Most_Serious_Injury_Past_12_Months_label',
    'Q20':'Bullied_Days_Past_30_Days_label',
    'Q21':'Most_Often_Bullied_Past_30_Days_label',
    'Q22':'Lonely_Frequency_Past_12_Months_label',
    'Q23':'Sleeplessness_Frequency_Past_12_Months_label',
    'Q25':'Suicide_Consideration_Past_12_Months_label',
    'Q26':'Suicide_Planning_Past_12_Months_label',
    'Q27':'Close_Friend_label',
}
GSHS2015 = GSHS2015.rename(columns=column_name_mapping_2015)
GSHS2015["YEAR"] = 2015
GSHS2007 = GSHS2007.rename(columns=column_name_mapping_2007)
GSHS2007["YEAR"] = 2007

GSHS = pd.concat([GSHS2015, GSHS2007])

year = st.selectbox("Year", [2015, 2007])

filtered_bullied_year = GSHS.query(f"(`YEAR` == {year}) & (`Most_Often_Bullied_Past_30_Days_label` != 1.0)")
length = len(filtered_bullied_year)

physical_bullied_percentage = round((len(filtered_bullied_year.query("`Most_Often_Bullied_Past_30_Days_label` == 2.0")) / length) * 100)
verbal_bullied_percentage = round((len(filtered_bullied_year.query("`Most_Often_Bullied_Past_30_Days_label` in (3.0, 4.0, 5.0, 7.0)")) / length) * 100)
social_bullied_percentage = round((len(filtered_bullied_year.query("`Most_Often_Bullied_Past_30_Days_label` == 6.0")) / length) * 100)
other_bullied_percentage = round((len(filtered_bullied_year.query("`Most_Often_Bullied_Past_30_Days_label` == 8.0")) / length) * 100)

st.subheader("Percentage of Bullying (by Type)")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Physical", f"{physical_bullied_percentage}%")
col2.metric("Verbal", f"{verbal_bullied_percentage}%")
col3.metric("Social", f"{social_bullied_percentage}%")
col4.metric("Other Way", f"{other_bullied_percentage}%")


fig_col1, fig_col2 = st.columns(2)

with fig_col1:
    df1 = filtered_bullied_year.copy(deep=True)
    df1['Most_Often_Bullied_Past_30_Days_label'] = df1['Most_Often_Bullied_Past_30_Days_label'].replace([2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, ], True)
    df1 = pd.DataFrame({'Percentage of bullied': df1.groupby(['Gender_label', 'Most_Often_Bullied_Past_30_Days_label']).size() * 100 / len(df1)}).reset_index()
    df1['Percentage of bullied'] = df1['Percentage of bullied'].round(decimals=2)
    fig1 = px.bar(df1, x="Gender_label", y="Percentage of bullied",
                hover_data=['Percentage of bullied'], labels={'Gender_label':'Gender'})
    fig1.update_xaxes(labelalias={1: 'Male', 2: 'Female'})
    fig1.update_yaxes(range=[0,100])
    st.plotly_chart(fig1)
    
with fig_col2:
    df2 = filtered_bullied_year.copy(deep=True)
    df2['Most_Often_Bullied_Past_30_Days_label'] = df2['Most_Often_Bullied_Past_30_Days_label'].replace([2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, ], True)
    df2 = pd.DataFrame({'Percentage of bullied': df2.groupby(['Grade_label', 'Most_Often_Bullied_Past_30_Days_label']).size() * 100 / len(df2)}).reset_index()
    df2['Percentage of bullied'] = df2['Percentage of bullied'].round(decimals=2)
    df2['Grade_label'] = df2['Grade_label'].replace([1.0, 2.0, 3.0, 4.0, 5.0, 6.0], [7, 8, 9, 10, 11, 12])
    fig2 = px.bar(df2, x="Grade_label", y="Percentage of bullied",
                hover_data=['Percentage of bullied'], labels={'Grade_label':'Grade'})
    # fig2.update_xaxes(labelalias={1: 'Male', 2: 'Female'})
    fig2.update_yaxes(range=[0,100])
    st.plotly_chart(fig2)
    
df3 = filtered_bullied_year.copy(deep=True)
df3['Most_Often_Bullied_Past_30_Days_label'] = df3['Most_Often_Bullied_Past_30_Days_label'].replace([2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, ], True)
df3 = pd.DataFrame({'Percentage of bullied': df3.groupby(['Age_label', 'Most_Often_Bullied_Past_30_Days_label']).size() * 100 / len(df3)}).reset_index()
df3['Age_label'] = df3['Age_label'].replace([1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0],
                            [11, 12, 13, 14, 15, 16, 17, 18])
df3['Percentage of bullied'] = df3['Percentage of bullied'].round(decimals=2)
fig3 = px.bar(df3, x="Age_label", y="Percentage of bullied",
            hover_data=['Percentage of bullied'], labels={'Age_label':'Age'})
# fig2.update_xaxes(labelalias={1: 'Male', 2: 'Female'})
fig3.update_yaxes(range=[0,100])
st.plotly_chart(fig3)