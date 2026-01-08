import typer

app = typer.Typer(help="Track habits and streaks")


@app.command()
def create(
    name: str = typer.Argument(..., help="Habit name"),
    frequency: str = typer.Option("daily", "--frequency", "-f", help="Frequency (daily, weekly, custom)"),
    goal: int = typer.Option(1, "--goal", "-g", help="Daily/weekly goal")
):
    """Create a new habit."""
    typer.echo(f"[*] Habit created: {name}")
    typer.echo(f"Frequency: {frequency}")
    typer.echo(f"Goal: {goal}x per {frequency}")
    typer.echo("[OK] Habit tracking started!")


@app.command()
def list(active: bool = typer.Option(True, "--all", help="Show all habits")):
    """List habits."""
    filter_text = "Active" if active else "All"
    typer.echo(f"[*] {filter_text} Habits:")
    typer.echo("No habits tracked yet.")


@app.command()
def log(habit_name: str = typer.Argument(..., help="Habit to log"), count: int = typer.Option(1, "--count", "-c")):
    """Log habit completion."""
    typer.echo(f"[OK] Logged {count}x for: {habit_name}")
    typer.echo(f"Current streak: 0 days")


@app.command()
def streak(habit_name: str = typer.Argument(..., help="Habit name")):
    """Check habit streak."""
    typer.echo(f"[*] Streak for {habit_name}:")
    typer.echo("Current: 0 days")
    typer.echo("Best: 0 days")


@app.command()
def progress(habit_name: str = typer.Argument(None, help="Habit name (optional)")):
    """Show habit progress."""
    if habit_name:
        typer.echo(f"📊 Progress: {habit_name}")
        typer.echo("Completed this week: 0/7")
    else:
        typer.echo("📊 All Habits Progress:")
        typer.echo("No habits to display")


@app.command()
def delete(habit_name: str = typer.Argument(..., help="Habit to delete"), force: bool = typer.Option(False, "--force")):
    """Delete a habit."""
    if not force:
        typer.confirm(f"Delete habit '{habit_name}'?", abort=True)
    typer.echo(f"🗑️  Deleted habit: {habit_name}")


@app.command()
def stats():
    """Show habit statistics."""
    typer.echo("📈 Habit Statistics:")
    typer.echo("Total habits: 0")
    typer.echo("Completion rate: 0%")
    typer.echo("Longest streak: 0 days")
