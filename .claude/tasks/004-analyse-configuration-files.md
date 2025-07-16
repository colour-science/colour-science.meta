# Project: Analyse Configuration Files

## Background and Motivation

Building on the configuration inventory from Task 3 and basic comparison from Task 4, this task performs an in-depth analysis of key configuration files across the colour-science ecosystem. The analysis focuses on five critical configuration file types that define the development workflow, code quality, and project structure. By using the `colour` repository as the reference standard, this analysis will identify specific differences, inconsistencies, and standardization opportunities across the ecosystem.

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

1. **Multi-file Type Analysis**: Handle five different configuration file types with varying formats
2. **Semantic Comparison**: Go beyond line differences to understand functional differences
3. **YAML/TOML/Python Parsing**: Parse and compare structured configuration formats
4. **Workflow Variations**: Identify meaningful differences in CI/CD configurations
5. **Missing File Handling**: Gracefully handle repositories missing certain config types
6. **Reference Baseline**: Use colour repository configurations as comparison standard

## High-level Task Breakdown

### Phase 1: Analysis Planning
- [ ] Task 1: Define analysis scope and comparison criteria
  - Repository: colour-science.meta/
  - Success Criteria: Clear specification for each file type analysis
  - Validation: Comprehensive analysis plan for all five file types

- [ ] Task 2: Design output format and structure
  - Repository: colour-science.meta/
  - Success Criteria: Define report structure and analysis metrics
  - Validation: Output format supports detailed comparison findings

### Phase 2: Configuration Analysis Implementation
- [ ] Task 3: Implement GitHub Workflows analysis
  - Repository: colour-science.meta/
  - Success Criteria: Compare workflow configurations and identify differences
  - Validation: Workflow variations accurately detected and categorized

- [ ] Task 4: Implement pre-commit configuration analysis
  - Repository: colour-science.meta/
  - Success Criteria: Analyze pre-commit hooks and settings differences
  - Validation: Hook differences and configuration variations identified

- [ ] Task 5: Implement tasks.py analysis
  - Repository: colour-science.meta/
  - Success Criteria: Compare invoke task definitions and implementations
  - Validation: Task availability and implementation differences detected

- [ ] Task 6: Implement docs/conf.py analysis
  - Repository: colour-science.meta/
  - Success Criteria: Compare Sphinx documentation configurations
  - Validation: Documentation settings and extension differences identified

- [ ] Task 7: Implement pyproject.toml analysis
  - Repository: colour-science.meta/
  - Success Criteria: Compare Python project configurations comprehensively
  - Validation: Dependencies, build settings, and tool configuration differences detected

### Phase 3: Report Generation
- [ ] Task 8: Generate comprehensive analysis report
  - Repository: colour-science.meta/
  - Success Criteria: Create detailed report with findings and recommendations
  - Validation: Report is actionable and identifies standardization opportunities

## Project Status Board

### In Progress
- [ ] Task 1: Define analysis scope and comparison criteria

### Completed
- [x] Project task definition and planning

### Blocked
- None currently

## Current Status / Progress Tracking

Task definition complete. Ready to begin detailed analysis planning and implementation.

## Executor's Feedback or Assistance Requests

None at this time.

## Lessons

- Detailed configuration analysis requires semantic understanding beyond line differences
- Structured file formats (YAML, TOML) enable more meaningful comparisons
- Reference baseline approach provides consistent comparison standard
- Configuration standardization improves maintainability across repositories

## Implementation Details

### Analysis Scope

#### 1. GitHub Workflow Files
**Files to analyze:**
- `.github/workflows/continuous-integration-documentation.yml`
- `.github/workflows/continuous-integration-quality-unit-tests.yml`
- `.github/workflows/continuous-integration-static-type-checking.yml`

**Analysis criteria:**
- Workflow triggers (push, pull_request, schedule)
- Job definitions and steps
- Python version matrices
- Dependencies and setup actions
- Test and build commands
- Artifact handling and caching strategies

#### 2. Pre-commit Configuration Files
**Files to analyze:**
- `.pre-commit-config.yaml`

**Analysis criteria:**
- Repository hooks and versions
- Hook configurations and arguments
- Excluded files and patterns
- Hook execution order and dependencies
- Custom hook definitions

#### 3. Task Runner Files
**Files to analyze:**
- `tasks.py`

**Analysis criteria:**
- Available invoke tasks and their purposes
- Task dependencies and relationships
- Command implementations and parameters
- Default values and configuration options
- Documentation and help strings

#### 4. Documentation Configuration Files
**Files to analyze:**
- `docs/conf.py`

**Analysis criteria:**
- Sphinx extensions and configurations
- Theme settings and customizations
- API documentation settings
- Build options and output formats
- Intersphinx mappings and external links

#### 5. Python Project Configuration Files
**Files to analyze:**
- `pyproject.toml`

**Analysis criteria:**
- Build system requirements and backend
- Project metadata (name, version, description)
- Dependencies (required, optional, development)
- Tool configurations (ruff, pytest, coverage, etc.)
- Entry points and scripts
- Package discovery and data files

### Analysis Algorithm

The implementation has been enhanced with comprehensive semantic analysis capabilities:

```python
import json
import yaml
import tomllib
import ast
import re
from pathlib import Path
from typing import Dict, List, Any, Optional, Set, Tuple
from datetime import datetime

class ConfigurationAnalyzer:
    """Comprehensive configuration files analyzer using colour as reference."""
    
    def __init__(self, config_json_path: str):
        """Initialize analyzer with configuration data from Task 3."""
        with open(config_json_path, 'r') as f:
            self.config_data = json.load(f)
        
        self.repositories = self.config_data['repositories']
        self.reference_repo = 'colour'
        self.base_path = Path('.')
    
    def analyze_github_workflows(self) -> Dict[str, Any]:
        """Analyze GitHub workflow configurations comprehensively."""
        workflows = [
            'continuous-integration-documentation.yml',
            'continuous-integration-quality-unit-tests.yml', 
            'continuous-integration-static-type-checking.yml'
        ]
        
        analysis = {}
        ref_workflows = self._load_workflows(self.reference_repo, workflows)
        
        for repo_name, repo_config in self.repositories.items():
            if repo_name == self.reference_repo or repo_name == 'meta-root':
                continue
                
            repo_workflows = self._load_workflows(repo_name, workflows)
            analysis[repo_name] = self._compare_workflows(ref_workflows, repo_workflows)
        
        return analysis
    
    def _load_workflows(self, repo_name: str, workflow_names: List[str]) -> Dict[str, Any]:
        """Load workflow YAML files for a repository."""
        workflows = {}
        repo_path = self.base_path / repo_name
        
        for workflow_name in workflow_names:
            workflow_path = repo_path / '.github' / 'workflows' / workflow_name
            if workflow_path.exists():
                try:
                    with open(workflow_path, 'r') as f:
                        workflows[workflow_name] = yaml.safe_load(f)
                except yaml.YAMLError as e:
                    workflows[workflow_name] = {'error': str(e)}
            else:
                workflows[workflow_name] = None
        
        return workflows
    
    def _compare_workflows(self, ref_workflows: Dict, target_workflows: Dict) -> Dict[str, Any]:
        """Compare workflow configurations between reference and target."""
        comparison = {}
        
        for workflow_name in ref_workflows:
            ref_workflow = ref_workflows[workflow_name]
            target_workflow = target_workflows.get(workflow_name)
            
            if target_workflow is None:
                comparison[workflow_name] = {'status': 'missing'}
            elif 'error' in target_workflow:
                comparison[workflow_name] = {'status': 'error', 'details': target_workflow['error']}
            else:
                comparison[workflow_name] = {
                    'status': 'exists',
                    'differences': self._analyze_workflow_differences(ref_workflow, target_workflow)
                }
        
        return comparison
    
    def _analyze_workflow_differences(self, ref: Dict, target: Dict) -> Dict[str, Any]:
        """Analyze specific differences between workflow configurations."""
        differences = {}
        
        # Compare triggers
        ref_triggers = ref.get('on', {})
        target_triggers = target.get('on', {})
        if ref_triggers != target_triggers:
            differences['triggers'] = {
                'reference': ref_triggers,
                'target': target_triggers
            }
        
        # Compare jobs
        ref_jobs = ref.get('jobs', {})
        target_jobs = target.get('jobs', {})
        
        job_differences = {}
        for job_name in set(ref_jobs.keys()) | set(target_jobs.keys()):
            if job_name not in ref_jobs:
                job_differences[job_name] = {'status': 'extra_in_target'}
            elif job_name not in target_jobs:
                job_differences[job_name] = {'status': 'missing_in_target'}
            else:
                job_diff = self._compare_job_configurations(ref_jobs[job_name], target_jobs[job_name])
                if job_diff:
                    job_differences[job_name] = job_diff
        
        if job_differences:
            differences['jobs'] = job_differences
        
        return differences
    
    def _compare_job_configurations(self, ref_job: Dict, target_job: Dict) -> Optional[Dict]:
        """Compare individual job configurations."""
        differences = {}
        
        # Compare strategy matrices
        ref_strategy = ref_job.get('strategy', {})
        target_strategy = target_job.get('strategy', {})
        if ref_strategy != target_strategy:
            differences['strategy'] = {
                'reference': ref_strategy,
                'target': target_strategy
            }
        
        # Compare steps
        ref_steps = ref_job.get('steps', [])
        target_steps = target_job.get('steps', [])
        
        if len(ref_steps) != len(target_steps):
            differences['step_count'] = {
                'reference': len(ref_steps),
                'target': len(target_steps)
            }
        
        # Analyze step differences (simplified)
        step_differences = []
        for i, (ref_step, target_step) in enumerate(zip(ref_steps, target_steps)):
            if ref_step != target_step:
                step_differences.append({
                    'step_index': i,
                    'reference': ref_step,
                    'target': target_step
                })
        
        if step_differences:
            differences['steps'] = step_differences
        
        return differences if differences else None
    
    def analyze_precommit_configs(self) -> Dict[str, Any]:
        """Analyze pre-commit configuration files."""
        analysis = {}
        ref_config = self._load_precommit_config(self.reference_repo)
        
        for repo_name, repo_config in self.repositories.items():
            if repo_name == self.reference_repo or repo_name == 'meta-root':
                continue
                
            target_config = self._load_precommit_config(repo_name)
            analysis[repo_name] = self._compare_precommit_configs(ref_config, target_config)
        
        return analysis
    
    def _load_precommit_config(self, repo_name: str) -> Optional[Dict]:
        """Load pre-commit configuration for a repository."""
        config_path = self.base_path / repo_name / '.pre-commit-config.yaml'
        if config_path.exists():
            try:
                with open(config_path, 'r') as f:
                    return yaml.safe_load(f)
            except yaml.YAMLError as e:
                return {'error': str(e)}
        return None
    
    def _compare_precommit_configs(self, ref_config: Optional[Dict], target_config: Optional[Dict]) -> Dict[str, Any]:
        """Compare pre-commit configurations comprehensively."""
        if target_config is None:
            return {'status': 'missing'}
        
        if 'error' in target_config:
            return {'status': 'error', 'details': target_config['error']}
        
        if ref_config is None:
            return {'status': 'reference_missing'}
        
        # Extract hooks from both configurations
        ref_hooks = self._extract_hooks_info(ref_config)
        target_hooks = self._extract_hooks_info(target_config)
        
        # Compare hook availability and versions
        all_hooks = set(ref_hooks.keys()) | set(target_hooks.keys())
        hook_comparison = {}
        
        for hook_id in all_hooks:
            if hook_id in ref_hooks and hook_id in target_hooks:
                hook_comparison[hook_id] = {
                    'status': 'both',
                    'ref_version': ref_hooks[hook_id].get('version', 'unknown'),
                    'target_version': target_hooks[hook_id].get('version', 'unknown')
                }
            elif hook_id in ref_hooks:
                hook_comparison[hook_id] = {
                    'status': 'missing_in_target',
                    'ref_version': ref_hooks[hook_id].get('version', 'unknown')
                }
            else:
                hook_comparison[hook_id] = {
                    'status': 'extra_in_target',
                    'target_version': target_hooks[hook_id].get('version', 'unknown')
                }
        
        # Analyze hook configuration differences
        hook_config_differences = self._analyze_hook_configurations(ref_config, target_config)
        
        # Analyze repository version differences
        repo_version_differences = self._analyze_repo_versions(ref_config, target_config)
        
        return {
            'status': 'exists',
            'hooks': hook_comparison,
            'hook_config_differences': hook_config_differences,
            'repo_version_differences': repo_version_differences,
            'total_hooks': len(all_hooks),
            'matching_hooks': len([h for h in hook_comparison.values() if h['status'] == 'both'])
        }
    
    def _analyze_hook_configurations(self, ref_hooks: Dict, target_hooks: Dict) -> Dict[str, Any]:
        """Analyze detailed hook configuration differences."""
        hook_diffs = {}
        
        for hook_id in set(ref_hooks.keys()) | set(target_hooks.keys()):
            if hook_id not in ref_hooks or hook_id not in target_hooks:
                continue
                
            ref_hook = ref_hooks[hook_id]
            target_hook = target_hooks[hook_id]
            
            differences = {}
            
            # Compare hook arguments, files patterns, exclude patterns, types
            for config_key in ['args', 'files', 'exclude', 'types']:
                ref_val = ref_hook.get(config_key)
                target_val = target_hook.get(config_key)
                if ref_val != target_val:
                    differences[config_key] = {
                        'reference': ref_val,
                        'target': target_val
                    }
            
            if differences:
                hook_diffs[hook_id] = differences
        
        return hook_diffs
    
    def _extract_hooks_info(self, config: Dict) -> Dict[str, Dict]:
        """Extract hook information from pre-commit configuration."""
        hooks_info = {}
        
        for repo in config.get('repos', []):
            repo_url = repo.get('repo', '')
            version = repo.get('rev', 'unknown')
            
            for hook in repo.get('hooks', []):
                hook_id = hook.get('id', '')
                if hook_id:
                    hooks_info[hook_id] = {
                        'version': version,
                        'repo_url': repo_url,
                        'config': hook
                    }
        
        return hooks_info
    
    def _analyze_repo_versions(self, ref_config: Dict, target_config: Dict) -> Dict[str, Any]:
        """Analyze version differences between repositories."""
        ref_repos = {repo['repo']: repo.get('rev', 'unknown') for repo in ref_config.get('repos', [])}
        target_repos = {repo['repo']: repo.get('rev', 'unknown') for repo in target_config.get('repos', [])}
        
        version_differences = {}
        
        # Compare versions for common repositories
        common_repos = set(ref_repos.keys()) & set(target_repos.keys())
        
        for repo_url in common_repos:
            ref_version = ref_repos[repo_url]
            target_version = target_repos[repo_url]
            
            if ref_version != target_version:
                version_differences[repo_url] = {
                    'reference': ref_version,
                    'target': target_version
                }
        
        return version_differences
    
    def _compare_precommit_repo(self, ref_repo: Dict, target_repo: Dict) -> Optional[Dict]:
        """Compare individual pre-commit repository configurations."""
        differences = {}
        
        # Compare versions/revisions
        if ref_repo.get('rev') != target_repo.get('rev'):
            differences['revision'] = {
                'reference': ref_repo.get('rev'),
                'target': target_repo.get('rev')
            }
        
        # Compare hooks
        ref_hooks = {hook['id']: hook for hook in ref_repo.get('hooks', [])}
        target_hooks = {hook['id']: hook for hook in target_repo.get('hooks', [])}
        
        hook_differences = {}
        for hook_id in set(ref_hooks.keys()) | set(target_hooks.keys()):
            if hook_id not in ref_hooks:
                hook_differences[hook_id] = {'status': 'extra_in_target'}
            elif hook_id not in target_hooks:
                hook_differences[hook_id] = {'status': 'missing_in_target'}
            else:
                if ref_hooks[hook_id] != target_hooks[hook_id]:
                    hook_differences[hook_id] = {
                        'status': 'different',
                        'reference': ref_hooks[hook_id],
                        'target': target_hooks[hook_id]
                    }
        
        if hook_differences:
            differences['hooks'] = hook_differences
        
        return differences if differences else None
    
    def analyze_tasks_files(self) -> Dict[str, Any]:
        """Analyze invoke tasks.py files using AST parsing."""
        analysis = {}
        ref_tasks = self._extract_tasks_from_py(self.reference_repo)
        
        for repo_name, repo_config in self.repositories.items():
            if repo_name == self.reference_repo or repo_name == 'meta-root':
                continue
                
            target_tasks = self._extract_tasks_from_py(repo_name)
            analysis[repo_name] = self._compare_tasks(ref_tasks, target_tasks)
        
        return analysis
    
    def analyze_docs_configs(self) -> Dict[str, Any]:
        """Analyze Sphinx docs/conf.py files using AST parsing."""
        analysis = {}
        ref_config = self._extract_docs_config(self.reference_repo)
        
        for repo_name, repo_config in self.repositories.items():
            if repo_name == self.reference_repo or repo_name == 'meta-root':
                continue
                
            target_config = self._extract_docs_config(repo_name)
            analysis[repo_name] = self._compare_docs_configs(ref_config, target_config)
        
        return analysis
    
    def analyze_pyproject_tomls(self) -> Dict[str, Any]:
        """Analyze pyproject.toml files."""
        analysis = {}
        ref_config = self._load_pyproject_toml(self.reference_repo)
        
        for repo_name, repo_config in self.repositories.items():
            if repo_name == self.reference_repo or repo_name == 'meta-root':
                continue
                
            target_config = self._load_pyproject_toml(repo_name)
            analysis[repo_name] = self._compare_pyproject_tomls(ref_config, target_config)
        
        return analysis
    
    def _load_pyproject_toml(self, repo_name: str) -> Optional[Dict]:
        """Load pyproject.toml for a repository."""
        toml_path = self.base_path / repo_name / 'pyproject.toml'
        if toml_path.exists():
            try:
                with open(toml_path, 'rb') as f:
                    return tomllib.load(f)
            except tomllib.TOMLDecodeError as e:
                return {'error': str(e)}
        return None
    
    def _compare_pyproject_tomls(self, ref_config: Optional[Dict], target_config: Optional[Dict]) -> Dict[str, Any]:
        """Compare pyproject.toml configurations."""
        if target_config is None:
            return {'status': 'missing'}
        
        if 'error' in target_config:
            return {'status': 'error', 'details': target_config['error']}
        
        if ref_config is None:
            return {'status': 'reference_missing'}
        
        differences = {}
        
        # Compare build system
        ref_build = ref_config.get('build-system', {})
        target_build = target_config.get('build-system', {})
        if ref_build != target_build:
            differences['build-system'] = {
                'reference': ref_build,
                'target': target_build
            }
        
        # Compare project metadata
        ref_project = ref_config.get('project', {})
        target_project = target_config.get('project', {})
        
        project_differences = {}
        for key in set(ref_project.keys()) | set(target_project.keys()):
            if ref_project.get(key) != target_project.get(key):
                project_differences[key] = {
                    'reference': ref_project.get(key),
                    'target': target_project.get(key)
                }
        
        if project_differences:
            differences['project'] = project_differences
        
        # Compare tool configurations with enhanced analysis for ruff
        ref_tools = ref_config.get('tool', {})
        target_tools = target_config.get('tool', {})
        
        tool_differences = {}
        for tool_name in set(ref_tools.keys()) | set(target_tools.keys()):
            ref_tool_config = ref_tools.get(tool_name)
            target_tool_config = target_tools.get(tool_name)
            
            if ref_tool_config != target_tool_config:
                tool_diff = {
                    'reference': ref_tool_config,
                    'target': target_tool_config
                }
                
                # Enhanced analysis for ruff configuration
                if tool_name == 'ruff' and ref_tool_config and target_tool_config:
                    tool_diff['analysis'] = self._analyze_ruff_differences(ref_tool_config, target_tool_config)
                
                tool_differences[tool_name] = tool_diff
        
        if tool_differences:
            differences['tools'] = tool_differences
        
        return {'status': 'exists', 'differences': differences} if differences else {'status': 'identical'}
    
    def _analyze_ruff_differences(self, ref_config: Dict, target_config: Dict) -> Dict[str, Any]:
        """Analyze specific ruff configuration differences with detailed rule analysis."""
        analysis = {}
        
        # Compare target-version
        ref_target = ref_config.get('target-version')
        target_target = target_config.get('target-version')
        if ref_target != target_target:
            analysis['target_version'] = {
                'reference': ref_target,
                'target': target_target
            }
        
        # Compare line-length
        ref_length = ref_config.get('line-length')
        target_length = target_config.get('line-length')
        if ref_length != target_length:
            analysis['line_length'] = {
                'reference': ref_length,
                'target': target_length
            }
        
        # Compare select rules with detailed breakdown
        ref_select = set(ref_config.get('select', []))
        target_select = set(target_config.get('select', []))
        if ref_select != target_select:
            analysis['select_rules'] = {
                'reference': sorted(list(ref_select)),
                'target': sorted(list(target_select)),
                'missing': sorted(list(ref_select - target_select)),
                'extra': sorted(list(target_select - ref_select))
            }
        
        # Compare ignore rules with detailed breakdown
        ref_ignore = set(ref_config.get('ignore', []))
        target_ignore = set(target_config.get('ignore', []))
        if ref_ignore != target_ignore:
            analysis['ignore_rules'] = {
                'reference': sorted(list(ref_ignore)),
                'target': sorted(list(target_ignore)),
                'missing': sorted(list(ref_ignore - target_ignore)),
                'extra': sorted(list(target_ignore - ref_ignore))
            }
        
        return analysis
    
    def _analyze_dependency_differences(self, ref_deps: List[str], target_deps: List[str]) -> Dict[str, Any]:
        """Analyze dependency version differences."""
        def parse_dependency(dep_str):
            """Parse dependency string to extract name and version."""
            match = re.match(r'^([a-zA-Z0-9\-_.]+)(?:[>=<~!]+(.+))?', dep_str)
            if match:
                name, version = match.groups()
                return name, version or 'any'
            return dep_str, 'any'
        
        ref_parsed = {parse_dependency(dep)[0]: parse_dependency(dep)[1] for dep in ref_deps}
        target_parsed = {parse_dependency(dep)[0]: parse_dependency(dep)[1] for dep in target_deps}
        
        differences = {}
        
        for dep_name in set(ref_parsed.keys()) | set(target_parsed.keys()):
            ref_version = ref_parsed.get(dep_name)
            target_version = target_parsed.get(dep_name)
            
            if ref_version != target_version:
                differences[dep_name] = {
                    'reference_version': ref_version,
                    'target_version': target_version
                }
        
        return differences
    
    def _format_workflow_differences(self, analysis: Dict) -> str:
        """Format workflows analysis grouped by workflow type for better readability."""
        # Group differences by workflow type rather than repository
        # Structure: workflow_type -> configuration_type -> [repositories]
        # Example:
        # #### continuous-integration-documentation.yml
        # **Missing Actions:**
        # - `repo1`: Missing `actions/upload-artifact`
        # - `repo2`: Missing `actions/upload-artifact`
        # **Operating System Matrix:**
        # - `repo3`: Uses `['ubuntu-latest']` instead of `['macOS-latest']`
        
        # Collect and group differences by workflow type, then configuration aspect
        grouped_differences = {}
        for repo_name, workflows in analysis.items():
            for workflow_name, workflow_data in workflows.items():
                if workflow_data.get('status') != 'exists' or not workflow_data.get('differences'):
                    continue
                    
                if workflow_name not in grouped_differences:
                    grouped_differences[workflow_name] = {}
                    
                differences = workflow_data['differences']
                jobs = differences.get('jobs', {})
                
                for job_name, job_data in jobs.items():
                    # Group by specific configuration aspects
                    if 'strategy' in job_data:
                        matrix = job_data['strategy'].get('matrix', {})
                        if 'os' in matrix:
                            config_type = 'Operating System Matrix'
                            if config_type not in grouped_differences[workflow_name]:
                                grouped_differences[workflow_name][config_type] = []
                            grouped_differences[workflow_name][config_type].append({
                                'repo': repo_name,
                                'difference': f"Uses `{matrix['target']}` instead of `{matrix['reference']}`"
                            })
        
        return self._format_grouped_differences_output(grouped_differences)
    
    def _format_hook_config_differences(self, analysis: Dict) -> str:
        """Format pre-commit analysis grouped by hook type for better readability."""
        # Group differences by hook type rather than repository
        # Structure: hook_type -> configuration_type -> [repositories]
        # Example:
        # #### codespell
        # **Arguments:**
        # - `repo1`: Uses `['--ignore-words-list=X']` instead of reference `['--ignore-words-list=Y']`
        # - `repo2`: Uses `['--ignore-words-list=X']` instead of reference `['--ignore-words-list=Y']`
        # **Exclude Patterns:**
        # - `repo3`: Missing exclude pattern `config-aces-reference.ocio.yaml`
        
        # Collect and group hook configuration differences by hook type
        grouped_by_hook = {}
        for repo_name, repo_data in analysis.items():
            if repo_data.get('status') != 'exists' or not repo_data.get('differences'):
                continue
                
            repositories = repo_data['differences'].get('repositories', {})
            for repo_url, repo_differences in repositories.items():
                hooks = repo_differences.get('hooks', {})
                for hook_id, hook_data in hooks.items():
                    if hook_data.get('status') == 'different':
                        if hook_id not in grouped_by_hook:
                            grouped_by_hook[hook_id] = {}
                            
                        # Group by configuration aspects
                        ref_hook = hook_data.get('reference', {})
                        target_hook = hook_data.get('target', {})
                        
                        for config_key in ['args', 'exclude', 'files', 'types']:
                            ref_val = ref_hook.get(config_key)
                            target_val = target_hook.get(config_key)
                            if ref_val != target_val:
                                config_type = f"{config_key.title()} Patterns" if config_key in ['exclude', 'files'] else config_key.title()
                                if config_type not in grouped_by_hook[hook_id]:
                                    grouped_by_hook[hook_id][config_type] = []
                                    
                                grouped_by_hook[hook_id][config_type].append({
                                    'repo': repo_name,
                                    'difference': f"Uses `{target_val}` instead of reference `{ref_val}`"
                                })
        
        return self._format_hook_grouped_output(grouped_by_hook)
    
    def _format_dependency_table(self, analysis: Dict) -> str:
        """Format dependency analysis grouped by usage patterns."""
        # Group dependencies by usage patterns rather than repository
        # Structure:
        # #### Repository Status Overview
        # | Repository | Dependencies Count | Status | Notes |
        # #### Core Ecosystem Dependencies  
        # Dependencies used by reference repository and multiple others
        # #### Colour Science Ecosystem Dependencies
        # Internal dependencies within the colour-science ecosystem
        # #### Common External Dependencies
        # External packages used by multiple repositories
        # #### Repository-Specific Dependencies
        # Dependencies used by only one repository
        
        # Collect dependency information from all repositories
        all_dependencies = {}
        repo_stats = {}
        
        for repo_name, repo_data in analysis.items():
            if repo_data.get('status') != 'exists':
                continue
                
            dependencies = repo_data.get('differences', {}).get('project', {}).get('dependencies', {})
            if dependencies:
                target_deps = dependencies.get('target', [])
                repo_stats[repo_name] = {
                    'count': len(target_deps),
                    'deps': target_deps
                }
                
                # Track dependency usage across repositories
                for dep in target_deps:
                    dep_name = self._extract_dependency_name(dep)
                    if dep_name not in all_dependencies:
                        all_dependencies[dep_name] = []
                    all_dependencies[dep_name].append(repo_name)
        
        # Categorize dependencies by usage patterns
        colour_science_deps = [dep for dep, repos in all_dependencies.items() 
                             if dep.startswith('colour-')]
        common_deps = [dep for dep, repos in all_dependencies.items() 
                      if len(repos) >= 3 and not dep.startswith('colour-')]
        unique_deps = [dep for dep, repos in all_dependencies.items() 
                      if len(repos) == 1]
        
        return self._format_dependency_patterns_output(repo_stats, colour_science_deps, 
                                                     common_deps, unique_deps)
    
    def _format_tool_config_differences(self, analysis: Dict) -> str:
        """Format tool configuration differences grouped by setting type."""
        # Group tool differences by configuration setting type
        # Structure: tool_name -> setting_type -> [repositories]
        # Example:
        # #### ruff Configuration
        # **Target Version:**
        # - `repo1`: Uses `py39` instead of reference `py310`
        # **Selected Rules:**
        # - `repo2`: Uses `[29 items]` instead of reference `['ALL']`
        # **Ignored Rules:**
        # - `repo3`: Uses `[36 items]` instead of reference `[35 items]`
        
        # Collect and group tool configuration differences
        tool_differences = {}
        for repo_name, repo_data in analysis.items():
            if repo_data.get('status') != 'exists' or not repo_data.get('differences'):
                continue
                
            tools = repo_data['differences'].get('tools', {})
            for tool_name, tool_config in tools.items():
                if tool_name not in tool_differences:
                    tool_differences[tool_name] = {}
                    
                ref_config = tool_config.get('reference', {})
                target_config = tool_config.get('target', {})
                
                # Group by specific configuration settings
                for setting_key in ['target-version', 'line-length', 'select', 'ignore']:
                    ref_val = ref_config.get(setting_key)
                    target_val = target_config.get(setting_key)
                    if ref_val != target_val:
                        setting_type = setting_key.replace('-', ' ').title()
                        if setting_type not in tool_differences[tool_name]:
                            tool_differences[tool_name][setting_type] = []
                            
                        tool_differences[tool_name][setting_type].append({
                            'repo': repo_name,
                            'difference': f"Uses `{target_val}` instead of reference `{ref_val}`"
                        })
        
        return self._format_tool_grouped_output(tool_differences)
    
    def generate_markdown_report(self) -> str:
        """Generate comprehensive analysis report in Markdown format."""
        # Perform all analyses
        workflows_analysis = self.analyze_github_workflows()
        precommit_analysis = self.analyze_precommit_configs()
        tasks_analysis = self.analyze_tasks_files()
        docs_analysis = self.analyze_docs_configs()
        pyproject_analysis = self.analyze_pyproject_tomls()
        
        # Build Markdown report with enhanced grouping structure
        report = []
        report.append("# Configuration Files Analysis Report\n")
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  ")
        report.append(f"Reference Repository: `{self.reference_repo}`\n")
        
        # Executive Summary with key metrics
        report.append("## Executive Summary\n")
        report.append("This report analyzes configuration consistency across the colour-science ecosystem...")
        
        # Enhanced analysis sections with improved grouping patterns
        report.append("\n## 1. GitHub Workflows Analysis\n")
        report.append("### Overview\n")
        report.append("### Repository Status\n") 
        report.append("### Detailed Differences\n")
        report.append("# Grouped by workflow type for better pattern recognition")
        report.append(self._format_workflow_differences(workflows_analysis))
        
        report.append("\n## 2. Pre-commit Configuration Analysis\n")
        report.append("### Overview\n")
        report.append("# Missing configurations and summary statistics")
        report.append(self._format_precommit_overview(precommit_analysis))
        report.append("### Hook Coverage\n")
        report.append("# Matrix showing hook availability across repositories")
        report.append(self._format_precommit_coverage_table(precommit_analysis))
        report.append("### Version Consistency\n")
        report.append("# Dedicated table showing hook version differences")
        report.append(self._format_precommit_versions(precommit_analysis))
        report.append("### Hook Configuration Differences\n")
        report.append("# Grouped by hook type, then by configuration type")
        report.append(self._format_hook_config_differences(precommit_analysis))
        
        report.append("\n## 3. Task Runner (tasks.py) Analysis\n")
        report.append("### Task Availability Matrix\n")
        report.append(self._format_tasks_analysis(tasks_analysis))
        
        report.append("\n## 4. Documentation Configuration (docs/conf.py) Analysis\n")
        report.append("### Sphinx Extensions Usage\n")
        report.append("### Theme Configuration\n")
        report.append(self._format_docs_analysis(docs_analysis))
        
        report.append("\n## 5. Python Project Configuration (pyproject.toml) Analysis\n")
        report.append("### Build System Consistency\n")
        report.append("### Dependency Management\n")
        report.append("# Grouped by dependency patterns and usage types")
        report.append(self._format_dependency_table(pyproject_analysis))
        report.append("### Tool Configuration Differences\n")
        report.append("# Grouped by tool, then by configuration setting type")
        report.append(self._format_tool_config_differences(pyproject_analysis))
        
        # Recommendations
        report.append("\n## Recommendations\n")
        report.append(self._generate_recommendations(
            workflows_analysis, precommit_analysis, tasks_analysis, 
            docs_analysis, pyproject_analysis
        ))
        
        # Conclusion
        report.append("\n## Conclusion\n")
        report.append("The colour-science ecosystem shows good overall standardization...")
        
        return '\n'.join(report)
    
    def _format_table(self, headers: List[str], rows: List[List[str]], center_cols: List[int] = None) -> str:
        """Format a properly aligned Markdown table with optional centered columns."""
        if center_cols is None:
            center_cols = []
            
        # Calculate column widths
        col_widths = [len(h) for h in headers]
        for row in rows:
            for i, cell in enumerate(row):
                col_widths[i] = max(col_widths[i], len(str(cell)))
        
        # Build table
        lines = []
        
        # Header
        header_cells = []
        for i, header in enumerate(headers):
            if i in center_cols:
                header_cells.append(header.center(col_widths[i]))
            else:
                header_cells.append(header.ljust(col_widths[i]))
        lines.append('| ' + ' | '.join(header_cells) + ' |')
        
        # Separator with alignment markers
        separator_cells = []
        for i, width in enumerate(col_widths):
            if i in center_cols:
                # Center alignment marker :----:
                separator_cells.append(':' + '-' * (width - 2) + ':')
            else:
                # Left alignment (default)
                separator_cells.append('-' * width)
        lines.append('|' + '-' + '-|-'.join(separator_cells) + '-|')
        
        # Rows
        for row in rows:
            row_cells = []
            for i, cell in enumerate(row):
                cell_str = str(cell)
                if i in center_cols and cell_str in ['✓', '✗']:
                    # Center checkmarks
                    row_cells.append(cell_str.center(col_widths[i]))
                else:
                    row_cells.append(cell_str.ljust(col_widths[i]))
            lines.append('| ' + ' | '.join(row_cells) + ' |')
        
        return '\n'.join(lines)
    
    def _format_workflows_analysis(self, analysis: Dict) -> str:
        """Format workflows analysis section with aligned tables."""
        lines = []
        
        # Build repository status table
        headers = ['Repository', 'Documentation', 'Quality/Tests', 'Type Checking', 'Notes']
        rows = []
        
        for repo_name, repo_analysis in analysis.items():
            doc_status = '✓' if repo_analysis.get('continuous-integration-documentation.yml', {}).get('status') == 'exists' else '✗'
            test_status = '✓' if repo_analysis.get('continuous-integration-quality-unit-tests.yml', {}).get('status') == 'exists' else '✗'
            type_status = '✓' if repo_analysis.get('continuous-integration-static-type-checking.yml', {}).get('status') == 'exists' else '✗'
            
            # Determine notes
            notes = ''
            if doc_status == '✗' and test_status == '✗' and type_status == '✗':
                notes = 'Missing all workflows'
            elif any(wf.get('differences') for wf in repo_analysis.values() if isinstance(wf, dict)):
                notes = 'Has differences'
            
            rows.append([repo_name, doc_status, test_status, type_status, notes])
        
        # Center checkmark columns (1, 2, 3)
        lines.append(self._format_table(headers, rows, center_cols=[1, 2, 3]))
        return '\n'.join(lines)
    
    def _format_precommit_analysis(self, analysis: Dict) -> str:
        """Format pre-commit analysis section with aligned tables."""
        pass
    
    def _format_tasks_analysis(self, analysis: Dict) -> str:
        """Format tasks analysis section with aligned tables."""
        lines = []
        
        # Get all unique tasks
        all_tasks = set()
        for repo_tasks in analysis.values():
            if isinstance(repo_tasks, dict):
                all_tasks.update(repo_tasks.keys())
        
        # Build task availability matrix with full repository names
        headers = ['Task', 'colour', 'colour-checker-detection', 'colour-clf-io', 
                   'colour-dash', 'colour-datasets', 'colour-demosaicing', 
                   'colour-hdri', 'colour-specio', 'colour-visuals']
        rows = []
        
        for task in sorted(all_tasks):
            row = [task]
            for repo in headers[1:]:  # Skip 'Task' header
                if repo in analysis and task in analysis[repo]:
                    row.append('✓')
                else:
                    row.append('✗')
            rows.append(row)
        
        # Center all checkmark columns (1 through 9)
        lines.append(self._format_table(headers, rows, center_cols=list(range(1, 10))))
        return '\n'.join(lines)
    
    def _format_docs_analysis(self, analysis: Dict) -> str:
        """Format documentation analysis section with aligned tables."""
        pass
    
    def _format_pyproject_analysis(self, analysis: Dict) -> str:
        """Format pyproject.toml analysis section with aligned tables."""
        pass
    
    def _generate_recommendations(self, *analyses) -> str:
        """Generate prioritized recommendations from analyses."""
        pass
    
    def save_markdown_report(self, output_path: str):
        """Generate and save the Markdown report."""
        report_content = self.generate_markdown_report()
        
        with open(output_path, 'w') as f:
            f.write(report_content)
        
        print(f"Analysis report saved to: {output_path}")
```

### Output Format

The analysis will generate a comprehensive Markdown report saved as `.sandbox/configuration-files-analysis.md` with the following structure:

```markdown
# Configuration Files Analysis Report

Generated: [timestamp]
Reference Repository: `colour`

## Executive Summary
Brief overview of findings with key metrics and statistics.

## 1. GitHub Workflows Analysis
- Repository status table showing which workflows are present/missing
- **Enhanced Detailed Differences**: Grouped by workflow type for better pattern recognition
  - Each workflow type shows configuration differences organized by type
  - Operating System Matrix differences grouped together
  - Missing/Extra Actions grouped together  
  - System Dependencies differences grouped together
  - Python Version Matrix differences grouped together
  - **Integrated Step-by-Step Comparison**: Detailed matrix table replacing step count differences
    - Table format with steps as rows and repositories as columns
    - Visual indicators: ✓ = Identical, ⚠️ = Different, ✗ = Missing, Extra = Additional step
    - Integrated within each workflow's differences section
    - Only displays steps that have differences across repositories
    - Identifies specific missing steps, extra steps, and configuration variations

## 2. Pre-commit Configuration Analysis
- **Overview**: Repository coverage and missing configurations
  - Summary statistics showing total vs configured repositories
  - Clear identification of repositories without pre-commit setup
- **Hook Coverage**: Matrix showing hook availability across repositories
  - Comprehensive table showing which hooks are implemented in each repository
  - Clear visual indicators for missing vs present hooks
- **Version Consistency**: Dedicated analysis of hook version differences
  - Table format with hooks as rows and repositories as columns
  - Reference column showing base versions from `colour` repository
  - Warning indicators (⚠️) for repositories with version differences
  - Only displays hooks that have version inconsistencies across repositories
  - Positive feedback when all versions are consistent
- **Hook Configuration Differences**: Grouped by hook type for better readability
  - Each hook shows configuration differences organized by type
  - Arguments differences grouped together
  - Exclude Patterns differences grouped together
  - File Patterns differences grouped together
  - Types differences grouped together

## 3. Task Runner (tasks.py) Analysis
- Task availability matrix across repositories with full repository names
- Repository-specific tasks identification
- Missing implementations clearly marked

## 4. Documentation Configuration (docs/conf.py) Analysis
- Sphinx extension usage comparison with proper table formatting
- Theme configuration consistency analysis
- Missing documentation setups identification

## 5. Python Project Configuration (pyproject.toml) Analysis
- Build system consistency verification
- **Enhanced Dependency Management**: Grouped by dependency patterns and usage types
  - Repository Status Overview with dependency counts and categorization
  - Core Ecosystem Dependencies (used by reference + multiple others)
  - Colour Science Ecosystem Dependencies (internal packages)
  - Common External Dependencies (used by multiple repositories)
  - Repository-Specific Dependencies (unique to one repository)
- **Enhanced Tool Configuration Differences**: Grouped by tool, then by setting type
  - Target Version differences grouped together
  - Line Length differences grouped together
  - **Enhanced Ruff Rule Analysis**: Shows specific missing vs extra rules
    - Selected Rules: Exact rule codes missing/extra compared to reference
    - Ignored Rules: Detailed breakdown of ignore rule differences
  - Selected Rules differences grouped together
  - Ignored Rules differences grouped together
- Dependency version analysis for key packages

## Recommendations
Prioritized list of actionable improvements:
- Priority 1: Critical gaps that need immediate attention
- Priority 2: Version and consistency alignments
- Priority 3: Enhancement opportunities

## Conclusion
Summary of overall standardization level and path to improvement.
```

### Table Formatting Standards

All tables in the report should follow these formatting rules:

1. **Column Alignment**:
   - First column (labels): Left-aligned
   - Checkmark columns (✓/✗): Center-aligned using `:----:` in separator
   - Text data columns: Left-aligned
   - Numeric data: Right-aligned if needed

2. **Column Headers**:
   - Use full repository names (e.g., `colour-checker-detection` not `checker`)
   - Keep headers concise but clear

3. **Cell Content**:
   - Center checkmarks with padding spaces
   - Keep text content left-aligned within cells
   - Use consistent symbols: ✓ for present/yes, ✗ for missing/no

4. **Table Structure**:
   - All column dividers must be properly aligned
   - Dynamic column sizing based on content width
   - Step columns sized to fit longest step name
   - Repository columns sized to match header width
   - Maintain consistent spacing throughout

5. **Step-by-Step Comparison Tables**:
   - Step column: Left-aligned, sized to longest step name
   - Repository columns: Center-aligned, sized to repository name length
   - Empty line after section title for proper Markdown rendering
   - Separator lines must match exact column widths

### Example Output Snippets

#### Repository Status Table Example
```markdown
| Repository               | Documentation | Quality/Tests | Type Checking | Notes                 |
|--------------------------|:-------------:|:-------------:|:-------------:|-----------------------|
| colour-checker-detection |       ✓       |       ✓       |       ✓       | Python matrix differs |
| colour-dash              |       ✗       |       ✗       |       ✗       | Missing all workflows |
```

#### Task Availability Matrix Example
```markdown
| Task  | colour | colour-checker-detection | colour-clf-io | colour-dash | colour-specio | colour-visuals |
|-------|:------:|:------------------------:|:-------------:|:-----------:|:-------------:|:--------------:|
| build |   ✓    |            ✓             |       ✓       |      ✓      |       ✗       |       ✓        |
| tests |   ✓    |            ✓             |       ✓       |      ✓      |       ✗       |       ✓        |
| serve |   ✗    |            ✗             |       ✗       |      ✓      |       ✗       |       ✗        |
```

#### Configuration Difference Example
```markdown
### colour-hdri
**continuous-integration-quality-unit-tests.yml**
- Additional OS matrix: Includes `windows-latest` 
- Python versions: Added `3.13` to matrix
- 41 step differences due to OS-specific handling
```

#### Enhanced Ruff Rule Analysis Example
```markdown
#### ruff Configuration
**Target Version:**
- `colour-specio`: Uses `py39` instead of reference `py310`

**Selected Rules:**
- `colour-specio`: Missing: ALL; Extra: A, ARG, B, C4, D, DTZ, E, EXE, F, G, I, ICN, INP, ISC, N, PGH, PIE, PL, RET, RUF, S, SIM, T10, T20, TID, TRY, UP, W, YTT

**Ignored Rules:**
- `colour-clf-io`: Extra: S320
- `colour-specio`: Missing: ANN401, C, C90, COM, ERA, FBT, FIX, NPY002, PT, PTH, PYI036, PYI051, PYI056, RUF022, TD, UP038; Extra: B008, B905, D104, ICN001, PIE804, PLE0605, PLR0911, RET504, RET505, RET506, RET507, RET508, S101, TRY300
```

#### Enhanced Pre-commit Version Analysis Example
```markdown
**Pre-commit Hook Version Analysis:**

| Hook | Reference | colour-datasets | colour-hdri | colour-visuals |
|------|-----------|-----------------|-------------|----------------|
| ruff | v0.8.2    | v0.6.1 ⚠️       | v0.6.1 ⚠️   | v0.6.1 ⚠️      |

*⚠️ indicates version differs from reference (`colour` repository)*
```

#### Enhanced Workflow Step Comparison Example (Integrated)
```markdown
#### continuous-integration-quality-unit-tests.yml
**Operating System Matrix:**
- `colour-datasets`: Uses `['ubuntu-latest']` instead of `['macOS-latest', 'ubuntu-latest', 'windows-latest']`

**System Dependencies:**
- `colour-hdri`: Extra brew dependencies: `adobe-dng-converter, dcraw, exiftool`

**Step-by-Step Comparison:**

| Step                            | colour-checker-detection | colour-clf-io | colour-datasets | colour-demosaicing | colour-hdri | colour-visuals |
|---------------------------------|--------------------------|---------------|-----------------|--------------------|-------------|----------------|
| Action: actions/upload-artifact |            ✗             |       ✓       |        ✗        |         ✗          |      ✗      |       ✗        |
| Environment Variables           |           ⚠️             |       ✓       |       ⚠️        |         ⚠️         |     ⚠️      |       ⚠️       |
| Install Dependencies (macOS)           |            ✓             |       ✗       |        ✗        |         ✓          |     ⚠️      |       ✓        |
| Install Adobe DNG Converter (Windows)  |            ✓             |       ✓       |        ✓        |         ✓          |    Extra    |       ✓        |

*Legend: ✓ = Identical, ⚠️ = Different, ✗ = Missing, Extra = Additional step*
```

### Execution Steps

1. **Initialize Analysis**
   - Load configuration data from `.claude/configuration-files.json`
   - Set up analysis framework with colour repository as reference
   - Prepare output structure for detailed findings

2. **Perform File Type Analysis**
   - Analyze GitHub workflow YAML files for CI/CD differences
   - Compare pre-commit configurations and hook variations
   - Examine invoke tasks.py files for task availability differences
   - Compare Sphinx docs/conf.py configurations
   - Analyze pyproject.toml files for dependency and tool differences

3. **Generate Comprehensive Report**
   - Compile analysis findings into structured Markdown report
   - Calculate standardization metrics and scores
   - Generate actionable recommendations for configuration alignment
   - Save detailed analysis to `.sandbox/detailed-config-analysis.md`

### Success Metrics

- All five configuration file types analyzed across all repositories
- Semantic differences identified beyond basic line-by-line comparison
- **Enhanced workflow step analysis**: Detailed step-by-step comparison tables showing exact workflow differences
- **Enhanced ruff rule analysis**: Specific missing/extra rule codes identified for precise standardization
- **Enhanced pre-commit version analysis**: Dedicated table showing hook version differences with clear visual indicators
- Missing configurations and variations accurately detected
- Actionable recommendations generated for standardization
- Report format supports both automated processing and human review
- Analysis completes without errors for all available configuration files

### Validation Checks

1. **Analysis Completeness**: All target file types processed for all repositories
2. **Semantic Accuracy**: Configuration differences reflect actual functional variations
3. **Missing File Handling**: Graceful handling of repositories lacking certain config types
4. **Data Structure Integrity**: Well-formatted Markdown with tables and clear sections
5. **Recommendation Quality**: Suggestions are specific, actionable, and prioritized
6. **Reference Baseline**: Colour repository consistently used as comparison standard
7. **Error Handling**: Malformed or unparseable configuration files handled gracefully
8. **Performance**: Analysis completes efficiently across all repositories and file types