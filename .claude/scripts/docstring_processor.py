# /// script
# dependencies = [
#   "aiofiles",
#   "click",
# ]
# requires-python = ">=3.10"
# ///

"""
Reusable Docstring Processing Script with Multi-LLM Support

A flexible, single-file Python script that can process docstrings using various
LLM tools (Claude CLI via `claude -p`, Gemini CLI via `gemini -p`). Supports parallel
processing and works across all colour-science repositories.
"""

import ast
import asyncio
import fnmatch
import logging
import re
import signal
import subprocess
import sys
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Optional, Union

import aiofiles
import click

# ==============================================================================
# CONFIGURATION
# ==============================================================================


@dataclass
class ProcessingConfig:
    """Configuration settings for docstring processing."""

    # File and logging settings
    log_file: Path = Path(".sandbox/docstring_processor.log")
    timeout: float = 180.0

    # Retry configuration
    max_retries: int = 4
    retry_delay: float = 5.0  # seconds
    retry_backoff_factor: float = 3.0

    # Formatting settings
    line_length: int = 79
    indentation: str = "    "
    single_line_threshold: int = 60

    # Context extraction settings
    module_context_lines: int = 20
    max_context_lines: int = 10
    class_context_before: int = 5
    class_context_after: int = 10
    function_context_before: int = 3
    function_context_after: int = 5


# Module-level logger
LOGGER = logging.getLogger(__name__)

# ==============================================================================
# UTILITY FUNCTIONS
# ==============================================================================


def setup_logging(log_file: Optional[Path] = None) -> logging.Logger:
    """Setup logging configuration."""
    if log_file is None:
        log_file = ProcessingConfig.log_file

    log_file.parent.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(name)33s - %(levelname)8s - %(message)s",
        handlers=[
            logging.FileHandler(log_file, mode="w"),
            logging.StreamHandler(sys.stdout),
        ],
    )

    return LOGGER


# ==============================================================================
# DATA STRUCTURES
# ==============================================================================


class DocstringType(Enum):
    """Enumeration of all docstring types."""

    MODULE = "module"
    CLASS = "class"
    METHOD = "method"
    FUNCTION = "function"
    PROPERTY = "property"
    CLASS_ATTRIBUTE = "class_attribute"
    MODULE_ATTRIBUTE = "module_attribute"
    CONSTANT = "constant"
    ASYNC_FUNCTION = "async_function"
    ASYNC_METHOD = "async_method"
    STATICMETHOD = "staticmethod"
    CLASSMETHOD = "classmethod"
    NESTED_FUNCTION = "nested_function"


@dataclass
class DocstringObject:
    """Container for a Python object's docstring and its context."""

    type: DocstringType
    name: str
    content: str
    line_start: int
    line_end: int
    code_context: str
    parent_context: Optional[str] = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class ProcessingResult:
    """Result of processing a single docstring."""

    original: str
    improved: str
    validation_status: str
    metrics: dict[str, Any] = field(default_factory=dict)
    tool_used: str = ""


# ==============================================================================
# PROMPT TEMPLATES
# ==============================================================================

# Core instruction templates
INSTRUCTION_MAIN = """
You are helping improve Python docstrings for scientific clarity and precision.

ENHANCEMENT PRIORITIES (in order of importance):
1. **Scientific Clarity**: Improve accuracy, precision, and comprehensibility of existing content
2. **Content Preservation**: Maintain all existing information while improving its presentation
3. **Imperative Mood**: Use imperative mood consistently (e.g., "Generate" not "Generates")
4. **Terminology Consistency**: Replace "given" with "specified", standardize scientific terms
5. **Professional Structure**: Enhance organization and readability

CRITICAL PRESERVATION RULES (NEVER VIOLATE):
- **PRESERVE ALL INFORMATION**: Do NOT remove any existing information, explanations, or factual content
- **PRESERVE EXAMPLES**: Do not modify any Examples sections or code blocks
- **PRESERVE REFERENCES**: Maintain all citation references and bibliography entries
- **PRESERVE RST MARKERS**: Keep :math:, :param:, :attr:, etc. functional
- **PRESERVE BRITISH SPELLING**: Maintain "colour", "colourspace", etc.
- **PRESERVE MEANING**: Enhance rather than change the fundamental meaning
- **PRESERVE EMPHASIS**: Keep *emphasis markers* around important terms intact

ENHANCEMENT GUIDELINES:
- **IMPROVE CLARITY**: Enhance readability and comprehensibility of existing text
- **IMPROVE TERMINOLOGY**: Use more precise scientific language where appropriate
- **IMPROVE STRUCTURE**: Better organize existing content for readability
- **IMPROVE CONSISTENCY**: Standardize formatting and terminology
- **NO CONTENT MIGRATION**: NEVER include content from other functions/classes
- **NO REDUNDANCY**: Don't repeat information already clear from context

CONTEXT-SPECIFIC RULES:
- **For Constants**: If existing docstring is single-line, keep it single-line; if multi-line, preserve all content
- **For Functions**: Preserve all existing sections (Parameters, Returns, Notes, Examples, References)
- **For Classes**: Maintain all existing structure and content

DOMAIN CONTEXT: This is a colour science library requiring professional scientific documentation.
"""

INSTRUCTION_FORMATTING_MULTI_LINE = """FORMATTING CONSTRAINTS:
- **LINE LENGTH**: Wrap lines at EXACTLY {computed_line_length} characters maximum. The {indentation_spaces} spaces of indentation have already been accounted for in this limit.
- **EMPHASIS**: Preserve *emphasis markers* around important terms
- **NO INDENTATION**: Do NOT add any indentation - start all lines at the beginning with no spaces
- **STRUCTURE**: Maintain consistent formatting and proper line breaks
- **EXAMPLES**: Preserve Examples sections exactly as they are - do not modify code blocks
- **LINE BREAKS**: Use the full {computed_line_length} character width when wrapping text - do not leave lines unnecessarily short"""

INSTRUCTION_FORMATTING_SINGLE_LINE = """FORMATTING CONSTRAINTS:
- **LINE LENGTH**: Single line only, max {computed_line_length} characters (indentation already accounted for)
- **EMPHASIS**: Preserve *emphasis markers* around important terms
- **NO INDENTATION**: Do NOT add any indentation - start all lines at the beginning with no spaces"""

# Docstring type-specific prompt templates
TYPE_PROMPTS = {
    "function": """
{instruction_base}

{instruction_formatting_multi_line}

FUNCTION TO IMPROVE:
{docstring_object.code_context}

Current docstring:
{docstring_object.content}

Please return ONLY the improved docstring. Keep improvements focused, concise, and appropriately sized.
Ensure all lines respect the {computed_line_length}-character limit.
""",
    "constant": """
{instruction_base}

{instruction_formatting_single_line}

CONSTANT TO DOCUMENT:
{docstring_object.code_context}

Current docstring:
{docstring_object.content}

REMEMBER: Constants get 1 LINE ONLY. Return a single-line docstring describing the constant's purpose.
""",
    "class": """
{instruction_base}

{instruction_formatting_multi_line}

CLASS TO IMPROVE:
{docstring_object.code_context}

Current docstring:
{docstring_object.content}

Please return ONLY the improved docstring. Focus on the class purpose and key functionality.
Ensure all lines respect the {computed_line_length}-character limit.
""",
    "method": """
{instruction_base}

{instruction_formatting_multi_line}

Parent class: {docstring_object.parent_context}

METHOD TO IMPROVE:
{docstring_object.code_context}

Current docstring:
{docstring_object.content}

Please return ONLY the improved docstring. Keep it concise and relevant to the method's role.
Ensure all lines respect the {computed_line_length}-character limit.
""",
    "property": """
{instruction_base}

{instruction_formatting_multi_line}

PROPERTY TO IMPROVE:
{docstring_object.code_context}

Current docstring:
{docstring_object.content}

Please return ONLY the improved docstring. Focus on what the property represents/returns.
Ensure all lines respect the {computed_line_length}-character limit.
""",
    "module": """
{instruction_base}

{instruction_formatting_multi_line}

MODULE TO IMPROVE:
{docstring_object.code_context}

Current docstring:
{docstring_object.content}

Please return ONLY the improved module-level docstring. Describe the module's purpose and key components.
Ensure all lines respect the {computed_line_length}-character limit.
""",
    "class_attribute": """
{instruction_base}

{instruction_formatting_multi_line}

CLASS ATTRIBUTE TO DOCUMENT:
Parent class: {docstring_object.parent_context}

{docstring_object.code_context}

Current docstring:
{docstring_object.content}

REMEMBER: Class attributes typically get brief descriptions. Return a concise docstring.
Ensure all lines respect the {computed_line_length}-character limit.
""",
    "module_attribute": """
{instruction_base}

{instruction_formatting_multi_line}

MODULE ATTRIBUTE TO DOCUMENT:
{docstring_object.code_context}

Current docstring:
{docstring_object.content}

Return a concise docstring describing this module-level attribute.
Ensure all lines respect the {computed_line_length}-character limit.
""",
}

# Add mappings for specialized types (async, static, etc.)
TYPE_PROMPTS.update(
    {
        "async_function": TYPE_PROMPTS["function"],
        "async_method": TYPE_PROMPTS["method"],
        "staticmethod": TYPE_PROMPTS["method"],
        "classmethod": TYPE_PROMPTS["method"],
        "nested_function": TYPE_PROMPTS["function"],
    }
)


# ==============================================================================
# CORE CLASSES
# ==============================================================================


class AsyncLLMProcessor:
    """Base processor for CLI tools using text blocks format."""

    def __init__(self, tool_name: str, cli_command: str):
        self.tool_name = tool_name
        self.cli_command = cli_command
        self.logger = logging.getLogger("%s.%s" % (__name__, self.__class__.__name__))

    async def _run_subprocess_with_timeout(
        self, command: list[str], timeout: float = None
    ) -> tuple[bytes, bytes]:
        """Run subprocess with timeout and proper cleanup."""
        if timeout is None:
            timeout = ProcessingConfig.timeout

        process = await asyncio.create_subprocess_exec(
            *command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        try:
            stdout, stderr = await asyncio.wait_for(
                process.communicate(), timeout=timeout
            )
        except asyncio.TimeoutError:
            # Graceful termination first
            process.terminate()
            try:
                await asyncio.wait_for(process.wait(), timeout=5.0)
            except asyncio.TimeoutError:
                # Force kill if termination doesn't work
                try:
                    process.kill()
                    await asyncio.wait_for(process.wait(), timeout=5.0)
                except (OSError, asyncio.TimeoutError):
                    # Process might already be dead
                    pass
            raise Exception(
                f"CLI process '{' '.join(command)}' timed out after {timeout} seconds"
            )

        if process.returncode != 0:
            stderr_str = stderr.decode()
            stdout_str = stdout.decode()
            raise Exception(
                f"CLI command '{' '.join(command)}' failed with returncode {process.returncode}: "
                f"stderr='{stderr_str}', stdout='{stdout_str}'"
            )

        return stdout, stderr

    def _build_prompt(
        self, docstring_object: DocstringObject, indentation: str = ""
    ) -> str:
        """Build prompt for the given docstring object."""
        indentation_spaces = len(indentation)
        computed_line_length = ProcessingConfig.line_length - indentation_spaces
        type_template = TYPE_PROMPTS[docstring_object.type.value]
        return type_template.format(
            instruction_base=INSTRUCTION_MAIN,
            instruction_formatting_multi_line=INSTRUCTION_FORMATTING_MULTI_LINE,
            instruction_formatting_single_line=INSTRUCTION_FORMATTING_SINGLE_LINE,
            docstring_object=docstring_object,
            indentation_spaces=indentation_spaces,
            computed_line_length=computed_line_length,
        )

    async def process_docstring(
        self, docstring_object: DocstringObject
    ) -> ProcessingResult:
        """Process docstring using CLI with text blocks output and retry logic."""

        object_name = docstring_object.name
        self.logger.info(
            "[%s] Starting %s CLI processing",
            object_name,
            self.tool_name,
        )

        # Detect docstring indentation
        if docstring_object.type == DocstringType.MODULE:
            indentation = ""
        elif docstring_object.code_context:
            indentation = ProcessingConfig.indentation
            lines = docstring_object.code_context.split("\n")
            for line in lines:
                stripped = line.strip()
                if stripped.startswith(("def ", "class ", "async def ")):
                    base_indentation = line[: len(line) - len(line.lstrip())]
                    indentation = base_indentation + ProcessingConfig.indentation
                    break
        else:
            indentation = ProcessingConfig.indentation

        prompt = f"""
{self._build_prompt(docstring_object, indentation)}

Please respond with the improved docstring in a reStructuredText code block, followed by a brief explanation.

Format your response exactly like this:

Improved Docstring

```reStructuredText
your improved docstring content here
```

Explanation

```text
brief explanation of the changes made
```

IMPORTANT: The docstring content should NOT include triple quotes - just the raw docstring text.
Use proper LaTeX math notation inside :math:`...` with double-escaped backslashes like ":math:`\\\\\\\\lambda`".
"""

        self.logger.debug(
            "[%s] Prompt created, length: %s chars",
            object_name,
            len(prompt),
        )

        # Retry logic with exponential backoff
        last_error = None
        for attempt in range(ProcessingConfig.max_retries + 1):
            try:
                if attempt > 0:
                    delay = ProcessingConfig.retry_delay * (
                        ProcessingConfig.retry_backoff_factor ** (attempt - 1)
                    )
                    self.logger.info(
                        "[%s] Retry attempt %s/%s after %.1fs delay",
                        object_name,
                        attempt,
                        ProcessingConfig.max_retries,
                        delay,
                    )
                    await asyncio.sleep(delay)

                self.logger.debug(
                    "[%s] Starting %s CLI subprocess...",
                    object_name,
                    self.tool_name,
                )
                command = [self.cli_command, "-p", prompt]
                stdout, stderr = await self._run_subprocess_with_timeout(command)

                stdout_str = stdout.decode()
                stderr_str = stderr.decode()

                self.logger.debug(
                    "[%s] Subprocess stdout length: %s chars",
                    object_name,
                    len(stdout_str),
                )
                if stderr_str:
                    self.logger.debug(
                        "[%s] Subprocess stderr: %s",
                        object_name,
                        stderr_str,
                    )

                # Log raw response content for debugging (truncated if too long)
                if len(stdout_str) <= 200:
                    self.logger.debug(
                        "[%s] Raw stdout: %r",
                        object_name,
                        stdout_str,
                    )
                else:
                    self.logger.debug(
                        "[%s] Raw stdout (first 200 chars): %r",
                        object_name,
                        stdout_str[:200],
                    )

                self.logger.debug("[%s] Parsing text response...", object_name)
                try:
                    improved_docstring, explanation = (
                        self._extract_docstring_from_response(stdout_str, object_name)
                    )

                    self.logger.debug(
                        "[%s] Successfully parsed text response",
                        object_name,
                    )
                    self.logger.info(
                        "[%s] Improved docstring length: %s chars",
                        object_name,
                        len(improved_docstring),
                    )

                    if attempt > 0:
                        self.logger.info(
                            "[%s] Success on retry attempt %s",
                            object_name,
                            attempt,
                        )

                    return ProcessingResult(
                        original=docstring_object.content,
                        improved=improved_docstring,
                        validation_status="success",
                        tool_used=self.tool_name,
                        metrics={
                            "response_length": len(improved_docstring),
                            "explanation": explanation,
                            "attempts": attempt + 1,
                        },
                    )
                except (ValueError, KeyError) as parse_error:
                    # Parse errors are less likely to succeed on retry, but give it one more chance
                    if attempt < ProcessingConfig.max_retries:
                        self.logger.warning(
                            "[%s] Parse error on attempt %s: %s",
                            object_name,
                            attempt + 1,
                            str(parse_error),
                        )
                        last_error = parse_error
                        continue
                    else:
                        self.logger.error(
                            "[%s] Failed to parse response after %s attempts: %s",
                            object_name,
                            attempt + 1,
                            str(parse_error),
                        )
                        return ProcessingResult(
                            original=docstring_object.content,
                            improved=docstring_object.content,
                            validation_status=f"parse_error: {str(parse_error)}",
                            tool_used=self.tool_name,
                            metrics={"attempts": attempt + 1},
                        )

            except Exception as error:
                # Network/subprocess errors are more likely to succeed on retry
                if attempt < ProcessingConfig.max_retries:
                    self.logger.warning(
                        "[%s] Error on attempt %s: %s",
                        object_name,
                        attempt + 1,
                        str(error),
                    )
                    last_error = error
                    continue
                else:
                    self.logger.error(
                        "[%s] Failed after %s attempts: %s",
                        object_name,
                        attempt + 1,
                        str(error),
                    )
                    return ProcessingResult(
                        original=docstring_object.content,
                        improved=docstring_object.content,
                        validation_status=f"error: {str(error)}",
                        tool_used=self.tool_name,
                        metrics={"attempts": attempt + 1},
                    )

        # Should never reach here, but fallback just in case
        return ProcessingResult(
            original=docstring_object.content,
            improved=docstring_object.content,
            validation_status=f"error: {str(last_error) if last_error else 'Unknown error'}",
            tool_used=self.tool_name,
            metrics={"attempts": ProcessingConfig.max_retries + 1},
        )

    def _extract_docstring_from_response(
        self, raw_response: str, object_name: str
    ) -> tuple[str, str]:
        """Extract improved docstring and explanation from CLI text response.

        Args:
            raw_response: Raw stdout from CLI with text blocks format
            object_name: Name of the object being processed for logging

        Returns:
            tuple of (improved_docstring, explanation)

        Raises:
            ValueError: If text block parsing fails
        """
        self.logger.debug(
            "[%s] Raw response length: %s chars",
            object_name,
            len(raw_response),
        )

        # Extract reStructuredText block
        docstring_match = re.search(
            r"```reStructuredText\s*\n(.*?)\n```", raw_response, re.DOTALL
        )
        if not docstring_match:
            # Log response content for debugging parse failures
            preview = raw_response[:500] if len(raw_response) > 500 else raw_response
            self.logger.debug(
                "[%s] Parse failure - response: %r",
                object_name,
                preview,
            )
            raise ValueError("Could not find reStructuredText block in response")

        improved_docstring = docstring_match.group(1).strip()

        # Extract explanation block
        explanation_match = re.search(
            r"```text\s*\n(.*?)\n```", raw_response, re.DOTALL
        )
        explanation = explanation_match.group(1).strip() if explanation_match else ""

        self.logger.debug(
            "[%s] Extracted docstring length: %s chars",
            object_name,
            len(improved_docstring),
        )

        return improved_docstring, explanation


class AsyncClaudeCodeProcessor(AsyncLLMProcessor):
    """Claude Code processor using CLI subprocess."""

    def __init__(self):
        super().__init__(tool_name="claude_cli", cli_command="claude")


class AsyncGeminiCLIProcessor(AsyncLLMProcessor):
    """Gemini processor using CLI subprocess."""

    def __init__(self):
        super().__init__(tool_name="gemini", cli_command="gemini")


# Available LLM processors
_PROCESSORS = {
    "claude": AsyncClaudeCodeProcessor,
    "gemini": AsyncGeminiCLIProcessor,
}


class AsyncDocstringProcessor:
    """Handles AST-based docstring extraction and replacement."""

    def __init__(self):
        self.logger = logging.getLogger("%s.%s" % (__name__, self.__class__.__name__))

    def _handle_file_error(
        self, error: Exception, operation: str, file_path: Path, context: str = ""
    ) -> None:
        """Standardized error handling for file operations."""
        if isinstance(error, (OSError, PermissionError)):
            self.logger.error(
                "Failed to %s file %s: %s", operation, file_path, str(error)
            )
        elif isinstance(error, UnicodeDecodeError):
            self.logger.error("File %s has encoding issues: %s", file_path, str(error))
        else:
            self.logger.error(
                "Unexpected error %s file %s: %s", operation, file_path, str(error)
            )

        if context:
            self.logger.debug("Context: %s", context)

    def extract_docstrings_from_file(self, file_path: Path) -> list[DocstringObject]:
        """Extract all docstrings from a Python file."""
        try:
            try:
                with open(file_path, "r", encoding="utf-8") as file_handle:
                    source = file_handle.read()
            except (OSError, PermissionError, UnicodeDecodeError) as error:
                self._handle_file_error(error, "read", file_path)
                return []

            try:
                tree = ast.parse(source)
            except SyntaxError as error:
                self.logger.error(
                    "Syntax error in file %s at line %s: %s",
                    file_path,
                    error.lineno,
                    str(error),
                )
                return []
            docstring_objects = []

            module_docstring = ast.get_docstring(tree)
            if module_docstring:
                # Extract module context (imports + first few lines)
                lines = source.split("\n")
                context_lines = []
                for line in lines[: ProcessingConfig.module_context_lines]:
                    if line.strip().startswith(("import ", "from ")):
                        context_lines.append(line)
                    elif line.strip() and not line.strip().startswith("#"):
                        context_lines.append(line)
                        if len(context_lines) >= ProcessingConfig.max_context_lines:
                            break
                module_context = "\n".join(context_lines)

                docstring_objects.append(
                    DocstringObject(
                        type=DocstringType.MODULE,
                        name=file_path.stem,
                        content=module_docstring,
                        line_start=1,
                        line_end=len(module_docstring.split("\n")),
                        code_context=module_context,
                    )
                )

            # Walk the tree to find functions, classes, and variable docstrings
            for node in ast.walk(tree):
                if isinstance(
                    node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)
                ):
                    docstring = ast.get_docstring(node)
                    if docstring:
                        docstring_object = self._create_docstring_object(
                            node, docstring, source
                        )
                        if docstring_object:
                            docstring_objects.append(docstring_object)

            # Find module-level variable docstrings (var.__doc__ = "...")
            lines = source.splitlines()
            for i, node in enumerate(tree.body):
                # Skip if not an assignment or not a __doc__ assignment
                if not isinstance(node, ast.Assign):
                    continue

                if not (
                    len(node.targets) == 1
                    and isinstance(node.targets[0], ast.Attribute)
                    and node.targets[0].attr == "__doc__"
                    and isinstance(node.targets[0].value, ast.Name)
                    and isinstance(node.value, ast.Constant)
                    and isinstance(node.value.value, str)
                ):
                    continue

                var_name = node.targets[0].value.id
                docstring = node.value.value

                # Find the variable definition by walking backwards
                var_def_node = None
                for j in range(i - 1, -1, -1):
                    # Handle both regular assignments and annotated assignments
                    if isinstance(tree.body[j], ast.Assign):
                        if any(
                            isinstance(t, ast.Name) and t.id == var_name
                            for t in tree.body[j].targets
                        ):
                            var_def_node = tree.body[j]
                            break
                    elif isinstance(tree.body[j], ast.AnnAssign):
                        if (
                            isinstance(tree.body[j].target, ast.Name)
                            and tree.body[j].target.id == var_name
                        ):
                            var_def_node = tree.body[j]
                            break

                if var_def_node:
                    # Extract context around variable definition
                    context_start = max(0, var_def_node.lineno - 3)
                    context_end = min(len(lines), node.end_lineno + 2)
                    code_context = "\n".join(lines[context_start:context_end])

                    docstring_objects.append(
                        DocstringObject(
                            type=DocstringType.MODULE_ATTRIBUTE,
                            name=var_name,
                            content=docstring,
                            line_start=node.lineno,
                            line_end=node.end_lineno or node.lineno,
                            code_context=code_context,
                        )
                    )

            return docstring_objects

        except Exception as error:
            self.logger.error("Unexpected error parsing %s: %s", file_path, str(error))
            return []

    def _create_docstring_object(
        self, node: ast.AST, docstring: str, source: str
    ) -> Optional[DocstringObject]:
        """Create DocstringObject from AST node."""
        if isinstance(node, ast.ClassDef):
            return DocstringObject(
                type=DocstringType.CLASS,
                name=node.name,
                content=docstring,
                line_start=node.lineno,
                line_end=node.lineno + len(docstring.split("\n")),
                code_context=self._get_class_context(node, source),
            )
        elif isinstance(node, ast.FunctionDef):
            func_type = self._classify_function(node)
            return DocstringObject(
                type=func_type,
                name=node.name,
                content=docstring,
                line_start=node.lineno,
                line_end=node.lineno + len(docstring.split("\n")),
                code_context=self._get_function_context(node, source),
            )
        elif isinstance(node, ast.AsyncFunctionDef):
            func_type = (
                DocstringType.ASYNC_METHOD
                if self._is_method(node)
                else DocstringType.ASYNC_FUNCTION
            )
            return DocstringObject(
                type=func_type,
                name=node.name,
                content=docstring,
                line_start=node.lineno,
                line_end=node.lineno + len(docstring.split("\n")),
                code_context=self._get_function_context(node, source),
            )

        return None

    def _classify_function(self, node: ast.FunctionDef) -> DocstringType:
        """Classify function type based on decorators and context."""
        for decorator in node.decorator_list:
            if isinstance(decorator, ast.Name):
                if decorator.id == "staticmethod":
                    return DocstringType.STATICMETHOD
                elif decorator.id == "classmethod":
                    return DocstringType.CLASSMETHOD
                elif decorator.id == "property":
                    return DocstringType.PROPERTY

        if self._is_method(node):
            return DocstringType.METHOD

        return DocstringType.FUNCTION

    def _is_method(self, node: Union[ast.FunctionDef, ast.AsyncFunctionDef]) -> bool:
        """Check if function is a method by examining first parameter."""
        if not node.args.args:
            return False
        # Methods typically have 'self' or 'cls' as first parameter
        first_param = node.args.args[0].arg
        return first_param in ("self", "cls")

    def _get_context_around_line(
        self, source: str, line_number: int, before: int, after: int
    ) -> str:
        """Extract context lines around a specific line number."""
        lines = source.split("\n")
        start_line = line_number - 1
        return "\n".join(
            lines[max(0, start_line - before) : min(len(lines), start_line + after)]
        )

    def _get_class_context(self, node: ast.ClassDef, source: str) -> str:
        """Extract class definition context."""
        return self._get_context_around_line(
            source,
            node.lineno,
            ProcessingConfig.class_context_before,
            ProcessingConfig.class_context_after,
        )

    def _get_function_context(
        self, node: Union[ast.FunctionDef, ast.AsyncFunctionDef], source: str
    ) -> str:
        """Extract function definition context."""
        return self._get_context_around_line(
            source,
            node.lineno,
            ProcessingConfig.function_context_before,
            ProcessingConfig.function_context_after,
        )

    async def replace_docstring_in_file(
        self, file_path: Path, docstring_object: DocstringObject, new_docstring: str
    ) -> bool:
        """
        Replace a docstring in a file, orchestrating the read, update, and write operations.
        """
        object_name = docstring_object.name
        self.logger.debug(
            "[%s] Starting replacement process in %s", object_name, file_path
        )

        read_result = await self._read_and_backup_file(file_path, object_name)
        if not read_result:
            return False  # Error already logged

        original_content, backup_path = read_result

        try:
            updated_content = self._replace_docstring_in_content(
                original_content, docstring_object, new_docstring
            )

            if updated_content is None:
                # Error occurred during content update, keep backup for investigation
                self.logger.warning(
                    "[%s] Content replacement failed, backup preserved at %s",
                    docstring_object.name,
                    backup_path,
                )
                return False

            if updated_content == original_content:
                self.logger.info(
                    "[%s] No changes made to content; skipping write.", object_name
                )
                if backup_path and backup_path.exists():
                    backup_path.unlink(missing_ok=True)
                return True

            write_success = await self._write_and_cleanup(
                file_path, updated_content, backup_path, object_name
            )

            if write_success:
                self.logger.info(
                    "[%s] Successfully replaced docstring in %s",
                    object_name,
                    file_path,
                )
            return write_success

        except Exception as error:
            self.logger.error(
                "[%s] Unhandled exception during docstring replacement in %s: %s",
                object_name,
                file_path,
                error,
            )
            # Ensure backup is cleaned up on unexpected error
            if backup_path and backup_path.exists():
                backup_path.unlink(missing_ok=True)
            return False

    async def _read_and_backup_file(
        self, file_path: Path, object_name: str
    ) -> Optional[tuple[str, Path]]:
        """Read file content and create a backup."""
        try:
            async with aiofiles.open(file_path, "r", encoding="utf-8") as file_handle:
                content = await file_handle.read()
        except (OSError, PermissionError, UnicodeDecodeError) as error:
            self._handle_file_error(error, "read", file_path, f"Context: {object_name}")
            return None

        backup_path = file_path.with_suffix(file_path.suffix + ".backup")
        try:
            async with aiofiles.open(backup_path, "w", encoding="utf-8") as file_handle:
                await file_handle.write(content)
            return content, backup_path
        except (OSError, PermissionError) as error:
            self._handle_file_error(
                error, "create backup", backup_path, f"Context: {object_name}"
            )
            return None

    def _replace_docstring_in_content(
        self,
        original_content: str,
        docstring_object: DocstringObject,
        new_docstring: str,
    ) -> Optional[str]:
        """Replace the docstring in the string content of a file."""
        object_name = docstring_object.name
        try:
            tree = ast.parse(original_content)
            lines = original_content.splitlines()

            docstring_location = self._find_docstring_location(tree, docstring_object)
            if not docstring_location:
                self.logger.error("[%s] Failed to locate docstring in AST", object_name)
                return None

            start_line, end_line, _, _ = docstring_location

            quote_style, indentation = self._detect_quote_style_and_indentation(
                lines[start_line]
            )

            self.logger.debug(
                "[%s] Detected indentation: '%s' (len: %s)",
                object_name,
                indentation,
                len(indentation),
            )

            # For module attributes, format as __doc__ assignment
            if docstring_object.type == DocstringType.MODULE_ATTRIBUTE:
                formatted_docstring_lines = []
                docstring_lines = new_docstring.split("\n")

                if len(docstring_lines) == 1:
                    # Single line: VAR.__doc__ = "content"
                    escaped_content = docstring_lines[0].replace('"', '\\"')
                    formatted_docstring_lines.append(
                        f"{indentation}{docstring_object.name}.__doc__ = {quote_style}{escaped_content}{quote_style}"
                    )
                else:
                    # Multi-line: VAR.__doc__ = """content"""
                    formatted_docstring_lines.append(
                        f"{indentation}{docstring_object.name}.__doc__ = {quote_style}"
                    )

                    for i, line in enumerate(docstring_lines):
                        if i == 0 and line.strip():
                            formatted_docstring_lines.append(f"{indentation}{line}")
                        elif line.strip():
                            formatted_docstring_lines.append(f"{indentation}{line}")
                        else:
                            formatted_docstring_lines.append("")

                    formatted_docstring_lines.append(f"{indentation}{quote_style}")
            else:
                formatted_docstring_lines = self._format_docstring(
                    new_docstring, quote_style, indentation
                )

            new_lines = (
                lines[:start_line] + formatted_docstring_lines + lines[end_line + 1 :]
            )
            return "\n".join(new_lines)

        except (SyntaxError, ValueError) as error:
            self.logger.error(
                "[%s] Error parsing or processing docstring content: %s",
                object_name,
                error,
            )
            return None

    async def _write_and_cleanup(
        self,
        file_path: Path,
        updated_content: str,
        backup_path: Path,
        object_name: str,
    ) -> bool:
        """Write updated content atomically and clean up backup file."""
        temporary_path = file_path.with_suffix(file_path.suffix + ".tmp")
        write_success = False
        restore_needed = False

        try:
            # Write to temporary file first
            async with aiofiles.open(
                temporary_path, "w", encoding="utf-8"
            ) as file_handle:
                await file_handle.write(updated_content)

            # Atomic move - this is the critical section
            temporary_path.replace(file_path)
            write_success = True

        except (OSError, PermissionError) as error:
            self._handle_file_error(
                error, "write updated", file_path, f"Context: {object_name}"
            )
            restore_needed = True

        finally:
            # Clean up temporary file if it still exists
            if temporary_path.exists():
                temporary_path.unlink(missing_ok=True)

        # Handle restoration if write failed
        if restore_needed:
            try:
                if backup_path.exists():
                    backup_path.replace(file_path)
                    self.logger.info(
                        "[%s] Restored original file from backup.", object_name
                    )
                else:
                    self.logger.error(
                        "[%s] CRITICAL: No backup file found for restoration of %s",
                        object_name,
                        file_path,
                    )
            except OSError as restore_error:
                self.logger.error(
                    "[%s] CRITICAL: Failed to restore backup for %s: %s",
                    object_name,
                    file_path,
                    restore_error,
                )
            return False

        # Clean up backup file on success
        if backup_path.exists():
            backup_path.unlink(missing_ok=True)

        return write_success

    def _find_docstring_location(
        self, tree: ast.AST, docstring_object: DocstringObject
    ) -> Optional[tuple[int, int, str, str]]:
        """Find the exact location of a docstring in the source code."""

        if docstring_object.type == DocstringType.MODULE:
            # Module docstring is the first statement if it's a string
            if isinstance(tree, ast.Module) and tree.body:
                first_stmt = tree.body[0]
                if (
                    isinstance(first_stmt, ast.Expr)
                    and isinstance(first_stmt.value, ast.Constant)
                    and isinstance(first_stmt.value.value, str)
                ):
                    return self._get_docstring_bounds(first_stmt.value)
            return None

        if docstring_object.type == DocstringType.MODULE_ATTRIBUTE:
            # For attributes, find the actual __doc__ assignment and locate the string content
            # We need to re-find the assignment node dynamically (don't rely on stored line numbers!)
            for node in ast.walk(tree):
                if (
                    isinstance(node, ast.Assign)
                    and len(node.targets) == 1
                    and isinstance(node.targets[0], ast.Attribute)
                    and node.targets[0].attr == "__doc__"
                    and isinstance(node.targets[0].value, ast.Name)
                    and node.targets[0].value.id == docstring_object.name
                    and isinstance(node.value, ast.Constant)
                    and isinstance(node.value.value, str)
                    and node.value.value.strip() == docstring_object.content.strip()
                ):
                    return self._get_docstring_bounds(node.value)
            return None

        # For functions, methods, and classes
        for node in ast.walk(tree):
            if hasattr(node, "name") and node.name == docstring_object.name:
                if isinstance(
                    node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)
                ):
                    docstring_node = self._get_docstring_node(node)
                    if docstring_node:
                        return self._get_docstring_bounds(docstring_node)

        return None

    def _get_docstring_node(self, node: ast.AST) -> Optional[ast.Constant]:
        """Get the docstring node from a function/class definition."""
        if hasattr(node, "body") and node.body:
            first_stmt = node.body[0]
            if isinstance(first_stmt, ast.Expr) and isinstance(
                first_stmt.value, ast.Constant
            ):
                if isinstance(first_stmt.value.value, str):
                    return first_stmt.value
        return None

    def _get_docstring_bounds(
        self, constant_node: ast.Constant
    ) -> tuple[int, int, str, str]:
        """Get the start and end line numbers of a docstring, plus quote style and indentation."""
        start_line = constant_node.lineno - 1
        end_line = constant_node.end_lineno - 1
        quote_style = '"""'
        indentation = ""

        return start_line, end_line, quote_style, indentation

    def _detect_quote_style_and_indentation(self, line: str) -> tuple[str, str]:
        """Detect the actual quote style and indentation from the source line."""
        indentation = line[: len(line) - len(line.lstrip())]
        stripped_line = line.strip()

        # Pattern to match string prefixes (r, u, f, b, etc.) followed by quotes
        # Handle combinations like rf, rb, etc.
        pattern = r'^([rRuUfFbB]*)("""|\'\'\'|"|\')'
        match = re.match(pattern, stripped_line)

        if match:
            prefix = match.group(1)
            quote_chars = match.group(2)

            # For docstrings, prefer triple quotes regardless of original
            if len(quote_chars) == 1:
                quote_style = '"""'  # Always use triple quotes for docstrings
            else:
                quote_style = quote_chars  # Keep existing triple quotes
        else:
            # Fallback to triple quotes
            quote_style = '"""'

        return quote_style, indentation

    def _format_docstring(
        self, docstring: str, quote_style: str, indentation: str
    ) -> list[str]:
        """Format a docstring with proper indentation and quotes."""
        lines = []

        docstring_lines = docstring.split("\n")
        while docstring_lines and not docstring_lines[0].strip():
            docstring_lines.pop(0)
        while docstring_lines and not docstring_lines[-1].strip():
            docstring_lines.pop()

        if not docstring_lines:
            lines.append(f"{indentation}{quote_style}{quote_style}")
            return lines

        if (
            len(docstring_lines) == 1
            and len(docstring_lines[0]) < ProcessingConfig.single_line_threshold
        ):
            lines.append(
                f"{indentation}{quote_style}{docstring_lines[0].strip()}{quote_style}"
            )
        else:
            lines.append(f"{indentation}{quote_style}")
            common_indent = self._detect_minimum_indentation(docstring_lines)
            for line in docstring_lines:
                if line.strip():
                    if line.startswith(common_indent):
                        relative_content = line[len(common_indent) :]
                        lines.append(f"{indentation}{relative_content}")
                    else:
                        lines.append(f"{indentation}{line.lstrip()}")
                else:
                    lines.append("")

            lines.append(f"{indentation}{quote_style}")

        return lines

    def _detect_minimum_indentation(self, lines: list[str]) -> str:
        """Detect the minimum indentation level of non-empty lines."""
        indentations = []
        for line in lines:
            if line.strip():
                indent_count = len(line) - len(line.lstrip())
                indentations.append(indent_count)

        if not indentations:
            return ""

        min_indent = min(indentations)
        return " " * min_indent


class AsyncFileProcessor:
    """Handles async file I/O operations."""

    def __init__(self):
        self.logger = logging.getLogger("%s.%s" % (__name__, self.__class__.__name__))

    def _handle_file_error(
        self, error: Exception, operation: str, file_path: Path, context: str = ""
    ) -> None:
        """Standardized error handling for file operations."""
        if isinstance(error, (OSError, PermissionError)):
            self.logger.error(
                "Failed to %s file %s: %s", operation, file_path, str(error)
            )
        elif isinstance(error, UnicodeDecodeError):
            self.logger.error("File %s has encoding issues: %s", file_path, str(error))
        else:
            self.logger.error(
                "Unexpected error %s file %s: %s", operation, file_path, str(error)
            )

        if context:
            self.logger.debug("Context: %s", context)

    async def find_python_files(
        self,
        paths: list[Path],
        file_pattern: Optional[str] = None,
    ) -> list[Path]:
        """Find Python files in given paths."""
        python_files = []

        for path in paths:
            if path.is_file() and path.suffix == ".py":
                python_files.append(path)
            elif path.is_dir():
                if file_pattern:
                    files = list(path.glob(file_pattern))
                else:
                    files = list(path.rglob("*.py"))

                for file in files:
                    python_files.append(file)

        return sorted(set(python_files))


class AsyncOrchestrationEngine:
    """Coordinates parallel file processing."""

    def __init__(self, llm_processor: AsyncLLMProcessor, max_concurrent: int = 4):
        self.llm_processor = llm_processor
        self.async_docstring_processor = AsyncDocstringProcessor()
        self.async_file_processor = AsyncFileProcessor()
        self.logger = logging.getLogger("%s.%s" % (__name__, self.__class__.__name__))

        self.semaphore = asyncio.Semaphore(max_concurrent)
        self.statistics = {
            "files_processed": 0,
            "docstrings_found": 0,
            "docstrings_improved": 0,
            "errors": 0,
        }
        self.statistics_lock = asyncio.Lock()

    async def process_files(
        self,
        file_paths: list[Path],
        object_pattern: Optional[str] = None,
        dry_run: bool = True,
    ) -> dict[str, Any]:
        """Process multiple files in parallel."""
        results = {}

        self.logger.info("Processing %s files...", len(file_paths))

        tasks = [
            self._process_file_with_logging(file_path, dry_run, object_pattern)
            for file_path in file_paths
        ]

        try:
            completed_tasks = await asyncio.gather(*tasks, return_exceptions=True)
        except asyncio.CancelledError:
            # If cancelled, try to cancel all pending tasks
            for task in tasks:
                if not task.done():
                    task.cancel()
            # Wait briefly for tasks to clean up
            await asyncio.gather(*tasks, return_exceptions=True)
            raise

        for completed_task in completed_tasks:
            if isinstance(completed_task, Exception):
                self.logger.error("Error: %s", completed_task)
                async with self.statistics_lock:
                    self.statistics["errors"] += 1
            else:
                file_path, file_result = completed_task
                results[str(file_path)] = file_result

        return results

    async def _process_file_with_logging(
        self, file_path: Path, dry_run: bool, object_pattern: Optional[str] = None
    ) -> tuple[Path, dict[str, Any]]:
        """Process a single file with logging."""
        self.logger.info("Processing: %s", file_path)
        result = await self._process_single_file(file_path, dry_run, object_pattern)
        self.logger.info("Completed: %s", file_path)
        return file_path, result

    async def _process_single_file(
        self, file_path: Path, dry_run: bool, object_pattern: Optional[str] = None
    ) -> dict[str, Any]:
        """Process a single file."""
        file_result = {
            "docstrings_found": 0,
            "docstrings_improved": 0,
            "improvements": [],
            "errors": [],
            "objects": [],  # Track individual object processing results
        }

        try:
            self.logger.info("Extracting docstrings from %s...", file_path.name)
            docstring_objects = (
                self.async_docstring_processor.extract_docstrings_from_file(file_path)
            )

            # Apply object pattern filter if specified
            if object_pattern:
                original_count = len(docstring_objects)
                docstring_objects = [
                    docstring_object
                    for docstring_object in docstring_objects
                    if fnmatch.fnmatch(docstring_object.name, object_pattern)
                ]
                self.logger.info(
                    "Object pattern '%s': %s/%s objects match",
                    object_pattern,
                    len(docstring_objects),
                    original_count,
                )

            file_result["docstrings_found"] = len(docstring_objects)
            async with self.statistics_lock:
                self.statistics["docstrings_found"] += len(docstring_objects)
            self.logger.info("Found %s docstrings", len(docstring_objects))

            # Process objects in parallel
            if docstring_objects:
                self.logger.info(
                    "Processing %s docstrings in parallel within %s...",
                    len(docstring_objects),
                    file_path.name,
                )
                tasks = [
                    self._process_single_object(file_path, docstring_object, dry_run)
                    for docstring_object in docstring_objects
                ]

                try:
                    object_results = await asyncio.gather(
                        *tasks, return_exceptions=True
                    )
                except asyncio.CancelledError:
                    # If cancelled, try to cancel all pending tasks
                    for task in tasks:
                        if not task.done():
                            task.cancel()
                    # Wait briefly for tasks to clean up
                    await asyncio.gather(*tasks, return_exceptions=True)
                    raise

                # Process results
                for i, object_result in enumerate(object_results):
                    if isinstance(object_result, Exception):
                        self.logger.error(
                            "[%s] Error processing %s: %s",
                            docstring_objects[i].name,
                            docstring_objects[i].name,
                            object_result,
                        )
                        async with self.statistics_lock:
                            self.statistics["errors"] += 1
                        file_result["errors"].append(
                            "%s: %s" % (docstring_objects[i].name, str(object_result))
                        )
                    else:
                        object_result_data, processing_result = object_result
                        file_result["objects"].append(object_result_data)

                        # Update stats and improvements
                        if object_result_data["improved"]:
                            file_result["docstrings_improved"] += 1
                            async with self.statistics_lock:
                                self.statistics["docstrings_improved"] += 1

                            file_result["improvements"].append(
                                {
                                    "name": object_result_data["name"],
                                    "type": object_result_data["type"],
                                    "line": object_result_data["line"],
                                    "original_length": len(processing_result.original),
                                    "improved_length": len(processing_result.improved),
                                }
                            )

                        if object_result_data["error"]:
                            async with self.statistics_lock:
                                self.statistics["errors"] += 1
                            file_result["errors"].append(
                                f"{object_result_data['name']}: {object_result_data['error']}"
                            )

            async with self.statistics_lock:
                self.statistics["files_processed"] += 1

        except Exception as error:
            file_result["errors"].append(str(error))
            async with self.statistics_lock:
                self.statistics["errors"] += 1

        return file_result

    async def _process_single_object(
        self, file_path: Path, docstring_object: DocstringObject, dry_run: bool
    ) -> tuple[dict[str, Any], ProcessingResult]:
        """Process a single docstring object."""
        self.logger.info(
            "[%s] Processing %s...",
            docstring_object.name,
            docstring_object.type.value,
        )
        self.logger.debug(
            "[%s] Content length: %s chars",
            docstring_object.name,
            len(docstring_object.content),
        )

        # Use async context manager for semaphore
        async with self.semaphore:
            self.logger.debug(
                "[%s] Starting processing %s with timeout...",
                docstring_object.name,
                docstring_object.name,
            )
            # Total timeout should account for retries with exponential backoff
            # Calculate actual retry delays with exponential backoff
            total_retry_delay = 0
            current_delay = ProcessingConfig.retry_delay
            for i in range(ProcessingConfig.max_retries):
                total_retry_delay += current_delay
                current_delay *= ProcessingConfig.retry_backoff_factor

            # Total time = (retries + 1) * base_timeout + total_retry_delays
            total_timeout = (
                ProcessingConfig.max_retries + 1
            ) * ProcessingConfig.timeout + total_retry_delay

            try:
                processing_result = await asyncio.wait_for(
                    self.llm_processor.process_docstring(docstring_object),
                    timeout=total_timeout,
                )
                self.logger.debug(
                    "[%s] Processing %s completed successfully",
                    docstring_object.name,
                    docstring_object.name,
                )
            except asyncio.TimeoutError:
                self.logger.warning(
                    "[%s] Timeout processing %s",
                    docstring_object.name,
                    docstring_object.name,
                )
                processing_result = ProcessingResult(
                    original=docstring_object.content,
                    improved=docstring_object.content,
                    validation_status="timeout",
                    tool_used=self.llm_processor.tool_name,
                    metrics={},
                )
            except Exception as processing_exception:
                self.logger.error(
                    "[%s] Exception processing %s: %s",
                    docstring_object.name,
                    docstring_object.name,
                    str(processing_exception),
                )
                processing_result = ProcessingResult(
                    original=docstring_object.content,
                    improved=docstring_object.content,
                    validation_status=f"error: {str(processing_exception)}",
                    tool_used=self.llm_processor.tool_name,
                    metrics={},
                )

        self.logger.info(
            "[%s] %s",
            docstring_object.name,
            processing_result.validation_status,
        )

        # Track individual object result
        object_result = {
            "name": docstring_object.name,
            "type": docstring_object.type.value,
            "line": docstring_object.line_start,
            "status": processing_result.validation_status,
            "improved": False,
            "error": None,
            "file_operation_success": None,
        }

        if processing_result.validation_status == "success":
            if processing_result.improved != processing_result.original:
                object_result["improved"] = True

                self._log_docstring_processing_summary(
                    file_path, docstring_object, processing_result
                )

                if not dry_run:
                    success = (
                        await self.async_docstring_processor.replace_docstring_in_file(
                            file_path, docstring_object, processing_result.improved
                        )
                    )
                    object_result["file_operation_success"] = success
                    if not success:
                        object_result["error"] = "Failed to replace in file"
        else:
            object_result["error"] = processing_result.validation_status

        return object_result, processing_result

    def _log_docstring_processing_summary(
        self,
        file_path: Path,
        docstring_object: DocstringObject,
        result: ProcessingResult,
    ):
        """Log detailed comparison of original vs improved docstring."""
        separator = "=" * 79

        summary = """
%s
DOCSTRING IMPROVEMENT: %s
Object: %s '%s' (line %s)
Tool: %s

--- ORIGINAL DOCSTRING ---
%s

--- IMPROVED DOCSTRING ---
%s

--- METRICS ---
Original: %s chars, %s lines
Improved: %s chars, %s lines""" % (
            separator,
            file_path.name,
            docstring_object.type.value,
            docstring_object.name,
            docstring_object.line_start,
            result.tool_used,
            self._sanitize_docstring_for_log(result.original),
            self._sanitize_docstring_for_log(result.improved),
            len(result.original),
            len(result.original.splitlines()),
            len(result.improved),
            len(result.improved.splitlines()),
        )

        if result.metrics and result.metrics.get("explanation"):
            summary += """

--- EXPLANATION ---
%s""" % result.metrics["explanation"]

        summary += (
            """
%s
"""
            % separator
        )

        self.logger.debug(summary)

    def _sanitize_docstring_for_log(self, docstring: str) -> str:
        """Sanitize a docstring for clean logging by handling empty content."""
        if not docstring.strip():
            return "(empty docstring)"

        return docstring


def _log_processing_summary(results: dict, dry_run: bool) -> None:
    """Log processing summary without logger timestamp formatting."""
    separator = "=" * 79
    summary = ["", separator, "DOCSTRING PROCESSING SUMMARY", separator]

    successful_object_results = []
    failed_object_results = []
    unchanged_object_results = []

    for file_path, file_result in results.items():
        for object_result in file_result.get("objects", []):
            object_result = {
                "file": file_path,
                "name": object_result["name"],
                "type": object_result["type"],
                "line": object_result["line"],
                "status": object_result["status"],
                "improved": object_result["improved"],
                "error": object_result["error"],
                "file_operation_success": object_result.get("file_operation_success"),
            }

            if object_result["error"]:
                failed_object_results.append(object_result)
            elif object_result["improved"]:
                successful_object_results.append(object_result)
            else:
                unchanged_object_results.append(object_result)

    # Add successful improvements
    if successful_object_results:
        summary.append("")
        summary.append(
            "✅ Successfully Improved (%s objects):" % len(successful_object_results)
        )
        for successful_object_result in successful_object_results:
            file_status = ""
            if (
                not dry_run
                and successful_object_result["file_operation_success"] is not None
            ):
                file_status = (
                    " (✅ applied)"
                    if successful_object_result["file_operation_success"]
                    else " (❌ failed to apply)"
                )
            summary.append(
                "  • %s '%s' in %s:%s%s"
                % (
                    successful_object_result["type"],
                    successful_object_result["name"],
                    successful_object_result["file"],
                    successful_object_result["line"],
                    file_status,
                )
            )

    # Add failed objects
    if failed_object_results:
        summary.append("")
        summary.append(
            "❌ Failed to Process (%s objects):" % len(failed_object_results)
        )
        for failed_object_result in failed_object_results:
            reason = (
                failed_object_result["error"]
                if failed_object_result["error"]
                else failed_object_result["status"]
            )
            summary.append(
                "  • %s '%s' in %s:%s - %s"
                % (
                    failed_object_result["type"],
                    failed_object_result["name"],
                    failed_object_result["file"],
                    failed_object_result["line"],
                    reason,
                )
            )

    # Add unchanged objects
    if unchanged_object_results and len(unchanged_object_results) <= 10:
        summary.append("")
        summary.append(
            "📄 No Changes Needed (%s objects):" % len(unchanged_object_results)
        )
        for unchanged_object_result in unchanged_object_results:
            summary.append(
                "  • %s '%s' in %s:%s"
                % (
                    unchanged_object_result["type"],
                    unchanged_object_result["name"],
                    unchanged_object_result["file"],
                    unchanged_object_result["line"],
                )
            )
    elif unchanged_object_results:
        summary.append("")
        summary.append(
            "📄 No Changes Needed: %s objects" % len(unchanged_object_results)
        )

    summary.append("")
    summary.append(separator)

    # Log as single statement with prepended line break
    LOGGER.info("\n" + "\n".join(summary))


def _display_results(
    results: dict[str, Any],
    statistics: dict[str, Any],
    dry_run: bool,
):
    """Display processing results."""

    if results:
        LOGGER.info("=== File Details ===")
        for file_path, file_result in results.items():
            if file_result["docstrings_improved"] > 0:
                LOGGER.info(
                    "✅ %s: %s improvements",
                    file_path,
                    file_result["docstrings_improved"],
                )
            elif file_result["errors"]:
                LOGGER.warning(
                    "❌ %s: %s errors", file_path, len(file_result["errors"])
                )
            else:
                LOGGER.info("📄 %s: No changes needed", file_path)

        # Clean console summary without logger formatting
        _log_processing_summary(results, dry_run)

    # Clean completion message
    if dry_run:
        LOGGER.info("\n💡 This was a preview. Remove --dry-run to apply changes.")
    else:
        # Only show "changes applied" if there were actual improvements and no errors
        if statistics["docstrings_improved"] > 0 and statistics["errors"] == 0:
            LOGGER.info("✅ Processing complete! Changes have been applied.")
        elif statistics["docstrings_improved"] > 0 and statistics["errors"] > 0:
            LOGGER.info(
                "⚠️ Processing complete with %s errors. Some changes were applied.",
                statistics["errors"],
            )
        elif statistics["errors"] > 0:
            LOGGER.info(
                "❌ Processing completed with %s errors. No changes were applied.",
                statistics["errors"],
            )
        else:
            LOGGER.info("📄 Processing complete! No changes were needed.")


async def _async_main(
    paths: tuple[Path, ...],
    tool: str,
    parallel: int,
    file_pattern: Optional[str],
    object_pattern: Optional[str],
    dry_run: bool,
):
    """Async main function."""

    # Set up signal handlers for graceful shutdown
    def signal_handler(sig, frame):
        LOGGER.info("Received signal %s, shutting down gracefully...", sig)
        # Cancel all pending tasks
        for task in asyncio.all_tasks():
            if not task.done():
                task.cancel()

    if sys.platform != "win32":  # Windows doesn't support these signals
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)

    # Validate parameters
    if parallel <= 0:
        LOGGER.error("Parallel count must be positive, got %s", parallel)
        sys.exit(1)

    if parallel > 50:  # Reasonable upper limit
        LOGGER.warning(
            "Parallel count %s seems very high, consider reducing it", parallel
        )

    # Validate paths exist
    for path in paths:
        if not path.exists():
            LOGGER.error("Path does not exist: %s", path)
            sys.exit(1)

    setup_logging()

    config_info = "dry_run=%s, tool=%s" % (dry_run, tool)
    if object_pattern:
        config_info += ", object_pattern='%s'" % object_pattern
    LOGGER.info("Configuration: %s", config_info)

    # Validate tool availability
    try:
        subprocess.run([tool, "--version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        LOGGER.error("Error: %s CLI is not available or not working", tool)
        sys.exit(1)

    # Create processor
    llm_processor = _PROCESSORS[tool]()
    LOGGER.info("Created %s processor", tool)

    LOGGER.info("Finding files to process...")
    file_processor = AsyncFileProcessor()

    if file_pattern:
        search_paths = list(paths) if paths else [Path.cwd()]
        python_files = []
        for search_path in search_paths:
            files = list(search_path.glob(file_pattern))
            python_files.extend(files)
    else:
        python_files = await file_processor.find_python_files(
            list(paths), file_pattern=None
        )

    LOGGER.info("Found %s files", len(python_files))

    if not python_files:
        LOGGER.warning("No Python files found to process")
        return

    mode_text = "DRY RUN" if dry_run else "LIVE PROCESSING"
    LOGGER.info("🚀 Docstring Processing - %s", mode_text)
    LOGGER.info(
        "Tool: %s, Files: %s, Parallel: %s",
        tool.upper(),
        len(python_files),
        parallel,
    )

    LOGGER.info("Creating orchestration engine...")
    engine = AsyncOrchestrationEngine(llm_processor, parallel)
    LOGGER.info("Starting file processing...")
    results = await engine.process_files(python_files, object_pattern, dry_run)
    LOGGER.info("File processing completed!")

    _display_results(results, engine.statistics, dry_run)


@click.command()
@click.argument("paths", nargs=-1, type=click.Path(exists=True, path_type=Path))
@click.option(
    "--tool",
    type=click.Choice(["claude", "gemini"]),
    default="claude",
    help="LLM tool selection (default: claude)",
)
@click.option(
    "--parallel", type=int, default=4, help="Max concurrent processes (default: 4)"
)
@click.option(
    "--file-pattern", type=str, help='File pattern matching (e.g., "**/*.py")'
)
@click.option(
    "--object-pattern",
    type=str,
    help='Filter objects by name pattern (e.g., "sd_to_XYZ_integration" or "sd_to_XYZ*" for wildcard)',
)
@click.option(
    "--dry-run",
    is_flag=True,
    default=False,
    help="Preview changes without applying them (default: apply changes)",
)
def main(
    paths: tuple[Path, ...],
    tool: str,
    parallel: int,
    file_pattern: Optional[str],
    object_pattern: Optional[str],
    dry_run: bool,
):
    """
    Reusable Docstring Processing Script with Multi-LLM Support

    Process Python docstrings using Claude Code or Gemini CLI across
    all colour-science repositories.

    Examples:

        # Apply changes with Claude (default behavior)
        uv run docstring_processor.py --tool claude --parallel 4 colour/

        # Preview only with Gemini on a single file
        uv run docstring_processor.py --tool gemini file.py --dry-run

        # Process multiple directories
        uv run docstring_processor.py colour-visuals/ colour-hdri/

        # File pattern matching (preview only)
        uv run docstring_processor.py --file-pattern "**/*.py" --dry-run

        # Target specific function
        uv run docstring_processor.py colour/ --object-pattern "sd_to_XYZ_integration"

        # Target multiple functions with wildcard
        uv run docstring_processor.py colour/ --object-pattern "sd_to_XYZ*"
    """
    try:
        asyncio.run(
            _async_main(paths, tool, parallel, file_pattern, object_pattern, dry_run)
        )
    except KeyboardInterrupt:
        LOGGER.info("Processing interrupted by user")
        sys.exit(130)  # Standard exit code for Ctrl+C
    except asyncio.CancelledError:
        LOGGER.info("Processing cancelled")
        sys.exit(1)


if __name__ == "__main__":
    main()
