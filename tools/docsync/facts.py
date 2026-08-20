"""Extract the repository's real, mechanical facts.

Everything here reads the tree statically: modules are parsed with :mod:`ast`, never
imported or executed. That matters for two reasons. Importing ``amf`` to inspect it would
make the detector's answer depend on the interpreter's import state, and executing
``cli.py`` to enumerate its parser would be a side effect in a tool whose whole value is
being side-effect free.

The one exception is :func:`collect_test_count`, which shells out to ``pytest
--collect-only`` because parametrised tests cannot be counted honestly any other way. It
degrades to ``None`` when pytest is unavailable, and the check that consumes it is skipped
rather than guessed.
"""

from __future__ import annotations

import ast
import os
import re
import subprocess
import sys
import tomllib
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

PACKAGE_DIR = Path("src/amf")
"""Package directory, relative to the repository root."""


@dataclass(frozen=True, slots=True)
class Argument:
    """One ``add_argument`` call recovered from the CLI's parser construction.

    Attributes:
        names: The flag spellings, e.g. ``("--output", "-o")``, or a single positional name.
        default: The literal default, or ``None`` when none was given.
        has_default: Whether ``default=`` was present at all (``None`` is a real default).
        choices: Resolved choice values, empty when the argument is unconstrained.
        required: Whether ``required=True`` was passed.
    """

    names: tuple[str, ...]
    default: Any = None
    has_default: bool = False
    choices: tuple[str, ...] = ()
    required: bool = False

    @property
    def primary(self) -> str:
        """Return the canonical spelling: the first long flag, else the first name."""
        for name in self.names:
            if name.startswith("--"):
                return name
        return self.names[0]


@dataclass(frozen=True, slots=True)
class Subcommand:
    """One ``add_parser`` subcommand and every argument attached to it."""

    name: str
    arguments: tuple[Argument, ...] = ()

    def flag(self, name: str) -> Argument | None:
        """Return the argument spelled ``name``, or ``None``."""
        return next((a for a in self.arguments if name in a.names), None)

    @property
    def flag_names(self) -> tuple[str, ...]:
        """Return every ``--flag`` this subcommand accepts, in declaration order."""
        return tuple(a.primary for a in self.arguments if a.primary.startswith("--"))


@dataclass(frozen=True, slots=True)
class ModuleFacts:
    """The public surface of one module in the package."""

    name: str
    classes: tuple[str, ...] = ()
    functions: tuple[str, ...] = ()
    assignments: tuple[str, ...] = ()
    imports: frozenset[str] = frozenset()

    @property
    def symbols(self) -> frozenset[str]:
        """Return every top-level name this module defines."""
        return frozenset(self.classes) | frozenset(self.functions) | frozenset(self.assignments)


@dataclass(frozen=True, slots=True)
class RepoFacts:
    """Everything the checks are allowed to treat as ground truth."""

    root: Path
    modules: dict[str, ModuleFacts] = field(default_factory=dict)
    exports: tuple[str, ...] = ()
    exceptions: dict[str, str] = field(default_factory=dict)
    dataclasses: dict[str, dict[str, Any]] = field(default_factory=dict)
    subcommands: tuple[Subcommand, ...] = ()
    cli_docstring_commands: tuple[str, ...] = ()
    constants: dict[str, Any] = field(default_factory=dict)
    package_version: str = ""
    pyproject_version: str = ""
    pyproject: dict[str, Any] = field(default_factory=dict)
    examples: tuple[str, ...] = ()
    doc_files: tuple[str, ...] = ()
    top_level: tuple[str, ...] = ()
    workflows: tuple[str, ...] = ()
    codeql_disable_directives: int = 0
    test_count: int | None = None

    def subcommand(self, name: str) -> Subcommand | None:
        """Return the subcommand called ``name``, or ``None``."""
        return next((s for s in self.subcommands if s.name == name), None)


def _literal(node: ast.expr) -> tuple[Any, bool]:
    """Evaluate ``node`` as a literal.

    Returns:
        A ``(value, ok)`` pair; ``ok`` is ``False`` when the node is not a literal.
    """
    try:
        return ast.literal_eval(node), True
    except (ValueError, TypeError, SyntaxError, MemoryError, RecursionError):
        return None, False


def _enum_values(tree: ast.Module) -> dict[str, tuple[str, ...]]:
    """Map each ``str``-valued enum in ``tree`` to its member values.

    Used to resolve ``choices=[k.value for k in SystemKind]`` into real strings instead of
    storing an opaque AST dump.
    """
    out: dict[str, tuple[str, ...]] = {}
    for node in tree.body:
        if not isinstance(node, ast.ClassDef):
            continue
        base_names = {b.id for b in node.bases if isinstance(b, ast.Name)}
        if "Enum" not in base_names:
            continue
        values: list[str] = []
        for stmt in node.body:
            if (
                isinstance(stmt, ast.Assign)
                and isinstance(stmt.value, ast.Constant)
                and isinstance(stmt.value.value, str)
            ):
                values.append(stmt.value.value)
        if values:
            out[node.name] = tuple(values)
    return out


def _resolve_choices(node: ast.expr, enums: dict[str, tuple[str, ...]]) -> tuple[str, ...]:
    """Resolve a ``choices=`` expression to concrete strings.

    Handles a plain list literal and the comprehension form ``[k.value for k in SomeEnum]``
    that the CLI uses for ``--target`` and ``--timeline``.
    """
    value, ok = _literal(node)
    if ok and isinstance(value, list):
        return tuple(str(v) for v in value)
    if isinstance(node, ast.ListComp) and len(node.generators) == 1:
        source = node.generators[0].iter
        if isinstance(source, ast.Name) and source.id in enums:
            return enums[source.id]
    return ()


def _argument_from_call(call: ast.Call, enums: dict[str, tuple[str, ...]]) -> Argument | None:
    """Build an :class:`Argument` from one ``add_argument`` call, or ``None``."""
    names = tuple(a.value for a in call.args if isinstance(a, ast.Constant) and isinstance(a.value, str))
    if not names:
        return None
    default: Any = None
    has_default = False
    choices: tuple[str, ...] = ()
    required = False
    for kw in call.keywords:
        if kw.arg == "default":
            default, _ = _literal(kw.value)
            has_default = True
        elif kw.arg == "choices":
            choices = _resolve_choices(kw.value, enums)
        elif kw.arg == "required":
            required = bool(_literal(kw.value)[0])
    return Argument(names=names, default=default, has_default=has_default, choices=choices, required=required)


def _helper_arguments(tree: ast.Module, enums: dict[str, tuple[str, ...]]) -> dict[str, tuple[Argument, ...]]:
    """Map each module-level helper to the arguments it adds to the parser it is given.

    ``cli.py`` factors the shared ``--format`` option into ``_add_format(parser)``. Without
    this pass the extractor would report ``--format`` missing from four subcommands and the
    detector would emit four false findings.
    """
    helpers: dict[str, tuple[Argument, ...]] = {}
    for node in tree.body:
        if not isinstance(node, ast.FunctionDef) or not node.args.args:
            continue
        target = node.args.args[0].arg
        found: list[Argument] = []
        for inner in ast.walk(node):
            if (
                isinstance(inner, ast.Call)
                and isinstance(inner.func, ast.Attribute)
                and inner.func.attr == "add_argument"
                and isinstance(inner.func.value, ast.Name)
                and inner.func.value.id == target
            ):
                argument = _argument_from_call(inner, enums)
                if argument is not None:
                    found.append(argument)
        if found:
            helpers[node.name] = tuple(found)
    return helpers


def extract_subcommands(cli_source: str, models_source: str) -> tuple[Subcommand, ...]:
    """Recover the full argparse tree from ``cli.py`` without importing it.

    Args:
        cli_source: Text of ``src/amf/cli.py``.
        models_source: Text of ``src/amf/models.py``, used to resolve enum-valued choices.

    Returns:
        Every subcommand in declaration order, each with its arguments.
    """
    cli_tree = ast.parse(cli_source)
    enums = _enum_values(ast.parse(models_source))
    helpers = _helper_arguments(cli_tree, enums)

    variables: dict[str, str] = {}
    order: list[str] = []
    for node in ast.walk(cli_tree):
        if (
            isinstance(node, ast.Assign)
            and isinstance(node.value, ast.Call)
            and isinstance(node.value.func, ast.Attribute)
            and node.value.func.attr == "add_parser"
            and node.value.args
            and len(node.targets) == 1
            and isinstance(node.targets[0], ast.Name)
        ):
            name, ok = _literal(node.value.args[0])
            if ok and isinstance(name, str):
                variables[node.targets[0].id] = name
                order.append(name)

    collected: dict[str, list[Argument]] = {name: [] for name in order}
    for node in ast.walk(cli_tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        if isinstance(func, ast.Attribute) and func.attr == "add_argument" and isinstance(func.value, ast.Name):
            subcommand = variables.get(func.value.id)
            if subcommand is not None:
                argument = _argument_from_call(node, enums)
                if argument is not None:
                    collected[subcommand].append(argument)
        elif isinstance(func, ast.Name) and func.id in helpers and node.args:
            first = node.args[0]
            if isinstance(first, ast.Name):
                subcommand = variables.get(first.id)
                if subcommand is not None:
                    collected[subcommand].extend(helpers[func.id])

    return tuple(Subcommand(name=name, arguments=tuple(collected[name])) for name in order)


def extract_module(name: str, source: str) -> ModuleFacts:
    """Summarise one package module's top-level surface and intra-package imports."""
    tree = ast.parse(source)
    classes: list[str] = []
    functions: list[str] = []
    assignments: list[str] = []
    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            classes.append(node.name)
        elif isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef):
            functions.append(node.name)
        elif isinstance(node, ast.Assign):
            assignments.extend(t.id for t in node.targets if isinstance(t, ast.Name))
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            assignments.append(node.target.id)

    imports: set[str] = set()
    for imported in ast.walk(tree):
        if isinstance(imported, ast.ImportFrom) and imported.module and imported.module.startswith("amf"):
            parts = imported.module.split(".")
            if len(parts) > 1:
                imports.add(parts[1])
        elif isinstance(imported, ast.Import):
            for alias in imported.names:
                parts = alias.name.split(".")
                if parts[0] == "amf" and len(parts) > 1:
                    imports.add(parts[1])
    return ModuleFacts(
        name=name,
        classes=tuple(classes),
        functions=tuple(functions),
        assignments=tuple(assignments),
        imports=frozenset(imports),
    )


def extract_exceptions(source: str) -> dict[str, str]:
    """Map every exception class in ``errors.py`` to its first base class name."""
    tree = ast.parse(source)
    out: dict[str, str] = {}
    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            base = node.bases[0] if node.bases else None
            out[node.name] = base.id if isinstance(base, ast.Name) else ""
    return out


def extract_dataclasses(source: str) -> dict[str, dict[str, Any]]:
    """Describe every dataclass in a module: frozen, slotted, and whether it defines ``to_dict``."""
    tree = ast.parse(source)
    out: dict[str, dict[str, Any]] = {}
    for node in tree.body:
        if not isinstance(node, ast.ClassDef):
            continue
        options: dict[str, Any] = {}
        is_dataclass = False
        for decorator in node.decorator_list:
            call = decorator if isinstance(decorator, ast.Call) else None
            target = call.func if call else decorator
            if isinstance(target, ast.Name) and target.id == "dataclass":
                is_dataclass = True
                if call:
                    for kw in call.keywords:
                        if kw.arg:
                            options[kw.arg] = _literal(kw.value)[0]
        if not is_dataclass:
            continue
        methods = {m.name for m in node.body if isinstance(m, ast.FunctionDef)}
        fields: dict[str, Any] = {}
        for stmt in node.body:
            if isinstance(stmt, ast.AnnAssign) and isinstance(stmt.target, ast.Name) and stmt.value is not None:
                value, ok = _literal(stmt.value)
                if ok:
                    fields[stmt.target.id] = value
        out[node.name] = {
            "frozen": bool(options.get("frozen")),
            "slots": bool(options.get("slots")),
            "to_dict": "to_dict" in methods,
            "fields": fields,
        }
    return out


def extract_constants(source: str) -> dict[str, Any]:
    """Return every module-level name bound to a numeric or string literal."""
    tree = ast.parse(source)
    out: dict[str, Any] = {}
    for node in tree.body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            value, ok = _literal(node.value)
            if ok and isinstance(value, int | float | str):
                out[node.targets[0].id] = value
    return out


def extract_exports(source: str) -> tuple[str, ...]:
    """Return ``__all__`` from the package ``__init__``, in declaration order."""
    tree = ast.parse(source)
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "__all__" for t in node.targets):
            value, ok = _literal(node.value)
            if ok and isinstance(value, list):
                return tuple(str(v) for v in value)
    return ()


def extract_module_docstring_commands(source: str) -> tuple[str, ...]:
    """Return the subcommand names named in ``cli.py``'s own module docstring.

    Checked against the real parser so the source's self-description cannot rot either --
    the drift guard points both ways.
    """
    doc = ast.get_docstring(ast.parse(source)) or ""
    return tuple(sorted(set(re.findall(r"``([a-z][a-z-]*)``", doc))))


def collect_test_count(root: Path) -> int | None:
    """Return the number of tests pytest collects, or ``None`` if it cannot be determined.

    Parametrised tests make any static count a guess, so this asks pytest. Two details are
    load-bearing:

    * ``--override-ini=addopts=`` clears the project's default arguments. Collection measures
      no code, so inheriting ``--cov-fail-under=100`` would fail the run.
    * The child is run with coverage's environment stripped. When this function is itself
      called from under ``pytest-cov``, an inherited ``COV_CORE_*`` makes the child write
      statement-only data into the parent's file, and combining that with the parent's branch
      data aborts the whole session with ``DataError``.
    """
    env = {k: v for k, v in os.environ.items() if not k.startswith(("COV_CORE_", "COVERAGE_"))}
    try:
        completed = subprocess.run(
            [sys.executable, "-m", "pytest", "--collect-only", "-q", "--override-ini=addopts="],
            check=False,
            capture_output=True,
            text=True,
            cwd=root,
            timeout=300,
            env=env,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    match = re.search(r"(\d+) tests? collected", completed.stdout)
    return int(match.group(1)) if match else None


def _tracked_top_level(root: Path) -> tuple[str, ...]:
    """Return the repository's tracked top-level entries.

    Asks git rather than reading the directory, because the layout block documents the
    *repository*, not whatever happens to be lying in the working tree. Without this a
    generated ``coverage.xml`` or a stray ``.venv`` would be reported as undocumented drift.

    Falls back to a directory listing when git is unavailable, so the tool still works on an
    exported source tree.
    """
    try:
        completed = subprocess.run(
            ["git", "ls-files", "-z"],
            check=False,
            capture_output=True,
            text=True,
            cwd=root,
            timeout=60,
        )
    except (OSError, subprocess.SubprocessError):
        completed = None
    if completed is not None and completed.returncode == 0 and completed.stdout:
        entries = {line.split("/", 1)[0] for line in completed.stdout.split("\0") if line}
        return tuple(sorted(entries))
    return tuple(sorted(p.name for p in root.iterdir() if not p.name.startswith(".git")))


def _read(path: Path) -> str:
    """Read a UTF-8 text file, returning an empty string when it is absent."""
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return ""


def collect(root: Path, *, with_test_count: bool = True) -> RepoFacts:
    """Gather every fact the checks may treat as ground truth.

    Args:
        root: Repository root.
        with_test_count: Whether to shell out to pytest for an authoritative test count.
            Disabled by the unit tests, which must stay fast and must not recurse.

    Returns:
        A populated :class:`RepoFacts`.
    """
    package = root / PACKAGE_DIR
    modules: dict[str, ModuleFacts] = {}
    for path in sorted(package.glob("*.py")):
        if path.stem == "__init__":
            continue
        modules[path.stem] = extract_module(path.stem, _read(path))

    init_source = _read(package / "__init__.py")
    cli_source = _read(package / "cli.py")
    models_source = _read(package / "models.py")

    constants: dict[str, Any] = {}
    for name, filename in (("diagnostics", "diagnostics.py"), ("simulation", "simulation.py"), ("graph", "graph.py")):
        for key, value in extract_constants(_read(package / filename)).items():
            constants[f"{name}.{key}"] = value

    dataclass_facts: dict[str, dict[str, Any]] = {}
    for path in sorted(package.glob("*.py")):
        for name, info in extract_dataclasses(_read(path)).items():
            dataclass_facts[name] = {**info, "module": path.stem}

    pyproject: dict[str, Any] = {}
    pyproject_path = root / "pyproject.toml"
    if pyproject_path.is_file():
        pyproject = tomllib.loads(pyproject_path.read_text(encoding="utf-8"))

    version_match = re.search(r'^__version__\s*=\s*"([^"]+)"', init_source, re.MULTILINE)
    workflow_dir = root / ".github" / "workflows"
    codeql = _read(workflow_dir / "codeql.yml")

    docs_dir = root / "docs"
    doc_files = (
        tuple(sorted(str(p.relative_to(root)).replace("\\", "/") for p in docs_dir.rglob("*.md")))
        if docs_dir.is_dir()
        else ()
    )

    examples_dir = root / "examples"
    examples = tuple(sorted(p.name for p in examples_dir.glob("*.py"))) if examples_dir.is_dir() else ()

    top_level = _tracked_top_level(root)
    workflows = tuple(sorted(p.name for p in workflow_dir.glob("*.yml"))) if workflow_dir.is_dir() else ()

    return RepoFacts(
        root=root,
        modules=modules,
        exports=extract_exports(init_source),
        exceptions=extract_exceptions(_read(package / "errors.py")),
        dataclasses=dataclass_facts,
        subcommands=extract_subcommands(cli_source, models_source),
        cli_docstring_commands=extract_module_docstring_commands(cli_source),
        constants=constants,
        package_version=version_match.group(1) if version_match else "",
        pyproject_version=str(pyproject.get("project", {}).get("version", "")),
        pyproject=pyproject,
        examples=examples,
        doc_files=doc_files,
        top_level=top_level,
        workflows=workflows,
        codeql_disable_directives=codeql.count("yamllint disable-line"),
        test_count=collect_test_count(root) if with_test_count else None,
    )
