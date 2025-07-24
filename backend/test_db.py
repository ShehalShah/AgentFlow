from app.database import engine
from sqlalchemy import text

try:
    # Test the connection
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        print("✅ Database connection successful!")
        
        # Test if we can access the agentflow database
        result = connection.execute(text("SELECT current_database()"))
        db_name = result.fetchone()[0]
        print(f"✅ Connected to database: {db_name}")
        
except Exception as e:
    print(f"❌ Database connection failed: {e}")
    print("\nPossible solutions:")
    print("1. Check if PostgreSQL is running")
    print("2. Verify your password in database.py")
    print("3. Make sure the 'agentflow' database exists")
    print("4. Check if the 'postgres' user has access to the database") 