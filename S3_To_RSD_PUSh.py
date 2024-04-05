import csv
import pymysql
import boto3

# AWS RDS MySQL credentials
db_host = 'database-2.cdemou8460th.ap-south-1.rds.amazonaws.com'
db_username = 'admin'
db_password = 'tanmay123'
new_db_name = 'new_database1'  # Specify the new database name
table_name = 'data'

# AWS S3 credentials and bucket information
s3_bucket_name = 'tanmaybucket18'
s3_object_key = 'data.csv'  # Specify the S3 object key for your CSV file

# AWS credentials (access key and secret key)
aws_access_key_id = <'Enter access key'>
aws_secret_access_key = <'secret'>

def create_database_if_not_exists(db_host, db_username, db_password, new_db_name):
    # Establish connection to MySQL server
    conn = pymysql.connect(host=db_host,
                           user=db_username,
                           password=db_password,
                           charset='utf8mb4',
                           cursorclass=pymysql.cursors.DictCursor)

    try:
        with conn.cursor() as cursor:
            # Check if the database already exists
            cursor.execute(f"SHOW DATABASES LIKE '{new_db_name}'")
            result = cursor.fetchone()

            # If the database doesn't exist, create it
            if not result:
                cursor.execute(f"CREATE DATABASE {new_db_name}")
                print(f"Database '{new_db_name}' created successfully!")
            else:
                print(f"Database '{new_db_name}' already exists.")

        # Commit the transaction
        conn.commit()
    except Exception as e:
        print(f"Error: {e}")
        # Rollback the transaction in case of error
        conn.rollback()
    finally:
        # Close the database connection
        conn.close()

def create_table_if_not_exists(db_host, db_username, db_password, db_name, table_name):
    # Establish connection to RDS MySQL
    conn = pymysql.connect(host=db_host,
                           user=db_username,
                           password=db_password,
                           db=db_name,
                           charset='utf8mb4',
                           cursorclass=pymysql.cursors.DictCursor)

    try:
        with conn.cursor() as cursor:
            # Check if the table already exists
            cursor.execute(f"SHOW TABLES LIKE '{table_name}'")
            result = cursor.fetchone()

            # If the table doesn't exist, create it
            if not result:
                cursor.execute(f"CREATE TABLE {table_name} (Name VARCHAR(255), Age INT, City VARCHAR(255))")
                print(f"Table '{table_name}' created successfully!")
            else:
                print(f"Table '{table_name}' already exists.")

        # Commit the transaction
        conn.commit()
    except Exception as e:
        print(f"Error: {e}")
        # Rollback the transaction in case of error
        conn.rollback()
    finally:
        # Close the database connection
        conn.close()

def upload_csv_to_rds(csv_data, db_host, db_username, db_password, db_name, table_name):
    # Establish connection to RDS MySQL
    conn = pymysql.connect(host=db_host,
                           user=db_username,
                           password=db_password,
                           db=db_name,
                           charset='utf8mb4',
                           cursorclass=pymysql.cursors.DictCursor)
    print("Connection to RDS established.")

    try:
        with conn.cursor() as cursor:
            csv_reader = csv.reader(csv_data.decode('utf-8').splitlines())
            # Skip header if exists
            next(csv_reader)
            # Iterate through CSV rows and insert into the database
            for row in csv_reader:
                # Construct SQL query to insert data into the table
                sql = f"INSERT INTO {table_name} (Name, Age, City) VALUES (%s, %s, %s)"
                # Execute the SQL query
                cursor.execute(sql, row)
        # Commit the transaction
        conn.commit()
        print("Data successfully uploaded to RDS!")
    except Exception as e:
        print(f"Error: {e}")
        # Rollback the transaction in case of error
        conn.rollback()
    finally:
        # Close the database connection
        conn.close()

# Create the new database if it doesn't exist
create_database_if_not_exists(db_host, db_username, db_password, new_db_name)

# Create the table if it doesn't exist
create_table_if_not_exists(db_host, db_username, db_password, new_db_name, table_name)

# Initialize the S3 client with AWS credentials
s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

try:
    # Fetch the CSV file from S3
    response = s3.get_object(Bucket=s3_bucket_name, Key=s3_object_key)
    csv_data = response['Body'].read()

    # Upload CSV data to RDS
    upload_csv_to_rds(csv_data, db_host, db_username, db_password, new_db_name, table_name)
except Exception as e:
    print(f"Error fetching CSV file from S3: {e}")
