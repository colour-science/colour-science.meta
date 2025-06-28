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
6. **Efficiency**: Use built-in tools (Glob, Grep) instead of writing custom Python scripts for better performance
7. **Accuracy**: Ensure we capture all config files without false positives

## High-level Task Breakdown

### Phase 1: Configuration Pattern Definition (COMPLETED)
- [x] Task 1: Define configuration file patterns
  - Repository: colour-science.meta/
  - Success Criteria: Comprehensive list of config file patterns (extensions, names)
  - Validation: Covers all common configuration types

### Phase 2: Repository Scanning (Simplified Approach)
- [ ] Task 2: Use Glob tool to find configuration files
  - Repository: All colour-* repositories
  - Success Criteria: Find all config files using pattern matching
  - Validation: Cross-check with known config files in each repo
  - Approach: Use multiple Glob calls with specific patterns rather than creating a script

- [ ] Task 3: Compile and organize results
  - Repository: colour-science.meta/
  - Success Criteria: Organize found files by repository and type
  - Validation: All repositories represented, no duplicates

### Phase 3: Output Generation
- [ ] Task 4: Create comprehensive output file
  - Repository: colour-science.meta/
  - Success Criteria: Create `.claude/configuration-files.txt` with all findings
  - Validation: File contains all config files organized by repo and category
  - Include: Statistics, categorization, and repository matrix

## Project Status Board

### In Progress
- [ ] Task 2: Use Glob tool to find configuration files

### Completed
- [x] Project task definition
- [x] Task 1: Define configuration file patterns

### Blocked
- None currently

## Current Status / Progress Tracking

Plan refined for more efficient implementation using built-in tools. Ready to begin scanning repositories using Glob tool rather than creating a custom Python script. This approach will be faster and more reliable.

## Executor's Feedback or Assistance Requests

None at this time.

## Lessons

- Configuration files span many tools and formats
- Repository-specific patterns may exist
- Systematic scanning prevents missing files

## Implementation Details

### Configuration File Patterns

Patterns to search for in each repository:

**Python/Package Management:**
- pyproject.toml
- setup.py
- setup.cfg
- requirements*.txt
- uv.lock
- poetry.lock
- Pipfile*
- tox.ini
- MANIFEST.in

**Task Runners:**
- tasks.py
- Makefile
- invoke.yaml

**Testing:**
- pytest.ini
- .coveragerc
- coverage.toml
- conftest.py (in test directories)

**Linting/Formatting:**
- .pre-commit-config.yaml
- .ruff.toml
- ruff.toml
- .flake8
- .pylintrc
- .isort.cfg
- .black.toml

**Documentation:**
- conf.py (Sphinx)
- mkdocs.yml
- .readthedocs.yaml
- .readthedocs.yml

**CI/CD:**
- .github/workflows/*.yml
- .github/workflows/*.yaml
- .github/dependabot.yml
- .gitlab-ci.yml
- .travis.yml
- azure-pipelines.yml
- .circleci/config.yml

**Version Control:**
- .gitignore
- .gitattributes
- .gitmodules

**Editors:**
- .editorconfig
- .vscode/*.json

**Other:**
- .env*
- Dockerfile*
- docker-compose*.yml
- *.dockerfile
- LICENSE*
- .mailmap
- .zenodo.json

### Scanning Approach

Instead of writing a custom Python script, we'll use the built-in Glob tool to scan each repository efficiently. The approach will be:

1. For each repository, run targeted Glob searches for specific config file patterns
2. Collect and deduplicate results
3. Organize by repository and category
4. Generate final report with statistics

This approach leverages Claude Code's optimized file searching capabilities.

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

1. **Scan Repositories**
   - Use Glob tool to search for each pattern in all repositories
   - Start with the most common patterns first
   - Collect all results

2. **Organize Results**
   - Group findings by repository
   - Categorize by configuration type
   - Remove duplicates
   - Sort alphabetically

3. **Generate Statistics**
   - Count total config files per repository
   - Identify most common configuration types
   - Create repository/config type matrix

4. **Create Output File**
   - Write to `.claude/configuration-files.txt`
   - Include timestamp
   - Add all organized sections
   - Ensure readable formatting

### Success Metrics

- All 9 colour-science repositories scanned
- No false positives (non-config files)
- No missed configuration files
- Output file is well-organized and parseable
- Categories are meaningful and complete
- Statistics accurately reflect findings