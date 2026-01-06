import pytest
from typer.testing import CliRunner
from devpulse.commands import project

runner = CliRunner()


def test_project_create():
    result = runner.invoke(project.app, ["create", "my-project"])
    assert result.exit_code == 0
    assert "my-project" in result.stdout


def test_project_create_with_options():
    result = runner.invoke(project.app, ["create", "web-app", "--description", "Web project", "--color", "red"])
    assert result.exit_code == 0
    assert "Web project" in result.stdout


def test_project_list():
    result = runner.invoke(project.app, ["list"])
    assert result.exit_code == 0
    assert "Projects" in result.stdout


def test_project_switch():
    result = runner.invoke(project.app, ["switch", "my-project"])
    assert result.exit_code == 0
    assert "my-project" in result.stdout


def test_project_delete_with_force():
    result = runner.invoke(project.app, ["delete", "my-project", "--force"])
    assert result.exit_code == 0
    assert "Deleted" in result.stdout


def test_project_info():
    result = runner.invoke(project.app, ["info", "my-project"])
    assert result.exit_code == 0
    assert "Info" in result.stdout


def test_project_archive():
    result = runner.invoke(project.app, ["archive", "my-project"])
    assert result.exit_code == 0
    assert "Archived" in result.stdout
