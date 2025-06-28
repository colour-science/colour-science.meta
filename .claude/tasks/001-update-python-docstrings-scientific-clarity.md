# Project: Update Python Docstrings for Scientific Clarity

## Background and Motivation

Python modules within colour-science sub-packages require docstring improvements to enhance scientific clarity and consistency. The goal is to recursively update all docstrings while maintaining research standards, preserving existing structure, and ensuring consistent formatting across the codebase.

## Affected Repositories
- [ ] colour/
- [ ] colour-checker-detection/
- [ ] colour-clf-io/
- [ ] colour-dash/
- [ ] colour-datasets/
- [ ] colour-demosaicing/
- [ ] colour-hdri/
- [ ] colour-specio/
- [ ] colour-visuals/

*Note: Specific repository will be determined based on the sub-package location*

## Key Challenges and Analysis

1. **Precision Requirements**: Each docstring must be manually reviewed for contextual appropriateness
2. **Format Preservation**: Must maintain all Sphinx/RST markers and emphasis
3. **Scientific Standards**: Apply research writing standards while improving clarity
4. **Scale Management**: Process potentially hundreds of modules systematically
5. **Validation Complexity**: Ensure no code modifications outside docstrings

## High-level Task Breakdown

### Phase 1: Discovery and Setup
- [ ] Task 1: Identify target sub-package and repository
  - Repository: [To be determined]
  - Success Criteria: Clear identification of sub-package path and module count
  - Validation: List of Python modules excluding test files

- [ ] Task 2: Create processing framework
  - Repository: [Target repository]
  - Success Criteria: Script to track processed modules and changes
  - Validation: Test on single module, verify change tracking works

- [ ] Task 3: Define validation checklist automation
  - Repository: [Target repository]
  - Success Criteria: Automated checks for formatting requirements
  - Validation: Catches common violations (line length, marker preservation)

### Phase 2: Content Standards Implementation
- [ ] Task 4: Implement docstring parser
  - Repository: [Target repository]
  - Success Criteria: Extracts docstrings while preserving exact formatting
  - Validation: Round-trip test (parse and reconstruct) matches original

- [ ] Task 5: Create modification rules engine
  - Repository: [Target repository]
  - Success Criteria: Applies all content standards systematically
  - Validation: Test cases for each rule (imperative mood, terminology, etc.)

- [ ] Task 6: Build exception detection system
  - Repository: [Target repository]
  - Success Criteria: Identifies functions that raise exceptions without "Raises" section
  - Validation: Correctly identifies exception patterns in code

### Phase 3: Processing Implementation
- [ ] Task 7: Process first batch (5-10 modules)
  - Repository: [Target repository]
  - Success Criteria: All docstrings updated per standards, no code changes
  - Validation: Manual review of changes, run tests

- [ ] Task 8: Refine based on initial results
  - Repository: [Target repository]
  - Success Criteria: Improved rules based on edge cases found
  - Validation: Re-process initial batch with refined rules

- [ ] Task 9: Complete full sub-package processing
  - Repository: [Target repository]
  - Success Criteria: All modules processed, change log generated
  - Validation: Full test suite passes, spot checks on changes

### Phase 4: Validation and Delivery
- [ ] Task 10: Run comprehensive validation
  - Repository: [Target repository]
  - Success Criteria: All checklist items verified programmatically
  - Validation: No regressions, all tests pass

- [ ] Task 11: Generate final report
  - Repository: [Target repository]
  - Success Criteria: Complete summary of all changes by module
  - Validation: Report accurately reflects git diff

## Project Status Board

### In Progress
- [ ] Initial setup and sub-package identification

### Completed
- [x] Project planning and requirements analysis

### Blocked
- None currently

## Current Status / Progress Tracking

Awaiting sub-package specification to begin implementation.

## Executor's Feedback or Assistance Requests

Need clarification on:
1. Which specific sub-package to process first
2. Whether to create reusable tooling for future docstring updates

## Lessons

- Docstring updates require careful balance between automation and manual review
- Preserving RST/Sphinx formatting is critical for documentation builds
- Scientific terminology requires domain expertise for proper casing

## Implementation Strategy

### Module Discovery Approach
```python
# Use pathlib for recursive module discovery
from pathlib import Path

def find_python_modules(root_path, exclude_tests=True):
    """Find all Python modules recursively."""
    modules = []
    for py_file in Path(root_path).rglob("*.py"):
        if exclude_tests and ("test_" in py_file.name or "/tests/" in str(py_file)):
            continue
        modules.append(py_file)
    return modules
```

### Docstring Processing Pipeline

1. **Parse Module**: Use AST to identify all docstrings
2. **Apply Rules**: 
   - Convert to imperative mood
   - Replace "given" → "specified" where appropriate
   - Lowercase "luminance"/"lightness" (except after colon/sentence start)
   - Consider alternatives to "Return"
   - Add "Raises" sections where needed
3. **Format**: Wrap at 79 characters while preserving markers
4. **Validate**: Check all preservation requirements
5. **Update**: Write back only if changes made

### Content Standards Rules

#### Imperative Mood Conversion
- "Returns X" → "Return X"
- "Generates Y" → "Generate Y"  
- "Calculates Z" → "Calculate Z"

#### Terminology Updates
- "given parameter" → "specified parameter"
- "Luminance" → "luminance" (unless sentence-initial)
- "Lightness" → "lightness" (unless sentence-initial)

#### Exception Documentation
```python
# Detect exception patterns
if "raise" in function_body:
    if "Raises" not in docstring_sections:
        add_raises_section()
```

### Validation Checklist Implementation

```python
def validate_docstring_update(original, updated):
    """Validate docstring modifications."""
    checks = {
        "sphinx_markers_preserved": check_sphinx_markers,
        "emphasis_preserved": check_emphasis_markers,
        "section_headers_unchanged": check_section_headers,
        "line_length_valid": check_line_length,
        "examples_unmodified": check_examples_section,
        "british_spelling_preserved": check_spelling,
        "no_type_additions": check_no_param_types,
    }
    return all(check(original, updated) for check in checks.values())
```

### Processing Workflow

1. **Batch Processing**: Process 5-10 modules at a time for manageable review
2. **Change Tracking**: Log all modifications with before/after snippets
3. **Test Integration**: Run module tests after each batch
4. **Progressive Refinement**: Adjust rules based on edge cases
5. **Final Validation**: Comprehensive check before completion

### Success Metrics

- All docstrings follow scientific writing standards
- No code outside docstrings modified
- All RST/Sphinx formatting preserved
- Test suite continues to pass
- Documentation builds successfully
- Consistent style across all processed modules