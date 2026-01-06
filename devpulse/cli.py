import typer
from devpulse.commands_registry import COMMAND_MODULES

app = typer.Typer(
    name="devpulse",
    help="DevPulse - Developer Productivity CLI Tool",
    add_completion=False,
)


def register_commands():
    """Register all command modules with the main CLI app."""
    for name, command_app, help_text in COMMAND_MODULES:
        app.add_typer(command_app, name=name, help=help_text)


# Register all commands when the module is loaded
register_commands()


@app.command()
def version():
    """Show DevPulse version information."""
    typer.echo("DevPulse v0.1.0")
    typer.echo("Developer Productivity CLI Tool")


def main():
    """Main entry point for the CLI."""
    app()


if __name__ == "__main__":
    main()
