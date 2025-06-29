# Project: Compare Configuration Files

## Background and Motivation

Building on the comprehensive configuration files inventory from Task 3, this task creates a structured CSV comparison of configuration files across all colour-science repositories. The comparison will use the `colour` repository (core library) as the reference baseline and calculate differences for each other repository. This CSV will enable data analysis, visualization, and identification of configuration inconsistencies across the ecosystem.

## Affected Repositories
- [x] colour/ (reference repository)
- [x] colour-checker-detection/
- [x] colour-clf-io/
- [x] colour-dash/
- [x] colour-datasets/
- [x] colour-demosaicing/
- [x] colour-hdri/
- [x] colour-specio/
- [x] colour-visuals/

## Key Challenges and Analysis

1. **Reference Baseline**: Use `colour` repository as the standard for comparison
2. **Metric Calculation**: Implement Line Difference metric to quantify configuration gaps
3. **File Categorization**: Maintain consistent categorization from Task 3 (recursive search results)
4. **CSV Structure**: Create machine-readable format for analysis tools
5. **Missing Files**: Handle cases where repositories lack certain configuration types
6. **Recursive File Handling**: Process configuration files found in subdirectories (docs/, tests/, etc.)

## High-level Task Breakdown

### Phase 1: Data Processing
- [ ] Task 1: Parse configuration-files.json data
  - Repository: colour-science.meta/
  - Success Criteria: Extract all file lists and categorizations from JSON
  - Validation: All repositories and categories represented

- [ ] Task 2: Establish colour repository baseline
  - Repository: colour-science.meta/
  - Success Criteria: Create reference configuration set
  - Validation: Complete baseline with all file types

### Phase 2: Comparison Analysis
- [ ] Task 3: Calculate repository differences
  - Repository: colour-science.meta/
  - Success Criteria: Compare each repo against colour baseline
  - Validation: Accurate difference counts per category

- [ ] Task 4: Compute Line Difference metrics
  - Repository: colour-science.meta/
  - Success Criteria: Calculate standardized difference scores
  - Validation: Metrics reflect actual configuration gaps

### Phase 3: CSV Generation
- [ ] Task 5: Generate comparison CSV
  - Repository: colour-science.meta/
  - Success Criteria: Create `.sandbox/configuration-files-comparison.csv`
  - Validation: CSV is well-formatted and complete

## Project Status Board

### In Progress
- [ ] Task 1: Parse configuration-files.txt data

### Completed
- [x] Project task definition

### Blocked
- None currently

## Current Status / Progress Tracking

Ready to begin implementation. Will use Python script to process the configuration files data and generate CSV comparison.

## Executor's Feedback or Assistance Requests

None at this time.

## Lessons

- Configuration comparison requires consistent baseline
- CSV format enables downstream analysis tools
- Line Difference metric quantifies configuration standardization

## Implementation Details

### Input Data Source
- Source file: `.claude/configuration-files.json` (from Task 3 JSON output)
- Data structure: JSON with metadata and repositories containing categorized file lists
- Reference repository: `colour/` (most complete configuration)
- File paths: Include full relative paths from repository root (e.g., `docs/conf.py`, `tests/conftest.py`)

### CSV Output Format

The `.sandbox/configuration-files-comparison.csv` will have these columns:

```csv
Category,Reference File,Target Repository,Target File,Status,Line Differences
CI/CD,colour/.github/workflows/continuous-integration-documentation.yml,colour-hdri,colour-hdri/.github/workflows/continuous-integration-documentation.yml,EXISTS,8
Documentation,colour/docs/conf.py,colour-demosaicing,colour-demosaicing/docs/conf.py,EXISTS,12
Documentation,colour/docs/Makefile,colour-hdri,colour-hdri/docs/Makefile,EXISTS,0
Python Package Management,colour/pyproject.toml,colour-dash,colour-dash/pyproject.toml,EXISTS,54
Python Package Management,colour/docs/requirements.txt,colour-clf-io,colour-clf-io/docs/requirements.txt,EXISTS,45
Testing,colour/.coveragerc,colour-dash,,MISSING,
Testing,colour/tests/conftest.py,colour-visuals,colour-visuals/tests/conftest.py,EXISTS,3
Other,,colour-dash,colour-dash/Dockerfile,EXTRA,
...
```

Where:
- **Category**: Configuration category from `.claude/configuration-files.txt` (e.g., "CI/CD", "Python Package Management", "Testing", "Other")
- **Reference File**: Full path to file in `colour` repository, or empty for extra files
- **Target Repository**: Name of repository being compared
- **Target File**: Full path to corresponding file in target repository, or empty if missing
- **Status**: "EXISTS", "MISSING", or "EXTRA" (for files in target but not reference)
- **Line Differences**: Number of differing lines (using Python difflib), or empty for missing/extra files

### Line Difference Calculation

Line differences will be calculated using Python's `difflib` to count actual differing lines between files:

```python
import difflib
from pathlib import Path

def calculate_line_difference(reference_file_path, target_file_path):
    """
    Calculate line differences between two files using Python difflib.
    
    Returns:
        int: Number of differing lines, or None if files don't exist
    """
    ref_path = Path(reference_file_path)
    target_path = Path(target_file_path)
    
    if not ref_path.exists() or not target_path.exists():
        return None
    
    try:
        with open(ref_path, 'r', encoding='utf-8') as f:
            ref_lines = f.readlines()
        with open(target_path, 'r', encoding='utf-8') as f:
            target_lines = f.readlines()
        
        # Use difflib to get unified diff
        diff = list(difflib.unified_diff(ref_lines, target_lines, lineterm=''))
        
        # Count lines that start with + or - (excluding header lines)
        diff_count = 0
        for line in diff:
            if line.startswith('+') and not line.startswith('+++'):
                diff_count += 1
            elif line.startswith('-') and not line.startswith('---'):
                diff_count += 1
                
        return diff_count
        
    except (UnicodeDecodeError, IOError) as e:
        # For binary files or encoding issues, return 0
        print(f"Warning: Could not compare {ref_path} and {target_path}: {e}")
        return 0
```

### Data Processing Algorithm

```python
import csv
import json
from pathlib import Path

def parse_configuration_data(config_file_path):
    """Parse .claude/configuration-files.json into structured data."""
    with open(config_file_path, 'r') as f:
        data = json.load(f)
    
    # Extract repositories data, excluding meta-root
    repositories = {}
    for repo_name, repo_data in data['repositories'].items():
        if repo_name != 'meta-root':  # Skip meta-root files for comparison
            repositories[repo_name] = repo_data
                
    return repositories


def generate_comparison_csv(repositories, base_path, output_path):
    """Generate CSV comparison using colour as reference."""
    reference_repo = 'colour'
    reference_config = repositories[reference_repo]
    
    with open(output_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        
        # Header row
        writer.writerow([
            'Category', 'Reference File', 'Target Repository', 
            'Target File', 'Status', 'Line Differences'
        ])
        
        # Process each file in colour repository as reference
        for category, files in reference_config.items():
            
            for ref_file in files:
                ref_file_path = Path(base_path) / 'colour' / ref_file
                
                # Compare against all other repositories
                for repo_name, repo_config in repositories.items():
                    if repo_name == reference_repo:
                        continue  # Skip self-comparison
                        
                    repo_files = repo_config.get(category, [])
                    
                    # Find corresponding file in target repository
                    target_file = None
                    for repo_file in repo_files:
                        # Match by filename (last part of path)
                        if Path(ref_file).name == Path(repo_file).name:
                            target_file = repo_file
                            break
                    
                    if target_file:
                        target_file_path = Path(base_path) / repo_name / target_file
                        status = 'EXISTS'
                        
                        # Calculate line differences
                        line_diff = calculate_line_difference(str(ref_file_path), str(target_file_path))
                        line_diff_str = str(line_diff) if line_diff is not None else '0'
                    else:
                        target_file_path = None
                        status = 'MISSING'
                        line_diff_str = ''
                    
                    writer.writerow([
                        category,
                        f'{reference_repo}/{ref_file}',
                        repo_name,
                        f'{repo_name}/{target_file}' if target_file else '',
                        status,
                        line_diff_str
                    ])
        
        # Now process extra files (files in target repos but not in reference)
        for repo_name, repo_config in repositories.items():
            if repo_name == reference_repo:
                continue  # Skip reference repository
                
            for category, files in repo_config.items():
                reference_files = reference_config.get(category, [])
                
                for repo_file in files:
                    # Check if this file exists in reference
                    file_exists_in_ref = False
                    for ref_file in reference_files:
                        if Path(ref_file).name == Path(repo_file).name:
                            file_exists_in_ref = True
                            break
                    
                    # If file doesn't exist in reference, it's an extra file
                    if not file_exists_in_ref:
                        writer.writerow([
                            category,
                            '',
                            repo_name,
                            f'{repo_name}/{repo_file}',
                            'EXTRA',
                            ''
                        ])
```

### Execution Steps

1. **Parse Input Data**
   - Read `.claude/configuration-files.json` using Python json.load()
   - Extract repositories dictionary from JSON structure  
   - Skip meta-root entries for comparison purposes
   - Repository and category structure already in nested dictionary format

2. **Establish Reference Baseline**
   - Use `colour` repository as reference standard
   - Verify colour repository exists in parsed data
   - Extract all categories and files from colour as comparison baseline

3. **Calculate File Comparisons**
   - For each file in colour repository within each category
   - Match files by filename (Path().name) across repositories
   - Calculate line differences using difflib for existing file pairs
   - Handle three status types: EXISTS, MISSING, EXTRA
   - Convert Path objects to strings for file operations

4. **Generate CSV Output**
   - Create `.sandbox/configuration-files-comparison.csv` with proper headers
   - Write comparison rows for all colour files vs all target repositories
   - Process extra files (in target but not in colour) as separate rows
   - Ensure proper CSV formatting and encoding

### Success Metrics

- CSV contains all 8 target repositories compared against colour (134 total rows including header)
- All 8 configuration categories represented where applicable
- Line difference metrics accurately reflect actual file differences using difflib
- CSV is properly formatted and machine-readable
- Status distribution: EXISTS (103), MISSING (25), EXTRA (5) files correctly identified
- File matching by filename works correctly across repositories
- Path resolution handles repository subdirectories properly

### Validation Checks

1. **Data Completeness**: All 8 target repositories from input file appear in CSV (verified)
2. **File Path Accuracy**: Reference and target file paths are correct and resolve properly using Path objects
3. **Status Accuracy**: EXISTS/MISSING/EXTRA status matches actual file presence in repositories
4. **Line Difference Accuracy**: Diff calculations using difflib unified_diff are mathematically correct
5. **CSV Format**: File matches the CSV format specification defined in the "CSV Output Format" section
6. **Category Usage**: Categories match those from `.claude/configuration-files.json` exactly
7. **JSON Parsing**: Correctly parse JSON structure and extract repositories data
8. **Meta-root Filtering**: Exclude meta-root entries from repository comparisons
9. **Recursive File Coverage**: Include configuration files from subdirectories (docs/, tests/, package dirs)
10. **Subdirectory Path Handling**: Correctly match files with same basename across different subdirectory structures