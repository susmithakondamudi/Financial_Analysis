# Import necessary libraries
import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import mysql.connector
from streamlit_option_menu import option_menu
import warnings
warnings.simplefilter("ignore")
from PIL import Image


st.set_page_config(layout="wide")
def setting_bg(background_image_url):
        st.markdown(f""" 
        <style>
            .stApp {{
                background: url('{background_image_url}') no-repeat center center fixed;
                background-size: cover;
                transition: background 0.5s ease;
            }}
            h1, h2, h3, h4, h5, h6 {{
                color: #f3f3f3;
                font-family: 'Roboto', sans-serif;
            }}
            .stButton>button {{
                color: #4e4376;
                background-color: #f3f3f3;
                transition: all 0.3s ease-in-out;
            }}
            .stButton>button:hover {{
                color: #f3f3f3;
                background-color: #2b5876;
            }}
            .stTextInput>div>div>input {{
                color: #4e4376;
                background-color: #f3f3f3;
            }}
        </style>
        """, unsafe_allow_html=True)

# Example usage with a background image URL
background_image_url = "https://www.iriscarbon.com/wp-content/uploads/2023/03/Financial-Analysis-and-Planning.jpg"
setting_bg(background_image_url)

st.markdown("""<div style='border:5px solid black; background-color:yellow; padding:10px;'> 
            <h1 style='text-align:center; color:red;'>Financial Analysis</h1> </div>""", unsafe_allow_html=True)


with st.sidebar:
    selected = option_menu(None, ["Home","Menu"], 
                    icons=["home","Menu"],
                    default_index=0,
                    orientation="vertical",  # Set orientation to vertical
                    styles={"nav-link": {"font-size": "25px", "text-align": "centre", "margin": "0px", "--hover-color": "#AB63FA", "transition": "color 0.3s ease, background-color 0.3s ease"},
                            "icon": {"font-size": "25px"},
                            "container" : {"max-width": "6000px", "padding": "10px", "border-radius": "5px","border": "5px solid black"},
                            "nav-link-selected": {"background-color": "red", "color": "white"}} )
    
    
if selected == "Home":
    st.markdown("## :green[**Overview :**] :red[This project revolves around analyzing historical loan application data to gain insights into repayment behaviors. By delving into past records, we aim to identify patterns and factors indicative of loan default risks. Our focus is on maintaining fairness in lending decisions while minimizing financial losses for the company.]")


mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234", database="financial_analysis")
mycursor = mydb.cursor()


if selected == "Menu":    
    Question = st.selectbox("", ('select Question ',
                                                        '1.Credit Types:',
                                                        '2.Income Distribution & Descriptive Statistics wrt. Credit Type:',
                                                        '3.Analysis of Goods Amount for Cash Loans:',
                                                        '4.Age Brackets of the Clients:',
                                                        '5.Documents Submission Analysis:',
                                                        '6.Overall Analysis of Credit Enquiries on Clients:',
                                                        '7.Analysis of individual applications based on the credit enquiries:',
                                                        '8.Deeper analysis on the Contact reach for clients who had payment difficulties but were from the Very Low Risk social surroundings:',
                                                        '9.Deeper analysis on the Contact reach for clients who had payment difficulties but were from the Very Low Risk social surroundings:',
                                                        '10.Top 15 customers and contact reach:'
                                                    )) 
                                                            
                                                  
    if Question == '1.Credit Types:':
        query1 = "SELECT DISTINCT NAME_CONTRACT_TYPE, COUNT(*) FROM cleaned_application_data GROUP BY NAME_CONTRACT_TYPE;"
        mycursor.execute(query1)

        # Fetch data
        data = mycursor.fetchall()

        # Process the data (if necessary)
        credit_types = [row[0] for row in data]
        counts = [row[1] for row in data]

        # Plot the data using matplotlib
        fig, ax = plt.subplots()
        ax.bar(credit_types, counts)
        ax.set_xlabel('Credit Types')
        ax.set_ylabel('Count')
        ax.set_title('Distribution of Credit Types')

        # Display the plot in Streamlit
        st.pyplot(fig)
    
    
    if Question == '2.Income Distribution & Descriptive Statistics wrt. Credit Type:':
        # SQL query to get income statistics by credit type
        query_income_stats = """
        SELECT
            NAME_CONTRACT_TYPE,
            COUNT(*) AS count,
            AVG(AMT_INCOME_TOTAL) AS mean_income,
            MIN(AMT_INCOME_TOTAL) AS min_income,
            MAX(AMT_INCOME_TOTAL) AS max_income,
            SUM(AMT_INCOME_TOTAL) AS sum_income
        FROM cleaned_application_data
        GROUP BY NAME_CONTRACT_TYPE
        """

        # Read data into DataFrame
        income_stats = pd.read_sql_query(query_income_stats, mydb)

        # SQL query to get income distribution by credit type
        query_income_distribution = """
        SELECT NAME_CONTRACT_TYPE, AMT_INCOME_TOTAL
        FROM cleaned_application_data
        """

        # Read data into DataFrame
        income_distribution = pd.read_sql_query(query_income_distribution, mydb)

        # Display income statistics in Streamlit
        st.write(":red[Income Statistics by Credit Type:]")
        st.write(income_stats)

        # Plot income distribution
        fig, ax = plt.subplots(figsize=(14, 7))
        sns.barplot(x='NAME_CONTRACT_TYPE', y='AMT_INCOME_TOTAL', data=income_distribution, ax=ax, estimator=sum, ci=None)
        ax.set_title('Income Distribution by Credit Type')
        ax.set_xlabel('Credit Type')
        ax.set_ylabel('Total Income Amount')
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
        # Display the plot in Streamlit
        st.pyplot(fig)

        # Display descriptive statistics
        st.write(":red[Descriptive Statistics for Income Distribution by Credit Type:]")
        st.write(income_distribution.groupby('NAME_CONTRACT_TYPE')['AMT_INCOME_TOTAL'].describe())


    
        
    if Question == '3.Analysis of Goods Amount for Cash Loans:':  
        query_cash_loans = """
        SELECT AMT_GOODS_PRICE
        FROM cleaned_application_data
        WHERE NAME_CONTRACT_TYPE = 'Cash loans'
        """

        cash_loans = pd.read_sql_query(query_cash_loans, mydb)


        plt.figure(figsize=(10, 6))
        sns.histplot(cash_loans['AMT_GOODS_PRICE'], bins=20, kde=True)
        plt.title('Distribution of Goods Amount for Cash Loans')
        plt.xlabel('Goods Amount')
        plt.ylabel('Frequency')
        st.pyplot(plt)
        st.write(cash_loans['AMT_GOODS_PRICE'].describe())
            
                                                        
    if Question == '4.Age Brackets of the Clients:':
        # Query to get age distribution
        query_age_distribution = """
        SELECT CASE
        WHEN DAYS_BIRTH < -36500 THEN '70+'
        WHEN DAYS_BIRTH < -29200 THEN '60-69'
        WHEN DAYS_BIRTH < -21900 THEN '50-59'
        WHEN DAYS_BIRTH < -14600 THEN '40-49'
        WHEN DAYS_BIRTH < -7300 THEN '30-39'
        WHEN DAYS_BIRTH < 0 THEN '20-29'
        END AS age_group,
        COUNT(*) AS count
        FROM cleaned_application_data
        GROUP BY age_group
        """

        # Read data into DataFrame
        age_distribution = pd.read_sql_query(query_age_distribution,mydb)

        # Plotting age distribution
        plt.figure(figsize=(10, 6))
        sns.barplot(x='age_group', y='count', data=age_distribution, palette='viridis')
        plt.title('Age Distribution of Clients')
        plt.xlabel('Age Group')
        plt.ylabel('Number of Clients')
        # Display the plot in Streamlit
        st.pyplot(plt)
                    
    if Question =='5.Documents Submission Analysis:':
        # Query to get document submission analysis
        query_document_submission = """
        SELECT SK_ID_CURR, COUNT(*) AS num_documents
        FROM cleaned_application_data
        WHERE FLAG_DOCUMENT_2 = 1 OR FLAG_DOCUMENT_3 = 1 OR FLAG_DOCUMENT_4 = 1 OR FLAG_DOCUMENT_5 = 1
        OR FLAG_DOCUMENT_6 = 1 OR FLAG_DOCUMENT_7 = 1 OR FLAG_DOCUMENT_8 = 1 OR FLAG_DOCUMENT_9 = 1
        OR FLAG_DOCUMENT_10 = 1 OR FLAG_DOCUMENT_11 = 1 OR FLAG_DOCUMENT_12 = 1 OR FLAG_DOCUMENT_13 = 1
        OR FLAG_DOCUMENT_14 = 1 OR FLAG_DOCUMENT_15 = 1 OR FLAG_DOCUMENT_16 = 1 OR FLAG_DOCUMENT_17 = 1
        OR FLAG_DOCUMENT_18 = 1 OR FLAG_DOCUMENT_19 = 1 OR FLAG_DOCUMENT_20 = 1 OR FLAG_DOCUMENT_21 = 1
        GROUP BY SK_ID_CURR
        """

        # Read data into DataFrame
        document_submission = pd.read_sql_query(query_document_submission, mydb)

        # Displaying the document submission analysis
        st.write(":red[Document Submission Analysis:]")
        st.write(document_submission)

        # Plotting document submission distribution
        plt.figure(figsize=(10, 6))
        sns.histplot(document_submission['num_documents'], bins=20, kde=True, color='skyblue')
        plt.title('Distribution of Number of Documents Submitted')
        plt.xlabel('Number of Documents')
        plt.ylabel('Frequency')
        # Display the plot in Streamlit
        st.pyplot(plt)
    
    if Question =='6.Overall Analysis of Credit Enquiries on Clients:':
        # SQL query for overall analysis of credit inquiries on clients
        query_overall_credit_enquiries = """
        SELECT 
            AMT_REQ_CREDIT_BUREAU_HOUR,
            AMT_REQ_CREDIT_BUREAU_DAY,
            AMT_REQ_CREDIT_BUREAU_WEEK,
            AMT_REQ_CREDIT_BUREAU_MON,
            AMT_REQ_CREDIT_BUREAU_QRT,
            AMT_REQ_CREDIT_BUREAU_YEAR
        FROM 
            cleaned_application_data
        """

        # Execute the SQL query and fetch the results
        overall_credit_enquiries = pd.read_sql_query(query_overall_credit_enquiries, mydb)

        # Display the overall analysis of credit inquiries on clients in Streamlit
        st.write(":red[Overall Analysis of Credit Enquiries on Clients:]")
        st.write(overall_credit_enquiries)

        # Plotting the overall analysis
        plt.figure(figsize=(10, 6))
        overall_credit_enquiries.sum().plot(kind='bar', color='skyblue')
        plt.title('Overall Analysis of Credit Enquiries on Clients')
        plt.xlabel('Credit Inquiry Type')
        plt.ylabel('Total Inquiries')
        plt.xticks(rotation=45)
        # Display the plot in Streamlit
        st.pyplot(plt)

        
        
    if Question =='7.Analysis of individual applications based on the credit enquiries:':
        # Query to get analysis of individual applications based on credit enquiries
        query_individual_credit_enquiries = """
        SELECT SK_ID_CURR, AMT_REQ_CREDIT_BUREAU_HOUR, AMT_REQ_CREDIT_BUREAU_DAY,
            AMT_REQ_CREDIT_BUREAU_WEEK, AMT_REQ_CREDIT_BUREAU_MON,
            AMT_REQ_CREDIT_BUREAU_QRT, AMT_REQ_CREDIT_BUREAU_YEAR
        FROM cleaned_application_data
        """

        # Read data into DataFrame
        individual_credit_enquiries = pd.read_sql_query(query_individual_credit_enquiries, mydb)

        # Displaying the analysis of individual applications based on credit enquiries
        st.write(":red[Analysis of Individual Applications based on Credit Enquiries:]")
        st.write(individual_credit_enquiries)

        # Plotting the distribution of credit inquiries
        plt.figure(figsize=(10, 6))
        sns.barplot(data=individual_credit_enquiries.drop(columns=['SK_ID_CURR']), orient="h", palette="Set2")
        plt.title('Distribution of Credit Inquiries')
        plt.xlabel('Number of Inquiries')
        plt.ylabel('Type of Inquiry')
        plt.yticks(ticks=range(6), labels=['Hour', 'Day', 'Week', 'Month', 'Quarter', 'Year'])
        # Display the plot in Streamlit
        st.pyplot(plt)
        


    if Question == '8.Deeper analysis on the Contact reach for clients who had payment difficulties but were from the Very Low Risk social surroundings:':
        # SQL query to analyze contact reach effectiveness
        query = """
        WITH PaymentDifficulties AS (
            SELECT 
                a.SK_ID_CURR,
                p.CHANNEL_TYPE,
                p.NAME_YIELD_GROUP
            FROM 
                cleaned_application_data a
            INNER JOIN 
                cleaned_previous_application p ON a.SK_ID_CURR = p.SK_ID_CURR
            WHERE 
                a.TARGET = 1 -- Assuming TARGET = 1 indicates payment difficulties
                AND a.REGION_RATING_CLIENT = 1 -- Assuming 1 represents very low-risk social surroundings
        )
        SELECT 
            CHANNEL_TYPE,
            COUNT(*) AS ContactAttempts,
            SUM(CASE WHEN NAME_YIELD_GROUP = 'XNA' THEN 1 ELSE 0 END) AS UnspecifiedAttempts,
            SUM(CASE WHEN NAME_YIELD_GROUP != 'XNA' THEN 1 ELSE 0 END) AS SpecifiedAttempts,
            COUNT(DISTINCT SK_ID_CURR) AS UniqueClients
        FROM 
            PaymentDifficulties
        GROUP BY 
            CHANNEL_TYPE
        ORDER BY 
            ContactAttempts DESC;
        """

        # Execute the SQL query and fetch the results
        result = pd.read_sql_query(query, mydb)

        # Display the analysis of contact reach effectiveness in Streamlit
        st.write(":red[Analysis of Contact Reach Effectiveness:]")
        st.write(result)

        # Plotting the contact reach effectiveness
        plt.figure(figsize=(10, 6))
        sns.barplot(x='CHANNEL_TYPE', y='ContactAttempts', data=result)
        plt.title('Contact Reach Effectiveness')
        plt.xlabel('Channel Type')
        plt.ylabel('Contact Attempts')
        plt.xticks(rotation=45)
        # Display the plot in Streamlit
        st.pyplot(plt)
        
    if Question =='9.Deeper analysis on the Contact reach for clients who had payment difficulties but were from the Very Low Risk social surroundings:':
    
    # SQL query to join current and previous application data
        join_query = """
        SELECT 
            curr.*, 
            prev.SK_ID_PREV,
            prev.AMT_CREDIT AS PREV_AMT_CREDIT,
            prev.AMT_ANNUITY AS PREV_AMT_ANNUITY,
            prev.NAME_CONTRACT_STATUS AS PREV_NAME_CONTRACT_STATUS
        FROM 
            cleaned_application_data curr
        LEFT JOIN 
            cleaned_previous_application prev ON curr.SK_ID_CURR = prev.SK_ID_CURR;
        """

        # Read data into DataFrame
        merged_data = pd.read_sql(join_query,mydb)

        # SQL query to aggregate previous application data
        aggregate_query = """
        SELECT 
            curr.SK_ID_CURR,
            COUNT(prev.SK_ID_PREV) AS PREV_APP_COUNT,
            CASE 
                WHEN COUNT(prev.SK_ID_PREV) > 0 THEN 1
                ELSE 0
            END AS HAS_PREV_APP
        FROM 
            cleaned_application_data curr
        LEFT JOIN 
            cleaned_previous_application prev ON curr.SK_ID_CURR = prev.SK_ID_CURR
        GROUP BY 
            curr.SK_ID_CURR;
        """

        # Read aggregated data into DataFrame
        previous_applications_count = pd.read_sql(aggregate_query, mydb)

        # Merge the aggregated data with the original merged data
        merged_data = pd.merge(merged_data, previous_applications_count, on='SK_ID_CURR', how='left')

        # Display the first few rows of the merged dataset in Streamlit
        st.write(":red[Merged Data:]")
        st.write(merged_data.head())

        # Plotting the count of previous applications and whether each current application has previous applications
        plt.figure(figsize=(10, 6))
        sns.countplot(x='HAS_PREV_APP', data=merged_data, palette='Set2')
        plt.title('Presence of Previous Applications')
        plt.xlabel('Has Previous Application')
        plt.ylabel('Count')
        # Display the plot in Streamlit
        st.pyplot(plt)


    if Question =='10.Top 15 customers and contact reach:':
        # SQL query to get the top 15 customers and their contact reach
        query_top_customers = """
        SELECT 
            SK_ID_CURR,
            COUNT(*) AS ContactAttempts
        FROM 
            cleaned_application_data
        GROUP BY 
            SK_ID_CURR
        ORDER BY 
            ContactAttempts DESC
        LIMIT 15;
        """

        # Read data into DataFrame
        top_customers = pd.read_sql_query(query_top_customers, mydb)

        # Display the top 15 customers and their contact reach in Streamlit
        st.write(":red[Top 15 Customers and Contact Reach:]")
        st.write(top_customers)

        # Plotting the contact reach for the top 15 customers
        plt.figure(figsize=(10, 6))
        sns.barplot(x='SK_ID_CURR', y='ContactAttempts', data=top_customers, palette='viridis')
        plt.title('Contact Reach for Top 15 Customers')
        plt.xlabel('Customer ID')
        plt.ylabel('Contact Attempts')
        plt.xticks(rotation=45)
        # Display the plot in Streamlit
        st.pyplot(plt)
