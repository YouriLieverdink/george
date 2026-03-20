"""TUI main loop — prompt_toolkit + rich REPL."""

from __future__ import annotations

import atexit
import sys

from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.history import InMemoryHistory
from rich.console import Console

from george import claude, persona, files
from george.commands import checkin, debrief, plan, review, status, chat, raceweek, postrace

COMMANDS = {
    "/checkin": checkin.run,
    "/debrief": debrief.run,
    "/plan": plan.run,
    "/review": review.run,
    "/status": status.run,
    "/chat": chat.run,
    "/raceweek": raceweek.run,
    "/postrace": postrace.run,
    "/help": None,  # handled inline
    "/quit": None,
    "/exit": None,
}

COMMAND_DESCRIPTIONS = {
    "/checkin": "Daily readiness check → adapted session",
    "/debrief": "Post-session logging + feedback",
    "/plan": "Generate next week's training plan",
    "/review": "Weekly/monthly trend analysis + plan adaptation",
    "/status": "Quick dashboard — phase, fitness, next session",
    "/chat": "Freeform conversation with George",
    "/raceweek": "Race week prep — schedule, pacing, mental",
    "/postrace": "Post-race debrief + recovery plan",
    "/help": "Show commands",
    "/quit": "Exit George",
}


class Session:
    """Holds state for one TUI session."""

    def __init__(self):
        self.console = Console()
        self.conversation = claude.Conversation()
        self.system = persona.build_system()
        self._exit_registered = False

    def register_exit_handler(self):
        if not self._exit_registered:
            atexit.register(self._on_exit)
            self._exit_registered = True

    def _on_exit(self):
        """Generate and save conversation summary on exit."""
        if self.conversation.session_id is None:
            return

        try:
            self.console.print("\n[dim]Saving conversation summary...[/dim]")
            summary = self.conversation.send_summary(self.system)
            files.write_conversation(
                "session",
                summary.split("\n")[0][:120],
                summary,
            )
            self.console.print("[dim]Saved.[/dim]")
        except Exception as e:
            self.console.print(f"[dim]Could not save summary: {e}[/dim]")


def show_help(console: Console) -> None:
    console.print("\n[bold]George — AI Endurance Coach[/bold]\n")
    for cmd, desc in COMMAND_DESCRIPTIONS.items():
        console.print(f"  [bold cyan]{cmd:<12}[/bold cyan] {desc}")
    console.print()
    console.print("  Type anything without a slash to chat with George.\n")


def show_welcome(console: Console) -> None:
    console.print("\n[bold]George[/bold] — AI Endurance Coach")
    console.print("[dim]Type /help for commands, or just start talking.[/dim]\n")


def run() -> None:
    """Main TUI entry point."""
    console = Console()
    session = Session()
    session.register_exit_handler()

    show_welcome(console)

    completer = WordCompleter(list(COMMANDS.keys()), sentence=True)
    prompt_session = PromptSession(
        history=InMemoryHistory(),
        completer=completer,
    )

    while True:
        try:
            user_input = prompt_session.prompt("you > ").strip()
        except (KeyboardInterrupt, EOFError):
            console.print("\n[dim]Tot morgen.[/dim]")
            break

        if not user_input:
            continue

        # Check for slash commands
        cmd = user_input.split()[0].lower() if user_input.startswith("/") else None

        if cmd in ("/quit", "/exit"):
            console.print("[dim]Tot morgen.[/dim]")
            break

        if cmd == "/help":
            show_help(console)
            continue

        if cmd and cmd in COMMANDS and COMMANDS[cmd] is not None:
            try:
                COMMANDS[cmd](session)
            except KeyboardInterrupt:
                console.print("\n[dim]Interrupted.[/dim]")
            except Exception as e:
                console.print(f"\n[red]Error: {e}[/red]")
            continue

        if cmd and cmd.startswith("/"):
            console.print(f"[dim]Unknown command: {cmd}. Type /help for options.[/dim]")
            continue

        # Default: chat with George
        try:
            chat.run(session, initial_message=user_input)
        except KeyboardInterrupt:
            console.print("\n[dim]Interrupted.[/dim]")
        except Exception as e:
            console.print(f"\n[red]Error: {e}[/red]")
