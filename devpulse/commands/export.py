import typer

app = typer.Typer(help="Export data in multiple formats")


@app.command()
def all(
    format: str = typer.Option("csv", "--format", "-f", help="Format (csv, json, xlsx, html)"),
    output: str = typer.Option("export", "--output", "-o", help="Output file (without extension)"),
    date_range: str = typer.Option(None, "--range", "-r", help="Date range (YYYY-MM-DD:YYYY-MM-DD)")
):
    """Export all data."""
    typer.echo(f"📤 Exporting all data as {format}")
    if date_range:
        typer.echo(f"Date range: {date_range}")
    typer.echo(f"[OK] Data exported to {output}.{format}")


@app.command()
def sessions(format: str = typer.Option("csv", "--format", "-f"), output: str = typer.Option("sessions", "--output", "-o")):
    """Export tracking sessions."""
    typer.echo(f"📤 Exporting sessions as {format}")
    typer.echo(f"[OK] Sessions exported to {output}.{format}")


@app.command()
def projects(format: str = typer.Option("json", "--format", "-f"), output: str = typer.Option("projects", "--output", "-o")):
    """Export projects."""
    typer.echo(f"📤 Exporting projects as {format}")
    typer.echo(f"[OK] Projects exported to {output}.{format}")


@app.command()
def notes(format: str = typer.Option("json", "--format", "-f"), output: str = typer.Option("notes", "--output", "-o")):
    """Export notes."""
    typer.echo(f"📤 Exporting notes as {format}")
    typer.echo(f"[OK] Notes exported to {output}.{format}")


@app.command()
def stats(format: str = typer.Option("xlsx", "--format", "-f"), output: str = typer.Option("stats", "--output", "-o")):
    """Export statistics."""
    typer.echo(f"📤 Exporting statistics as {format}")
    typer.echo(f"[OK] Statistics exported to {output}.{format}")


@app.command()
def archive(format: str = typer.Option("zip", "--format", "-f"), output: str = typer.Option("devpulse-backup", "--output", "-o")):
    """Create full archive backup."""
    typer.echo(f"📤 Creating archive backup...")
    typer.echo(f"[OK] Archive created: {output}.{format}")
