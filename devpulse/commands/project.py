import typer

app = typer.Typer(help="Manage projects and workspaces")


@app.command()
def create(
    name: str = typer.Argument(..., help="Project name"),
    description: str = typer.Option(None, "--description", "-d", help="Project description"),
    color: str = typer.Option("blue", "--color", "-c", help="Project color tag")
):
    """Create a new project."""
    typer.echo(f"📁 Creating project: {name}")
    if description:
        typer.echo(f"Description: {description}")
    typer.echo(f"Color: {color}")
    typer.echo("[OK] Project created successfully!")


@app.command()
def list():
    """List all projects."""
    typer.echo("[*] Projects:")
    typer.echo("No projects yet. Create one with 'devpulse project create <name>'")


@app.command()
def switch(project_name: str = typer.Argument(..., help="Project to switch to")):
    """Switch to a different project."""
    typer.echo(f"🔄 Switching to project: {project_name}")
    typer.echo("[OK] Project switched!")


@app.command()
def delete(project_name: str = typer.Argument(..., help="Project to delete"), force: bool = typer.Option(False, "--force", "-f")):
    """Delete a project."""
    if not force:
        typer.confirm(f"Delete project '{project_name}'?", abort=True)
    typer.echo(f"🗑️  Deleted project: {project_name}")


@app.command()
def info(project_name: str = typer.Argument(None, help="Project name")):
    """Show project information."""
    target = project_name or "current"
    typer.echo(f"ℹ️  Project Info: {target}")
    typer.echo("Created: N/A")
    typer.echo("Tasks: 0")
    typer.echo("Time logged: 0h")


@app.command()
def archive(project_name: str = typer.Argument(..., help="Project to archive")):
    """Archive a project."""
    typer.echo(f"📦 Archived project: {project_name}")
    typer.echo("[OK] Project archived!")
