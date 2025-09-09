#!/usr/bin/env python
"""
Deployment preparation script for Django Movie Tracker
Run this script before deploying to ensure all static files are ready.
"""

import os
import sys
import django
from django.core.management import execute_from_command_line

def prepare_deployment():
    """Prepare the application for deployment."""
    
    print("🚀 Preparing Django Movie Tracker for deployment...")
    
    # Set Django settings module
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'movietracker.settings')
    
    try:
        django.setup()
        
        # Collect static files
        print("📦 Collecting static files...")
        execute_from_command_line(['manage.py', 'collectstatic', '--noinput'])
        
        # Run system checks
        print("🔍 Running system checks...")
        execute_from_command_line(['manage.py', 'check', '--deploy'])
        
        print("✅ Deployment preparation completed successfully!")
        print("\n🎯 Next Steps:")
        print("1. Push your code to GitHub")
        print("2. Follow the DEPLOYMENT_GUIDE.md instructions")
        print("3. Deploy on PythonAnywhere")
        
    except Exception as e:
        print(f"❌ Error during deployment preparation: {e}")
        sys.exit(1)

if __name__ == '__main__':
    prepare_deployment()
