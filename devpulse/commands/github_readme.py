"""
GitHub README Generator Module

Generates professional README.md files for GitHub repositories.
Collects repository context and creates customizable README content.
"""

import os
import subprocess
from pathlib import Path
from typing import Optional, Dict, List, Literal
from dataclasses import dataclass
import typer
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax

console = Console()


@dataclass
class RepoContext:
    """Repository context data collected from local or remote repo."""
    name: str
    description: Optional[str]
    languages: List[str]
    has_package_json: bool
    has_pyproject_toml: bool
    has_requirements_txt: bool
    has_license: bool
    license_type: Optional[str]
    top_level_files: List[str]
    remote_url: Optional[str]
    is_local: bool


class ReadmeGenerator:
    """Generates professional README.md content."""

    STYLE_TEMPLATES = {
        "minimal": {
            "sections": ["title", "description", "installation", "usage", "license"],
            "description": "Minimal README with essentials only"
        },
        "standard": {
            "sections": ["title", "description", "features", "tech_stack", "installation", "usage", "contributing", "license"],
            "description": "Standard README with common sections"
        },
        "detailed": {
            "sections": ["title", "description", "features", "tech_stack", "installation", "usage", "api", "contributing", "license"],
            "description": "Detailed README with extensive sections"
        }
    }

    def __init__(self):
        self.sections = {}

    def generate(
        self,
        context: RepoContext,
        style: Literal["minimal", "standard", "detailed"] = "standard"
    ) -> str:
        """
        Generate README content based on repository context.
        
        Args:
            context: Repository context data
            style: README style template (minimal, standard, detailed)
            
        Returns:
            Generated README content as string
        """
        self.sections = {}
        template = self.STYLE_TEMPLATES.get(style, self.STYLE_TEMPLATES["standard"])
        
        # Generate all possible sections
        self._generate_title(context)
        self._generate_description(context)
        self._generate_features(context)
        self._generate_tech_stack(context)
        self._generate_installation(context)
        self._generate_usage(context)
        self._generate_api(context)
        self._generate_contributing(context)
        self._generate_license(context)
        
        # Assemble sections in template order
        content_parts = []
        for section in template["sections"]:
            if section in self.sections:
                content_parts.append(self.sections[section])
        
        return "\n\n".join(content_parts)

    def _generate_title(self, context: RepoContext) -> None:
        """Generate title section."""
        self.sections["title"] = f"# {context.name}"

    def _generate_description(self, context: RepoContext) -> None:
        """Generate description section."""
        desc = context.description or f"A {context.name} project."
        self.sections["description"] = desc

    def _generate_features(self, context: RepoContext) -> None:
        """Generate features section (placeholder)."""
        features = [
            "🚀 Fast and efficient",
            "🔧 Easy to configure",
            "📊 Comprehensive logging"
        ]
        self.sections["features"] = "## Features\n\n" + "\n".join(f"- {f}" for f in features)

    def _generate_tech_stack(self, context: RepoContext) -> None:
        """Generate tech stack section."""
        tech_parts = ["## Tech Stack\n"]
        
        if context.languages:
            tech_parts.append(f"**Languages:** {', '.join(context.languages)}\n")
        
        # Detect frameworks and tools
        frameworks = []
        if context.has_package_json:
            frameworks.append("Node.js/npm")
        if context.has_pyproject_toml:
            frameworks.append("Python (Poetry)")
        if context.has_requirements_txt:
            frameworks.append("Python (pip)")
        
        if frameworks:
            tech_parts.append(f"**Frameworks/Tools:** {', '.join(frameworks)}\n")
        
        self.sections["tech_stack"] = "".join(tech_parts).strip()

    def _generate_installation(self, context: RepoContext) -> None:
        """Generate installation instructions."""
        install_parts = ["## Installation\n"]
        
        if context.has_package_json:
            install_parts.append("```bash\nnpm install\n```\n")
        elif context.has_requirements_txt:
            install_parts.append("```bash\npip install -r requirements.txt\n```\n")
        elif context.has_pyproject_toml:
            install_parts.append("```bash\npoetry install\n```\n")
        else:
            install_parts.append("```bash\n# Installation instructions\n```\n")
        
        self.sections["installation"] = "".join(install_parts).strip()

    def _generate_usage(self, context: RepoContext) -> None:
        """Generate usage section."""
        usage = "## Usage\n\n```bash\n# Add usage examples here\n```"
        self.sections["usage"] = usage

    def _generate_api(self, context: RepoContext) -> None:
        """Generate API documentation section (placeholder)."""
        api = "## API Documentation\n\n[Add API documentation here]"
        self.sections["api"] = api

    def _generate_contributing(self, context: RepoContext) -> None:
        """Generate contributing guidelines."""
        contributing = """## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request"""
        self.sections["contributing"] = contributing

    def _generate_license(self, context: RepoContext) -> None:
        """Generate license section."""
        if context.has_license and context.license_type:
            license_text = f"## License\n\nThis project is licensed under the {context.license_type} License - see the LICENSE file for details."
        else:
            license_text = "## License\n\n[Specify your license here]"
        self.sections["license"] = license_text


class RepositoryContextCollector:
    """Collects context information about a repository."""

    @staticmethod
    def collect_local(repo_path: Optional[str] = None) -> RepoContext:
        """
        Collect context from a local repository.
        
        Args:
            repo_path: Path to repository (default: current directory)
            
        Returns:
            RepoContext with collected information
            
        Raises:
            ValueError: If not a valid git repository
        """
        repo_path = repo_path or "."
        repo_dir = Path(repo_path).resolve()
        
        if not (repo_dir / ".git").exists():
            raise ValueError(f"Not a git repository: {repo_dir}")
        
        # Get repo name
        name = repo_dir.name
        
        # Get remote URL
        remote_url = RepositoryContextCollector._get_remote_url(repo_dir)
        
        # Check for description file (GitHub's repository description is often in a file)
        description = RepositoryContextCollector._get_description(repo_dir)
        
        # Detect languages from file extensions
        languages = RepositoryContextCollector._detect_languages(repo_dir)
        
        # Check for config files
        has_package_json = (repo_dir / "package.json").exists()
        has_pyproject_toml = (repo_dir / "pyproject.toml").exists()
        has_requirements_txt = (repo_dir / "requirements.txt").exists()
        
        # Check for license
        has_license, license_type = RepositoryContextCollector._detect_license(repo_dir)
        
        # Get top-level files
        top_level_files = [f.name for f in repo_dir.iterdir() 
                          if f.is_file() and not f.name.startswith(".")]
        
        return RepoContext(
            name=name,
            description=description,
            languages=languages,
            has_package_json=has_package_json,
            has_pyproject_toml=has_pyproject_toml,
            has_requirements_txt=has_requirements_txt,
            has_license=has_license,
            license_type=license_type,
            top_level_files=top_level_files,
            remote_url=remote_url,
            is_local=True
        )

    @staticmethod
    def _get_remote_url(repo_dir: Path) -> Optional[str]:
        """Get remote URL from git config."""
        try:
            result = subprocess.run(
                ["git", "-C", str(repo_dir), "config", "--get", "remote.origin.url"],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.stdout.strip() if result.returncode == 0 else None
        except Exception:
            return None

    @staticmethod
    def _get_description(repo_dir: Path) -> Optional[str]:
        """Get description from repository (if stored in .description file)."""
        desc_file = repo_dir / ".description"
        if desc_file.exists():
            try:
                return desc_file.read_text().strip()
            except Exception:
                pass
        return None

    @staticmethod
    def _detect_languages(repo_dir: Path) -> List[str]:
        """Detect programming languages by file extensions."""
        extensions = {}
        
        # Recursively scan files (limit depth to avoid deep nesting)
        def scan_dir(d: Path, depth: int = 0):
            if depth > 3:  # Limit depth
                return
            try:
                for item in d.iterdir():
                    if item.name.startswith("."):
                        continue
                    if item.is_file() and item.suffix:
                        extensions[item.suffix] = extensions.get(item.suffix, 0) + 1
                    elif item.is_dir():
                        scan_dir(item, depth + 1)
            except (PermissionError, OSError):
                pass
        
        scan_dir(repo_dir)
        
        # Map extensions to languages
        ext_to_lang = {
            ".py": "Python",
            ".js": "JavaScript",
            ".ts": "TypeScript",
            ".jsx": "React",
            ".tsx": "React/TypeScript",
            ".java": "Java",
            ".go": "Go",
            ".rs": "Rust",
            ".cpp": "C++",
            ".c": "C",
            ".cs": "C#",
            ".php": "PHP",
            ".rb": "Ruby",
            ".swift": "Swift",
            ".kt": "Kotlin",
        }
        
        languages = set()
        for ext, count in extensions.items():
            if ext in ext_to_lang:
                languages.add(ext_to_lang[ext])
        
        return sorted(list(languages)) or ["Python"]  # Default to Python if no files found

    @staticmethod
    def _detect_license(repo_dir: Path) -> tuple[bool, Optional[str]]:
        """Detect license file and type."""
        license_patterns = {
            "LICENSE": "Unknown License",
            "LICENSE.md": "Unknown License",
            "LICENSE.txt": "Unknown License",
            "COPYING": "COPYING",
        }
        
        for pattern, default_type in license_patterns.items():
            license_file = repo_dir / pattern
            if license_file.exists():
                # Try to detect license type from content
                try:
                    content = license_file.read_text()
                    if "MIT" in content:
                        return True, "MIT"
                    elif "Apache" in content:
                        return True, "Apache 2.0"
                    elif "GPL" in content:
                        return True, "GPL"
                    elif "BSD" in content:
                        return True, "BSD"
                    else:
                        return True, default_type
                except Exception:
                    return True, default_type
        
        return False, None


def validate_readme_not_exists(repo_path: str, output_file: Optional[str] = None) -> bool:
    """
    Check if README.md already exists.
    
    Args:
        repo_path: Path to repository
        output_file: Custom output file (if specified, check that instead)
        
    Returns:
        True if file doesn't exist or user confirms overwrite
    """
    target_file = Path(output_file or repo_path) / "README.md" if not output_file else Path(output_file)
    
    if target_file.exists():
        console.print(f"[yellow]⚠️  {target_file} already exists[/yellow]")
        overwrite = typer.confirm("Overwrite?")
        return overwrite
    return True


def save_readme(content: str, repo_path: str, output_file: Optional[str] = None) -> Path:
    """
    Save README content to file.
    
    Args:
        content: README content
        repo_path: Path to repository
        output_file: Custom output file path (optional)
        
    Returns:
        Path to saved file
        
    Raises:
        PermissionError: If file cannot be written
        ValueError: If path is invalid
    """
    if output_file:
        target_path = Path(output_file)
    else:
        target_path = Path(repo_path) / "README.md"
    
    target_path.parent.mkdir(parents=True, exist_ok=True)
    target_path.write_text(content)
    return target_path
