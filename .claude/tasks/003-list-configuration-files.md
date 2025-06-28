# Project: List All Configuration Files in Colour Science Repositories

## Background and Motivation

The colour-science ecosystem consists of multiple repositories, each containing various configuration files for different tools and systems. Creating a comprehensive list of all configuration files will help in understanding the project structure, maintaining consistency across repositories, and identifying configuration patterns. This list will be valuable for auditing, documentation, and standardization efforts.

## Affected Repositories
- [x] colour/
- [x] colour-checker-detection/
- [x] colour-clf-io/
- [x] colour-dash/
- [x] colour-datasets/
- [x] colour-demosaicing/
- [x] colour-hdri/
- [x] colour-specio/
- [x] colour-visuals/

## Key Challenges and Analysis

1. **Configuration File Identification**: Need to identify all types of configuration files across different tools
2. **Repository Traversal**: Must systematically scan all allowed repositories
3. **Pattern Recognition**: Configuration files may have various extensions and naming conventions
4. **Output Organization**: Results should be organized by repository and category
5. **Exclusion Handling**: Avoid including generated files or cache directories

## High-level Task Breakdown

### Phase 1: Configuration Pattern Definition
- [ ] Task 1: Define configuration file patterns
  - Repository: colour-science.meta/
  - Success Criteria: Comprehensive list of config file patterns (extensions, names)
  - Validation: Covers all common configuration types

- [ ] Task 2: Create scanning script structure
  - Repository: colour-science.meta/
  - Success Criteria: Script framework that can traverse repositories safely
  - Validation: Test on single repository, respects .gitignore

### Phase 2: Repository Scanning
- [ ] Task 3: Scan colour/ repository
  - Repository: colour/
  - Success Criteria: All config files identified and catalogued
  - Validation: Manual spot check against known configs

- [ ] Task 4: Scan remaining repositories
  - Repository: All other colour-* repositories
  - Success Criteria: Complete scan of all repositories
  - Validation: No repositories missed, all patterns detected

### Phase 3: Output Generation
- [ ] Task 5: Generate organized output
  - Repository: colour-science.meta/
  - Success Criteria: Create `.claude/configuration-files.txt` with structured content
  - Validation: File is readable, well-organized, and complete

- [ ] Task 6: Add categorization and statistics
  - Repository: colour-science.meta/
  - Success Criteria: Config files grouped by type, summary statistics included
  - Validation: Categories are logical and comprehensive

## Project Status Board

### In Progress
- [ ] Initial planning and pattern definition

### Completed
- [x] Project task definition

### Blocked
- None currently

## Current Status / Progress Tracking

Task planning complete. Ready to begin implementation.

## Executor's Feedback or Assistance Requests

None at this time.

## Lessons

- Configuration files span many tools and formats
- Repository-specific patterns may exist
- Systematic scanning prevents missing files

## Implementation Details

### Configuration File Patterns

Common configuration file patterns to search for:

#### Python/Package Management
- `pyproject.toml`
- `setup.py`
- `setup.cfg`
- `requirements*.txt`
- `uv.lock`
- `poetry.lock`
- `Pipfile*`
- `tox.ini`

#### Task Runners
- `tasks.py`
- `Makefile`
- `invoke.yaml`

#### Testing
- `pytest.ini`
- `.coveragerc`
- `coverage.toml`

#### Linting/Formatting
- `.pre-commit-config.yaml`
- `.ruff.toml`
- `ruff.toml`
- `.flake8`
- `.pylintrc`
- `.isort.cfg`
- `.black.toml`

#### Documentation
- `conf.py` (Sphinx)
- `mkdocs.yml`
- `.readthedocs.yaml`
- `.readthedocs.yml`

#### CI/CD
- `.github/workflows/*.yml`
- `.github/workflows/*.yaml`
- `.github/dependabot.yml`
- `.gitlab-ci.yml`
- `.travis.yml`
- `azure-pipelines.yml`

#### Version Control
- `.gitignore`
- `.gitattributes`
- `.gitmodules`

#### Editors
- `.editorconfig`
- `.vscode/*`

#### Other
- `.env*`
- `Dockerfile*`
- `docker-compose*.yml`
- `*.dockerfile`
- `LICENSE*`
- `MANIFEST.in`
- `.mailmap`
- `.zenodo.json`

### Scanning Algorithm

Use the `Glob` tool to search each repository for configuration files:

- For exact files: `pyproject.toml`, `setup.py`, etc.
- For patterns: `requirements*.txt`, `.github/workflows/*.yml`, etc.
- For directories: `.vscode/*`, `Dockerfile*`, etc.

Respect `.gitignore` patterns and exclude build/cache directories.

### Output Format

The `.claude/configuration-files.txt` file will be structured as:

```
# Configuration Files in Colour Science Repositories
Generated: [timestamp]

## Summary Statistics
Total repositories scanned: 9
Total configuration files found: [count]

## By Repository

### colour/
Category: Python Package Management
  - pyproject.toml
  - uv.lock
  
Category: Testing
  - pytest.ini
  - .coveragerc
  
Category: Linting
  - .pre-commit-config.yaml
  - ruff.toml
  
Category: CI/CD
  - .github/workflows/continuous-integration.yml
  - .github/workflows/release.yml
  
Category: Documentation
  - docs/conf.py
  - .readthedocs.yaml

[Continue for each repository...]

## By Category

### Python Package Management
- colour/pyproject.toml
- colour/uv.lock
- colour-checker-detection/pyproject.toml
- colour-checker-detection/uv.lock
[etc...]

### Testing
- colour/pytest.ini
- colour/.coveragerc
[etc...]

## Unique Configuration Types
[List of unique config file types found across all repos]

## Repository Configuration Matrix
[Table showing which repos have which config types]
```

### Execution Steps

1. **Initialize Scanner**
   - Set up configuration patterns
   - Prepare output structure
   - Create progress tracking

2. **Scan Each Repository**
   - Navigate to repository root
   - Apply pattern matching
   - Respect .gitignore rules
   - Collect file paths

3. **Process Results**
   - Categorize by file type
   - Group by repository
   - Calculate statistics
   - Identify unique patterns

4. **Generate Output**
   - Create structured text file
   - Include timestamps
   - Add summary sections
   - Format for readability

### Success Metrics

- All 9 colour-science repositories scanned
- No false positives (non-config files)
- No missed configuration files
- Output file is well-organized and parseable
- Categories are meaningful and complete
- Statistics accurately reflect findings