# Caffeine Tracker — Gemini context

## Build & Test
- **Install**: `task install` (uses `uv`)
- **Test**: `task test`
- **Lint/Format**: `task lint`, `task format`
- **Deploy**: `task deploy` (rsync to HA)

## Architecture
- **`coordinator.py`**: Pure computation (decay/absorption) + HA DataUpdateCoordinator.
- **`__init__.py`**: Entry point, domain-level service registration in `async_setup`.
- **`sensor.py`**: Entity definitions. `CaffeineCurrentSensor` is the primary entity.
- **`const.py`**: Constants, domain, and default settings.
- **`services.yaml`**: UI definitions for services.

## Service handling
- Registered at the **domain level**.
- Use `service.async_extract_config_entry_ids(call)` (non-deprecated) for once-per-profile targeting.
- Supported: `log_consumption`, `remove_last_consumption`, `remove_consumption`, `clear_today`.
- **Target the Device** for reliable once-per-profile logging.

## Testing
- Tests in `tests/`.
- `test_sensor.py`: integration tests, service calls, device targeting.
- `test_coordinator.py`: pure logic and computation.
- Run with `uv run pytest`.

## Commit conventions
Always use [Conventional Commits](https://www.conventionalcommits.org/). Commit type determines changelog inclusion and version bumps.

| Prefix | Use for | In changelog |
|--------|---------|--------------|
| `feat:` | New user-facing feature | Yes — Features |
| `fix:` | Bug fix | Yes — Bug Fixes |
| `docs:` | Documentation only | Yes — Documentation |
| `perf:` | Performance improvement | Yes — Performance |
| `refactor:` | Internal refactor, no behaviour change | Yes — Refactoring |
| `test:` | Adding or updating tests | Yes — Testing |
| `chore(deps):` | Dependency updates | Yes — Dependencies |
| `chore:` | Maintenance, tooling, config | No |
| `ci:` | CI/CD pipeline changes | No |

Use `feat!:` or a `BREAKING CHANGE:` footer for breaking changes. Never use generic messages like "update", "fix stuff", or "WIP".
