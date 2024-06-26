import pandas as pd
import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
import psycopg2

from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Retrieve database connection parameters from environment variables
DATABASE_TYPE = os.getenv('DATABASE_TYPE')
DBAPI = os.getenv('DBAPI')
ENDPOINT = os.getenv('ENDPOINT')
USER = os.getenv('USER')
PASSWORD = os.getenv('PASSWORD')
PORT = int(os.getenv('PORT', 5433))  # Provide default value if not set
DATABASE = os.getenv('DATABASE')

# Create the connection string
connection_string = f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{ENDPOINT}:{PORT}/{DATABASE}"

engine = create_engine(connection_string)

directories = [
    r"C:\Users\eric\Documents\cost_of_cup\corsi_vals_II",
    r"C:\Users\eric\Documents\cost_of_cup\Kaggle_stats",
    r"C:\Users\eric\Documents\cost_of_cup\team_files",
    r"C:\Users\eric\Documents\cost_of_cup\player_files"
    # Add more directories as needed
]


for directory_path in directories:
    print(f"Processing directory: {directory_path}")
    
    for filename in os.listdir(directory_path):
        if filename.endswith('.csv'):
            # Load the CSV file into a pandas DataFrame
            file_path = os.path.join(directory_path, filename)
            df = pd.read_csv(file_path)

            # Define the table name (without the .csv extension)
            table_name = os.path.splitext(filename)[0]
            
            # Special handling for player_ and team_ files
            if filename.startswith('player_') or filename.startswith('team_'):
                df = pd.read_csv(file_path, index_col=None)
            else:
                df = pd.read_csv(file_path)
                
            # Write the DataFrame to the SQL database
            try:
                df.to_sql(table_name, engine, index=False, if_exists='replace')
                print(f"Table '{table_name}' created successfully.")
            except SQLAlchemyError as e:
                print(f"Error occurred while creating table '{table_name}': {e}")

