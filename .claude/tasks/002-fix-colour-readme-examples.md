# Project: Fix colour/README.rst Python Examples

## Background and Motivation

The `colour/README.rst` file contains numerous Python code examples that need to be validated and corrected. The file is very large with excessive token count, making direct processing challenging. We need to create an automated solution that systematically processes all examples to ensure they are functional and accurate, while handling the file size constraints efficiently.

## Affected Repositories
- [x] colour/

## Key Challenges and Analysis

1. **File Size Constraints**: The README.rst file is too large for direct token-based processing
2. **Code Block Extraction**: Need to accurately parse RST format to identify Python code blocks and their expected outputs
3. **Import Dependencies**: Many code examples may have missing imports that need to be auto-detected
4. **Safe Execution**: Code blocks must be executed in isolated environments to prevent side effects
5. **Output Validation**: Need to capture and compare actual vs expected outputs
6. **Plotting Handling**: Matplotlib examples need non-interactive backend configuration

## High-level Task Breakdown

### Phase 1: Script Development
- [ ] Task 1: Create RST parser module
  - Repository: colour/
  - Success Criteria: Can extract all Python code blocks with line numbers from README.rst
  - Validation: Test on small RST sample, verify code block boundaries are correct

- [ ] Task 2: Implement code execution engine
  - Repository: colour/
  - Success Criteria: Safely executes code blocks in isolated namespace, captures stdout/stderr
  - Validation: Test with sample code blocks including errors and outputs

- [ ] Task 3: Build import detection system
  - Repository: colour/
  - Success Criteria: Analyzes code for undefined names, suggests appropriate colour imports
  - Validation: Test on code samples with missing imports

- [ ] Task 4: Create batch processing framework
  - Repository: colour/
  - Success Criteria: Processes code blocks in configurable batches with progress tracking
  - Validation: Process test file with memory monitoring

### Phase 2: Processing Implementation
- [ ] Task 5: Implement file reconstruction logic
  - Repository: colour/
  - Success Criteria: Rebuilds RST file with updated code blocks while preserving formatting
  - Validation: Diff comparison shows only code block changes

- [ ] Task 6: Add comprehensive error handling
  - Repository: colour/
  - Success Criteria: Gracefully handles all edge cases, creates detailed logs
  - Validation: Test with intentionally broken code blocks

- [ ] Task 7: Create backup and rollback mechanism
  - Repository: colour/
  - Success Criteria: Creates timestamped backup before modification, can rollback if needed
  - Validation: Verify backup creation and restoration process

### Phase 3: Execution and Validation
- [ ] Task 8: Run full processing on README.rst
  - Repository: colour/
  - Success Criteria: All code blocks processed, corrected file generated
  - Validation: Spot check multiple examples, run pytest on README examples if applicable

- [ ] Task 9: Generate processing report
  - Repository: colour/
  - Success Criteria: Detailed log showing all modifications made
  - Validation: Report accurately reflects changes, includes statistics

## Project Status Board

### In Progress
- [ ] Initial project setup and analysis

### Completed
- [x] Project planning and task breakdown

### Blocked
- None currently

## Current Status / Progress Tracking

Project initialized. Ready to begin implementation of RST parser module.

## Executor's Feedback or Assistance Requests

None at this time.

## Lessons

- Large RST files require streaming/chunking approaches for processing
- Code execution in isolated environments prevents side effects
- Automated import detection can save significant manual effort

## Implementation Details

### Script Structure
```
colour/utilities/
├── fix_readme_examples.py      # Main script
├── rst_parser.py              # RST parsing utilities
├── code_executor.py           # Safe code execution engine
├── import_detector.py         # Import analysis and correction
└── batch_processor.py         # Batch processing framework
```

### Key Components

1. **RST Parser Module** (`rst_parser.py`)
   - Use regex patterns to identify code blocks: `r'\.\. code-block:: python\n((?:    .*\n)+)'`
   - Track line numbers for accurate replacement
   - Handle nested indentation correctly

2. **Code Executor** (`code_executor.py`)
   - Create isolated namespace with colour imports
   - Use `contextlib.redirect_stdout()` for output capture
   - Configure matplotlib: `matplotlib.use('Agg')`
   - Implement timeout mechanism for long-running code

3. **Import Detector** (`import_detector.py`)
   - Parse AST to find undefined names
   - Map to colour module structure
   - Generate minimal import statements

4. **Batch Processor** (`batch_processor.py`)
   - Process N code blocks at a time
   - Save intermediate results to JSON
   - Implement resume capability for interruptions

### Execution Flow

1. Parse README.rst to extract all code blocks
2. Group code blocks into batches
3. For each batch:
   - Detect missing imports
   - Execute code blocks
   - Compare outputs
   - Update if needed
4. Reconstruct file with corrections
5. Generate detailed report

### Safety Measures

- All file operations use context managers
- Original file backed up with timestamp
- Dry-run mode for testing without modification
- Comprehensive logging at each step
- Rollback capability if errors occur

### Success Metrics

- All code examples execute without errors
- Import statements are complete and minimal
- Output matches actual execution results
- File structure and formatting preserved
- Processing completes within reasonable time/memory limits