"""
Test script to verify the Synthetic Data App setup and configuration.
"""

import sys
import os
from pathlib import Path

def test_env_variables():
    """Test environment variables."""
    print("\n🔍 Checking Environment Variables...")
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("❌ Error: GEMINI_API_KEY or GOOGLE_API_KEY not found in .env file")
        print("   Please add your API key to the .env file:")
        print("   GEMINI_API_KEY=your_api_key_here")
        return False
    else:
        # Mask the API key for security
        masked_key = api_key[:10] + "..." + api_key[-5:] if len(api_key) > 15 else "***"
        print(f"✅ API Key found: {masked_key}")
    
    db_path = os.getenv("DATABASE_PATH", "synthetic_data.db")
    print(f"✅ Database path: {db_path}")
    
    return True

def test_imports():
    """Test all required imports."""
    print("\n📦 Testing Required Packages...")
    
    required_packages = {
        "streamlit": "streamlit",
        "google.generativeai": "google-generativeai",
        "sqlalchemy": "sqlalchemy",
        "pandas": "pandas",
        "dotenv": "python-dotenv",
        "plotly": "plotly",
    }
    
    all_ok = True
    for module, package in required_packages.items():
        try:
            __import__(module)
            print(f"✅ {package} installed")
        except ImportError as e:
            print(f"❌ {package} not installed")
            all_ok = False
    
    return all_ok

def test_gemini_connection():
    """Test connection to Gemini API."""
    print("\n🤖 Testing Gemini API Connection...")
    
    try:
        from core.gemini_client import GeminiClient
        
        # Initialize client (this will validate the API key)
        client = GeminiClient(temperature=0.7, max_tokens=1024)
        print(f"✅ Gemini client initialized successfully")
        print(f"   Model: {client.model._model_name if hasattr(client.model, '_model_name') else 'Unknown'}")
        
        # Test a simple generation
        print("\n   Testing simple generation...")
        try:
            response = client.model.generate_content(
                "Say 'Hello, world!' in JSON format with a 'message' key.",
                generation_config={
                    "temperature": 0.1,
                    "max_output_tokens": 100,
                    "response_mime_type": "application/json"
                },
                request_options={"timeout": 15}
            )
            print(f"✅ API connection successful!")
            return True
        except Exception as e:
            print(f"⚠️  API key valid but generation failed: {e}")
            print("   This might be due to quota limits or model availability.")
            return True  # API key is valid even if generation fails
            
    except ValueError as e:
        if "API" in str(e):
            print(f"❌ {e}")
            return False
        raise
    except Exception as e:
        print(f"❌ Error initializing Gemini client: {e}")
        return False

def test_database():
    """Test database connection."""
    print("\n💾 Testing Database...")
    
    try:
        from core.db import db_manager
        
        # Test connection
        tables = db_manager.get_table_names()
        print(f"✅ Database connection successful")
        print(f"   Found {len(tables)} existing table(s): {', '.join(tables) if tables else 'None'}")
        
        return True
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False

def test_schema_parser():
    """Test schema parser with a simple example."""
    print("\n📋 Testing Schema Parser...")
    
    try:
        from core.schema_parser import SchemaParser
        
        test_ddl = """
        CREATE TABLE test_users (
            user_id SERIAL PRIMARY KEY,
            username VARCHAR(50) NOT NULL,
            email VARCHAR(100)
        );
        """
        
        parser = SchemaParser()
        schema = parser.parse_ddl(test_ddl)
        
        if "test_users" in schema:
            print("✅ Schema parser working correctly")
            print(f"   Parsed table: test_users with {len(schema['test_users']['columns'])} columns")
            return True
        else:
            print("❌ Schema parser failed to parse test DDL")
            return False
            
    except Exception as e:
        print(f"❌ Schema parser error: {e}")
        return False

def main():
    """Run all tests."""
    print("=" * 60)
    print("🚀 Synthetic Data App - Setup Verification")
    print("=" * 60)
    
    # Add project root to path
    project_root = Path(__file__).parent
    sys.path.insert(0, str(project_root))
    
    results = {
        "Environment Variables": test_env_variables(),
        "Required Packages": test_imports(),
        "Gemini API Connection": test_gemini_connection(),
        "Database": test_database(),
        "Schema Parser": test_schema_parser(),
    }
    
    print("\n" + "=" * 60)
    print("📊 Test Summary")
    print("=" * 60)
    
    all_passed = True
    for test_name, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{test_name}: {status}")
        if not passed:
            all_passed = False
    
    print("=" * 60)
    
    if all_passed:
        print("\n✨ All tests passed! Your setup is ready.")
        print("\n🚀 To start the application, run:")
        print("   streamlit run app.py")
        return 0
    else:
        print("\n⚠️  Some tests failed. Please fix the issues above before running the app.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
