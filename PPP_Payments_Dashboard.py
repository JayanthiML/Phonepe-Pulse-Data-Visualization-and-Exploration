import streamlit as st
import pandas as pd
import requests
import json
import mysql.connector
import plotly.express as px
import locale

# Set the locale to Indian numbering system
locale.setlocale(locale.LC_NUMERIC, 'en_IN')

# Fetch data from MySQL Data base
# Connect to MySQL
mysql_connection = mysql.connector.connect(
    host="127.0.0.1",
    port=3306,
    user="root",
    password="MySql_Password",
    database="phonepe_pulse"
)

mysql_cursor = mysql_connection.cursor()

# Configure the default settings of the page.
st.set_page_config(page_title='PhonePe Pulse - Payments', page_icon="rupee.png", layout="wide")

# Title
st.header(':white[Phonepe Pulse Payments and Users Data Visualization ]')

# Function to fetch data from MySQL based on user selections
def fetch_trans_data(year, quarter, transaction_type):
    cursor = mysql_connection.cursor()
    query = f"SELECT State, Transaction_count, Transaction_amount FROM aggregated_transaction WHERE Year = '{trans_year}' AND Quarter = '{trans_quarter}' AND Transaction_type = '{transaction_type}';"
    cursor.execute(query)
    data = cursor.fetchall()
    df_trans = pd.DataFrame(data, columns=['State', 'Transaction_count', 'Transaction_amount'])
    cursor.close()
    return df_trans

def fetch_state_trans_data(state, year, quarter):
    cursor = mysql_connection.cursor()
    query = f"SELECT Transaction_type, Transaction_count, Transaction_amount FROM aggregated_transaction WHERE State = '{trans_state}' AND Year = '{trans_state_year}' AND Quarter = '{trans_state_quarter}';"
    cursor.execute(query)
    data = cursor.fetchall()
    df_state_trans = pd.DataFrame(data, columns=['Transaction_type', 'Transaction_count', 'Transaction_amount'])
    cursor.close()
    return df_state_trans

def fetch_map_trans_data(state, year, quarter):
    cursor = mysql_connection.cursor()
    query = f"SELECT District, Transaction_Count, Transaction_Amount FROM map_transaction WHERE State = '{trans_state}' AND Year = '{trans_state_year}' AND Quarter = '{trans_state_quarter}';"
    cursor.execute(query)
    data = cursor.fetchall()
    df_map_trans = pd.DataFrame(data, columns=['District', 'Transaction_count', 'Transaction_amount'])
    cursor.close()
    return df_map_trans

def fetch_top_trans_data(year):
    cursor = mysql_connection.cursor()
    query = f"SELECT State, SUM(Transaction_amount) As Transaction_amount FROM top_transaction WHERE Year = '{trans_top_year}'GROUP BY State ORDER BY Transaction_amount DESC LIMIT 10;"
    cursor.execute(query)
    data = cursor.fetchall()
    df_top_trans = pd.DataFrame(data, columns=['State', 'Top 10 Transaction amount'])
    cursor.close()
    return df_top_trans

def fetch_top_trans_dist_data(state, year):
    cursor = mysql_connection.cursor()
    query = f"SELECT District, SUM(Transaction_Amount) As Transaction_amount FROM map_transaction WHERE State = '{top_state}' AND Year = '{trans_top_year}' GROUP BY District ORDER BY Transaction_amount DESC LIMIT 10;"
    cursor.execute(query)
    data = cursor.fetchall()
    df_top_dist_trans = pd.DataFrame(data, columns=['District', 'Top 10 Transaction amount'])
    cursor.close()
    return df_top_dist_trans

def fetch_user_data(year, quarter):
    cursor = mysql_connection.cursor()
    query = f"SELECT State, Total_Registered_Users FROM aggregated_user WHERE Year = '{user_year}' AND Quarter = '{user_quarter}' ;"
    cursor.execute(query)
    data = cursor.fetchall()
    df_user = pd.DataFrame(data, columns=['State', 'Total_Registered_Users'])
    cursor.close()
    return df_user

def fetch_state_user_data(state, year):
    cursor = mysql_connection.cursor()
    query = f"SELECT Quarter, Total_Registered_Users FROM aggregated_user WHERE State = '{user_state}' AND Year = '{user_state_year}';"
    cursor.execute(query)
    data = cursor.fetchall()
    df_state_user = pd.DataFrame(data, columns=['Quarter', 'Total_Registered_Users'])
    cursor.close()
    return df_state_user

def fetch_map_user_data(state, year):
    cursor = mysql_connection.cursor()
    query = f"SELECT District, SUM(Registered_User) AS Total_Registered_Users FROM map_user WHERE State = '{user_state}' AND Year = '{user_state_year}' GROUP BY District;"
    cursor.execute(query)
    data = cursor.fetchall()
    df_map_user = pd.DataFrame(data, columns=['District', 'Registered_User'])
    cursor.close()
    return df_map_user

def fetch_top_user_data(year):
    cursor = mysql_connection.cursor()
    query = f"SELECT State, SUM(Registered_User) AS Top_user FROM top_user WHERE Year = '{user_top_year}' GROUP BY State ORDER BY Top_user DESC LIMIT 10;"
    cursor.execute(query)
    data = cursor.fetchall()
    df_top_user = pd.DataFrame(data, columns=['State', 'Top 10 User Count'])
    cursor.close()
    return df_top_user

def fetch_top_user_dist_data(state, year):
    cursor = mysql_connection.cursor()
    query = f"SELECT District, SUM(Registered_User) AS Top_user FROM map_user WHERE State = '{top_state}' AND Year = '{user_top_year}' GROUP BY District ORDER BY Top_user DESC LIMIT 10;"
    cursor.execute(query)
    data = cursor.fetchall()
    df_top_dist_user = pd.DataFrame(data, columns=['District', 'Top 10 User Count'])
    cursor.close()
    return df_top_dist_user

# Selection option
option = st.radio('',('All India', 'State wise','Top Trends'),horizontal=True)

if option == 'All India':
    tab1, tab2 = st.tabs(['Transaction', 'User'])
    with tab1:
        col1, col2 = st.columns([3, 1])
        with col1:
            col3, col4, col5 = st.columns(3)
            with col3:
                trans_year = st.selectbox("Select Year", ['Select', '2018', '2019', '2020', '2021', '2022'], key='year_selectbox')
            with col4:
                trans_quarter = st.selectbox("Select Quarter", ['Select', '1', '2', '3', '4'], key='quarter_selectbox')
            with col5:
                transaction_type = st.selectbox("Select Transaction Type", ['Select', 'Recharge & bill payments', 'Peer-to-peer payments', 'Merchant payments', 'Financial Services', 'Others'], key='transaction_type_selectbox')
            
            # Check if all three select boxes have been set to a valid option
            if trans_year != 'Select' and trans_quarter != 'Select' and transaction_type != 'Select':

                trans_data = fetch_trans_data(trans_year, trans_quarter, transaction_type)
                trans_data.insert(0, 'No.', range(1, len(trans_data) + 1))
                trans_data['Transaction_count'] = trans_data['Transaction_count'].apply(lambda x: locale.format('%d', x, grouping=True))
                trans_data['Transaction_amount'] = trans_data['Transaction_amount'].apply(lambda x: locale.format('%d', x, grouping=True))
                trans_data['Transaction_amount'] = '\u20B9 ' + trans_data['Transaction_amount']

                st.dataframe(trans_data, hide_index=True)
                
        with col2:
            with st.container():
                if trans_year != 'Select' and trans_quarter != 'Select' and transaction_type != 'Select':
                    # for Summary of Transaction
                    summary_trans_data = fetch_trans_data(trans_year, trans_quarter, transaction_type)

                    total_count = summary_trans_data['Transaction_count'].sum()
                    average_count = summary_trans_data['Transaction_count'].mean()
                    total_amount = summary_trans_data['Transaction_amount'].sum()
                    average_amount = summary_trans_data['Transaction_amount'].mean()

                    total_count_formatted = locale.format("%d", total_count, grouping=True)
                    average_count_formatted = locale.format("%d", average_count, grouping=True)  
                    total_amount_formatted = "₹ " + locale.format("%d", total_amount, grouping=True)  
                    average_amount_formatted = "₹ " + locale.format("%d", average_amount, grouping=True)
                    
                    summary_trans_df = pd.DataFrame({
                        'Metric': ['Total Transaction Count', 'Average Transaction Count', 'Total Transaction Amount', 'Average Transaction Amount'],
                        'Value': [total_count_formatted, average_count_formatted, total_amount_formatted, average_amount_formatted]
                    })
                    
                    st.subheader("Summary of Transactions:")
                    st.dataframe(summary_trans_df, hide_index=True)
        
        # ------    /  Geo visualization dashboard for Transaction /   ---- #
        if trans_year != 'Select' and trans_quarter != 'Select' and transaction_type != 'Select':

            trans_data_geo = fetch_trans_data(trans_year, trans_quarter, transaction_type)
            trans_data_map = trans_data_geo.copy()
            columns_to_drop = ['State', 'Transaction_count'] 
            trans_data_map.drop(columns=columns_to_drop, inplace=True)

            # Clone the gio data
            url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
            response = requests.get(url)
            data1 = json.loads(response.content)

            # Extract state names and sort them in alphabetical order
            state_names_tra = [feature['properties']['ST_NM'] for feature in data1['features']]
            state_names_tra.sort()

            # Create a DataFrame with the state names column
            df_state_names_tra = pd.DataFrame({'State': state_names_tra})
            
            # Combine the Gio State name with data
            df_state_names_tra['Transaction_amount']=trans_data_map

            # convert dataframe to csv file
            df_state_names_tra.to_csv('State_trans.csv', index=False)

            # Read csv
            df_trans = pd.read_csv('State_trans.csv')

            # Geo plot
            fig_trans = px.choropleth(
                df_trans,
                geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                featureidkey='properties.ST_NM',locations='State',color='Transaction_amount',color_continuous_scale='aggrnyl',title = 'Transaction Analysis')
            fig_trans.update_geos(fitbounds="locations", visible=False)
            fig_trans.update_layout(title_font=dict(size=33),title_font_color='#FBFBFB', height=800)
            fig_trans.update_geos(bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_trans,use_container_width=True)

            # Bar
            trans_data_geo['State'] = trans_data_geo['State'].astype(str)
            trans_data_geo['Transaction_amount'] = trans_data_geo['Transaction_amount'].astype(float)
            trans_data_bar = px.bar(trans_data_geo , x = 'State', y ='Transaction_amount', color ='Transaction_amount', color_continuous_scale = 'aggrnyl', title = 'Transaction Analysis Chart', height = 700,)
            trans_data_bar.update_layout(title_font=dict(size=33),title_font_color='#6739b7')
            st.plotly_chart(trans_data_bar,use_container_width=True)

    with tab2:
        col1, col2 = st.columns([3, 1])
        with col1:
            col3, col4 = st.columns(2)
            with col3:
                user_year = st.selectbox("Select Year", ['Select', '2018', '2019', '2020', '2021', '2022'], key='year_user_selectbox')
            with col4:
                user_quarter = st.selectbox("Select Quarter", ['Select', '1', '2', '3', '4'], key='quarter_user_selectbox')
            
            if user_year != 'Select' and user_quarter != 'Select':
                                    
                user_data = fetch_user_data(user_year, user_quarter)
                user_data.insert(0, 'No.', range(1, len(user_data) + 1))
                user_data['Total_Registered_Users'] = user_data['Total_Registered_Users'].apply(lambda x: locale.format('%d', x, grouping=True))
                st.dataframe(user_data, hide_index=True)

        with col2:
            with st.container():
                if user_year != 'Select' and user_quarter != 'Select':

                    summary_user = fetch_user_data(user_year, user_quarter)

                    total_registered_count = summary_user['Total_Registered_Users'].sum()
                    total_registered_count_formatted = locale.format("%d", total_registered_count, grouping=True)
                
                    summary_user_data = pd.DataFrame({
                        'Metric': ['Total Registered Users'],
                        'Value': [total_registered_count_formatted]
                    })

                    st.subheader("Summary of Transactions:")
                    st.dataframe(summary_user_data, hide_index=True)

        # ------    /  Geo visualization dashboard for User /   ---- #
        if user_year != 'Select' and user_quarter != 'Select':
            user_geo = fetch_user_data(user_year, user_quarter)
            user_data_map = user_geo.copy()
            columns_to_drop = ['State'] 
            user_data_map.drop(columns=columns_to_drop, inplace=True)

            # Clone the gio data
            url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
            response = requests.get(url)
            data1 = json.loads(response.content)

            # Extract state names and sort them in alphabetical order
            state_names_user = [feature['properties']['ST_NM'] for feature in data1['features']]
            state_names_user.sort()

            # Create a DataFrame with the state names column
            df_state_names_user = pd.DataFrame({'State': state_names_user})
            
            # Combine the Gio State name with data
            df_state_names_user['Total_Registered_Users']=user_data_map

            # convert dataframe to csv file
            df_state_names_user.to_csv('State_user.csv', index=False)

            # Read csv
            df_user = pd.read_csv('State_user.csv')

            # Geo plot
            fig_user = px.choropleth(
                df_user,
                geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                featureidkey='properties.ST_NM',locations='State',color='Total_Registered_Users',color_continuous_scale='YlOrRd',title = 'User Analysis')
            fig_user.update_geos(fitbounds="locations", visible=False)
            fig_user.update_layout(title_font=dict(size=33),title_font_color='#FBFBFB', height=800)
            fig_user.update_geos(bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_user,use_container_width=True)

            # Bar
            user_geo['State'] = user_geo['State'].astype(str)
            user_geo['Total_Registered_Users'] = user_geo['Total_Registered_Users'].astype(int)
            user_data_bar = px.bar(user_geo , x = 'State', y ='Total_Registered_Users', color ='Total_Registered_Users', color_continuous_scale = 'YlOrRd', title = 'User Analysis Chart', height = 700,)
            user_data_bar.update_layout(title_font=dict(size=33),title_font_color='#6739b7')
            st.plotly_chart(user_data_bar,use_container_width=True)

elif option == "State wise":
    tab3, tab4 = st.tabs(['Transaction', 'User'])
    with tab3:
        col1, col2 = st.columns([3,1])
        with col1:
            col3, col4, col5 = st.columns(3)
            with col3: 
                trans_state = st.selectbox("Select State", ('Select', 'andaman-&-nicobar-islands', 'andhra-pradesh', 'arunachal-pradesh','assam', 'bihar', 
                    'chandigarh', 'chhattisgarh','dadra-&-nagar-haveli-&-daman-&-diu', 'delhi', 'goa', 'gujarat', 'haryana', 'himachal-pradesh', 
                    'jammu-&-kashmir', 'jharkhand', 'karnataka', 'kerala', 'ladakh', 'lakshadweep', 'madhya-pradesh','maharashtra', 'manipur', 
                    'meghalaya', 'mizoram', 'nagaland','odisha', 'puducherry', 'punjab', 'rajasthan', 'sikkim', 'tamil-nadu', 'telangana', 
                'tripura', 'uttar-pradesh', 'uttarakhand', 'west-bengal'), key='state_selectbox')
            with col4:
                trans_state_year = st.selectbox("Select Year", ['Select', '2018', '2019', '2020', '2021', '2022'], key='year_state_selectbox')
            with col5:
                trans_state_quarter = st.selectbox("Select Quarter", ['Select', '1', '2', '3', '4'], key='quarter_state_selectbox')
        
        with col2:
            if trans_state != 'Select' and trans_state_year != 'Select' and trans_state_quarter != 'Select':

                summary_state_trans_data = fetch_state_trans_data(trans_state, trans_state_year, trans_state_quarter)
                
                total_count = summary_state_trans_data['Transaction_count'].sum()
                average_count = summary_state_trans_data['Transaction_count'].mean()
                total_amount = summary_state_trans_data['Transaction_amount'].sum()
                average_amount = summary_state_trans_data['Transaction_amount'].mean()

                total_count_formatted = locale.format("%d", total_count, grouping=True)
                average_count_formatted = locale.format("%d", average_count, grouping=True)  
                total_amount_formatted = "₹ " + locale.format("%d", total_amount, grouping=True)  
                average_amount_formatted = "₹ " + locale.format("%d", average_amount, grouping=True)

                summary_state_trans_df = pd.DataFrame({
                    'Metric': ['Total Transaction Count', 'Average Transaction Count', 'Total Transaction Amount', 'Average Transaction Amount'],
                    'Value': [total_count_formatted, average_count_formatted, total_amount_formatted, average_amount_formatted]
                })
                with st.container():
                    st.subheader("Summary of Transactions:")
                    st.dataframe(summary_state_trans_df, hide_index=True)

        col6, col7 = st.columns([1,2])
        with col6:
            if trans_state != 'Select' and trans_state_year != 'Select' and trans_state_quarter != 'Select':

                map_trans_data = fetch_map_trans_data(trans_state, trans_state_year, trans_state_quarter)
                
                map_trans_data['Transaction_count'] = map_trans_data['Transaction_count'].apply(lambda x: locale.format('%d', x, grouping=True))
                map_trans_data['Transaction_amount'] = map_trans_data['Transaction_amount'].apply(lambda x: locale.format('%d', x, grouping=True))
                map_trans_data['Transaction_amount'] = '\u20B9 ' + map_trans_data['Transaction_amount']

                st.dataframe(map_trans_data, hide_index=True)
        
        with col7:
            if trans_state != 'Select' and trans_state_year != 'Select' and trans_state_quarter != 'Select':

                map_trans_bar = fetch_map_trans_data(trans_state, trans_state_year, trans_state_quarter)
                
                map_trans_bar['District'] = map_trans_bar['District'].astype(str)
                map_trans_bar['Transaction_amount'] = map_trans_bar['Transaction_amount'].astype(float)
                map_trans_data_bar = px.bar(map_trans_bar , x = 'District', y ='Transaction_amount', color ='Transaction_amount', color_continuous_scale = 'aggrnyl', title = 'Transaction Analysis Chart', height = 700,)
                map_trans_data_bar.update_layout(title_font=dict(size=33),title_font_color='#6739b7')
                st.plotly_chart(map_trans_data_bar,use_container_width=True)

        col8, col9 = st.columns([1,2])
        state_trans_data = None
        with col8:
            if trans_state != 'Select' and trans_state_year != 'Select' and trans_state_quarter != 'Select':
                
                state_trans_data = fetch_state_trans_data(trans_state, trans_state_year, trans_state_quarter)
                
                state_trans_data['Transaction_count'] = state_trans_data['Transaction_count'].apply(lambda x: locale.format('%d', x, grouping=True))
                state_trans_data['Transaction_amount'] = state_trans_data['Transaction_amount'].apply(lambda x: locale.format('%d', x, grouping=True))
                state_trans_data['Transaction_amount'] = '\u20B9 ' + state_trans_data['Transaction_amount']

                st.dataframe(state_trans_data, hide_index=True)
        with col9:
            if trans_state != 'Select' and trans_state_year != 'Select' and trans_state_quarter != 'Select':
                state_trans_bar = fetch_state_trans_data(trans_state, trans_state_year, trans_state_quarter)
                state_trans_bar['Transaction_type'] = state_trans_bar['Transaction_type'].astype(str)
                state_trans_bar['Transaction_amount'] = state_trans_bar['Transaction_amount'].astype(float)
                state_trans_data_bar = px.bar(state_trans_data , x = 'Transaction_type', y ='Transaction_amount', color ='Transaction_amount', color_continuous_scale = 'aggrnyl', title = 'Transaction Analysis Chart', height = 700,)
                state_trans_data_bar.update_layout(title_font=dict(size=33),title_font_color='#6739b7')
                st.plotly_chart(state_trans_data_bar,use_container_width=True)

    with tab4:
        col1, col2 = st.columns([3, 1])
        with col1:
            col3, col4 = st.columns(2)
            with col3:
                user_state = st.selectbox('Select State',('Select', 'andaman-&-nicobar-islands', 'andhra-pradesh', 'arunachal-pradesh','assam', 'bihar', 
                'chandigarh', 'chhattisgarh','dadra-&-nagar-haveli-&-daman-&-diu', 'delhi', 'goa', 'gujarat', 'haryana', 'himachal-pradesh', 
                'jammu-&-kashmir', 'jharkhand', 'karnataka', 'kerala', 'ladakh', 'lakshadweep', 'madhya-pradesh','maharashtra', 'manipur', 
                'meghalaya', 'mizoram', 'nagaland','odisha', 'puducherry', 'punjab', 'rajasthan', 'sikkim', 'tamil-nadu', 'telangana', 
                'tripura', 'uttar-pradesh', 'uttarakhand', 'west-bengal'),key='user_state')

            with col4:
                user_state_year = st.selectbox("Select Year", ['Select', '2018', '2019', '2020', '2021', '2022'], key='year_state_user_selectbox')
            
        with col2:
            if user_state != 'Select' and user_state_year != 'Select':
                
                summary_state_user_df = fetch_state_user_data(user_state, user_state_year)
                               
                total_registered_count = summary_state_user_df['Total_Registered_Users'].sum()
                total_registered_count_formatted = locale.format("%d", total_registered_count, grouping=True)
                
                summary_state_user_data = pd.DataFrame({
                    'Metric': ['Total Registered Users'],
                    'Value': [total_registered_count_formatted]
                })

                with st.container():
                    if summary_state_user_data is not None:
                        st.subheader("Summary of Transactions:")
                        st.dataframe(summary_state_user_data, hide_index=True)

        col5, col6 = st.columns([1,2])
        with col5:
            if user_state != 'Select' and user_state_year != 'Select':
                
                map_user_data = fetch_map_user_data(user_state, user_state_year)
                map_user_data['Registered_User'] = map_user_data['Registered_User'].apply(lambda x: locale.format('%d', x, grouping=True))

                st.dataframe(map_user_data, hide_index=True)

        with col6:
            if user_state != 'Select' and user_state_year != 'Select':
                map_user_bar = fetch_map_user_data(user_state, user_state_year)
                map_user_bar['District'] = map_user_bar['District'].astype(str)
                map_user_bar['Registered_User'] = map_user_bar['Registered_User'].astype(float)
                map_user_data_bar = px.bar(map_user_bar , x = 'District', y ='Registered_User', color ='Registered_User', color_continuous_scale = 'aggrnyl', title = 'User Analysis Chart', height = 700,)
                map_user_data_bar.update_layout(title_font=dict(size=33),title_font_color='#6739b7')
                st.plotly_chart(map_user_data_bar,use_container_width=True)

        col8, col9 = st.columns([1,2])
        with col8:
            if user_state != 'Select' and user_state_year != 'Select':
                
                state_user_data = fetch_state_user_data(user_state, user_state_year)
                state_user_data['Total_Registered_Users'] = state_user_data['Total_Registered_Users'].apply(lambda x: locale.format('%d', x, grouping=True))

                st.dataframe(state_user_data, hide_index=True)
        with col9:
            if user_state != 'Select' and user_state_year != 'Select':
                state_user_bar = fetch_state_user_data(user_state, user_state_year)

                state_user_bar['Quarter'] = state_user_bar['Quarter'].astype(str)
                state_user_bar['Total_Registered_Users'] = state_user_bar['Total_Registered_Users'].astype(float)
                state_user_data_bar = px.bar(state_user_bar , x = 'Quarter', y ='Total_Registered_Users', color ='Total_Registered_Users', color_continuous_scale = 'aggrnyl', title = 'User Analysis Chart', height = 700,)
                state_user_data_bar.update_layout(title_font=dict(size=33),title_font_color='#6739b7')
                st.plotly_chart(state_user_data_bar,use_container_width=True)


else:
    tab5, tab6 = st.tabs(['Transaction','User'])
    with tab5:
        col1, col2 = st.columns([1,3])
        with col1:
            trans_top_year = st.selectbox('Select Year', ('Select', '2018','2019','2020','2021','2022'),key='top_trans_year')
        with col1:
            if trans_top_year != 'Select':
                top_trans_data = fetch_top_trans_data(trans_top_year)
                top_trans_data['Top 10 Transaction amount'] = top_trans_data['Top 10 Transaction amount'].apply(lambda x: locale.format('%d', x, grouping=True))
                top_trans_data['Top 10 Transaction amount'] = '\u20B9 ' + top_trans_data['Top 10 Transaction amount']

                st.dataframe(top_trans_data, hide_index=True)
        with col2:
            if trans_top_year != 'Select':
                top_trans_pie = fetch_top_trans_data(trans_top_year)

                pie_data = top_trans_pie.groupby('State')['Top 10 Transaction amount'].sum().reset_index()
                fig = px.pie(pie_data, values='Top 10 Transaction amount', names='State', title='Top 10 Transaction Amount by State', height=600,)
                st.plotly_chart(fig, use_container_width=True)
        
        top_state = None # Define top_state outside the conditional block

        col3, col4 = st.columns([1,2])
        with col3:
            if trans_top_year != 'Select':
                top_state = st.selectbox('Select State',('Select', 'andaman-&-nicobar-islands', 'andhra-pradesh', 'arunachal-pradesh','assam', 'bihar', 
                    'chandigarh', 'chhattisgarh','dadra-&-nagar-haveli-&-daman-&-diu', 'delhi', 'goa', 'gujarat', 'haryana', 'himachal-pradesh', 
                    'jammu-&-kashmir', 'jharkhand', 'karnataka', 'kerala', 'ladakh', 'lakshadweep', 'madhya-pradesh','maharashtra', 'manipur', 
                    'meghalaya', 'mizoram', 'nagaland','odisha', 'puducherry', 'punjab', 'rajasthan', 'sikkim', 'tamil-nadu', 'telangana', 
                    'tripura', 'uttar-pradesh', 'uttarakhand', 'west-bengal'),key='top_state')
        with col3:
            if top_state is not None:
                if trans_top_year != 'Select' and top_state != 'Select':
                    top_trans_dist_data = fetch_top_trans_dist_data(top_state, trans_top_year)
                    
                    top_trans_dist_data['Top 10 Transaction amount'] = top_trans_dist_data['Top 10 Transaction amount'].apply(lambda x: locale.format('%d', x, grouping=True))
                    top_trans_dist_data['Top 10 Transaction amount'] = '\u20B9 ' + top_trans_dist_data['Top 10 Transaction amount']

                    st.dataframe(top_trans_dist_data, hide_index=True)
        with col4:
            if top_state is not None:
                if trans_top_year != 'Select' and top_state != 'Select':
                    top_trans_dist_pie = fetch_top_trans_dist_data(top_state, trans_top_year)

                    pie_data = top_trans_dist_pie.groupby('District')['Top 10 Transaction amount'].sum().reset_index()
                    fig = px.pie(pie_data, values='Top 10 Transaction amount', names='District', title='Top 10 Transaction Amount by State', height=600,)
                    st.plotly_chart(fig, use_container_width=True)

    with tab6:
        col1, col2 = st.columns([1,3])
        with col1:
            user_top_year = st.selectbox('Select Year', ('Select', '2018','2019','2020','2021','2022'),key='top_user_year')
        with col1:
            if user_top_year != 'Select':
                top_user_data = fetch_top_user_data(user_top_year)
                top_user_data['Top 10 User Count'] = top_user_data['Top 10 User Count'].apply(lambda x: locale.format('%d', x, grouping=True))
                st.dataframe(top_user_data, hide_index=True)
        with col2:
            if user_top_year != 'Select':
                top_user_pir = fetch_top_user_data(user_top_year)
                pie_data = top_user_pir.groupby('State')['Top 10 User Count'].sum().reset_index()
                fig = px.pie(pie_data, values='Top 10 User Count', names='State', title='Top 10 User Count by State', height=600,)
                st.plotly_chart(fig, use_container_width=True)

        col3, col4 = st.columns([1,2])
        with col3:
            if user_top_year != 'Select':
                top_state = st.selectbox('Select State',('Select', 'andaman-&-nicobar-islands', 'andhra-pradesh', 'arunachal-pradesh','assam', 'bihar', 
                    'chandigarh', 'chhattisgarh','dadra-&-nagar-haveli-&-daman-&-diu', 'delhi', 'goa', 'gujarat', 'haryana', 'himachal-pradesh', 
                    'jammu-&-kashmir', 'jharkhand', 'karnataka', 'kerala', 'ladakh', 'lakshadweep', 'madhya-pradesh','maharashtra', 'manipur', 
                    'meghalaya', 'mizoram', 'nagaland','odisha', 'puducherry', 'punjab', 'rajasthan', 'sikkim', 'tamil-nadu', 'telangana', 
                    'tripura', 'uttar-pradesh', 'uttarakhand', 'west-bengal'),key='top_user_dist_state')
        with col3:
            if user_top_year != 'Select' and top_state != 'Select':
                top_user_dist_data = fetch_top_user_dist_data(top_state, user_top_year)
                top_user_dist_data['Top 10 User Count'] = top_user_dist_data['Top 10 User Count'].apply(lambda x: locale.format('%d', x, grouping=True))
                st.dataframe(top_user_dist_data, hide_index=True)
        with col4:
            if user_top_year != 'Select' and top_state != 'Select':
                top_user_dist_pie = fetch_top_user_dist_data(top_state, user_top_year)
                pie_data = top_user_dist_pie.groupby('District')['Top 10 User Count'].sum().reset_index()
                fig = px.pie(pie_data, values='Top 10 User Count', names='District', title='Top 10 User Count by District', height=600,)
                st.plotly_chart(fig, use_container_width=True)


# I have repeated funtions many times, because I formatted some columns of dataframes