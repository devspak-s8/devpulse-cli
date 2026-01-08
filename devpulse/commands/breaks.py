import typer

app = typer.Typer(help="Break management and reminders")


@app.command()
def schedule(
    interval: int = typer.Option(60, "--interval", "-i", help="Minutes between breaks"),
    duration: int = typer.Option(5, "--duration", "-d", help="Break duration in minutes")
):
    """Schedule automatic breaks."""
    typer.echo(f"☕ Breaks scheduled: every {interval}m for {duration}m")
    typer.echo("[OK] Schedule activated!")


@app.command()
def take(
    duration: int = typer.Option(5, "--duration", "-d", help="Break duration in minutes")
):
    """Take a break now."""
    typer.echo(f"☕ Break started ({duration} minutes)")
    typer.echo("Relax! Stretch, drink water, rest your eyes...")


@app.command()
def skip():
    """Skip next break."""
    typer.echo("⏭️  Break skipped")
    typer.echo("Next break in: 60m")


@app.command()
def status():
    """Check break schedule status."""
    typer.echo("☕ Break Schedule: Active")
    typer.echo("Interval: 60 minutes")
    typer.echo("Next break: 45 minutes from now")


@app.command()
def history(limit: int = typer.Option(10, "--limit", "-l")):
    """View break history."""
    typer.echo(f"📊 Last {limit} breaks:")
    typer.echo("No break history.")


@app.command()
def reminders(enabled: bool = typer.Option(None, "--enable", help="Enable reminders")):
    """Manage break reminders."""
    if enabled is None:
        typer.echo("🔔 Reminders: Disabled")
    elif enabled:
        typer.echo("🔔 Reminders: Enabled")
    else:
        typer.echo("🔔 Reminders: Disabled")


@app.command()
def suggestions():
    """Get break activity suggestions."""
    typer.echo("💡 Break Suggestions:")
    typer.echo("- Go for a quick walk")
    typer.echo("- Do some stretching")
    typer.echo("- Drink water")
    typer.echo("- Look away from screen")
