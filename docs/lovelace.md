# Lovelace Dashboard

Example cards for a caffeine tracking dashboard.

## Prerequisites (install via HACS Frontend)

| Card | What it's used for |
|------|-------------------|
| [mini-graph-card](https://github.com/kalkih/mini-graph-card) | Caffeine decay graph |
| [Mushroom](https://github.com/piitaya/lovelace-mushroom) | Status chips + log buttons |
| [card-mod](https://github.com/thomasloven/lovelace-card-mod) | Custom styling (optional) |

---

## Caffeine graph

Shows the decay curve over the last 12 hours. Line color shifts from green
(sleep-safe) through amber and orange to red as caffeine builds up.

```yaml
type: custom:mini-graph-card
name: Caffeine Level
icon: mdi:coffee
entities:
  - entity: sensor.erik_caffeine_level
    name: Erik
show:
  fill: fade
  icon: true
  legend: false
  extrema: true
  labels: true
  points: false
color_thresholds:
  - value: 0
    color: "#4CAF50"
  - value: 50
    color: "#FFC107"
  - value: 150
    color: "#FF9800"
  - value: 300
    color: "#F44336"
lower_bound: 0
line_width: 3
font_size: 75
height: 120
points_per_hour: 12
hours_to_show: 12
animate: true
card_mod:
  style: |
    ha-card {
      border-radius: 20px;
      background: rgba(255, 255, 255, 0.05);
      backdrop-filter: blur(12px);
      box-shadow: 0 4px 12px rgba(0,0,0,0.4);
      transition: all 0.3s ease;
    }
    ha-card:hover {
      transform: scale(1.01);
      box-shadow: 0 6px 16px rgba(0,0,0,0.6);
    }
```

For multiple household members, add more entities:
```yaml
entities:
  - entity: sensor.erik_caffeine_level
    name: Erik
  - entity: sensor.girlfriend_caffeine_level
    name: Girlfriend
```

---

## Status chips

A compact row showing current level, today's total, and sleep-safe time.

```yaml
type: custom:mushroom-chips-card
chips:
  - type: entity
    entity: sensor.erik_caffeine_level
    icon: mdi:coffee
    icon_color: >-
      {% set v = states('sensor.erik_caffeine_level') | float(0) %}
      {% if v < 50 %}green{% elif v < 150 %}orange{% else %}red{% endif %}
  - type: entity
    entity: sensor.erik_caffeine_consumed_today
    icon: mdi:coffee-maker
    icon_color: brown
  - type: entity
    entity: sensor.erik_sleep_safe_at
    icon: mdi:sleep
    icon_color: blue
```

---

## Quick-log buttons

A 3-column grid of mushroom template cards. Tap to log, long-press Undo to
avoid accidental clears.

Replace `sensor.erik_caffeine_level` with your own entity and adjust `mg`
values to match your actual drinks.

```yaml
type: grid
columns: 3
square: false
cards:
  - type: custom:mushroom-template-card
    primary: Espresso
    secondary: 80 mg
    icon: mdi:coffee
    icon_color: brown
    tap_action:
      action: call-service
      service: caffeine_tracker.log_consumption
      target:
        entity_id: sensor.erik_caffeine_level
      service_data:
        mg: 80
        label: Espresso

  - type: custom:mushroom-template-card
    primary: Filter coffee
    secondary: 95 mg
    icon: mdi:coffee-maker
    icon_color: brown
    tap_action:
      action: call-service
      service: caffeine_tracker.log_consumption
      target:
        entity_id: sensor.erik_caffeine_level
      service_data:
        mg: 95
        label: Filter coffee

  - type: custom:mushroom-template-card
    primary: Cappuccino
    secondary: 80 mg
    icon: mdi:coffee
    icon_color: amber
    tap_action:
      action: call-service
      service: caffeine_tracker.log_consumption
      target:
        entity_id: sensor.erik_caffeine_level
      service_data:
        mg: 80
        label: Cappuccino

  - type: custom:mushroom-template-card
    primary: Cold brew
    secondary: 155 mg
    icon: mdi:cup
    icon_color: deep-orange
    tap_action:
      action: call-service
      service: caffeine_tracker.log_consumption
      target:
        entity_id: sensor.erik_caffeine_level
      service_data:
        mg: 155
        label: Cold brew

  - type: custom:mushroom-template-card
    primary: Energy drink
    secondary: 160 mg
    icon: mdi:lightning-bolt
    icon_color: yellow
    tap_action:
      action: call-service
      service: caffeine_tracker.log_consumption
      target:
        entity_id: sensor.erik_caffeine_level
      service_data:
        mg: 160
        label: Energy drink

  - type: custom:mushroom-template-card
    primary: Undo
    secondary: Last entry
    icon: mdi:undo
    icon_color: red
    tap_action:
      action: call-service
      service: caffeine_tracker.remove_last_consumption
      target:
        entity_id: sensor.erik_caffeine_level
```

---

## Full dashboard stack

Combines the graph, status chips, and log buttons into a single card you can
drop onto any view.

```yaml
type: vertical-stack
cards:
  - type: custom:mini-graph-card
    name: Caffeine Level
    icon: mdi:coffee
    entities:
      - entity: sensor.erik_caffeine_level
        name: Erik
    show:
      fill: fade
      icon: true
      legend: false
      extrema: true
      labels: true
      points: false
    color_thresholds:
      - value: 0
        color: "#4CAF50"
      - value: 50
        color: "#FFC107"
      - value: 150
        color: "#FF9800"
      - value: 300
        color: "#F44336"
    lower_bound: 0
    line_width: 3
    font_size: 75
    height: 120
    points_per_hour: 12
    hours_to_show: 12
    animate: true
    card_mod:
      style: |
        ha-card {
          border-radius: 20px;
          background: rgba(255, 255, 255, 0.05);
          backdrop-filter: blur(12px);
          box-shadow: 0 4px 12px rgba(0,0,0,0.4);
        }

  - type: custom:mushroom-chips-card
    chips:
      - type: entity
        entity: sensor.erik_caffeine_level
        icon: mdi:coffee
        icon_color: >-
          {% set v = states('sensor.erik_caffeine_level') | float(0) %}
          {% if v < 50 %}green{% elif v < 150 %}orange{% else %}red{% endif %}
      - type: entity
        entity: sensor.erik_caffeine_consumed_today
        icon: mdi:coffee-maker
        icon_color: brown
      - type: entity
        entity: sensor.erik_sleep_safe_at
        icon: mdi:sleep
        icon_color: blue

  - type: grid
    columns: 3
    square: false
    cards:
      - type: custom:mushroom-template-card
        primary: Espresso
        secondary: 80 mg
        icon: mdi:coffee
        icon_color: brown
        tap_action:
          action: call-service
          service: caffeine_tracker.log_consumption
          target:
            entity_id: sensor.erik_caffeine_level
          service_data:
            mg: 80
            label: Espresso

      - type: custom:mushroom-template-card
        primary: Filter coffee
        secondary: 95 mg
        icon: mdi:coffee-maker
        icon_color: brown
        tap_action:
          action: call-service
          service: caffeine_tracker.log_consumption
          target:
            entity_id: sensor.erik_caffeine_level
          service_data:
            mg: 95
            label: Filter coffee

      - type: custom:mushroom-template-card
        primary: Undo
        secondary: Last entry
        icon: mdi:undo
        icon_color: red
        tap_action:
          action: call-service
          service: caffeine_tracker.remove_last_consumption
          target:
            entity_id: sensor.erik_caffeine_level
```
