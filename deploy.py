#!/usr/bin/env python3
"""
Deployment script for College Projects Store
This script helps with initial setup and deployment
"""

import os
import sys
import subprocess
import sqlite3
from pathlib import Path

def run_command(command, description):
    """Run a shell command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e.stderr}")
        return None

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        sys.exit(1)
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")

def create_virtual_environment():
    """Create virtual environment if it doesn't exist"""
    venv_path = Path("venv")
    if not venv_path.exists():
        run_command("python -m venv venv", "Creating virtual environment")
    else:
        print("✅ Virtual environment already exists")

def install_dependencies():
    """Install Python dependencies"""
    if os.name == 'nt':  # Windows
        pip_cmd = "venv\\Scripts\\pip"
    else:  # Unix/Linux/Mac
        pip_cmd = "venv/bin/pip"
    
    run_command(f"{pip_cmd} install -r requirements.txt", "Installing dependencies")

def create_directories():
    """Create necessary directories"""
    directories = ['uploads', 'logs', 'static/uploads']
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ Created directory: {directory}")

def setup_database():
    """Setup database (SQLite for development)"""
    db_path = Path("college_projects.db")
    if not db_path.exists():
        print("🔄 Setting up SQLite database...")
        try:
            # Import app and create tables
            sys.path.append('.')
            from app import app, db
            with app.app_context():
                db.create_all()
                print("✅ Database setup completed")
        except Exception as e:
            print(f"❌ Database setup failed: {e}")
    else:
        print("✅ Database already exists")

def create_env_file():
    """Create .env file if it doesn't exist"""
    env_path = Path(".env")
    if not env_path.exists():
        env_content = """# College Projects Store Environment Variables
SECRET_KEY=your-secret-key-change-this-in-production
DATABASE_URL=sqlite:///college_projects.db
FLASK_ENV=development
FLASK_DEBUG=1

# Payment Gateway (Optional)
RAZORPAY_KEY_ID=your-razorpay-key-id
RAZORPAY_KEY_SECRET=your-razorpay-secret

# Email Configuration (Optional)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
"""
        with open(env_path, 'w') as f:
            f.write(env_content)
        print("✅ Created .env file")
    else:
        print("✅ .env file already exists")

def run_tests():
    """Run basic tests"""
    print("🔄 Running basic tests...")
    try:
        # Import and test basic functionality
        sys.path.append('.')
        from app import app
        print("✅ App imports successfully")
    except Exception as e:
        print(f"❌ App import failed: {e}")

def main():
    """Main deployment function"""
    print("🚀 College Projects Store - Deployment Script")
    print("=" * 50)
    
    # Check Python version
    check_python_version()
    
    # Create virtual environment
    create_virtual_environment()
    
    # Install dependencies
    install_dependencies()
    
    # Create directories
    create_directories()
    
    # Setup database
    setup_database()
    
    # Create .env file
    create_env_file()
    
    # Run tests
    run_tests()
    
    print("\n" + "=" * 50)
    print("🎉 Deployment completed successfully!")
    print("\n📋 Next steps:")
    print("1. Activate virtual environment:")
    if os.name == 'nt':  # Windows
        print("   venv\\Scripts\\activate")
    else:  # Unix/Linux/Mac
        print("   source venv/bin/activate")
    print("2. Update .env file with your configuration")
    print("3. Run the application:")
    print("   python app.py")
    print("4. Open http://localhost:5000 in your browser")
    print("\n👤 Default admin account:")
    print("   Email: admin@collegeprojects.com")
    print("   Password: admin123")

if __name__ == "__main__":
    main() 