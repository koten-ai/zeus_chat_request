#!/usr/bin/env python3
"""Compare mode packs after neutralizing mode tokens (clone detector).

Usage:
  python3 scripts/diff_modes.py --base 5.1
  python3 scripts/diff_modes.py --base 5.1 --fail-if-clone
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

MODES = [
    "analytics",
    "auto",
    "code",
    "custom",
    "fraud",
    "open",
    "private",
    "regulated",
    "research",
    "tenant",
]

# Keywords expected in overlays (case-insensitive)
EXPECT = {
    "fraud": ["device", "weak", "iban", "address"],
    "research": ["doi", "paper", "author", "cit"],
    "code": ["function", "class", "call", "import"],
    "regulated": ["redact", "pii", "0.80", "tenant", "privacy", "sensitive"],
    "tenant": ["tenant", "wall", "cross-tenant", "hard"],
    "private": ["user", "personal", "backlink", "corpus"],
    "open": ["noise", "super-node", "serendip"],
    "auto": ["onboarding", "propose", "recommend", "discovery", "hand"],
    "custom": ["operator", "conservative", "escape", "inject"],
    "analytics": ["real link", "noise", "0.50", "degree", "safe default", "bi"],
}


def system_content(doc: dict) -> str:
    for m in doc.get("messages") or []:
        if isinstance(m, dict) and m.get("role") == "system":
            return str(m.get("content") or "")
    return ""


def neutralize(text: str, mode: str) -> str:
    t = text
    t = re.sub(re.escape(mode), "MODE", t, flags=re.I)
    t = re.sub(r"base-[\d.]+", "BASE", t)
    return t


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--base", default="5.1", help="Pack id e.g. 5.1 (folder v2/base/base-5.1)")
    ap.add_argument("--repo-root", default=".")
    ap.add_argument(
        "--fail-if-clone",
        action="store_true",
        help="Exit 1 if a non-auto mode lacks MODE_OVERLAY marker or expected keywords",
    )
    ap.add_argument(
        "--report",
        default="",
        help="Optional path to write markdown report",
    )
    args = ap.parse_args(argv)
    root = Path(args.repo_root).resolve()
    bare = str(args.base).removeprefix("base-")
    pack = root / "v2" / "base" / f"base-{bare}" / "min"

    rows = []
    errors: list[str] = []
    sigs: dict[str, list[str]] = defaultdict(list)

    for mode in MODES:
        path = pack / f"chat_request_{mode}_base-{bare}.json"
        if not path.is_file():
            errors.append(f"missing {path.name}")
            continue
        doc = json.loads(path.read_text())
        content = system_content(doc)
        neut = neutralize(content, mode)
        sig = hashlib.sha256(neut.encode()).hexdigest()[:16]
        sigs[sig].append(mode)
        has_overlay = "## Mode:" in content or f"## Mode: {mode}" in content
        low = content.lower()
        expect = EXPECT.get(mode, [])
        hits = [k for k in expect if k.lower() in low]
        miss = [k for k in expect if k.lower() not in low]
        rows.append(
            {
                "mode": mode,
                "len": len(content),
                "sig": sig,
                "overlay": has_overlay,
                "hits": hits,
                "miss": miss,
            }
        )
        if args.fail_if_clone and mode != "analytics":
            if not has_overlay:
                errors.append(f"{mode}: missing ## Mode: overlay section")
            # require at least 2 keyword hits for specialty modes
            if mode in ("fraud", "research", "code", "regulated", "auto") and len(hits) < 2:
                errors.append(f"{mode}: weak keyword hits {hits} missing {miss}")

    # clone clusters (same neutralized system prompt)
    print(f"base-{bare} mode system-prompt report")
    print(f"{'mode':12} {'len':>6} overlay  sig              keywords")
    for r in rows:
        print(
            f"{r['mode']:12} {r['len']:6} {'yes' if r['overlay'] else 'NO ':3}  {r['sig']}  hits={r['hits']}"
        )

    print("\nidentical neutralized system signatures:")
    any_clone = False
    for sig, modes in sigs.items():
        if len(modes) > 1:
            any_clone = True
            print(f"  {sig}: {modes}")
            if args.fail_if_clone:
                errors.append(f"clone cluster: {modes}")
    if not any_clone:
        print("  (none)")

    if args.report:
        lines = [
            f"# Mode diff report base-{bare}",
            "",
            "| mode | len | overlay | sig | keyword hits | missing |",
            "| --- | ---: | --- | --- | --- | --- |",
        ]
        for r in rows:
            lines.append(
                f"| {r['mode']} | {r['len']} | {r['overlay']} | `{r['sig']}` | {', '.join(r['hits']) or '—'} | {', '.join(r['miss']) or '—'} |"
            )
        Path(args.report).write_text("\n".join(lines) + "\n")
        print(f"\nwrote {args.report}")

    if errors:
        print(f"\nFAIL ({len(errors)}):", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1
    print("\nOK mode differentiation checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
