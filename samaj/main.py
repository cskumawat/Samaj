"""Application entrypoint for Samaj."""

from __future__ import annotations

import argparse
from collections.abc import Sequence
from pathlib import Path

from samaj.app import run_doctor, run_gui


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="samaj",
        description="Launch the Samaj safety-first GUI shell.",
    )
    parser.add_argument(
        "--doctor",
        action="store_true",
        help="Check current runtime configuration without launching the GUI.",
    )
    parser.add_argument(
        "--settings-path",
        type=Path,
        default=None,
        help="Optional settings JSON path for local testing.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.doctor:
        return run_doctor(settings_path=args.settings_path)

    return run_gui(settings_path=args.settings_path)


if __name__ == "__main__":
    raise SystemExit(main())
