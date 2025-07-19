# /// script
# dependencies = [
#   "click",
# ]
# requires-python = ">=3.10"
# ///

"""
__all__ Section Processor

A comprehensive tool for verifying and fixing __all__ sections to match the actual
import order (not alphabetical order) in Python modules. This ensures proper API
consistency across the colour-science project.
"""

import ast
import contextlib
import fnmatch
import logging
import os
import shutil
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import click

LOGGER = logging.getLogger("__all__processor")

# Constants
CONTIGUOUS_GROUP_GAP_THRESHOLD = 5  # Max line gap for grouping __all__ sections


# =============================================================================
# Data Structures
# =============================================================================


@dataclass
class DunderAllSection:
    """Represents an __all__ section in the file."""

    section_type: str
    names: list[str]
    lineno: int
    is_complex: bool = False  # True for expressions like module.__all__


@dataclass
class ImportBlock:
    """Represents a block of consecutive import statements."""
    
    names: list[str]
    start_line: int
    end_line: int


@dataclass 
class ContiguousGroup:
    """Represents a contiguous group of __all__ sections."""
    
    sections: list[DunderAllSection]
    start_line: int
    end_line: int


class DunderAllProcessor:
    """Processor for checking and fixing __all__ sections in Python files."""

    # =============================================================================
    # Initialization & File Loading
    # =============================================================================

    def __init__(self, file_path: Path):
        self.file_path = file_path
        self.content = ""
        self.lines = []
        self.tree = None
        self.import_blocks = []
        self.dunder_all_sections = []
        self.contiguous_groups = []
        self.first_group = None
        self._load_and_parse()

    def _load_and_parse(self):
        """Load file once and parse all needed information."""
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                self.lines = f.readlines()
                self.content = "".join(self.lines)

            self.tree = ast.parse(self.content)
            self._parse_dunder_all_sections()
            self._find_contiguous_groups()
            self._parse_import_blocks()
        except (SyntaxError, UnicodeDecodeError, OSError) as error:
            LOGGER.error("Error loading %s: %s", self.file_path, error)

    # =============================================================================
    # AST Parsing Methods
    # =============================================================================

    def _parse_dunder_all_sections(self):
        """Extract all __all__ sections from the parsed AST."""
        if not self.tree:
            return

        for node in self.tree.body:
            section_type = None
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id == "__all__":
                        section_type = "assign"
                        break
            elif isinstance(node, ast.AugAssign):
                if isinstance(node.target, ast.Name) and node.target.id == "__all__":
                    section_type = "augassign"

            if section_type:
                if isinstance(node.value, ast.List):
                    # Simple list of strings
                    names = []
                    for elt in node.value.elts:
                        if isinstance(elt, ast.Constant) and isinstance(elt.value, str):
                            names.append(elt.value)
                    self.dunder_all_sections.append(
                        DunderAllSection(section_type, names, node.lineno, is_complex=False)
                    )
                else:
                    # Complex expression like module.__all__
                    self.dunder_all_sections.append(
                        DunderAllSection(section_type, [], node.lineno, is_complex=True)
                    )

    def _find_contiguous_groups(self):
        """Find contiguous groups of __all__ sections using line distance analysis."""
        if not self.dunder_all_sections:
            return
        
        # Sort sections by line number
        sorted_sections = sorted(self.dunder_all_sections, key=lambda s: s.lineno)
        
        # Group sections by line distance (gap analysis)
        groups = []
        current_group = [sorted_sections[0]]
        
        for i in range(1, len(sorted_sections)):
            prev_section = sorted_sections[i - 1]
            curr_section = sorted_sections[i]
            
            # Calculate gap by finding the actual end line of the previous section
            prev_end_line = self._find_section_end_line(self.lines, prev_section.lineno - 1)
            line_gap = curr_section.lineno - prev_end_line - 1
            
            # If gap is more than threshold non-__all__ lines, start a new group
            if line_gap > CONTIGUOUS_GROUP_GAP_THRESHOLD:
                # Finalize current group
                groups.append(ContiguousGroup(
                    sections=current_group,
                    start_line=current_group[0].lineno,
                    end_line=self._find_section_end_line(self.lines, current_group[-1].lineno - 1)
                ))
                current_group = [curr_section]
            else:
                current_group.append(curr_section)
        
        # Add the final group
        if current_group:
            groups.append(ContiguousGroup(
                sections=current_group,
                start_line=current_group[0].lineno,
                end_line=self._find_section_end_line(self.lines, current_group[-1].lineno - 1)
            ))
        
        self.contiguous_groups = groups
        self.first_group = groups[0] if groups else None
        
        LOGGER.info(f"  📊 Found {len(groups)} contiguous __all__ groups")
        if self.first_group:
            LOGGER.info(f"    First group: {len(self.first_group.sections)} sections (lines {self.first_group.start_line}-{self.first_group.end_line})")
    
    def _parse_import_blocks(self):
        """Parse individual import statements as separate blocks."""
        if not self.tree or not self.first_group:
            return
        
        # Parse imports up to the start of the first __all__ group
        import_cutoff_line = self.first_group.start_line
        
        # Create one block per import statement
        for node in self.tree.body:
            if node.lineno >= import_cutoff_line:
                break
            
            if isinstance(node, (ast.Import, ast.ImportFrom)) and node.names:
                # Handle both regular imports and module imports
                if isinstance(node, ast.ImportFrom) and node.level > 0:
                    # Check if this is a module import (from . import module)
                    if (node.module is None and len(node.names) == 1 and 
                        node.names[0].name and not node.names[0].asname):
                        # This is a module import like "from . import datasets"
                        module_name = node.names[0].name
                        # Create a special block for module imports
                        self.import_blocks.append(ImportBlock(
                            names=[f"_MODULE_{module_name}"],  # Special marker for module imports
                            start_line=node.lineno,
                            end_line=node.lineno
                        ))
                    else:
                        # Regular import with specific names
                        import_names = self._extract_import_names(node)
                        if import_names:
                            self.import_blocks.append(ImportBlock(
                                names=import_names,
                                start_line=node.lineno,
                                end_line=node.lineno
                            ))
        
        LOGGER.info(f"  📦 Found {len(self.import_blocks)} import blocks")
        for i, block in enumerate(self.import_blocks):
            if block.names and block.names[0].startswith("_MODULE_"):
                module_name = block.names[0][8:]  # Remove "_MODULE_" prefix
                LOGGER.info(f"    Block {i+1}: module import '{module_name}'")
            else:
                LOGGER.info(f"    Block {i+1}: {len(block.names)} names ({', '.join(block.names[:3])}{'...' if len(block.names) > 3 else ''})")
    
    def _extract_import_names(self, node: ast.stmt) -> list[str]:
        """Extract importable names from relative import nodes only."""
        names = []
        
        if isinstance(node, ast.ImportFrom):
            # Only process relative imports (level > 0 indicates relative import)
            if not node.level or node.level == 0:
                return names
            
            for alias in node.names:
                if not alias.name or alias.name == '*':
                    continue
                name = alias.asname or alias.name
                if not name.startswith("_"):
                    names.append(name)
                    
        # Skip all regular ast.Import nodes as they are not relative imports
        
        return names

    # =============================================================================
    # Public Interface Methods
    # =============================================================================

    def validate(self) -> bool:
        """Check if __all__ structure needs reconstruction."""
        if not self.first_group:
            LOGGER.info("  ✅ No contiguous __all__ groups found")

            return True

        if not self.import_blocks:
            LOGGER.info("  ✅ No import blocks found")

            return True

        # Always trigger reconstruction to ensure sections match import order
        LOGGER.warning("  ❌ __all__ structure needs reconstruction based on import block mapping")

        return False

    def fix(self, dry_run: bool = False) -> bool:
        """Reconstruct __all__ structure using import block mapping."""
        mode = "[DRY RUN] " if dry_run else ""
        LOGGER.info("%sReconstructing __all__ structure for %s", mode, self.file_path)

        if not self.first_group:
            LOGGER.info("  ✅ No contiguous __all__ groups found")

            return True

        if not self.import_blocks:
            LOGGER.info("  ✅ No import blocks found")

            return True

        # Reconstruct the __all__ structure
        new_all_lines = self._reconstruct_all_structure()
        
        if dry_run:
            LOGGER.info("  📋 Would reconstruct first contiguous group:")
            for line in new_all_lines:
                LOGGER.info(f"    {line.rstrip()}")

            return True

        # Replace the first contiguous group with reconstructed structure
        return self._replace_contiguous_group(new_all_lines)
    
    def _reconstruct_all_structure(self) -> list[str]:
        """Reconstruct __all__ structure based on import block order."""
        lines = []
        first_section_written = False
        
        # Process import blocks in order, handling module imports specially
        for i, import_block in enumerate(self.import_blocks):
            if not import_block.names:
                continue
            
            # Check if this is a module import
            if import_block.names[0].startswith("_MODULE_"):
                module_name = import_block.names[0][8:]  # Remove "_MODULE_" prefix
                
                # Create a simple module reference
                operator = "=" if not first_section_written else "+="
                lines.append(f"__all__ {operator} {module_name}.__all__\n")
                first_section_written = True
            else:
                # Regular import block - generate section directly from import block
                operator = "=" if not first_section_written else "+="
                first_section_written = True
                
                lines.append(f"__all__ {operator} [\n")
                for name in import_block.names:
                    lines.append(f'    "{name}",\n')
                lines.append("]\n")
        
        return lines
    
    def _replace_contiguous_group(self, new_lines: list[str]) -> bool:
        """Replace the first contiguous group with new content."""
        if not self.first_group:
            return False
        
        # Find the exact boundaries of the first contiguous group
        start_line = self.first_group.start_line - 1  # Convert to 0-based
        
        # Find the end of the last section in the group
        last_section = max(self.first_group.sections, key=lambda s: s.lineno)
        end_line = self._find_section_end_line(self.lines, last_section.lineno - 1)
        
        LOGGER.info(f"  🔧 Replacing lines {start_line + 1}-{end_line + 1} with {len(new_lines)} new lines")
        
        # Replace the range
        updated_lines = self.lines.copy()
        updated_lines[start_line:end_line + 1] = new_lines
        
        # Write the updated file
        return _write_file_safely(self.file_path, updated_lines, 1)

    # =============================================================================
    # Utility Methods
    # =============================================================================

    def _find_section_end_line(self, lines: list[str], start_line: int) -> int:
        """Find the end line of an __all__ section using AST approach with fallbacks."""
        try:
            # Try AST approach first
            for node in self.tree.body:
                if (
                    isinstance(node, (ast.Assign, ast.AugAssign))
                    and node.lineno == start_line + 1
                ):
                    if isinstance(node.value, ast.List) and hasattr(
                        node.value, "end_lineno"
                    ):
                        if node.value.end_lineno is not None:
                            return node.value.end_lineno - 1
                    break

            # Fallback: count brackets manually
            bracket_count = 0
            for i in range(start_line, len(lines)):
                for char in lines[i]:
                    if char == "[":
                        bracket_count += 1
                    elif char == "]":
                        bracket_count -= 1
                        if bracket_count == 0:
                            return i
        except Exception:
            # Ultra-safe fallback: only replace the start line
            return start_line

        # If brackets never closed, fallback to start line
        return start_line


# =============================================================================
# File I/O Functions
# =============================================================================


def _write_file_safely(
    file_path: Path, updated_lines: list[str], fixes_made: int
) -> bool:
    """Write file content atomically to prevent corruption."""

    try:
        temp_fd, temp_path_str = tempfile.mkstemp(
            suffix=".tmp", prefix=f"{file_path.name}.", dir=file_path.parent
        )
        temp_path = Path(temp_path_str)

        try:
            # Write to temporary file
            with os.fdopen(temp_fd, "w", encoding="utf-8") as temp_file:
                temp_file.writelines(updated_lines)

            # Validate the temporary file
            try:
                with open(temp_path, "r", encoding="utf-8") as f:
                    test_content = f.read()
                ast.parse(test_content)
            except (SyntaxError, UnicodeDecodeError) as error:
                temp_path.unlink()
                LOGGER.error("Generated invalid Python for %s: %s", file_path, error)

                return False

            # Atomically replace original file
            shutil.move(str(temp_path), file_path)
            LOGGER.info("  ✅ Applied %d fixes to %s", fixes_made, file_path)

            return True

        except Exception as error:
            # Clean up temp file on any error
            with contextlib.suppress(OSError):
                temp_path.unlink()
            raise error

    except (OSError, PermissionError) as error:
        LOGGER.error("Failed to write fixes to %s: %s", file_path, error)

        return False
    except Exception as error:
        LOGGER.error("Unexpected error writing fixes to %s: %s", file_path, error)

        return False


# =============================================================================
# Utility Functions
# =============================================================================


def _setup_logging(
    log_file: Path = Path(".sandbox/__all__processor.log"),
) -> None:
    """Setup logging configuration for the script."""

    log_file.parent.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)33s - %(levelname)8s - %(message)s",
        handlers=[
            logging.FileHandler(log_file, mode="w"),
            logging.StreamHandler(sys.stdout),
        ],
    )


def _find_python_files(
    paths: tuple[Path, ...], file_pattern: Optional[str] = None
) -> list[Path]:
    """Find all python files in the given paths, optionally filtered by pattern."""

    found_files = set()
    pattern = file_pattern or "**/__init__.py"

    for path in paths:
        if path.is_dir():
            for py_file in path.rglob("*.py"):
                if fnmatch.fnmatch(str(py_file), pattern):
                    found_files.add(py_file)
        elif path.is_file():
            if path.name.endswith(".py") and fnmatch.fnmatch(str(path), pattern):
                found_files.add(path)

    return sorted(found_files)


# =============================================================================
# Main Entry Point
# =============================================================================


@click.command()
@click.argument("paths", nargs=-1, type=click.Path(exists=True, path_type=Path))
@click.option(
    "--file-pattern",
    type=str,
    help='File pattern matching (default: "**/__init__.py")',
)
@click.option(
    "--dry-run",
    is_flag=True,
    default=False,
    help="Preview changes without applying them (default: apply changes)",
)
def main(
    paths: tuple[Path, ...],
    file_pattern: Optional[str],
    dry_run: bool,
):
    """
    __all__ Section Processor

    Verify and fix __all__ sections to match the actual import order (not alphabetical
    order) in Python modules. This ensures proper API consistency across the
    colour-science project.

    The script ensures that __all__ sections are grouped and ordered to match
    their corresponding import blocks.

    Examples:

        # Check all __init__.py files in a directory (dry run)
        uv run __all__processor.py colour/ --dry-run

        # Fix all __all__init__.py files in a directory
        uv run __all__processor.py colour/

        # Check specific files
        uv run __all__processor.py colour/utilities/__init__.py --dry-run

        # Fix issues in specific files
        uv run __all__processor.py colour/utilities/__init__.py

        # Use custom file pattern
        uv run __all__processor.py colour/ --file-pattern "colour/models/**/__init__.py"
    """

    _setup_logging()

    if not paths:
        LOGGER.error("Must specify at least one path")
        sys.exit(1)

    files_to_process = _find_python_files(paths, file_pattern)
    if not files_to_process:
        pattern_str = file_pattern or "**/__init__.py"
        LOGGER.warning("No python files found matching pattern: %s", pattern_str)
        sys.exit(0)

    if dry_run:
        mode_str = "🔍 DRY RUN MODE"
        operation = "Checking"
    else:
        mode_str = "🔧 FIX MODE"
        operation = "Fixing"

    LOGGER.info(
        "%s: %s __all__ sections for import order consistency",
        mode_str,
        operation,
    )
    LOGGER.info("=" * 79)
    LOGGER.info("Files to process: %d", len(files_to_process))
    LOGGER.info("")

    files_with_issues = 0

    for file_path in files_to_process:
        processor = DunderAllProcessor(file_path)

        if dry_run:
            LOGGER.info("Checking %s", file_path)
            is_correct = processor.validate()
            if not is_correct:
                files_with_issues += 1
                processor.fix(dry_run=True)
        else:
            processor.fix(dry_run=False)

        LOGGER.info("")

    LOGGER.info("=" * 79)
    LOGGER.info("Files processed: %d", len(files_to_process))

    if dry_run:
        LOGGER.info("Files with import order issues: %d", files_with_issues)
        LOGGER.info(
            "Files correctly ordered: %d", len(files_to_process) - files_with_issues
        )

        if files_with_issues == 0:
            LOGGER.info("✅ All __all__ sections match import order!")
        else:
            LOGGER.warning("❌ Some __all__ sections do not match import order")
            LOGGER.info("Run without --dry-run to fix these issues.")
    else:
        LOGGER.info("✅ Fix operation completed!")

    LOGGER.info("=" * 79)


if __name__ == "__main__":
    main()
