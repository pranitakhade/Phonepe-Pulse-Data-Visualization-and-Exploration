import streamlit as st
import mysql.connector
import pandas as pd
import plotly.express as px
from decimal import Decimal
import matplotlib.pyplot as plt

conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='phonepe'
)
cursor = conn.cursor()


def convert_to_crores(number):
    if isinstance(number, Decimal):
        number = float(number)  # Convert Decimal to float
    if number >= 1e7:  # 1 Crore is 1e7 (10,000,000)
        result = "{:.2f} Crores".format(number / 1e7)
    else:
        result = "{:.2f}".format(number)
    return result


st.set_page_config(page_title="PhonePe Pulse - Made by: Pranit Akhade",layout="wide",initial_sidebar_state="auto")
#st.set_page_config(page_title="PhonePe Pulse", layout="wide", initial_sidebar_state="expanded")

# Set the title and description at the top left with custom CSS for color
st.markdown('<h1 style="color: #190482;">PhonePe Pulse | The Beat of Progress</h1>', unsafe_allow_html=True)
st.write("Welcome to PhonePe Pulse, where we explore the data and progress.")

st.sidebar.markdown(
    """
    <style>
    div[data-testid="stSidebar"] {
        background-color: purple;
    }
    </style>
    """,
    unsafe_allow_html=True
)
# Type SelectBox
Type = st.sidebar.selectbox("Select Type", ("Transactions", "Users"))

# Year Slider
year = st.sidebar.slider("Select Year", min_value=2018, max_value=2023, value=2018)

# Quarter Slider
quarter_labels = {1: "Q1", 2: "Q2", 3: "Q3", 4: "Q4"}
quarter = st.sidebar.slider("Select Quarter", min_value=1, max_value=4, value=1)
formatted_quarter = quarter_labels[quarter]  # Format the quarter value as needed


if Type == "Transactions":

    col1, col2, col3 = st.columns([1.5,1.5,3],gap='small')

    with col1:
        sql_query11 = '''
            SELECT Year, Quarter, 
                SUM(Transaction_amount) AS Total_Transaction_amount
            FROM Agg_Transaction
            WHERE year = %s AND quarter = %s
            GROUP BY Year, Quarter
            '''
        cursor.execute(sql_query11,(year,formatted_quarter))
        data11 = pd.DataFrame(cursor.fetchall(),columns=['Year','Quarter','Total_Transaction_amount'])

        total_amount = data11["Total_Transaction_amount"].values[0]
        total_amount_crores = convert_to_crores(total_amount)
        #st.write(f"Total Payment {year} - {formatted_quarter}: {total_amount_crores}")
        st.markdown(
            f'<p style="color: black; font-weight: bold;">Total Payment {year} - {formatted_quarter}:</p>'
            f'<p style="color: purple; font-weight: bold;"> {total_amount_crores}</p>',
            unsafe_allow_html=True
        )


    with col2:
        sql_query12 = '''
            SELECT Year, Quarter, 
            SUM(Transaction_count) AS Total_Transaction_count 
            FROM Agg_Transaction
            WHERE year = %s AND quarter = %s
            GROUP BY Year, Quarter
            '''
        cursor.execute(sql_query12,(year,formatted_quarter))
        data12 = pd.DataFrame(cursor.fetchall(),columns=['Year','Quarter','Total_Transaction_count'])

        total_count = data12["Total_Transaction_count"].values[0]
        #st.write(f"Total Payment {year} - {formatted_quarter}: {total_count}")
        st.markdown(
            f'<p style="color: black; font-weight: bold;">Total Payment {year} - {formatted_quarter}:</p>'
            f'<p style="color: purple; font-weight: bold;"> {total_count}</p>',
            unsafe_allow_html=True
        )


    with col3:
        sql_query13 = '''
            SELECT Year,Quarter,Transaction_type,
            SUM(Transaction_count) AS Total_Count 
            FROM Agg_Transaction 
            WHERE year = %s AND quarter = %s
            GROUP BY Year,Quarter,Transaction_type
        '''
        cursor.execute(sql_query13,(year,formatted_quarter))
        data13 = pd.DataFrame(cursor.fetchall(),columns=['Year','Quarter','Transaction_type','Total_Count'])

        #st.write(f"Total Transaction Count for {year} - {formatted_quarter}")
        #st.write(data13[["Transaction_type", "Total_Count"]])

        st.markdown(
            f'<p style="color: black; font-weight: bold;">Total Transaction Count for {year} - {formatted_quarter}:</p>',
            unsafe_allow_html=True
        )
        st.write(data13[["Transaction_type", "Total_Count"]])


    st.markdown("### :violet[State ]")
    sql_query1 = '''
        SELECT State,
            SUM(Transaction_count) AS Transactions_Count,
            SUM(Transaction_amount) AS Transaction_amount
        FROM Agg_Transaction
        WHERE year = %s AND quarter = %s
        GROUP BY State
        ORDER BY Transactions_Count DESC
    '''
    cursor.execute(sql_query1, (year, formatted_quarter))
    data1 = pd.DataFrame(cursor.fetchall(), columns=["State", "Transactions_Count", "Transaction_amount"])

    data1['State'] = data1['State'].str.replace('-', ' ')
    data1['State'] = data1['State'].str.title()
    data1['Transaction_amount'] = data1['Transaction_amount'].apply(convert_to_crores)
    data1['State'] = data1['State'].str.replace('&', 'and')
    data1['State'] = data1['State'].str.replace('Andaman and Nicobar Islands', 'Andaman & Nicobar')

    fig = px.choropleth(data1, geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                        featureidkey='properties.ST_NM',
                        locations='State',
                        color='Transactions_Count',
                        hover_data='Transaction_amount',
                        color_continuous_scale='purples')
    

    fig.update_geos(fitbounds="locations", visible=False)
    st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns([3, 3], gap="small")
    with col1:
        sql_query2 = '''
                        SELECT State,
                            SUM(Transaction_count) AS Transactions_Count,
                            SUM(Transaction_amount) AS Transaction_amount
                        FROM Agg_Transaction
                        WHERE year = %s AND quarter = %s
                        GROUP BY State
                        ORDER BY Transactions_Count DESC
                        LIMIT 10
                    '''
        cursor.execute(sql_query2, (year, formatted_quarter))
        data2 = pd.DataFrame(cursor.fetchall(), columns=["State", "Transactions_Count", "Transaction_amount"])

        data2['State'] = data2['State'].str.replace('-', ' ')
        data2['State'] = data2['State'].str.title()
        data2['Transaction_amount'] = data2['Transaction_amount'].apply(convert_to_crores)

        fig = px.pie(data2, values='Transactions_Count', names='State',
                    title='Top 10 States by Total Count',
                    color_discrete_sequence=px.colors.sequential.Agsunset,
                    hover_data=['Transaction_amount'],
                    labels={'Transactions_Count': 'Transactions Count'})

        # Update trace settings
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)


    with col2:
        sql_query3 = '''
                SELECT Map_district,
                      SUM(Map_count) AS Total_Count,
                      SUM(Map_amount) AS Total_Amount
                FROM Map_Transaction
                WHERE year = %s AND quarter = %s
                GROUP BY Map_District
                ORDER BY Total_Amount DESC
                LIMIT 10
            '''
        cursor.execute(sql_query3, (year, formatted_quarter))
        data3 = pd.DataFrame(cursor.fetchall(), columns=["Map_district", "Total_Count", "Total_Amount"])

        data3['Map_district'] = data3['Map_district'].str.capitalize()
        data3['Map_district'] = data3['Map_district'].str.replace(' district', '')
        data3['Total_Amount'] = data3['Total_Amount'].apply(convert_to_crores)

        fig = px.pie(data3, values='Total_Count', names='Map_district',
             title='Top 10 Districts by Total Count',
             color_discrete_sequence=px.colors.sequential.Agsunset,
             hover_data=['Total_Amount'],
             labels={'Total_Count': 'Total Count'})
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns([3, 3], gap="small")
    with col1:
        sql_query4 = '''
            SELECT Pincode,
                SUM(Transaction_Count) AS Total_Transaction_Count,
                SUM(Transaction_Amount) AS Total_Transaction_Amount
            FROM Top_Transaction
            WHERE year = %s AND quarter = %s
            GROUP BY Pincode
            ORDER BY Total_Transaction_Amount DESC
            LIMIT 10
        '''
        cursor.execute(sql_query4, (year, formatted_quarter))
        data4 = pd.DataFrame(cursor.fetchall(), columns=['Pincode', 'Total_Transaction_Count', 'Total_Transaction_Amount'])

        data4['Total_Transaction_Amount'] = data4['Total_Transaction_Amount'].apply(convert_to_crores)

        fig = px.pie(data4, values='Total_Transaction_Count', names='Pincode',
                    title='Top 10 Pincodes by Total Count',
                    color_discrete_sequence=px.colors.sequential.Agsunset,
                    hover_data=['Total_Transaction_Amount'],
                    labels={'Total_Transaction_Count': 'Total Transaction Count'})
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        sql_query9 = '''
                SELECT Transaction_type,
                    SUM(Transaction_count) AS Total_Transaction_count,
                    SUM(Transaction_amount) AS Total_Transaction_amount
                FROM Agg_Transaction
                WHERE year = %s AND quarter = %s
                GROUP BY Transaction_type
                ORDER BY Transaction_type
            '''
        cursor.execute(sql_query9,(year,formatted_quarter))
        data9 = pd.DataFrame(cursor.fetchall(),columns = ['Transaction_type','Total_Transaction_count','Total_Transaction_amount'])

        fig = px.bar(data9,
                    title='Transaction Types vs Total Transactions',
                    x="Transaction_type",
                    y="Total_Transaction_count",
                    orientation='v',
                    color='Total_Transaction_amount',
                    color_continuous_scale=px.colors.sequential.Agsunset)
        st.plotly_chart(fig,use_container_width=True)

    sql_query10 = '''
            SELECT Year, Quarter, SUM(Transaction_count) AS Total_Transaction_Count
            FROM Agg_Transaction
            GROUP BY Year, Quarter
            '''
    cursor.execute(sql_query10)
    data10 = pd.DataFrame(cursor.fetchall(),columns = ['Year','Quarter','Total_Transaction_Count'])
    data10['YearQuarter'] = data10['Year'].astype(str) + ' ' + data10['Quarter']

    plt.figure(figsize=(12, 6))
    plt.plot(data10['YearQuarter'], data10['Total_Transaction_Count'], marker='o')
    plt.title('Sum of Transaction Count Over Time')
    plt.xlabel('Year and Quarter')
    plt.ylabel('Transaction Count')
    plt.xticks(rotation=45)
    st.pyplot(plt)
    plt.close()

    plt.figure(figsize=(12, 6))
    plt.bar(data10['YearQuarter'], data10['Total_Transaction_Count'])
    plt.title('Sum of Transaction Count by Year and Quarter')
    plt.xlabel('Year and Quarter')
    plt.ylabel('Transaction Count')
    plt.xticks(rotation=45)
    st.pyplot(plt)
    plt.close()

if Type == "Users":

    col1, col2 = st.columns([1,1],gap='small')

    with col1:
        sql_query14 = '''
            SELECT Year, Quarter, SUM(Registered_users) AS Total_Registered_users
            FROM Map_User
            WHERE year = %s AND quarter = %s
            GROUP BY Year, Quarter
            '''
        cursor.execute(sql_query14,(year, formatted_quarter))
        data14 = pd.DataFrame(cursor.fetchall(),columns=['Year','Quarter','Total_Registered_users'])

        total_users = data14["Total_Registered_users"].values[0]
        #st.write(f"Total Users {year} - {formatted_quarter}: {total_users}")

        st.markdown(
            f'<p style="color: black; font-weight: bold;">Total Users {year} - {formatted_quarter}:</p>'
            f'<p style="color: purple; font-weight: bold;"> {total_users}</p>',
            unsafe_allow_html=True
        )

    with col2:
        sql_query15 = '''
            SELECT Year, Quarter, SUM(App_Opens) AS Total_App_Opens
            FROM Map_User
            WHERE year = %s AND quarter = %s
            GROUP BY Year, Quarter
            '''
        cursor.execute(sql_query15,(year, formatted_quarter))
        data15 = pd.DataFrame(cursor.fetchall(),columns=['Year','Quarter','Total_App_Opens'])

        total_app_open = data15["Total_App_Opens"].values[0]
        #st.write(f"Total App Open {year} - {formatted_quarter}: {total_app_open}")

        st.markdown(
            f'<p style="color: black; font-weight: bold;">Total App Open {year} - {formatted_quarter}:</p>'
            f'<p style="color: purple; font-weight: bold;"> {total_app_open}</p>',
            unsafe_allow_html=True
        )

    st.markdown("### :violet[State]")

    sql_query13 = '''
                SELECT State,
                      SUM(Registered_users) AS Total_Registered_users,
                      SUM(App_Opens) AS Total_App_Opens
                FROM Map_User
                WHERE year = %s AND quarter = %s
                GROUP BY State
                ORDER BY Total_Registered_users DESC
            '''
    cursor.execute(sql_query13,(year,formatted_quarter))
    data13 = pd.DataFrame(cursor.fetchall(), columns=['State','Total_Registered_users','Total_App_Opens'])

    data13['State'] = data13['State'].str.replace('-', ' ')
    data13['State'] = data13['State'].str.title()
    data13['State'] = data13['State'].str.replace('&', 'and')
    data13['State'] = data13['State'].str.replace('Andaman and Nicobar Islands', 'Andaman & Nicobar')

    fig = px.choropleth(data13,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                      featureidkey='properties.ST_NM',
                      locations='State',
                      color='Total_Registered_users',
                      hover_data= 'Total_App_Opens',
                      color_continuous_scale='purples')

    fig.update_geos(fitbounds="locations", visible=False)
    st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns([3,3],gap='small')

    with col1:
        sql_query5 = '''
                SELECT User_brand,
                      SUM(User_count) AS Total_User_Count,
                      AVG(User_percentage)*100 AS Total_User_Percentage
                FROM Agg_User
                WHERE year = %s AND quarter = %s
                GROUP BY User_Brand
                ORDER BY Total_User_Count DESC
                LIMIT 10
            '''
        cursor.execute(sql_query5,(year, formatted_quarter))
        data5 = pd.DataFrame(cursor.fetchall(), columns = ['User_brand','Total_User_Count','Total_User_Percentage'])

        fig = px.pie(data5, values='Total_User_Count', names='User_brand',
                    title='Top 10 Brands by Count',
                    color_discrete_sequence=px.colors.sequential.Agsunset,
                    #hover_data=['Total_Transaction_Amount'],
                    labels={'Total_User_Count': 'Total User Count'})
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig,use_container_width=True)

    with col2:
        fig = px.bar(data5,title='Top 10 Brands with their Count',
                    x="Total_User_Count",
                    y="User_brand",
                    orientation='h',
                    color='Total_User_Percentage',
                    color_continuous_scale=px.colors.sequential.Agsunset)
        st.plotly_chart(fig, use_container_width=True)

    col3,col4 = st.columns([3,3],gap='small')

    with col3:
        sql_query6 = '''
                SELECT District,
                      SUM(Registered_users) AS Total_Registered_users
                FROM Map_User
                WHERE year = %s AND quarter = %s
                GROUP BY District
                ORDER BY Total_Registered_users DESC
                LIMIT 10
            '''
        cursor.execute(sql_query6,(year, formatted_quarter))
        data6 = pd.DataFrame(cursor.fetchall(), columns=['District','Total_Registered_users'])

        data6['District']= data6['District'].str.replace(' district','')
        data6['District'] = data6['District'].str.title()

        fig = px.pie(data6, values='Total_Registered_users', names='District',
                    title='Top 10 Districts by Total Registered Users',
                    color_discrete_sequence=px.colors.sequential.Agsunset,
                    #hover_data=['Total_Transaction_Amount'],
                    labels={'Total_Registered_users': 'Total Registered Users'})
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)

    
    with col4:
        sql_query7 = '''
                SELECT State,
                      SUM(User_count) AS Total_User_Count
                FROM Agg_User
                WHERE year = %s AND quarter = %s
                GROUP BY State
                ORDER BY Total_User_Count DESC
                LIMIT 10
            '''
        cursor.execute(sql_query7,(year, formatted_quarter))
        data7 = pd.DataFrame(cursor.fetchall(), columns=['State','Total_User_Count'])

        data7['State'] = data7['State'].str.title()

        fig = px.pie(data7, values='Total_User_Count', names='State',
                    title='Top 10 State by Total User Count',
                    color_discrete_sequence=px.colors.sequential.Agsunset,
                    #hover_data=['Total_Transaction_Amount'],
                    labels={'Total_User_Count': 'Total User Count'})
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)


    col5, col6, col7 = st.columns([1,3,1],gap='small')

    with col6:
        sql_query8 = '''
                SELECT Pincode,
                      SUM(Registered_users) AS Total_Registered_Users
                FROM Top_User
                WHERE year = %s AND quarter = %s
                GROUP BY Pincode
                ORDER BY Total_Registered_Users DESC
                LIMIT 10
            '''
        cursor.execute(sql_query8,(year, formatted_quarter))
        data8 = pd.DataFrame(cursor.fetchall(), columns=['Pincode','Total_Registered_Users'])

        fig = px.pie(data8, values='Total_Registered_Users', names='Pincode',
                    title='Top 10 Pincode by Total Users',
                    color_discrete_sequence=px.colors.sequential.Agsunset,
                    #hover_data=['Total_Transaction_Amount'],
                    labels={'Total_Registered_Users': 'Total Registered Users'})
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)




cursor.close()
conn.close()






