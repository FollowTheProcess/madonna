"""
Nox sessions for project automation.
"""

from __future__ import annotations

import os
import webbrowser
from pathlib import Path

import nox

# Nox config
nox.options.error_on_external_run = True

# GitHub Actions
ON_CI = bool(os.getenv("CI"))

# Global project stuff
ROOT = Path(__file__).parent.resolve()
SRC = ROOT / "src"
TESTS = ROOT / "tests"
COVERAGE_BADGE = ROOT / "docs" / "img" / "coverage.svg"

# Git info
DEFAULT_BRANCH = "main"

# Virtual environment stuff
VENV = ROOT / ".venv"
PYTHON = os.fsdecode(VENV / "bin" / "python")

# All supported python versions for madonna
PYTHONS = [
    "3.8",
    "3.9",
    "3.10",
    "3.11",
]

# "dev" should only be run if no virtual environment found and we're not on CI
# i.e. someone is using nox to set up their local dev environment to
# work on the project
if not VENV.exists() and not ON_CI:
    nox.options.sessions = ["dev"]
else:
    nox.options.sessions = ["test", "coverage", "lint", "docs"]


@nox.session(python=False)
def dev(session: nox.Session) -> None:
    """
    Sets up a python dev environment for the project if one doesn't already exist.
    """
    session.run("poetry", "install", external=True)


@nox.session(python=PYTHONS)
def test(session: nox.Session) -> None:
    """
    Runs the test suite against all supported python versions.
    """
    # Tests require the package to be installed
    session.install(".")
    session.install("pytest", "pytest-cov", "covdefaults")

    session.run("pytest", f"--cov={SRC}", f"{TESTS}")
    session.notify("coverage")


@nox.session
def coverage(session: nox.Session) -> None:
    """
    Test coverage analysis.
    """
    session.install("coverage[toml]", "coverage-badge", "covdefaults")

    session.run("coverage-badge", "-fo", f"{COVERAGE_BADGE}")


@nox.session
def lint(session: nox.Session) -> None:
    """
    Run pre-commit linting.
    """
    session.install("pre-commit", "mypy")
    session.run("pre-commit", "run", "--all-files")
    session.run("mypy")


@nox.session
def docs(session: nox.Session) -> None:
    """
    Builds the project documentation. Use '-- serve' to see changes live.
    """
    session.install("mkdocs", "mkdocs-material", "mkdocstrings[python]")
    session.install(".")

    if "serve" in session.posargs:
        webbrowser.open(url="http://127.0.0.1:8000/madonna/")
        session.run("mkdocs", "serve")
    else:
        session.run("mkdocs", "build", "--clean")


@nox.session
def deploy_docs(session: nox.Session) -> None:
    """
    Used by GitHub actions to deploy docs to GitHub Pages.
    """
    session.install("mkdocs", "mkdocs-material", "mkdocstrings[python]")
    session.install(".")
    session.run("mkdocs", "gh-deploy")


@nox.session
def build(session: nox.Session) -> None:
    """
    Builds the package sdist and wheel.
    """
    session.install("build")
    session.run("python", "-m", "build", ".")
