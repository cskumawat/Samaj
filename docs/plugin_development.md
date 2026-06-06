# Plugin Development

Plugin execution is planned for Phase 12 and is not implemented in the current
foundation phase.

Future plugins must declare:

- Name
- Version
- Author
- Description
- Required permissions
- Supported actions
- Risk level
- Input schema
- Output schema
- Safe Mode behavior

Unsafe plugins must be disabled by default and must not bypass scope enforcement.
