# Project: Add Existing Repositories as Git Submodules

## Background and Motivation
The user has created a git repository at the root of the colour-science directory and wants to add the existing colour-science repositories as sub-repositories. This will create a meta-repository that manages all colour-science projects as a cohesive unit.

## Affected Repositories
- [x] Root repository (newly created)
- [ ] colour/
- [ ] colour-checker-detection/
- [ ] colour-clf-io/
- [ ] colour-dash/
- [ ] colour-datasets/
- [ ] colour-demosaicing/
- [ ] colour-hdri/
- [ ] colour-specio/
- [ ] colour-visuals/

**Excluded:**
- colour-science.devcontainer/
- Workspace/

## Key Challenges and Analysis

### Current State Analysis:
1. Root repository exists but has no commits yet
2. Only `colour/` appears to be a git repository with remote origin
3. Other directories (colour-checker-detection, colour-clf-io, etc.) are NOT git repositories - they contain source code but no .git directory
4. Need to preserve existing source code while converting to submodules

### Approach: Replace with Git Submodules
Since the directories contain source code but aren't git repositories (except colour/), we'll:
1. Move existing directories to temporary locations
2. Add them as git submodules from GitHub
3. Verify the GitHub version matches local version
4. Remove temporary directories after verification

## High-level Task Breakdown

### Phase 1: Preparation
- [ ] Task 1: Create .gitignore for root repository
  - Repository: Root directory
  - Success Criteria: .gitignore excludes colour-science.devcontainer/ and Workspace/
  - Validation: git status doesn't show excluded directories

- [ ] Task 2: Get list of GitHub repository URLs
  - Repository: Root directory  
  - Success Criteria: Have URLs for all 9 colour-science repos
  - Validation: All URLs verified to exist on GitHub

- [ ] Task 3: Check for local modifications
  - Repository: All colour-* directories
  - Success Criteria: Identify any local changes that differ from GitHub
  - Validation: Document any differences found

### Phase 2: Backup Current State
- [ ] Task 4: Create backup of current directories
  - Repository: Root directory
  - Success Criteria: All directories backed up safely
  - Validation: Backup file created and verified

### Phase 3: Convert to Submodules
- [ ] Task 5: Handle colour/ repository (special case)
  - Repository: Root directory
  - Success Criteria: Convert existing git repo to submodule
  - Validation: Submodule points to correct commit

- [ ] Task 6: Convert colour-checker-detection/ to submodule
  - Repository: Root directory
  - Success Criteria: Added as submodule from GitHub
  - Validation: Content matches previous directory

- [ ] Task 7: Convert colour-clf-io/ to submodule
  - Repository: Root directory
  - Success Criteria: Added as submodule from GitHub
  - Validation: Content matches previous directory

- [ ] Task 8: Convert colour-dash/ to submodule
  - Repository: Root directory
  - Success Criteria: Added as submodule from GitHub
  - Validation: Content matches previous directory

- [ ] Task 9: Convert colour-datasets/ to submodule
  - Repository: Root directory
  - Success Criteria: Added as submodule from GitHub
  - Validation: Content matches previous directory

- [ ] Task 10: Convert colour-demosaicing/ to submodule
  - Repository: Root directory
  - Success Criteria: Added as submodule from GitHub
  - Validation: Content matches previous directory

- [ ] Task 11: Convert colour-hdri/ to submodule
  - Repository: Root directory
  - Success Criteria: Added as submodule from GitHub
  - Validation: Content matches previous directory

- [ ] Task 12: Convert colour-specio/ to submodule
  - Repository: Root directory
  - Success Criteria: Added as submodule from GitHub
  - Validation: Content matches previous directory

- [ ] Task 13: Convert colour-visuals/ to submodule
  - Repository: Root directory
  - Success Criteria: Added as submodule from GitHub
  - Validation: Content matches previous directory

### Phase 4: Finalization
- [ ] Task 14: Create initial commit
  - Repository: Root directory
  - Success Criteria: Root repo has commit with all submodules
  - Validation: git log shows commit, git submodule status shows all repos

- [ ] Task 15: Create README.rst for meta-repository
  - Repository: Root directory
  - Success Criteria: README.rst explains structure and common operations
  - Validation: Clear documentation for users

## Project Status Board
### In Progress
- [ ] Planning submodule conversion strategy

### Completed
- [x] Analyzed repository structure
- [x] Identified repositories to include/exclude
- [x] Determined that most directories need GitHub source

### Blocked
- None

## Current Status / Progress Tracking
Plan created based on user requirements. Ready to proceed with implementation.

## Executor's Feedback or Assistance Requests
Ready to execute the plan once approved.

## Lessons
- colour-science repositories exist on GitHub but local copies aren't git repositories (except colour/)
- Need careful handling of the one existing git repository (colour/)

## Implementation Strategy

### For colour/ (e
xisting git repo):
```bash
# Special handling needed - it's already a git repo
# Option 1: Remove and re-add as submodule
# Option 2: Convert in place (more complex)
```

### For other directories (non-git):
```bash
# Example for colour-checker-detection:
mv colour-checker-detection colour-checker-detection.backup
git submodule add https://github.com/colour-science/colour-checker-detection.git
# Verify contents match
# Remove backup after verification
```

### Repository URLs (to be verified):
- https://github.com/colour-science/colour.git
- https://github.com/colour-science/colour-checker-detection.git
- https://github.com/colour-science/colour-clf-io.git
- https://github.com/colour-science/colour-dash.git
- https://github.com/colour-science/colour-datasets.git
- https://github.com/colour-science/colour-demosaicing.git
- https://github.com/colour-science/colour-hdri.git
- https://github.com/colour-science/colour-specio.git
- https://github.com/colour-science/colour-visuals.git

## Risks and Mitigation
1. **Data Loss**: Current directories might contain local changes
   - Mitigation: Create backups before any operations
   - Compare local vs GitHub versions

2. **colour/ Repository**: Already a git repo, needs special handling
   - Mitigation: Check for uncommitted changes first
   - Document the current commit/branch state

3. **Version Mismatch**: Local code might be different from GitHub
   - Mitigation: Verify contents after submodule addition
   - Keep backups until confirmed matching