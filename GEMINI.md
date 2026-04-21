# Gemini CLI - Caffeine Tracker Project Status

## Project Overview
This is a Home Assistant custom integration for tracking caffeine consumption. It calculates current caffeine levels using an exponential decay model with optional absorption delay.

## Current State
- **Domain Services Fix**: Migrated entity services (platform-level) to domain services (integration-level).
- **Deduplication**: Fixed the issue where targeting a device with multiple entities caused multiple consumption logs. The integration now uses `async_extract_config_entry_ids` in the service handler to fire once per profile.
- **Cleanup**: Removed unused feature flags (`CaffeineEntityFeature`) and redundant logic in `coordinator.py`.
- **Testing**: All 33 tests pass, including a new regression test for device targeting.

## Technical Details
- **Services**: Registered in `async_setup` in `__init__.py`.
- **Targeting**: Supports `device_id` and `entity_id`.
- **Coordinator**: Manages state, storage, and decay logic.
- **Sensors**: Current level, Consumed today, Sleep safe at, and Peak level (optional).

## Next Steps
- **Restart HA**: A full restart is recommended to clear old entity service registrations.
- **Validation**: Confirm `log_consumption` fires exactly once in a real HA environment.
- **UI Improvements**: Potentially add more sensor attributes or interactive elements.
