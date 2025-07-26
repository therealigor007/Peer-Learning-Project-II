import pymssql
import os
from dotenv import load_dotenv

load_dotenv()

def test_azure_connection():    
    # Get connection details from environment
    server = os.getenv('AZURE_SQL_SERVER')
    database = os.getenv('AZURE_SQL_DATABASE') 
    username = os.getenv('AZURE_SQL_USERNAME')
    password = os.getenv('AZURE_SQL_PASSWORD')
    
    print(f"Connecting to: {server}")
    print(f"Database: {database}")
    print(f"Username: {username}")
    
    try:
        connection = pymssql.connect(
            server=server,
            user=username,
            password=password,
            database=database,
            port=1433,
            timeout=30
        )
        
        print("SUCCESS: Connected to Azure SQL Database!")
        
        # Test a simple query
        cursor = connection.cursor()
        cursor.execute("SELECT @@VERSION")
        version = cursor.fetchone()[0]
        print(f"Database version: {version[:50]}...")
        
        connection.close()
        return True
        
    except Exception as e:
        print("FAILED: Could not connect to database")
        print(f"Error: {e}")
        return False

def create_tables():    
    server = os.getenv('AZURE_SQL_SERVER')
    database = os.getenv('AZURE_SQL_DATABASE') 
    username = os.getenv('AZURE_SQL_USERNAME')
    password = os.getenv('AZURE_SQL_PASSWORD')
    
    try:
        # FIXED: Use pymssql.connect (not connection string)
        connection = pymssql.connect(
            server=server,
            user=username,
            password=password,
            database=database,
            port=1433,
            timeout=30
        )
        
        cursor = connection.cursor()
        
        # Create categories table
        cursor.execute("""
            IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='categories' AND xtype='U')
            CREATE TABLE categories (
                id INT PRIMARY KEY,
                name NVARCHAR(100) NOT NULL,
                description NVARCHAR(500)
            )
        """)
        
        # Create reviews table
        cursor.execute("""
            IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='reviews' AND xtype='U')
            CREATE TABLE reviews (
                id NVARCHAR(50) PRIMARY KEY,
                category_id INT NOT NULL,
                item_name NVARCHAR(200) NOT NULL,
                rating INT NOT NULL,
                content NVARCHAR(MAX) NOT NULL,
                anonymous_id NVARCHAR(50) NOT NULL,
                timestamp DATETIME2 NOT NULL,
                helpful_votes INT DEFAULT 0
            )
        """)
        
        connection.commit()
        
        # Insert default categories
        cursor.execute("SELECT COUNT(*) FROM categories")
        count = cursor.fetchone()[0]
        
        if count == 0:
            print("Inserting default categories...")
            categories = [
                (1, "Courses", "Academic courses and modules"),
                (2, "Services", "Library, Dining, IT Support"), 
                (3, "Locations", "Study Spaces, Facilities"),
                (4, "Events", "University events and activities")
            ]
            
            for cat in categories:
                cursor.execute(
                    "INSERT INTO categories (id, name, description) VALUES (%s, %s, %s)",
                    cat
                )
            
            connection.commit()
        
        print("Tables created successfully!")
        connection.close()
        return True
        
    except Exception as e:
        print(f"Failed to create tables: {e}")
        return False

if __name__ == "__main__":
    print("Testing Azure SQL Database Setup...")
    print("=" * 50)
    
    if test_azure_connection():
        print("\nCreating database tables...")
        create_tables()
    else:
        print("\nPlease check your .env file and Azure database settings.")