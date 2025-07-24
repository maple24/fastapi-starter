#!/usr/bin/env python3
"""Test script to check if the app works"""

try:
    from app.core.app import create_app
    app = create_app()
    print("✅ FastAPI app created successfully!")
    print(f"📄 App title: {app.title}")
    print(f"📋 App description: {app.description}")
except Exception as e:
    import traceback
    print("❌ Error creating FastAPI app:")
    traceback.print_exc()
