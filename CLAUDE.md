# Caffeine Tracker Integration

## Build & Test
- **Install**: `task install` (uses `uv`)
- **Test**: `task test` (runs all 34 tests)
- **Lint/Format**: `task lint`, `task format`
- **Deploy**: `task deploy` (rsync to HA)
- **Reload**: `task reload` (HA API call)
- **Restart**: `task restart` (Full HA restart via API)

## Architecture
- **`coordinator.py`**: Heart of the integration. Pure computation functions for decay/absorption logic + HA DataUpdateCoordinator.
- **`__init__.py`**: Entry point. Domain-level service registrations occur here in `async_setup`.
- **`sensor.py`**: Entity definitions. `CaffeineCurrentSensor` is the primary entity.
- **`const.py`**: Constants, domain, and default settings.
- **`services.yaml`**: UI definitions for services.

## Service Handling
- Services are registered at the **domain level**.
- They use `service.async_extract_config_entry_ids(call)` (non-deprecated) to ensure a single call per target device/profile.
- Supported services: `log_consumption`, `remove_last_consumption`, `remove_consumption`, `clear_today`.
- **Targeting**: Target the **Device** for reliable once-per-profile logging.

## Testing
- Tests are in `tests/`.
- `test_sensor.py` covers integration tests, service calls, and device targeting.
- `test_coordinator.py` covers pure logic and computation.
- Use `uv run pytest` to execute.
