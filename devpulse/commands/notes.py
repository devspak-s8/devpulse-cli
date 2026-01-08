import typer

app = typer.Typer(help="Quick note-taking and management")


@app.command()
def add(
    content: str = typer.Argument(..., help="Note content"),
    tag: str = typer.Option(None, "--tag", "-t", help="Note tag/category"),
    priority: str = typer.Option("normal", "--priority", "-p", help="Priority (low, normal, high)")
):
    """Add a quick note."""
    typer.echo(f"📝 Note added")
    if tag:
        typer.echo(f"Tag: {tag}")
    typer.echo(f"Priority: {priority}")
    typer.echo("[OK] Note saved!")


@app.command()
def list(
    tag: str = typer.Option(None, "--tag", "-t", help="Filter by tag"),
    limit: int = typer.Option(10, "--limit", "-l", help="Max notes to show")
):
    """List all notes."""
    filter_text = f"(tag: {tag})" if tag else ""
    typer.echo(f"[*] Notes {filter_text}:")
    typer.echo("No notes yet.")


@app.command()
def search(query: str = typer.Argument(..., help="Search query")):
    """Search notes."""
    typer.echo(f"🔍 Searching for: {query}")
    typer.echo("No matches found.")


@app.command()
def delete(note_id: int = typer.Argument(..., help="Note ID"), force: bool = typer.Option(False, "--force")):
    """Delete a note."""
    if not force:
        typer.confirm(f"Delete note #{note_id}?", abort=True)
    typer.echo(f"🗑️  Deleted note #{note_id}")


@app.command()
def tags():
    """List all note tags."""
    typer.echo("🏷️  Tags:")
    typer.echo("No tags yet.")


@app.command()
def export(format: str = typer.Option("txt", "--format", "-f", help="Export format (txt, md, json)")):
    """Export notes."""
    typer.echo(f"📤 Exporting notes as {format}...")
    typer.echo("[OK] Export complete!")
