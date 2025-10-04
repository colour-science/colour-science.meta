LE# Project: Fix detect_colour_checkers_templated Implementation

## Background and Motivation
The `detect_colour_checkers_templated` function in colour-checker-detection needs to be fixed using the working implementation from `.sandbox/Demo/perspective_demo.ipynb`. The current implementation has issues with perspective transformation detection and template matching that prevent it from working correctly.

## Affected Repositories
- [x] colour-checker-detection/

## Key Challenges and Analysis

### Current Implementation Issues:
1. **Missing imports**: The current code imports `load_template` but it's missing other critical imports like `WarpingData`, `cdist`, `linear_sum_assignment`
2. **Incomplete segmentation logic**: The `segmenter_templated` function doesn't properly implement the perspective-aware detection shown in the demo
3. **Broken transformation logic**: The `determine_best_transformation` function exists but isn't properly integrated
4. **Missing correspondence logic**: The demo shows complex correspondence matching that's not in the current implementation

### Working Demo Implementation Key Components:
1. **Proper swatch detection**: Uses DBSCAN for outlier removal and proper contour filtering
2. **Cluster-based detection**: Groups swatches into clusters representing potential colour checkers
3. **Perspective transformation**: Uses brute-force correspondence matching with multiple templates
4. **Validation**: Includes colour validation against template colours

### Dependencies Needed:
- `from dataclasses import dataclass` (for WarpingData)
- `from scipy.spatial.distance import cdist`
- `from scipy.optimize import linear_sum_assignment`
- `from sklearn.cluster import DBSCAN`
- Proper Template loading with correspondences

## High-level Task Breakdown

### Phase 1: Fix Core Dependencies and Data Structures
- [ ] Task 1: Add missing imports to templated.py
  - Repository: colour-checker-detection/
  - Success Criteria: All necessary imports present (dataclass, scipy, sklearn)
  - Validation: Module imports without errors

- [ ] Task 2: Ensure WarpingData dataclass is properly defined
  - Repository: colour-checker-detection/
  - Success Criteria: WarpingData class exists with all fields from demo
  - Validation: Can instantiate WarpingData objects

### Phase 2: Update Segmenter Function
- [ ] Task 3: Reimplement segmenter_templated with perspective-aware logic
  - Repository: colour-checker-detection/
  - Success Criteria: Implements swatch detection, DBSCAN outlier removal, clustering
  - Validation: Returns proper DataSegmentationColourCheckers

- [ ] Task 4: Add order_centroids functionality
  - Repository: colour-checker-detection/
  - Success Criteria: Orders centroids by quadrant for correspondence matching
  - Validation: Produces 4 ordered points per cluster

### Phase 3: Fix Transformation Determination
- [ ] Task 5: Update determine_best_transformation function
  - Repository: colour-checker-detection/
  - Success Criteria: Implements brute-force correspondence matching as in demo
  - Validation: Returns WarpingData with valid transformations

- [ ] Task 6: Integrate transformation logic with templates
  - Repository: colour-checker-detection/
  - Success Criteria: Works with multiple templates (colour, gray)
  - Validation: Correctly identifies best template match

### Phase 4: Update Extractor Function
- [ ] Task 7: Reimplement extractor_templated with transformation application
  - Repository: colour-checker-detection/
  - Success Criteria: Applies perspective transformation and extracts colours
  - Validation: Returns DataDetectionColourChecker objects

- [ ] Task 8: Add colour validation logic
  - Repository: colour-checker-detection/
  - Success Criteria: Validates extracted colours against template
  - Validation: Detects flipped checkers and invalid detections

### Phase 5: Integration and Testing
- [ ] Task 9: Update detect_colour_checkers_templated main function
  - Repository: colour-checker-detection/
  - Success Criteria: Properly orchestrates segmenter and extractor
  - Validation: Function works end-to-end

- [ ] Task 10: Test with perspective images
  - Repository: colour-checker-detection/
  - Success Criteria: Successfully detects checkers in perspective views
  - Validation: Produces correct colour values

## Project Status Board
### In Progress
- [ ] Creating implementation plan

### Completed
- [x] Analyzed current implementation
- [x] Reviewed working demo implementation
- [x] Identified key differences and dependencies

### Blocked
- None

## Current Status / Progress Tracking
- Completed analysis of both implementations
- Identified that the demo uses a more sophisticated approach with:
  - DBSCAN for outlier removal
  - Proper clustering of swatches
  - Brute-force correspondence matching
  - Template-based perspective transformation
- Key insight: The demo implementation is much more robust for perspective views

## Implementation Strategy

The fix requires substantial changes to bring the production code in line with the demo:

1. **Import Structure**: Add all missing scientific computing dependencies
2. **Data Flow**: Implement the three-stage pipeline (detect_swatches → determine_transformation → extract_colours)
3. **Template Integration**: Ensure templates have proper correspondences
4. **Validation**: Add colour validation to detect incorrect detections

## Potential Failure Points Identified

### ✅ Dependencies Check
- WarpingData dataclass: **Already exists and imports correctly**
- scipy.spatial.distance.cdist: **Available and working**
- scipy.optimize.linear_sum_assignment: **Available and working**
- sklearn.cluster.DBSCAN: **Available and working**

### ⚠️ Critical Issues to Address

1. **Import Organization**: While dependencies exist, they're not imported in templated.py:
   - Need to add: `from scipy.spatial.distance import cdist`
   - Need to add: `from sklearn.cluster import DBSCAN`
   - Already has: `from scipy.optimize import linear_sum_assignment`

2. **Function Integration Gap**: 
   - `determine_best_transformation` exists but isn't called by segmenter/extractor
   - `order_centroids` exists but may not be properly integrated
   - Missing connection between segmenter output and transformation determination

3. **Template Correspondence Loading**:
   - Need to verify templates are loaded with valid correspondences
   - Current `load_template` function exists and uses NPZ format

4. **Data Flow Issues**:
   - Current `segmenter_templated` doesn't return clustered centroids needed for transformation
   - Current `extractor_templated` doesn't use WarpingData from transformation step
   - Main function doesn't orchestrate the three-stage pipeline correctly

### Revised Implementation Priority

1. **First**: Add missing imports (low risk, immediate benefit)
2. **Second**: Fix data flow between functions (critical for pipeline)
3. **Third**: Update segmenter to return proper data structure
4. **Fourth**: Update extractor to use transformation data
5. **Fifth**: Fix main orchestration function
6. **Sixth**: Create comprehensive unit tests

## Unit Test Verification Strategy

### Test Structure (Based on test_detect_colour_checkers_segmentation)
Create new test class `TestDetectColourCheckersTemplated` that:

1. **Follows exact pattern** of `test_detect_colour_checkers_segmentation`:
   - Uses same PNG_FILES test images
   - Platform-specific handling (macOS only for reproducibility)
   - Tests multiple images with expected output arrays

2. **Test data structure**:
   ```python
   test_swatches = [
       (np.array([...]),),  # Expected output for image 1
       (np.array([...]),),  # Expected output for image 2
       # ... for each test image
   ]
   ```

3. **Key differences for templated version**:
   - Call `detect_colour_checkers_templated()` instead of `detect_colour_checkers_segmentation()`
   - Update expected test values based on perspective-corrected output
   - Add tests for both 'colour' and 'gray' templates
   - Test with `additional_data=True` to verify WarpingData output

4. **Additional test cases**:
   - Test perspective transformation accuracy
   - Test template correspondence matching
   - Test colour validation (flipped checker detection)
   - Test multi-template detection (colour vs gray)

5. **Validation approach**:
   ```python
   for i, png_file in enumerate(PNG_FILES):
       np.testing.assert_allclose(
           detect_colour_checkers_templated(
               png_file, 
               prefer_template='colour',
               additional_data=False
           ),
           test_swatches[i],
           atol=0.0001,
       )
   ```

## Executor's Feedback or Assistance Requests
None currently - plan validated and ready for implementation

## Lessons
- The demo implementation uses a more sophisticated multi-stage approach than the current production code
- Key to perspective handling is the brute-force correspondence matching with template points
- DBSCAN clustering is crucial for removing outlier swatches
- The transformation determination step is critical and was missing from the production flow
- **NEW**: Most dependencies already exist, main issue is integration and data flow between functions