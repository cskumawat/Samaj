"""Typer command-line helper for Samaj."""

from __future__ import annotations

from pathlib import Path

from samaj.app import run_doctor, run_gui

try:
    import typer
except ModuleNotFoundError:  # pragma: no cover - exercised only without dependencies.

    def app() -> None:
        raise SystemExit(run_gui())

else:
    app = typer.Typer(
        add_completion=False,
        no_args_is_help=False,
        help="Samaj helper commands.",
    )

    @app.callback(invoke_without_command=True)
    def default(
        ctx: typer.Context,
        settings_path: Path | None = typer.Option(
            None,
            "--settings-path",
            help="Optional settings JSON path for local testing.",
        ),
    ) -> None:
        if ctx.invoked_subcommand is None:
            raise typer.Exit(run_gui(settings_path=settings_path))

    @app.command()
    def gui(
        settings_path: Path | None = typer.Option(
            None,
            "--settings-path",
            help="Optional settings JSON path for local testing.",
        ),
    ) -> None:
        """Launch the Samaj GUI shell."""

        raise typer.Exit(run_gui(settings_path=settings_path))

    @app.command()
    def doctor(
        settings_path: Path | None = typer.Option(
            None,
            "--settings-path",
            help="Optional settings JSON path for local testing.",
        ),
    ) -> None:
        """Check local runtime settings."""

        raise typer.Exit(run_doctor(settings_path=settings_path))
