"""Allow workspace_cli to be executed as a module with python -m."""

from workspace_cli.cli import main

if __name__ == "__main__":
    main()
