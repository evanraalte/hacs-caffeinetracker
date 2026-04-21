# Caffeine Tracker for Home Assistant

[![HACS](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://hacs.xyz)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Track caffeine in your body using pharmacokinetic modelling. Supports multiple
people (household), configurable half-life, and a sleep-safe threshold sensor.

## Features

- **Caffeine Level** sensor — current mg in your body, updated every minute using
  exponential decay
- **Consumed Today** sensor — total mg since local midnight
- **Sleep Safe At** sensor — timestamp when your level will drop below your
  configured threshold
- Per-person profiles with individual half-life and sleep-safe settings
- Survives restarts (events stored in HA `.storage/`)
- Services for logging, undoing, and clearing intakes
- Log from Apple Watch via the HA companion app (or iOS Shortcuts for Apple Health sync)

## Installation

### HACS (recommended)

1. In HACS → **Integrations** → **⋮** → **Custom repositories**
2. Add `https://github.com/erikvanraalte/ha-caffeine-tracker` as an
   **Integration**
3. Install **Caffeine Tracker**
4. Restart Home Assistant

### Manual

Copy `custom_components/caffeine_tracker/` into your HA
`config/custom_components/` directory and restart.

## Setup

1. **Settings → Devices & Services → Add Integration → Caffeine Tracker**
2. Enter a name (e.g. *Erik*) and configure:
   - **Half-life** — how long (hours) for caffeine to halve in your body.
     Default 5 h. Range 3–10 h. Faster metabolisers: 3–4 h, slower: 6–7 h.
   - **Sleep-safe threshold** — the mg level at which you consider it safe to
     sleep. Default 50 mg.
3. Repeat for additional household members.

Each person gets their own device with three sensor entities.

## Sensors

| Entity | Description | Unit |
|--------|-------------|------|
| `sensor.<name>_caffeine_level` | Current caffeine in body | mg |
| `sensor.<name>_caffeine_consumed_today` | Total since midnight | mg |
| `sensor.<name>_sleep_safe_at` | When level ≤ threshold | timestamp |

The `caffeine_level` sensor carries an `events` attribute — a list of all active
intake events with `id`, `timestamp`, `mg`, and `label` fields.

## Services

All services target a sensor entity (`entity_id`) to identify the person.

### `caffeine_tracker.log_consumption`

Log a caffeine intake.

| Field | Required | Description |
|-------|----------|-------------|
| `preset` | one of | Preset drink name (see list below) |
| `mg` | one of | Custom caffeine amount in mg |
| `label` | no | Display name for the event |
| `timestamp` | no | ISO 8601 datetime (defaults to now) |

Either `preset` or `mg` must be provided. If both are given, `preset` wins.

**Example (YAML action):**
```yaml
action: caffeine_tracker.log_consumption
target:
  entity_id: sensor.erik_caffeine_level
data:
  preset: espresso
```

### `caffeine_tracker.remove_last_consumption`

Undo the most recent intake event.

### `caffeine_tracker.remove_consumption`

Remove a specific event by ID (IDs visible in the `events` attribute).

| Field | Required | Description |
|-------|----------|-------------|
| `event_id` | yes | UUID of the event to remove |

### `caffeine_tracker.clear_today`

Remove all events logged since local midnight.


## Dashboard

See **[docs/lovelace.md](docs/lovelace.md)** for all card YAML, including:

- **Caffeine graph** — mini-graph-card with colour thresholds (green → red)
- **Status chips** — current level, today's total, sleep-safe time (mushroom)
- **Quick-log buttons** — mushroom template cards per drink
- **Full stack** — combined vertical card ready to drop on any view

Required HACS frontend cards: [mini-graph-card](https://github.com/kalkih/mini-graph-card), [Mushroom](https://github.com/piitaya/lovelace-mushroom), [card-mod](https://github.com/thomasloven/lovelace-card-mod) (optional, for styling).

## Logging from Apple Watch / iPhone

Two options depending on whether you want to stay entirely inside the HA
ecosystem or also write to Apple Health.

### Option A — HA Companion app on Apple Watch (recommended)

The [Home Assistant companion app](https://companion.home-assistant.io) has a
native Apple Watch app. You create HA scripts for your common drinks, add them
as Watch actions, and tap them from your wrist — no tokens, no Shortcuts, no
extra setup.

**1. Create scripts in HA** (`configuration.yaml` or via the Scripts UI):

```yaml
script:
  caffeine_espresso_erik:
    alias: "Espresso - Erik"
    icon: mdi:coffee
    sequence:
      - action: caffeine_tracker.log_consumption
        target:
          entity_id: sensor.erik_caffeine_level
        data:
          mg: 80
          label: Espresso

  caffeine_drip_coffee_erik:
    alias: "Filter coffee - Erik"
    icon: mdi:coffee-maker
    sequence:
      - action: caffeine_tracker.log_consumption
        target:
          entity_id: sensor.erik_caffeine_level
        data:
          mg: 95
          label: Filter coffee

  caffeine_undo_erik:
    alias: "Undo last - Erik"
    icon: mdi:undo
    sequence:
      - action: caffeine_tracker.remove_last_consumption
        target:
          entity_id: sensor.erik_caffeine_level
```

Repeat for each household member (different `entity_id`).

**2. Add scripts to the Watch app:**

On your iPhone:
1. Open the **Home Assistant** app → **Settings** (bottom right)
2. **Companion App → Apple Watch**
3. Tap **+** and add each script you created above
4. Arrange them in the order you want on the watch

**3. Use it:**

Raise your wrist → open the HA Watch app → tap the drink. Done. The sensor
updates within seconds.

> The Watch app works both on local Wi-Fi and remotely via
> [Nabu Casa](https://www.nabucasa.com) / your own remote access setup. No
> long-lived tokens or API calls to manage.

---

### Option B — iOS Shortcuts (if you also want Apple Health sync)

Use this if you want caffeine logged in **both** HA and Apple Health, or if you
want automations triggered by a third-party app writing to HealthKit.

**Log on demand (also adds to Apple Health):**

1. Open **Shortcuts** → **+** → name it *Espresso*
2. Add action: **Log Health Sample** → **Dietary Caffeine** → `80` mg
3. Add action: **Get Contents of URL**
   - Method: `POST`
   - URL: `http://<ha-ip>:8123/api/services/caffeine_tracker/log_consumption`
   - Headers: `Authorization: Bearer <long-lived-token>`
   - Request Body: JSON
     ```json
     { "entity_id": "sensor.erik_caffeine_level", "preset": "espresso" }
     ```
4. Add to Home Screen or invoke via Siri.

**Sync when any app writes to Apple Health (advanced):**

1. **Shortcuts → Automation → + → Health → Dietary Caffeine → Is Added**
2. Add action: **Get Health Samples → Dietary Caffeine → Latest 1**
3. Add action: **Get Contents of URL** (same as above, use the sample's mg value
   via Magic Variables instead of a hardcoded amount)

> iOS Health automations only fire when a sample is written by an app — not
> when you edit manually in the Health app.

**Generating a long-lived access token:**
In HA: **Profile → Long-Lived Access Tokens → Create Token**.

---

### Option C — HA Scripts on Apple Watch

The simplest possible logging flow: one tap on your wrist, no phone needed.
Scripts live entirely in HA — no tokens, no HTTP calls to configure.

**1. Add the scripts to HA**

Copy [`docs/example_scripts.yaml`](docs/example_scripts.yaml) into your HA
config, or add individual scripts via
**Settings → Automations & Scenes → Scripts → + Add Script → Create from YAML**.

Example for a single espresso script:

```yaml
caffeine_espresso_erik:
  alias: "Espresso - Erik"
  icon: mdi:coffee
  sequence:
    - action: caffeine_tracker.log_consumption
      target:
        entity_id: sensor.erik_caffeine_level
      data:
        preset: espresso
```

See [`docs/example_scripts.yaml`](docs/example_scripts.yaml) for a full set
covering espresso, filter coffee, cappuccino, cold brew, energy drink, and undo.

**2. Add scripts to the Watch app**

On your iPhone: **Home Assistant app → Settings → Companion App → Apple Watch**
→ tap **+** → select the scripts you want on your wrist.

**3. Use it**

Raise wrist → open HA app → tap drink. Done.

---

## Dashboard

See **[docs/lovelace.md](docs/lovelace.md)** for copy-paste YAML for all cards.

## Background: the pharmacokinetics model

Caffeine follows first-order elimination:

```
level(t) = dose × 0.5^(t / half_life)
```

Multiple doses are summed:

```
level(now) = Σᵢ doseᵢ × 0.5^((now − tᵢ) / half_life)
```

The sleep-safe timestamp solves the above for *t*:

```
t_safe = t_now + half_life × log₂(level_now / threshold)
```

Events older than `7 × half_life` (< 1% of original dose) are pruned
automatically.

> Real caffeine metabolism is bi-exponential and varies with genetics (CYP1A2),
> pregnancy, smoking, and liver function. The configurable half-life is a
> personalisation knob — start at 5 h and adjust based on how you feel.

## Development

### Prerequisites

- [uv](https://docs.astral.sh/uv/) — `brew install uv`
- [Task](https://taskfile.dev) — `brew install go-task`

```bash
git clone https://github.com/erikvanraalte/ha-caffeine-tracker
cd ha-caffeine-tracker
task install   # sets up .venv with all dev deps
task test      # run the full test suite
task check     # lint + typecheck + tests
```

### Testing in your own HA instance

Three deployment flows depending on your setup — pick the one that fits.

---

#### Option A — rsync over SSH (simplest)

Works for any setup where you can SSH into the machine hosting HA's config files
(HA OS, Docker on a server, supervised, etc.).

**1. Set up passwordless SSH from your dev machine:**
```bash
ssh-copy-id user@your-server
```

**2. Create `.env.local`** in the project root (gitignored, auto-loaded by
the Taskfile):
```bash
# .env.local — Docker on a server example
HA_HOST=your-server          # IP or hostname
HA_USER=youruser             # SSH user
HA_CONFIG_PATH=/path/to/ha/config   # where the HA config volume is mounted on the server
HA_TOKEN=your-long-lived-token      # Profile → Long-Lived Access Tokens
```

**3. First deploy:**
```bash
task deploy
```

**4. Restart HA once** (required on first install of any custom component):
```bash
# In the HA UI: Settings → System → Restart
# Or on the server:
docker restart homeassistant
```

**5. Install the integration:**
1. **Settings → Devices & Services → + Add Integration → Caffeine Tracker**
2. Enter a name, half-life, sleep threshold → **Submit**
3. Repeat for additional household members

---

#### Option B — auto-deploy on save (best for active iteration)

Same SSH setup as Option A, but file changes are pushed automatically every
time you save.

```bash
brew install fswatch   # one-time
task deploy:watch      # reads .env.local automatically
```

Leave that terminal running. Every time you save a file in
`custom_components/caffeine_tracker/`, it rsync's to the server automatically.
After each sync, reload the integration in the HA UI:
**Settings → Devices & Services → Caffeine Tracker → ⋮ → Reload**

Or via the Taskfile (needs `HA_TOKEN` in `.env.local`):
```bash
task reload
```

---

#### Option C — symlink on server (cleanest for multi-machine work)

Clone the repo directly on your server and symlink it into the HA config.
No file sync needed — a `git pull` on the server is the deploy step.

```bash
# On the server:
git clone https://github.com/erikvanraalte/ha-caffeine-tracker
ln -s /path/to/ha-caffeine-tracker/custom_components/caffeine_tracker \
      /path/to/ha/config/custom_components/caffeine_tracker
docker restart homeassistant
```

Dev cycle from your local machine:
```bash
# Local: commit + push
git push

# Server: pull + reload
ssh user@your-server "cd ha-caffeine-tracker && git pull"
# then reload integration in HA UI
```

---

#### Smoke test checklist

- [ ] All three sensors appear under the new device
- [ ] Call `caffeine_tracker.log_consumption` with `preset: espresso` targeting
  `sensor.<name>_caffeine_level` — level should jump to ~80 mg
- [ ] Wait a minute — level should tick down slightly
- [ ] `sensor.<name>_sleep_safe_at` shows a future timestamp
- [ ] Call `caffeine_tracker.remove_last_consumption` — level returns to 0
- [ ] Options flow: Settings → Devices & Services → Caffeine Tracker → Configure
  → change half-life → Save — integration reloads with new value
- [ ] Add a second person profile — verify two separate devices appear

### Useful Taskfile tasks

| Task | What it does |
|------|-------------|
| `task install` | Set up `.venv` with all dev deps |
| `task test` | Run full test suite |
| `task test:unit` | Run only pure math tests (fast, no HA mock) |
| `task check` | Lint + typecheck + tests |
| `task fix` | Auto-fix lint issues + reformat |
| `task deploy` | rsync component to HA over SSH |
| `task clean` | Remove generated artifacts |

### Publishing to HACS

#### Phase 1 — Public GitHub repo

1. Create a public repo on GitHub (e.g. `ha-caffeine-tracker`)
2. Push the code:
   ```bash
   git remote add origin https://github.com/youruser/ha-caffeine-tracker.git
   git push -u origin main
   ```
3. Update the `documentation` and `issue_tracker` URLs in
   `custom_components/caffeine_tracker/manifest.json` to point at your repo.

#### Phase 2 — Create a release

HACS installs from GitHub releases, not branches.

1. Tag and push a release:
   ```bash
   git tag v0.1.0
   git push origin v0.1.0
   ```
2. On GitHub: **Releases → Draft a new release** → select tag `v0.1.0` →
   publish. The tag must match the `version` field in `manifest.json`.

Automate future releases with `.github/workflows/release.yml` (optional but
recommended — generates a release from a tag push).

#### Phase 3 — Brand assets (required for HACS default, optional for custom repos)

1. Fork [home-assistant/brands](https://github.com/home-assistant/brands)
2. Add a directory `custom_components/caffeine_tracker/` containing:
   - `icon.png` — 256×256 px, transparent background
   - `icon@2x.png` — 512×512 px, same design
   - `logo.png` — 256×256 px (can be same as icon)
   - `logo@2x.png` — 512×512 px
3. Open a PR — brands PRs are reviewed by the HA team and take a few days.
   The PR **must be merged** before you can submit to the HACS default list.

#### Phase 4 — Add as a custom HACS repository (shareable immediately)

Anyone (including yourself for testing) can install it before the brands PR
merges:

1. In HA: **HACS → ⋮ → Custom repositories**
2. URL: `https://github.com/youruser/ha-caffeine-tracker`
3. Category: **Integration**
4. Click **Add** → the integration appears in HACS and can be installed normally

This is a good way to share with early testers before the official listing.

#### Phase 5 — Submit to HACS default list

Once the brands PR is merged and you're happy with the integration:

1. Open an issue at [hacs/default](https://github.com/hacs/default) using the
   **Add new default repository** template
2. Fill in the checklist — HACS will run automated checks against your repo
3. A maintainer reviews and merges — the integration is then available to all
   HACS users without needing to add a custom repository

**HACS automated checks include:** valid `hacs.json`, valid `manifest.json`,
GitHub release present, no hardcoded credentials, README exists. Run
`task check` to catch code issues before submitting.

## Contributing

PRs welcome. Run `task check` before opening one.

## License

MIT — see [LICENSE](LICENSE).
