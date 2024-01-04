import streamlit as st
import os
import time
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def main():
    st.set_page_config(page_title="Interaction Differentiation")
    st.header("Calculate and Visulaise the Interaction Feature Differences 📊")

    #uploading file
    csv1 = st.file_uploader("Upload your Interaction Matrix of 1st Complex", type="csv")
    csv2 = st.file_uploader("Upload your Interaction Matrix of 2nd Complex", type="csv")


    d1 = pd.read_csv(csv1)
    st.write(d1)

    if csv2 is not None:
        d2 = pd.read_csv(csv2)
    st.write(d2)

    d3 = pd.DataFrame()
    d3['interaction'] = d2['interaction'].copy()

    d4=pd.DataFrame(d1.drop(['entry','interaction'], axis=1).subtract(d2.drop(['entry','interaction'], axis=1)))

    joined_df = pd.concat([d3.reset_index(drop=True), d4.reset_index(drop=True)], axis=1)
    joined_df.set_index("interaction")

    st.header("Calculate and Visulaise the Interaction Feature Differences 📊")

    fig1 = sns.heatmap(d1.drop(['entry', 'interaction'], axis=1), yticklabels=d3['interaction'], cmap="Blues", linewidths=0.5, linecolor='black')
    st.pyplot(fig1.get_figure())

    st.header("Calculate and Visulaise the Interaction Feature Differences 📊")
    fig2 = sns.heatmap(d2.drop(['entry', 'interaction'], axis=1), yticklabels=d3['interaction'], cmap="Reds", linewidths=0.5, linecolor='black')
    st.pyplot(fig2.get_figure()) 
    
    st.header("Calculate and Visulaise the Interaction Feature Differences 📊")
    fig3 = sns.heatmap(d4, yticklabels=joined_df['interaction'], cmap='coolwarm', linewidths=0.5, linecolor='black')
    st.pyplot(fig3.get_figure())

if __name__ =='__main__':
    main()
