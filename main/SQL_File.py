import pandas as pd
import mysql.connector

df = pd.read_csv("PhonePe_States.csv")
user_df = pd.read_csv("PhonePe_User.csv")
map_df = pd.read_csv("PhonePe_Map_Transaction.csv")
df_map_user = pd.read_csv("PhonePe_Map_User.csv")
df_top_trans = pd.read_csv("PhonePe_Top_Trans.csv")
df_top_trans = df_top_trans.fillna(0)
df_top_user = pd.read_csv("PhonePe_Top_User.csv")

conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database = 'demo'
    )
cursor = conn.cursor()

def convert_to_crores(number):
    if number >= 1e7:  # 1 Crore is 1e7 (10,000,000)
        result = "{:.2f} Crores".format(number / 1e7)
    else:
        result = "{:.2f}".format(number)
    return result



def create_and_insert_agg_transaction_table(df):
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Agg_Transaction (
            State VARCHAR(255),
            Year INT,
            Quarter CHAR(2),
            Transaction_type VARCHAR(255),
            Transaction_count INT,
            Transaction_amount DECIMAL(18, 2)
        );
    ''')

    conn.commit()
    print('Table "Agg_Transaction" created.')

    sql = "INSERT INTO Agg_Transaction (State, Year, Quarter, Transaction_type, Transaction_count, Transaction_amount) VALUES (%s, %s, %s, %s, %s, %s)"

    for index, row in df.iterrows():
        values = (row['State'], row['Year'], row['Quarter'], row['Transaction_type'], row['Transaction_count'], row['Transaction_amount'])
        cursor.execute(sql, values)

    conn.commit()
    print('Data inserted into "Agg_Transaction" table.')


def create_and_insert_agg_user_table(user_df):
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Agg_User (
            State VARCHAR(255),
            Year INT,
            Quarter CHAR(2),
            User_brand VARCHAR(255),
            User_count INT,
            User_percentage DECIMAL(18, 2)
        );
    ''')

    conn.commit()
    print('Table "Agg_User" created.')


    sql = "INSERT INTO Agg_User (State, Year, Quarter, User_brand, User_count, User_percentage) VALUES (%s, %s, %s, %s, %s, %s)"
    for index, row in user_df.iterrows():
        # Use a tuple of values from the row to replace the placeholders
        values = (row['State'], row['Year'], row['Quarter'], row['User_Brand'], row['User_Count'], row['User_Percentage'])
        cursor.execute(sql, values)

    
    conn.commit()
    print('Data inserted into "Agg_User" table.')


def create_and_insert_map_transaction_table(map_df):
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Map_Transaction (
            State VARCHAR(255),
            Year INT,
            Quarter CHAR(2),
            Map_district VARCHAR(255),
            Map_count INT,
            Map_amount DECIMAL(18, 2)
        );
    ''')
    conn.commit()
    print('Table "Map_Transaction" created.')

    sql = "INSERT INTO Map_Transaction (State, Year, Quarter, Map_district, Map_count, Map_amount) VALUES (%s, %s, %s, %s, %s, %s)"

    for index, row in map_df.iterrows():
        # Use a tuple of values from the row to replace the placeholders
        values = (row['State'], row['Year'], row['Quarter'], row['Map_District'], row['Map_Count'], row['Map_Amount'])
        cursor.execute(sql, values)

    
    conn.commit()

    print('Data inserted into "Map_Transaction" table.')


def create_and_insert_map_user_table(df_map_user):
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Map_User (
            State VARCHAR(255),
            Year INT,
            Quarter CHAR(2),
            District VARCHAR(255),
            Registered_users INT,
            App_opens INT
        );
    ''')

    conn.commit()

    print('Table "Map_User" created.')

    sql = "INSERT INTO Map_User (State, Year, Quarter, District, Registered_users, App_opens) VALUES (%s, %s, %s, %s, %s, %s)"

    for index, row in df_map_user.iterrows():
        # Use a tuple of values from the row to replace the placeholders
        values = (row['States'], row['Year'], row['Quarter'], row['District'], row['Registered_users'], row['App_Opens'])
        cursor.execute(sql, values)

    # Commit the changes after inserting all rows
    conn.commit()

    print('Data inserted into "Map_User" table.')


def create_and_insert_top_transaction_table(df_top_trans):
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Top_Transaction (
            State VARCHAR(255),
            Year INT,
            Quarter CHAR(2),
            Pincode INT,
            Transaction_count INT,
            Transaction_amount INT
        );
    ''')

    conn.commit()
    print('Table "Top_Transaction" created.')


    sql = "INSERT INTO Top_Transaction (State, Year, Quarter, Pincode, Transaction_count, Transaction_amount) VALUES (%s, %s, %s, %s, %s, %s)"

    for index, row in df_top_trans.iterrows():
        # Use a tuple of cleaned values from the row to replace the placeholders
        values = (row['State'], row['Year'], row['Quarter'], row['Pincode'], row['Transaction_Count'], row['Transaction_Amount'])
        # Execute the SQL query with the provided values
        cursor.execute(sql, values)

    # Commit the changes after inserting all rows
    conn.commit()

    print('Data inserted into "Top_Transaction" table.')


def create_and_insert_top_user_table(df_top_user):
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Top_User (
            State VARCHAR(255),
            Year INT,
            Quarter CHAR(2),
            Pincode INT,
            Registered_users INT
        );
    ''')
    conn.commit()

    print('Table "Top_User" created.')

    sql = "INSERT INTO Top_User (State, Year, Quarter, Pincode, Registered_users) VALUES (%s, %s, %s, %s, %s)"

    for index, row in df_top_user.iterrows():
        values = (row['State'], row['Year'], row['Quarter'], row['Pincode'], row['Registered_Users'])
        cursor.execute(sql, values)


    conn.commit()

    print('Data inserted into "Top_User" table.')


if __name__ == "__main__":

    create_and_insert_agg_transaction_table(df)
    
    create_and_insert_agg_user_table(user_df)
    
    create_and_insert_map_transaction_table(map_df)
    
    create_and_insert_map_user_table(df_map_user)
    
    create_and_insert_top_transaction_table(df_top_trans)
    
    create_and_insert_top_user_table(df_top_user)


# Close the database connection when done
cursor.close()
conn.close()
