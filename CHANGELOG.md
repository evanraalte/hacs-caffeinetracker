# Changelog

All notable changes to this project will be documented in this file.
## [0.2.2] - 2026-04-26

### Bug Fixes

- Sort manifest keys, fix services.yaml targets, add CONFIG_SCHEMA, clean hacs.json
- Use entity target filter in services.yaml (hassfest rejects device filter)
- Add brand/icon.png for HACS brands validation

## [0.2.1] - 2026-04-26

### Dependencies

- **deps**: Update codecov/codecov-action action to v6
- **deps**: Update astral-sh/setup-uv action to v8
- **deps**: Update actions/checkout action to v6
- **deps**: Pin orhun/git-cliff-action action to f50e115

### Documentation

- Add conventional commit conventions to README, CLAUDE.md, and GEMINI.md

## [0.2.0] - 2026-04-21

### Bug Fixes

- Update renovate configuration to use best-practices preset
- Quote git commit command and auto-push tags in release task

### Dependencies

- **deps**: Update astral-sh/setup-uv action to v7
- **deps**: Pin dependencies

### Features

- Update dashboard preview in README
- Replace release-please with git-cliff

## [0.1.3] - 2026-04-21

### Features

- Add resized icons for HACS and Home Assistant integration

## [0.1.1] - 2026-04-21

### Bug Fixes

- Migrate entity services to domain services and add documentation
- Resolve CI dependency resolution issues
- Resolve CI type errors while maintaining compatibility
- CI dependency conflicts and HA pinning
- Taskfile syntax error in release task
- Taskfile yaml syntax error in release description

### Documentation

- Update github account and service targeting examples
- Include all sensors in dashboard examples

### Features

- Add sensor for number of consumptions today

### Style

- Fix import sorting and formatting

