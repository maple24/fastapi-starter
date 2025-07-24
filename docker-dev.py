#!/usr/bin/env python3
"""
Docker development helper script for FastAPI Starter
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path


def run_command(cmd: list[str], check: bool = True) -> subprocess.CompletedProcess:
    """Run a command and return the result."""
    print(f"Running: {' '.join(cmd)}")
    return subprocess.run(cmd, check=check)


def handle_build_command(args):
    """Handle the build command."""
    cmd = ["docker", "build", "-t", "fastapi-starter", "."]
    if args.no_cache:
        cmd.append("--no-cache")
    run_command(cmd)


def handle_dev_command(args):
    """Handle the dev command."""
    cmd = ["docker-compose", "-f", "docker-compose.dev.yml", "up"]
    if args.build:
        cmd.append("--build")
    if not args.logs:
        cmd.append("-d")

    run_command(cmd)

    if args.logs and not args.logs:
        run_command(["docker-compose", "-f", "docker-compose.dev.yml", "logs", "-f"])


def handle_prod_command(args):
    """Handle the prod command."""
    cmd = ["docker-compose", "up"]
    if args.build:
        cmd.append("--build")
    if not args.nginx:
        cmd.extend(["app", "db", "redis"])
    cmd.append("-d")

    run_command(cmd)
    print("Production environment started. Access the app at http://localhost:8000")


def handle_db_command(args):
    """Handle database operations."""
    if args.action == "start":
        run_command(["docker-compose", "up", "-d", "db"])
    elif args.action == "stop":
        run_command(["docker-compose", "stop", "db"])
    elif args.action == "reset":
        run_command(["docker-compose", "down", "-v"])
        run_command(["docker-compose", "up", "-d", "db"])
    elif args.action == "shell":
        run_command([
            "docker-compose", "exec", "db",
            "psql", "-U", "fastapi_user", "-d", "fastapi_db"
        ])


def handle_logs_command(args):
    """Handle logs command."""
    cmd = ["docker-compose", "logs"]
    if args.follow:
        cmd.append("-f")
    cmd.append(args.service)
    run_command(cmd)


def handle_shell_command(args):
    """Handle shell command."""
    run_command(["docker-compose", "exec", args.service, "bash"])


def handle_stop_command():
    """Handle stop command."""
    run_command(["docker-compose", "down"])


def handle_clean_command(args):
    """Handle clean command."""
    run_command(["docker-compose", "down", "-v"])
    if args.all:
        run_command(["docker", "system", "prune", "-af"])
        run_command(["docker", "volume", "prune", "-f"])


def create_parser():
    """Create and configure the argument parser."""
    parser = argparse.ArgumentParser(description="FastAPI Starter Docker Helper")

    # Subcommands
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Build command
    build_parser = subparsers.add_parser("build", help="Build Docker image")
    build_parser.add_argument("--no-cache", action="store_true", help="Build without cache")

    # Development command
    dev_parser = subparsers.add_parser("dev", help="Start development environment")
    dev_parser.add_argument("--build", action="store_true", help="Build images before starting")
    dev_parser.add_argument("--logs", action="store_true", help="Follow logs after starting")

    # Production command
    prod_parser = subparsers.add_parser("prod", help="Start production environment")
    prod_parser.add_argument("--build", action="store_true", help="Build images before starting")
    prod_parser.add_argument("--nginx", action="store_true", help="Include Nginx service")

    # Database command
    db_parser = subparsers.add_parser("db", help="Database operations")
    db_parser.add_argument("action", choices=["start", "stop", "reset", "shell"], help="Database action")

    # Logs command
    logs_parser = subparsers.add_parser("logs", help="View service logs")
    logs_parser.add_argument("service", nargs="?", default="app", help="Service name (default: app)")
    logs_parser.add_argument("-f", "--follow", action="store_true", help="Follow logs")

    # Shell command
    subparsers.add_parser("shell", help="Open shell in running container").add_argument(
        "service", nargs="?", default="app", help="Service name (default: app)"
    )

    # Stop command
    subparsers.add_parser("stop", help="Stop all services")

    # Clean command
    clean_parser = subparsers.add_parser("clean", help="Clean up Docker resources")
    clean_parser.add_argument("--all", action="store_true", help="Remove all Docker resources")

    return parser


def main():
    """Main function."""
    parser = create_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    # Change to project directory
    project_dir = Path(__file__).parent
    os.chdir(project_dir)

    command_handlers = {
        "build": handle_build_command,
        "dev": handle_dev_command,
        "prod": handle_prod_command,
        "db": handle_db_command,
        "logs": handle_logs_command,
        "shell": handle_shell_command,
        "stop": lambda _: handle_stop_command(),
        "clean": handle_clean_command,
    }

    try:
        handler = command_handlers.get(args.command)
        if handler:
            if args.command == "stop":
                handler(None)
            else:
                handler(args)
    except subprocess.CalledProcessError as e:
        print(f"Command failed with exit code {e.returncode}")
        sys.exit(e.returncode)
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(1)


if __name__ == "__main__":
    main()
