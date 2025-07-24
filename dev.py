#!/usr/bin/env python3
# ruff: noqa: T201  # Allow print statements in development script
"""
Development startup script
Sets up the development environment and starts the FastAPI server
"""

import subprocess
import sys
from pathlib import Path


def run_command(command: str, description: str) -> bool:
    """Run a command and return success status"""
    print(f"🔄 {description}...")
    try:
        subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e.stderr}")
        return False


def main():
    """Main startup function"""
    project_root = Path(__file__).parent

    print("🚀 FastAPI Starter - Development Setup")
    print("=" * 50)

    # Check if .env exists, create from template if not
    env_file = project_root / ".env"
    env_template = project_root / ".env.template"

    if not env_file.exists() and env_template.exists():
        print("📋 Creating .env file from template...")
        env_file.write_text(env_template.read_text())
        print("✅ .env file created. Please review and update the configuration.")

    # Install dependencies
    if not run_command("uv sync", "Installing dependencies"):
        print("⚠️  UV not found, trying with pip...")
        if not run_command("pip install -e .", "Installing with pip"):
            print("❌ Failed to install dependencies")
            return 1

    # Run quality checks
    print("\n🔍 Running code quality checks...")
    run_command("ruff check app", "Linting code")
    run_command("black --check app", "Checking code formatting")
    run_command("mypy app", "Type checking")

    # Start the development server
    print("\n🌟 Starting FastAPI development server...")
    print("📖 API Documentation will be available at:")
    print("   - Swagger UI: http://localhost:8000/api/v1/docs")
    print("   - ReDoc: http://localhost:8000/api/v1/redoc")
    print("   - Health Check: http://localhost:8000/health")
    print("\n💡 Press Ctrl+C to stop the server")
    print("=" * 50)

    try:
        subprocess.run([sys.executable, "main.py"], check=True)
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Server failed to start: {e}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
