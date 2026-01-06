import pytest
from typer.testing import CliRunner
from devpulse.commands import notes

runner = CliRunner()


def test_notes_add():
    result = runner.invoke(notes.app, ["add", "Remember to review PR"])
    assert result.exit_code == 0
    assert "added" in result.stdout


def test_notes_add_with_tag():
    result = runner.invoke(notes.app, ["add", "Fix bug", "--tag", "bugs"])
    assert result.exit_code == 0
    assert "bugs" in result.stdout


def test_notes_list():
    result = runner.invoke(notes.app, ["list"])
    assert result.exit_code == 0
    assert "Notes" in result.stdout


def test_notes_search():
    result = runner.invoke(notes.app, ["search", "meeting"])
    assert result.exit_code == 0
    assert "Searching" in result.stdout


def test_notes_delete_with_force():
    result = runner.invoke(notes.app, ["delete", "1", "--force"])
    assert result.exit_code == 0
    assert "Deleted" in result.stdout


def test_notes_tags():
    result = runner.invoke(notes.app, ["tags"])
    assert result.exit_code == 0
    assert "Tags" in result.stdout


def test_notes_export():
    result = runner.invoke(notes.app, ["export"])
    assert result.exit_code == 0
    assert "Export" in result.stdout
