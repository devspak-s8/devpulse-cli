"""
Command registry for DevPulse CLI.
Imports all command modules and makes them available for registration.
"""

from devpulse.commands import track, logs, secrets, stats, sync, ai, health, project, timer, notes, focus, breaks, report, config, export, habits, dashboard, github

# List of all command modules with their CLI names
COMMAND_MODULES = [
    ("track", track.app, "Track time and commands"),
    ("logs", logs.app, "Analyze and search logs"),
    ("secrets", secrets.app, "Scan for secrets and sensitive data"),
    ("stats", stats.app, "View analytics and statistics"),
    ("sync", sync.app, "Sync data with cloud dashboard"),
    ("ai", ai.app, "AI-powered insights and suggestions"),
    ("health", health.app, "System health monitoring"),
    ("project", project.app, "Manage projects and workspaces"),
    ("timer", timer.app, "Pomodoro and interval timers"),
    ("notes", notes.app, "Quick note-taking and management"),
    ("focus", focus.app, "Focus mode and distraction blocking"),
    ("breaks", breaks.app, "Break management and reminders"),
    ("report", report.app, "Enhanced productivity reports"),
    ("config", config.app, "Configuration management"),
    ("export", export.app, "Export data in multiple formats"),
    ("habits", habits.app, "Track habits and streaks"),
    ("dashboard", dashboard.app, "Summary dashboard view"),
    ("github", github.app, "GitHub integration and statistics"),
]
