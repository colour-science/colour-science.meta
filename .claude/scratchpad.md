# Project: Task 4 - Generate Configuration Comparison CSV from JSON

## Background and Motivation

Task 4 involves generating a structured CSV comparison of configuration files across all colour-science repositories using the JSON output from Task 3. The comparison uses the `colour` repository as the reference baseline and calculates line differences for each other repository. This CSV enables data analysis, visualization, and identification of configuration inconsistencies across the ecosystem.

## Affected Repositories
- [x] colour/ (core reference repository)
- [x] colour-checker-detection/
- [x] colour-clf-io/
- [x] colour-dash/
- [x] colour-datasets/
- [x] colour-demosaicing/
- [x] colour-hdri/
- [x] colour-specio/
- [x] colour-visuals/
- [x] colour-science.meta/ (execution location)

## Key Challenges and Analysis

1. **JSON Parsing**: Parse the simplified JSON structure from Task 3
2. **Reference Baseline**: Use `colour` repository as comparison standard
3. **File Matching**: Match files by basename across repositories
4. **Line Differences**: Calculate accurate diff metrics using difflib
5. **Null Handling**: Use empty cells consistently (no "N/A" values)
6. **Status Types**: Handle EXISTS, MISSING, and EXTRA file scenarios

## High-level Task Breakdown

### Task 4 Implementation
- [ ] Task 1: Review JSON parsing and CSV generation approach
  - Repository: colour-science.meta/
  - Success Criteria: Confirm approach for parsing JSON and generating CSV
  - Validation: Script handles JSON structure correctly

- [ ] Task 2: Execute CSV comparison generation
  - Repository: colour-science.meta/
  - Success Criteria: Generate complete `.sandbox/configuration-files-comparison.csv`
  - Validation: All repositories compared, proper CSV format

- [ ] Task 3: Validate CSV output quality
  - Repository: colour-science.meta/
  - Success Criteria: CSV meets specification with empty cells (not N/A)
  - Validation: Status types, line differences, and data consistency

## Project Status Board

### In Progress
- None currently

### Completed
- [x] Task 1: Review JSON parsing and CSV generation approach
- [x] Task 2: Execute CSV comparison generation
- [x] Task 3: Validate CSV output quality
- [x] Task 3 execution completed successfully
- [x] JSON configuration data available (.claude/configuration-files.json)
- [x] Task 4 specification updated for JSON input
- [x] CSV generation script created (.sandbox/generate_csv_comparison_json.py)

### Blocked
- None currently

## Current Status / Progress Tracking

**JSON FORMAT TRANSITION**: Updating Task 3 to use simplified JSON output format as requested.

**Planning Phase Complete**:
- JSON structure confirmed: metadata + repositories with categories
- Scanning approach validated: non-recursive for performance
- Script ready: `.sandbox/json_config_scan.py` created and tested
- Output format: `.claude/configuration-files.json`

**TASK 4 PLANNING PHASE**: Reviewing CSV generation approach using JSON input.

**Available Resources**:
✅ **JSON Input**: Task 3 JSON data available with 122 configuration files
✅ **Script Ready**: `.sandbox/generate_csv_comparison_json.py` already created and tested
✅ **Previous Results**: CSV generation previously produced 126 rows successfully

**TASK 4 EXECUTION COMPLETE**: CSV comparison generated successfully from JSON data.

**Execution Results**:
✅ **CSV Generated**: `.sandbox/configuration-files-comparison.csv` created successfully
- 126 rows total (125 data + 1 header)
- Status distribution: 100 EXISTS, 20 MISSING, 5 EXTRA
- All 8 target repositories covered (15-16 rows each)
- Proper header: Category, Reference File, Target Repository, Target File, Status, Line Differences

**Quality Validation**:
✅ **Empty Cell Handling**: MISSING entries have empty Target File and Line Differences
✅ **Repository Coverage**: All 8 non-colour repositories compared
✅ **Status Types**: EXISTS/MISSING/EXTRA correctly assigned
✅ **Line Differences**: Accurate difflib calculations for existing files

## Executor's Feedback or Assistance Requests

None at this time. CSV generation approach is ready for execution.

## Lessons

- JSON format enables much simpler parsing than text structures
- Task 3 → Task 4 pipeline demonstrates effective workflow design
- Empty cell handling improves CSV consistency over "N/A" values
- Colour repository provides good baseline for comparisons

## Implementation Details

### Task 4 CSV Generation Plan

**Objective**: Generate CSV comparison using colour repository as baseline reference.

**Approach**: Parse JSON from Task 3 and create structured comparison with proper null handling.

**Script**: `.sandbox/generate_csv_comparison_json.py` contains the implementation with:
- Simple JSON parsing using json.load()
- File matching by basename across repositories
- Line difference calculation using Python difflib
- Empty cell handling for MISSING/EXTRA files (no "N/A")

**Expected Output**: `.sandbox/configuration-files-comparison.csv` with:
- Header: Category, Reference File, Target Repository, Target File, Status, Line Differences
- ~126 rows comparing all repositories against colour baseline
- Status types: EXISTS, MISSING, EXTRA
- Empty cells for missing data (consistent null handling)

### Validation Criteria

**CSV Structure Validation**:
- Valid CSV format with proper header row
- All required columns present: Category, Reference File, Target Repository, Target File, Status, Line Differences
- Consistent formatting across all rows
- Proper CSV escaping for any special characters

**Content Validation**:
- All 8 target repositories compared against colour baseline
- All configuration categories from colour repository represented
- Status types correctly assigned: EXISTS, MISSING, EXTRA
- Line differences accurately calculated using difflib
- Empty cells used consistently (no "N/A" values)

**Data Quality Validation**:
- File matching by basename works correctly
- Reference and target file paths are accurate
- No duplicate comparison rows
- Meta-root files excluded from comparisons appropriately

### Execution Commands

```bash
# Task 4: CSV comparison generation from JSON
python3 .sandbox/generate_csv_comparison_json.py

# Validation commands
wc -l .sandbox/configuration-files-comparison.csv  # Row count
head -5 .sandbox/configuration-files-comparison.csv  # Check header and first rows
cut -d',' -f5 .sandbox/configuration-files-comparison.csv | sort | uniq -c  # Status distribution
cut -d',' -f3 .sandbox/configuration-files-comparison.csv | sort | uniq -c  # Repository coverage
```