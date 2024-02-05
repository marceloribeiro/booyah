#!/usr/bin/env python
from booyah.server.booyah_runner import BooyahRunner
import argparse

BOOYAH_COMMAND_VERSION = '1.0.0'

def run():
    parser = argparse.ArgumentParser(description="Booyah console HELP - Commands list")
    parser.add_argument("--version", action="store_true", help="Show the version")
    subparsers = parser.add_subparsers(title="Commands", dest="command")

    generate_parser = subparsers.add_parser("generate", aliases=["g"], help="Generate controller with given name and actions")
    generate_parser.add_argument("generator", help="Name of the generator")
    generate_parser.add_argument("args", nargs="*", help="Generator args")

    new_parser = subparsers.add_parser("new", help="Create a new project with given name")
    new_parser.add_argument("project_name", help="The project name")

    subparsers.add_parser("s", help="Starts the booyah server")
    subparsers.add_parser("c", help="Starts the booyah console")
    subparsers.add_parser("w", help="Starts the booyah worker")
    subparsers.add_parser("ws", help="Starts the booyah worker scheduler")

    db_parser = subparsers.add_parser("db", help="Run db operations")
    db_subparsers = db_parser.add_subparsers(title="DB Operations", dest="db_command")

    db_subparsers.add_parser("create", help="Create database")
    migrate_parser = db_subparsers.add_parser("migrate", help="Migrate database")
    migrate_up_parser = db_subparsers.add_parser("migrate_up", help="Migrate a single version file up")
    migrate_down_parser = db_subparsers.add_parser("migrate_down", help="Migrate a single version file down")
    db_subparsers.add_parser("drop", help="Drop database")
    db_subparsers.add_parser("seed", help="Seed database")
    db_subparsers.add_parser("rollback", help="Rollback the last migration")

    migrate_up_parser.add_argument("args", nargs="*", help="Generator args")
    migrate_down_parser.add_argument("args", nargs="*", help="Generator args")
    migrate_parser.add_argument("args", nargs="*", help="Generator args")

    args = parser.parse_args()
    if args.version:
        print(f"Booyah command-line version {BOOYAH_COMMAND_VERSION}")  # Replace with your actual version number
        return
    elif args.command:
        getattr(BooyahRunner(), f"run_{args.command}")()