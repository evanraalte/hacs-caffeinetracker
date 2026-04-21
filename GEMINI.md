# Gemini CLI - Caffeine Tracker Project Status

## Project Overview
This is a Home Assistant custom integration for tracking caffeine consumption. It calculates current caffeine levels using an exponential decay model with optional absorption delay.

## Current State
- **Domain Services Fix**: Migrated entity services (platform-level) to domain services (integration-level).
- **Deduplication**: Fixed the issue where targeting a device with multiple entities caused multiple consumption logs. The integration now uses `async_extract_config_entry_ids` in the service handler to fire once per profile.
- **New Sensor**: Added a "Consumptions Today" sensor to track the number of intake events.
- **Cleanup**: Removed unused feature flags (`CaffeineEntityFeature`) and redundant logic in `coordinator.py`.
- **Testing**: All 34 tests pass, including a new regression test for device targeting and the new count sensor.

## Technical Details
- **Services**: Registered in `async_setup` in `__init__.py`.
- **Targeting**: Supports `device_id` and `entity_id`. Device targeting is preferred.
- **Coordinator**: Manages state, storage, and decay logic.
- **Sensors**: Current level, Consumed today, Consumptions today, Sleep safe at, and Peak level (optional).

## Next Steps
- **Validation**: Confirm `log_consumption` fires exactly once in a real HA environment after a restart.
- **UI Improvements**: Potentially add more sensor attributes or interactive elements.
