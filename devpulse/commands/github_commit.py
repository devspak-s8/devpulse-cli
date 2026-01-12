"""
GitHub Commit Message Generator Module

Generates conventional commit messages based on changed files and git status.
"""

import subprocess
from pathlib import Path
from typing import Optional, Literal, List, Tuple
from dataclasses import dataclass

import typer
from rich.console import Console

console = Console()


@dataclass
class GitStatus:
    """Git repository status information."""
    is_git_repo: bool
    has_changes: bool
    has_staged: bool
    has_unstaged: bool
    changed_files: List[str]
    staged_files: List[str]
    unstaged_files: List[str]
    diff_stat: str


class GitStatusCollector:
    """Collects git repository status information."""

    @staticmethod
    def collect(repo_path: Optional[str] = None) -> GitStatus:
        """
        Collect git status for repository.
        
        Args:
            repo_path: Path to repository (default: current directory)
            
        Returns:
            GitStatus with repository information
            
        Raises:
            ValueError: If not a git repository
        """
        repo_path = repo_path or "."
        repo_dir = Path(repo_path).resolve()
        
        # Check if git repository
        if not GitStatusCollector._is_git_repo(repo_dir):
            raise ValueError(f"Not a git repository: {repo_dir}")
        
        # Get git status
        staged_files = GitStatusCollector._get_staged_files(repo_dir)
        unstaged_files = GitStatusCollector._get_unstaged_files(repo_dir)
        
        all_changed = list(set(staged_files + unstaged_files))
        has_changes = len(all_changed) > 0
        has_staged = len(staged_files) > 0
        has_unstaged = len(unstaged_files) > 0
        
        # Get diff statistics
        diff_stat = GitStatusCollector._get_diff_stat(repo_dir)
        
        return GitStatus(
            is_git_repo=True,
            has_changes=has_changes,
            has_staged=has_staged,
            has_unstaged=has_unstaged,
            changed_files=all_changed,
            staged_files=staged_files,
            unstaged_files=unstaged_files,
            diff_stat=diff_stat
        )

    @staticmethod
    def _is_git_repo(repo_dir: Path) -> bool:
        """Check if directory is a git repository."""
        try:
            result = subprocess.run(
                ["git", "-C", str(repo_dir), "rev-parse", "--git-dir"],
                capture_output=True,
                timeout=5
            )
            return result.returncode == 0
        except Exception:
            return False

    @staticmethod
    def _get_staged_files(repo_dir: Path) -> List[str]:
        """Get list of staged files."""
        try:
            result = subprocess.run(
                ["git", "-C", str(repo_dir), "diff", "--cached", "--name-only"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                return [f.strip() for f in result.stdout.strip().split("\n") if f.strip()]
            return []
        except Exception:
            return []

    @staticmethod
    def _get_unstaged_files(repo_dir: Path) -> List[str]:
        """Get list of unstaged files."""
        try:
            result = subprocess.run(
                ["git", "-C", str(repo_dir), "diff", "--name-only"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                return [f.strip() for f in result.stdout.strip().split("\n") if f.strip()]
            return []
        except Exception:
            return []

    @staticmethod
    def _get_diff_stat(repo_dir: Path) -> str:
        """Get diff statistics."""
        try:
            result = subprocess.run(
                ["git", "-C", str(repo_dir), "diff", "--stat"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                return result.stdout.strip()
            return ""
        except Exception:
            return ""


class ConventionalCommitGenerator:
    """Generates conventional commit messages."""

    VALID_TYPES = ["feat", "fix", "docs", "style", "refactor", "perf", "test", "chore", "ci", "build"]
    VALID_SCOPES = ["auth", "api", "ui", "db", "config", "core", "utils", "cli"]

    def __init__(self):
        self.type = "feat"
        self.scope: Optional[str] = None
        self.breaking = False

    def generate(
        self,
        git_status: GitStatus,
        commit_type: str = "feat",
        scope: Optional[str] = None,
        breaking: bool = False,
        dry_run: bool = False
    ) -> str:
        """
        Generate a conventional commit message.
        
        Args:
            git_status: Git status information
            commit_type: Commit type (feat, fix, docs, etc.)
            scope: Optional scope (auth, api, etc.)
            breaking: Whether this is a breaking change
            dry_run: If True, don't actually execute git commit
            
        Returns:
            Generated commit message
            
        Raises:
            ValueError: If commit type is invalid
        """
        if commit_type not in self.VALID_TYPES:
            raise ValueError(f"Invalid commit type: {commit_type}. Must be one of: {', '.join(self.VALID_TYPES)}")
        
        self.type = commit_type
        self.scope = scope
        self.breaking = breaking
        
        # Analyze changed files to generate summary
        summary = self._generate_summary(git_status, commit_type)
        
        # Generate body from file changes
        body = self._generate_body(git_status)
        
        # Construct full message
        message_parts = [summary]
        if body:
            message_parts.append("")  # blank line
            message_parts.append(body)
        
        if breaking:
            message_parts.append("")
            message_parts.append("BREAKING CHANGE: [describe the breaking change]")
        
        return "\n".join(message_parts)

    def _generate_summary(self, git_status: GitStatus, commit_type: str) -> str:
        """Generate commit message summary line."""
        # Build scope part
        scope_str = ""
        if self.scope:
            scope_str = f"({self.scope})"
        
        # Infer action from files or use generic message
        action = self._infer_action(git_status, commit_type)
        
        summary = f"{commit_type}{scope_str}: {action}"
        
        if self.breaking:
            summary += "!"
        
        return summary

    def _infer_action(self, git_status: GitStatus, commit_type: str) -> str:
        """Infer commit action from changed files."""
        if not git_status.changed_files:
            actions = {
                "feat": "add new feature",
                "fix": "fix issue",
                "docs": "update documentation",
                "style": "improve code style",
                "refactor": "refactor code",
                "perf": "improve performance",
                "test": "add tests",
                "chore": "update dependencies",
                "ci": "update CI configuration",
                "build": "update build configuration"
            }
            return actions.get(commit_type, "update code")
        
        # Analyze file types
        file_types = set()
        for f in git_status.changed_files:
            if f.endswith((".py",)):
                file_types.add("Python")
            elif f.endswith((".js", ".ts", ".jsx", ".tsx")):
                file_types.add("JavaScript/TypeScript")
            elif f.endswith((".md",)):
                file_types.add("documentation")
            elif "test" in f:
                file_types.add("tests")
            elif f.startswith("."):
                file_types.add("configuration")
        
        if commit_type == "feat":
            return f"add {', '.join(file_types)} feature" if file_types else "add new feature"
        elif commit_type == "fix":
            return f"fix {', '.join(file_types)} issue" if file_types else "fix issue"
        elif commit_type == "docs":
            return "update documentation"
        elif commit_type == "test":
            return "add tests"
        else:
            return f"update {', '.join(file_types)}" if file_types else "update code"

    def _generate_body(self, git_status: GitStatus) -> str:
        """Generate commit message body from changed files."""
        if not git_status.changed_files or len(git_status.changed_files) > 10:
            # Only add file list if reasonable number of files
            return ""
        
        body_parts = []
        for f in git_status.changed_files[:10]:
            body_parts.append(f"- {f}")
        
        return "\n".join(body_parts)


class CommitMessageValidator:
    """Validates commit messages against best practices."""

    @staticmethod
    def validate_format(message: str) -> Tuple[bool, str]:
        """
        Validate commit message format.
        
        Args:
            message: Commit message to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not message or not message.strip():
            return False, "Commit message cannot be empty"
        
        lines = message.strip().split("\n")
        if not lines:
            return False, "Commit message cannot be empty"
        
        summary = lines[0]
        
        # Check summary length
        if len(summary) > 72:
            return False, f"Summary line too long ({len(summary)} > 72 characters)"
        
        if len(summary) < 10:
            return False, "Summary line too short (< 10 characters)"
        
        # Check for conventional format
        if ":" not in summary:
            # Not conventional, but still acceptable
            pass
        
        return True, ""

    @staticmethod
    def validate_conventional(message: str) -> Tuple[bool, str]:
        """
        Validate conventional commit format.
        
        Args:
            message: Commit message to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not message or not message.strip():
            return False, "Commit message cannot be empty"
        
        lines = message.strip().split("\n")
        if not lines:
            return False, "Commit message cannot be empty"
        
        summary = lines[0]
        valid_types = ["feat", "fix", "docs", "style", "refactor", "perf", "test", "chore", "ci", "build"]
        
        # Check if it has a colon (conventional format)
        if ":" not in summary:
            return False, "Invalid conventional commit format: missing ':'"
        
        # Extract type (before colon, before any parentheses)
        type_and_scope = summary.split(":")[0]
        
        # Remove scope if present: feat(auth) -> feat
        if "(" in type_and_scope:
            type_part = type_and_scope.split("(")[0].strip()
        else:
            type_part = type_and_scope.strip()
        
        if type_part not in valid_types:
            return False, f"Invalid commit type: {type_part}"
        
        return CommitMessageValidator.validate_format(message)


def apply_commit_message(repo_path: str, message: str) -> bool:
    """
    Apply commit message (execute git commit).
    
    Args:
        repo_path: Path to repository
        message: Commit message
        
    Returns:
        True if commit succeeded, False otherwise
        
    Raises:
        RuntimeError: If git command fails
    """
    try:
        result = subprocess.run(
            ["git", "-C", repo_path, "commit", "-m", message],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            return True
        else:
            error = result.stderr or result.stdout
            console.print(f"[red]Git commit failed: {error}[/red]")
            return False
    except Exception as e:
        console.print(f"[red]Error executing git commit: {e}[/red]")
        return False
