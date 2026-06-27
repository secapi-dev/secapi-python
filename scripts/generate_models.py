#!/usr/bin/env python3
"""Generate Pydantic v2 response models from the SEC API OpenAPI document.

The API is the contract. Rather than hand-maintain ~125 response models, this
script reads ``scripts/openapi.json`` (a vendored snapshot of
``https://api.secapi.dev/api/core/v3/api-docs``) and emits clean, typed model
modules into ``secapi/models/``.

Usage::

    python scripts/generate_models.py                 # regenerate from snapshot
    python scripts/generate_models.py --check         # fail if output is stale
    python scripts/generate_models.py --spec URL/PATH # use a different spec

Run ``--check`` in CI to detect drift between the SDK and the live API.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.request
from pathlib import Path
from typing import Dict, List, Set, Tuple

ROOT = Path(__file__).resolve().parent.parent
SPEC_PATH = ROOT / "scripts" / "openapi.json"
MODELS_DIR = ROOT / "secapi" / "models"

# Map each schema (by name prefix) to a destination module.
DOMAIN_MODULES = ("common", "entity", "filing", "financial", "insider", "institution")


def friendly(name: str) -> str:
    """Friendly class name: drop the ``DTO`` suffix the Java side uses."""
    return name[:-3] if name.endswith("DTO") else name


def domain_of(name: str) -> str:
    if name in ("ApiErrorDTO", "ErrorResponseDTO"):
        return "common"
    if name.startswith("Entity") or name.startswith("Entities"):
        return "entity"
    if name.startswith("Filing"):
        return "filing"
    if name.startswith("Insider"):
        return "insider"
    if name.startswith("Institution"):
        return "institution"
    # Financials bucket: Financial*, Canonical*, Company/Companies*, Concept*,
    # Statement*, Xbrl*, *LineDTO, etc.
    return "financial"


def to_snake(name: str) -> str:
    s1 = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", name)
    s2 = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", s1)
    return s2.lower()


def load_spec(spec: str) -> dict:
    if spec.startswith("http://") or spec.startswith("https://"):
        with urllib.request.urlopen(spec) as resp:  # noqa: S310 (trusted URL)
            return json.loads(resp.read().decode("utf-8"))
    return json.loads(Path(spec).read_text())


class TypeResolver:
    def __init__(self) -> None:
        self.uses_datetime = False

    def resolve(self, schema: dict) -> Tuple[str, Set[str]]:
        """Return ``(python_type, {referenced_friendly_names})``."""
        if "$ref" in schema:
            fr = friendly(schema["$ref"].split("/")[-1])
            return fr, {fr}
        t = schema.get("type")
        if t == "array":
            inner, refs = self.resolve(schema.get("items", {}))
            return f"List[{inner}]", refs
        if t == "string":
            fmt = schema.get("format")
            if fmt == "date":
                self.uses_datetime = True
                return "datetime.date", set()
            if fmt == "date-time":
                self.uses_datetime = True
                return "datetime.datetime", set()
            return "str", set()
        if t == "integer":
            return "int", set()
        if t == "number":
            return "float", set()
        if t == "boolean":
            return "bool", set()
        if t == "object":
            return "Dict[str, Any]", set()
        return "Any", set()


def topo_sort(names: List[str], deps: Dict[str, Set[str]]) -> List[str]:
    """Stable topological sort so dependencies are defined first."""
    ordered: List[str] = []
    seen: Set[str] = set()
    local = set(names)

    def visit(n: str, stack: Set[str]) -> None:
        if n in seen or n not in local:
            return
        if n in stack:  # cycle: break it, rely on model_rebuild()
            return
        stack.add(n)
        for d in sorted(deps.get(n, set())):
            visit(d, stack)
        stack.discard(n)
        seen.add(n)
        ordered.append(n)

    for n in names:
        visit(n, set())
    return ordered


def build() -> Dict[str, str]:
    spec = load_spec(str(SPEC_PATH))
    schemas: Dict[str, dict] = spec["components"]["schemas"]

    name_to_module = {friendly(n): domain_of(n) for n in schemas}

    # Collect per-module class definitions. Each entry tracks the imports it
    # needs so generated modules only import what they actually use.
    modules: Dict[str, List[Tuple[str, str, Set[str]]]] = {m: [] for m in DOMAIN_MODULES}
    module_uses: Dict[str, Dict[str, bool]] = {
        m: {"datetime": False, "list": False, "dict": False, "any": False, "field": False}
        for m in DOMAIN_MODULES
    }

    for orig in sorted(schemas):
        schema = schemas[orig]
        cls = friendly(orig)
        module = domain_of(orig)
        resolver = TypeResolver()
        props: Dict[str, dict] = schema.get("properties", {})
        uses = module_uses[module]

        lines: List[str] = []
        refs: Set[str] = set()
        doc = schema.get("description")
        if doc:
            lines.append(f'    """{doc.strip()}"""')

        for pname, pschema in props.items():
            pytype, prefs = resolver.resolve(pschema)
            refs |= prefs
            if "List[" in pytype:
                uses["list"] = True
            if "Dict[" in pytype:
                uses["dict"] = True
            if "Any" in pytype:
                uses["any"] = True
            snake = to_snake(pname)
            alias = pname if snake != pname else None

            description = pschema.get("description")
            enum = pschema.get("enum")
            if enum:
                allowed = ", ".join(str(e) for e in enum)
                description = (f"{description} " if description else "") + f"Allowed values: {allowed}"

            field_args: List[str] = ["default=None"]
            if alias:
                field_args.append(f'alias="{alias}"')
            if description:
                safe = description.replace("\\", "\\\\").replace('"', '\\"')
                field_args.append(f'description="{safe}"')

            if len(field_args) == 1:  # only default=None
                lines.append(f"    {snake}: Optional[{pytype}] = None")
            else:
                uses["field"] = True
                lines.append(f"    {snake}: Optional[{pytype}] = Field({', '.join(field_args)})")

        if not props:
            lines.append("    pass")

        body = "\n".join(lines)
        modules[module].append((cls, body, refs))
        if resolver.uses_datetime:
            uses["datetime"] = True

    # Render each module.
    rendered: Dict[str, str] = {}
    for module in DOMAIN_MODULES:
        entries = modules[module]
        local_names = [c for c, _, _ in entries]
        deps = {c: {r for r in refs if name_to_module.get(r) == module and r != c} for c, _, refs in entries}
        order = topo_sort(local_names, deps)
        by_name = {c: (b, refs) for c, b, refs in entries}
        uses = module_uses[module]

        # External imports grouped by module.
        external: Dict[str, Set[str]] = {}
        for _c, _b, refs in entries:
            for r in refs:
                rmod = name_to_module.get(r)
                if rmod and rmod != module:
                    external.setdefault(rmod, set()).add(r)

        typing_names = []
        if uses["any"]:
            typing_names.append("Any")
        if uses["dict"]:
            typing_names.append("Dict")
        if uses["list"]:
            typing_names.append("List")
        typing_names.append("Optional")  # every field is Optional[...]

        out: List[str] = []
        out.append('"""Auto-generated SEC API models. Do not edit by hand.')
        out.append("")
        out.append("Regenerate with: python scripts/generate_models.py")
        out.append('"""')
        out.append("")
        out.append("from __future__ import annotations")
        out.append("")
        if uses["datetime"]:
            out.append("import datetime")
        out.append(f"from typing import {', '.join(typing_names)}")
        out.append("")
        if uses["field"]:
            out.append("from pydantic import Field")
            out.append("")
        out.append("from ._base import SecBaseModel")
        for rmod in sorted(external):
            names = ", ".join(sorted(external[rmod], key=str.lower))
            out.append(f"from .{rmod} import {names}")
        out.append("")
        out.append("")

        for cls in order:
            body, _ = by_name[cls]
            out.append(f"class {cls}(SecBaseModel):")
            out.append(body)
            out.append("")
            out.append("")

        # Resolve forward references across the module.
        out.append("__all__ = [")
        for cls in sorted(local_names, key=str.lower):
            out.append(f'    "{cls}",')
        out.append("]")
        out.append("")
        out.append("for _m in list(globals().values()):")
        out.append("    if isinstance(_m, type) and issubclass(_m, SecBaseModel):")
        out.append("        _m.model_rebuild()")
        out.append("")

        rendered[module] = "\n".join(out)

    # models/__init__.py re-exports every friendly model name.
    init_lines = ['"""Typed response models for the SEC API."""', "", "from __future__ import annotations", ""]
    all_names: List[str] = []
    for module in DOMAIN_MODULES:
        names = sorted((friendly(n) for n in schemas if domain_of(n) == module), key=str.lower)
        if not names:
            continue
        init_lines.append(f"from .{module} import (")
        for n in names:
            init_lines.append(f"    {n},")
            all_names.append(n)
        init_lines.append(")")
    init_lines.append("")
    init_lines.append("__all__ = [")
    for n in sorted(all_names, key=str.lower):
        init_lines.append(f'    "{n}",')
    init_lines.append("]")
    init_lines.append("")
    rendered["__init__"] = "\n".join(init_lines)

    return rendered


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="fail if generated files are stale")
    parser.add_argument("--spec", default=None, help="override spec path or URL")
    args = parser.parse_args()

    global SPEC_PATH
    if args.spec:
        if args.spec.startswith(("http://", "https://")):
            data = load_spec(args.spec)
            SPEC_PATH.write_text(json.dumps(data, indent=2) + "\n")
        else:
            SPEC_PATH = Path(args.spec)

    rendered = build()
    stale = []
    for module, content in rendered.items():
        path = MODELS_DIR / f"{module}.py"
        existing = path.read_text() if path.exists() else None
        if existing != content:
            stale.append(module)
            if not args.check:
                path.write_text(content)

    if args.check:
        if stale:
            print("Stale generated modules: " + ", ".join(stale), file=sys.stderr)
            print("Run: python scripts/generate_models.py", file=sys.stderr)
            return 1
        print("Models are up to date with the OpenAPI spec.")
        return 0

    print(f"Generated {len(rendered)} module(s): " + ", ".join(sorted(rendered)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
