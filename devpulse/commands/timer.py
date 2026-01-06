import typer

app = typer.Typer(help="Pomodoro and interval timers")


@app.command()
def start(
    duration: int = typer.Argument(25, help="Timer duration in minutes"),
    task: str = typer.Option(None, "--task", "-t", help="Task name for this session")
):
    """Start a Pomodoro timer."""
    typer.echo(f"⏱️  Starting {duration}-minute timer")
    if task:
        typer.echo(f"Task: {task}")
    typer.echo("Timer running... [Future: real countdown implementation]")


@app.command()
def stop():
    """Stop the current timer."""
    typer.echo("⏹️  Timer stopped")
    typer.echo("Session time: 25m 0s")


@app.command()
def status():
    """Show timer status."""
    typer.echo("⏱️  Timer Status: Not running")
    typer.echo("Last session: 25m")


@app.command()
def preset(
    name: str = typer.Argument(..., help="Preset name (pomodoro, shortbreak, longbreak, custom)"),
    duration: int = typer.Option(None, "--duration", "-d", help="Custom duration")
):
    """Use a timer preset."""
    presets = {"pomodoro": 25, "shortbreak": 5, "longbreak": 15}
    minutes = duration or presets.get(name, 25)
    typer.echo(f"⏱️  Starting {name} preset: {minutes} minutes")


@app.command()
def history(limit: int = typer.Option(10, "--limit", "-l")):
    """View timer history."""
    typer.echo(f"📊 Last {limit} sessions:")
    typer.echo("No sessions recorded.")


@app.command()
def stats():
    """Show timer statistics."""
    typer.echo("📈 Timer Statistics:")
    typer.echo("Total pomodoros: 0")
    typer.echo("Total time: 0h 0m")
    typer.echo("Completion rate: 0%")
