import streamlit as st
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd
import plotly.express as px
# Custom CSS for background color and sidebar styling
def add_custom_styles():
    st.markdown(
        """
        <style>
        
        /* Center the title */
        .title {
            text-align: center;
            font-size: 2.5em; /* Adjust the font size as needed */
            color: #4B0082; /* Indigo color for the title */
        }
        
         /* Adjust sidebar width */
        .css-1n2mz7e3 {  /* Adjusts the sidebar container class */
            width: 50px;  /* Set the desired width in pixels */
        }
        
        /* Optional: Adjust the main content area to prevent overlap */
        .css-1v0mbdj {  /* Adjusts the main content area */
            margin-left: 220px;  /* Set to the width of your sidebar + some extra space */
        }
        
        /* Background color for the main app */
        .stApp {
            background-color: #ADD8E6; /* Light blue */
        }

        /* Sidebar background color */
        .css-1n2mz7e3 {  /* This targets the sidebar container */
            background-color: #f5f5dc; /* Cream color */
        }

        /* Universal sidebar selector to apply background for updated Streamlit versions */
        section[data-testid="stSidebar"] {
            background-color: #f5f5dc; /* Cream color */
        }

        /* Sidebar text and link color for menu items */
        div[data-testid="stSidebar"] .css-18e3th9 a {
            color: #4B0082; /* Indigo for unselected menu */
            font-weight: bold;
        }

        /* Hover effect for sidebar menu items */
        div[data-testid="stSidebar"] .css-18e3th9 a:hover {
            color: #FFA500; /* Orange on hover */
        }

        /* Selected menu item color */
        div[data-testid="stSidebar"] .css-1avcm0n .css-18e3th9 a {
            color: #DC143C; /* Crimson for selected menu */
        }

        /* Light peach background for Customer and Staff Options dropdown */
        div[data-testid="stSelectbox"] > div {
            background-color: #FFDAB9; /* Light peach color */
        }

        /* Dropdown text color */
        div[data-testid="stSelectbox"] > div select {
            color: #4B0082; /* Indigo color for dropdown text */
            font-weight: bold;
        }
        
        </style>
        """,
        unsafe_allow_html=True
    )
  
st.set_page_config(page_title="SENTIMENTAL ANALYSIS SYSTEM",page_icon="C:/MyProjects/amazonsentimentalanalaysis/urlimage.png")
# Call the function to apply custom styles
add_custom_styles()  
st.title("SENTIMENTAL ANALYSIS SYSTEM")
st.sidebar.image("C:/MyProjects/amazonsentimentalanalaysis/amazon.png", width=250)
choice=st.sidebar.selectbox("My Menu",("HOME","ANALYSIS","VISUALIZATION"))
# Sidebar Images
st.sidebar.image("C:/MyProjects/amazonsentimentalanalaysis/side1.png", width=150)
st.sidebar.image("C:/MyProjects/amazonsentimentalanalaysis/side2.png", width=150)
if(choice=="HOME"):
    st.image("C:/MyProjects/amazonsentimentalanalaysis/home.gif")
    st.write("This Project is developed by Prasanna as part of training Project")
elif(choice=="ANALYSIS"):
    url=st.text_input("enter google sheet url")
    c=st.text_input("enter column name to be analyzed")
    btn=st.button("Analyze")
    if btn:
       mymodel=SentimentIntensityAnalyzer()
       #sheet_url = "https://docs.google.com/spreadsheets/d/18-F2aJj7GgOocBeWg1jkkvZ4ADVQiRALSwZ9Pf9FQqI/export?format=csv"
       sheet_url = "https://docs.google.com/spreadsheets/d/1vTqBGhEAX4fIGc-nCTGqSZ-n7QVTDLAphN38qEw3Mo8/export?format=csv"
       df = pd.read_csv(sheet_url)
       df["review_date"] = pd.to_datetime(df["review_date"], errors='coerce').dt.strftime('%d-%b-%y')
       #df=pd.read_csv("https://docs.google.com/spreadsheets/d/18-F2aJj7GgOocBeWg1jkkvZ4ADVQiRALSwZ9Pf9FQqI/edit?usp=sharing")
       X=df['review_body']
       l=[]
       for k in X:
           pred=mymodel.polarity_scores(k)
           if(pred['compound']>0.05):
               l.append("Positive")
           elif(pred['compound']<-0.05):
               l.append("Negative")
           else:
               l.append("Neutral")
       df["Sentiment"]=l
       df.to_csv("result.csv",index=False)
       st.header("Sentiment Analysis successfull,results saved as result.csv file")
elif(choice=="VISUALIZATION"):
    df=pd.read_csv("result.csv")
    st.dataframe(df)
    choice2=st.selectbox("Choose Visualization",("NONE","PIE CHART","HISTOGRAM"))
    if(choice2=="PIE CHART"):
        pos=(len(df[df["Sentiment"]=="Positive"])/len(df))*100
        neg=(len(df[df["Sentiment"]=="Negative"])/len(df))*100
        neu=(len(df[df["Sentiment"]=="Neutral"])/len(df))*100
        fig=px.pie(values=[pos,neg,neu],names=["Positive","Negative","Neutral"])
        #fig.show()
        st.plotly_chart(fig)
    elif(choice2=="HISTOGRAM"):
       c=st.selectbox("Choose column name",df.columns)
       if c:
           fig=px.histogram(x=df[c],color=df['Sentiment'])
           st.plotly_chart(fig)
