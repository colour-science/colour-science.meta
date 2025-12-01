# Project Context

## Purpose
This is the Colour Science meta-repository workspace containing multiple colour science libraries and tools. The workspace enables cross-repository automation and management of the colour-science ecosystem.

## Workspace Repositories
You may ONLY work within these colour-science repositories:
- `colour/` - Core colour science library
- `colour-checker-detection/` - Library for detecting colour checkers
- `colour-clf-io/` - Common LUT Format (CLF) I/O library
- `colour-cxf/` - Color Exchange Format (CXF) I/O library
- `colour-dash/` - Dash-based web application for colour science
- `colour-datasets/` - Package for accessing colour science datasets
- `colour-demosaicing/` - Demosaicing algorithms
- `colour-hdri/` - High Dynamic Range imaging library
- `colour-specio/` - Spectral I/O library
- `colour-visuals/` - Library for colour science visuals

**CRITICAL:** Never modify files outside these repositories.

## Tech Stack
- **Language:** Python
- **Package Management:** `uv` with `uv.lock` files
- **Task Runner:** `invoke` (tasks.py)
- **Testing:** `pytest`
- **Linting:** `ruff`, `pre-commit`
- **Type Checking:** `pyright`
- **Documentation:** Sphinx with reStructuredText
- **CI/CD:** GitHub Actions

## Project Conventions

### Code Style
- Follow PEP 8 style guidelines
- Use NumPy-style docstrings
- Run linting and formatting before committing
- Follow Conventional Commits specification
- Always use Unix-style line endings (LF)

### Architecture Patterns
- Each subdirectory is an independent Git repository
- Cross-repository automation enabled via meta-repository structure
- Maintain Sphinx compatibility with reStructuredText for documentation

### Testing Strategy
- Include tests for new functionality
- Run doctests alongside unit tests
- Validation commands (run from repository root):
  ```bash
  # Installation
  uv sync --all-extras

  # Code Quality
  pre-commit run --all-files  # or invoke precommit
  ruff check .
  ruff format .
  pyright --threads --skipunannotated --level warning  # or invoke quality

  # Testing
  pytest --doctest-modules  # or invoke tests
  pytest tests/test_specific.py  # for specific tests

  # Documentation
  invoke docs  # if available
  ```

### Git Workflow
- Each repository has independent version control
- Ensure changes don't break GitHub Actions workflows
- Configure git with `git config core.autocrlf false` when cloning
- Ask before using `--force` git commands

## Domain Context
Colour science libraries and tools for professional color management, image processing, and scientific analysis. The ecosystem includes:
- Core color science computations and transformations
- Color checker detection and analysis
- LUT and color exchange format handling
- HDR imaging and demosaicing
- Spectral data I/O
- Web-based visualization and data exploration

## Important Constraints
- **Repository Scope:** Only modify files within the allowed colour-science repositories
- **Simplicity First:** Always strive for the simplest, most elegant solution. Avoid overengineering
- **API Stability:** Be extra careful with API changes in `colour/` core library
- **Version Control:** Never `git restore` or `git reset` without asking the user first
- **GitHub Activity:** Never post on Github without asking the user first
- **Linting:** Never `# noqa` linting errors unless you got confirmation from user first

## External Dependencies
- Python ecosystem via `uv` package manager
- GitHub for CI/CD and version control
- Sphinx documentation system
- NumPy for numerical computations (implied by docstring style)

## Repository-Specific Notes
- **colour/**: Core library - be extra careful with API changes
- **colour-dash/**: May include `invoke serve` for web app; may need `npm audit` if vulnerabilities appear
- **colour-**/**: Check for project-specific invoke tasks using `invoke --list`

## Utility Guidelines
### Script Creation
- When creating scripts, always write them in the `.sandbox` directory unless specified otherwise
- This keeps temporary scripts organized and separate from the main codebase

### Common Commands
- Use `uv sync --all-extras` for dependencies
- Run `invoke --list` to see available tasks per repository
- Use `uv run python -c "code"` for execution
- Navigate to correct repository before commands: `cd colour-*/`
