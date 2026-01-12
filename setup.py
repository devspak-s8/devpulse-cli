from pathlib import Path

from setuptools import find_packages, setup


BASE_DIR = Path(__file__).parent
README = (BASE_DIR / "README.md").read_text(encoding="utf-8") if (BASE_DIR / "README.md").exists() else ""


setup(
    name="devpulse-cli",  # PyPI name ("devpulse" is taken)
    version="0.3.0",
    packages=find_packages(),
    include_package_data=True,
    # Keep core install fast; heavy deps moved to extras
    install_requires=[
        "typer>=0.21.0",  # Fixed compatibility issues with older versions
        "rich>=13.7.0",
        "colorama>=0.4.6",
        "tabulate>=0.9.0",
        "psutil>=5.9.0",
        "pathspec>=0.12.0",
        "tqdm>=4.66.0",
        "questionary>=2.0.0",
        "pyperclip>=1.8.2",
        "python-dateutil>=2.8.2",
    ],
    extras_require={
        "ai": ["openai>=1.10.0", "anthropic>=0.8.0"],
        "data": ["pandas>=2.1.0", "numpy>=1.26.0"],
        "viz": ["matplotlib>=3.8.0", "plotly>=5.18.0"],
        "db": ["sqlalchemy>=2.0.0", "alembic>=1.13.0"],
        "config": ["pydantic>=2.5.0", "pydantic-settings>=2.1.0", "python-dotenv>=1.0.0", "PyYAML>=6.0.1"],
        "time": ["pendulum>=3.0.0"],
        "secrets": ["detect-secrets>=1.4.0", "python-magic>=0.4.27"],
        "watch": ["watchdog>=3.0.0"],
        "http": ["requests>=2.31.0", "httpx>=0.26.0"],
        "full": [
            "openai>=1.10.0",
            "anthropic>=0.8.0",
            "pandas>=2.1.0",
            "numpy>=1.26.0",
            "matplotlib>=3.8.0",
            "plotly>=5.18.0",
            "sqlalchemy>=2.0.0",
            "alembic>=1.13.0",
            "pydantic>=2.5.0",
            "pydantic-settings>=2.1.0",
            "python-dotenv>=1.0.0",
            "PyYAML>=6.0.1",
            "pendulum>=3.0.0",
            "detect-secrets>=1.4.0",
            "python-magic>=0.4.27",
            "watchdog>=3.0.0",
            "requests>=2.31.0",
            "httpx>=0.26.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "devpulse=devpulse.cli:main",
        ],
    },
    author="DevPulse Maintainers",
    author_email="maintainers@devpulse.dev",
    description="DevPulse – Developer Productivity CLI Tool",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/devpulse",
    project_urls={
        "Source": "https://github.com/yourusername/devpulse",
        "Tracker": "https://github.com/yourusername/devpulse/issues",
    },
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries",
        "Topic :: Utilities",
    ],
    python_requires=">=3.9",
    keywords="developer productivity cli time-tracking logs secrets analytics",
)
