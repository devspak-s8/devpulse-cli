import pytest
from typer.testing import CliRunner
from devpulse.commands import ai

runner = CliRunner()


def test_ai_suggest_default():
    """Test AI suggest command with default context"""
    result = runner.invoke(ai.app, ["suggest"])
    assert result.exit_code == 0
    assert "AI Suggestions" in result.stdout
    assert "general" in result.stdout


def test_ai_suggest_with_context():
    """Test AI suggest command with custom context"""
    result = runner.invoke(ai.app, ["suggest", "--context", "coding"])
    assert result.exit_code == 0
    assert "coding" in result.stdout


def test_ai_analyze():
    """Test AI analyze command"""
    result = runner.invoke(ai.app, ["analyze"])
    assert result.exit_code == 0
    assert "Running AI analysis" in result.stdout
    assert "productivity patterns" in result.stdout


def test_ai_chat_with_message():
    """Test AI chat command with message"""
    result = runner.invoke(ai.app, ["chat", "Hello AI"])
    assert result.exit_code == 0
    assert "You: Hello AI" in result.stdout


def test_ai_chat_interactive():
    """Test AI chat command in interactive mode"""
    result = runner.invoke(ai.app, ["chat", "--interactive"])
    assert result.exit_code == 0
    assert "interactive AI chat" in result.stdout


def test_ai_chat_no_message():
    """Test AI chat command without message or interactive mode"""
    result = runner.invoke(ai.app, ["chat"])
    assert result.exit_code == 0
    assert "provide a message" in result.stdout


def test_ai_recommend_default():
    """Test AI recommend command with defaults"""
    result = runner.invoke(ai.app, ["recommend"])
    assert result.exit_code == 0
    assert "AI Recommendations" in result.stdout
    assert "all" in result.stdout


def test_ai_recommend_with_category():
    """Test AI recommend command with specific category"""
    result = runner.invoke(ai.app, ["recommend", "--category", "tasks", "--count", "3"])
    assert result.exit_code == 0
    assert "tasks" in result.stdout
    assert "3" in result.stdout


def test_ai_insights_default():
    """Test AI insights command with defaults"""
    result = runner.invoke(ai.app, ["insights"])
    assert result.exit_code == 0
    assert "AI Insights" in result.stdout
    assert "week" in result.stdout


def test_ai_insights_detailed():
    """Test AI insights command with detailed flag"""
    result = runner.invoke(ai.app, ["insights", "--detailed"])
    assert result.exit_code == 0
    assert "Peak productivity hours" in result.stdout
    assert "Task completion patterns" in result.stdout


def test_ai_insights_with_export():
    """Test AI insights command with export option"""
    result = runner.invoke(ai.app, ["insights", "--export", "insights.json"])
    assert result.exit_code == 0
    assert "insights.json" in result.stdout


def test_ai_predict():
    """Test AI predict command"""
    result = runner.invoke(ai.app, ["predict", "time"])
    assert result.exit_code == 0
    assert "AI Prediction: time" in result.stdout
    assert "7 days" in result.stdout


def test_ai_predict_custom_days():
    """Test AI predict command with custom days"""
    result = runner.invoke(ai.app, ["predict", "completion", "--days", "14"])
    assert result.exit_code == 0
    assert "completion" in result.stdout
    assert "14 days" in result.stdout


def test_ai_optimize():
    """Test AI optimize command"""
    result = runner.invoke(ai.app, ["optimize", "schedule"])
    assert result.exit_code == 0
    assert "AI Optimization" in result.stdout
    assert "Suggestions:" in result.stdout


def test_ai_optimize_with_apply():
    """Test AI optimize command with apply flag"""
    result = runner.invoke(ai.app, ["optimize", "tasks", "--apply"])
    assert result.exit_code == 0
    assert "tasks" in result.stdout
