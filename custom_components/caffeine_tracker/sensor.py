"""Sensor platform for Caffeine Tracker."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from homeassistant.components.sensor import (
    SensorEntity,
)
from homeassistant.components.sensor.const import (
    SensorDeviceClass,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
import homeassistant.util.dt as dt_util

from .const import (
    ATTR_EVENTS,
    DOMAIN,
)
from .coordinator import CaffeineCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator: CaffeineCoordinator = hass.data[DOMAIN][entry.entry_id]

    entities: list[_CaffeineBase] = [
        CaffeineCurrentSensor(coordinator, entry),
        CaffeineConsumedTodaySensor(coordinator, entry),
        CaffeineConsumedTodayCountSensor(coordinator, entry),
        CaffeineSleepSafeAtSensor(coordinator, entry),
    ]
    if coordinator.enable_absorption:
        entities.append(CaffeinePeakSensor(coordinator, entry))
    async_add_entities(entities)


class _CaffeineBase(CoordinatorEntity[CaffeineCoordinator], SensorEntity):
    """Base entity for Caffeine Tracker sensors."""

    _attr_has_entity_name = True

    def __init__(self, coordinator: CaffeineCoordinator, entry: ConfigEntry) -> None:
        super().__init__(coordinator)
        self._entry = entry

    @property
    def device_info(self) -> DeviceInfo:
        return DeviceInfo(
            identifiers={(DOMAIN, self.coordinator.entry_id)},
            name=self.coordinator.person_name,
            manufacturer="Caffeine Tracker",
            model="Virtual Caffeine Monitor",
        )


class CaffeineCurrentSensor(_CaffeineBase):
    """Current caffeine level in the body (mg)."""

    _attr_native_unit_of_measurement = "mg"
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_icon = "mdi:coffee"
    _attr_suggested_display_precision = 0
    _attr_translation_key = "current"

    def __init__(self, coordinator: CaffeineCoordinator, entry: ConfigEntry) -> None:
        super().__init__(coordinator, entry)
        self._attr_unique_id = f"{entry.entry_id}_current"

    @property
    def native_value(self) -> float | None:
        return self.coordinator.data.current_mg if self.coordinator.data else None

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        if not self.coordinator.data:
            return {}
        return {
            ATTR_EVENTS: [
                {
                    "id": e.id,
                    "timestamp": e.timestamp.isoformat(),
                    "mg": e.mg,
                    "label": e.label,
                }
                for e in self.coordinator.data.events
            ]
        }


class CaffeineConsumedTodaySensor(_CaffeineBase):
    """Total caffeine consumed since local midnight (mg)."""

    _attr_native_unit_of_measurement = "mg"
    _attr_state_class = SensorStateClass.TOTAL_INCREASING
    _attr_icon = "mdi:coffee-maker"
    _attr_suggested_display_precision = 0
    _attr_translation_key = "consumed_today"

    def __init__(self, coordinator: CaffeineCoordinator, entry: ConfigEntry) -> None:
        super().__init__(coordinator, entry)
        self._attr_unique_id = f"{entry.entry_id}_consumed_today"

    @property
    def native_value(self) -> float | None:
        return (
            self.coordinator.data.consumed_today_mg if self.coordinator.data else None
        )


class CaffeineConsumedTodayCountSensor(_CaffeineBase):
    """Number of caffeine events since local midnight."""

    _attr_state_class = SensorStateClass.TOTAL_INCREASING
    _attr_icon = "mdi:counter"
    _attr_translation_key = "consumed_today_count"

    def __init__(self, coordinator: CaffeineCoordinator, entry: ConfigEntry) -> None:
        super().__init__(coordinator, entry)
        self._attr_unique_id = f"{entry.entry_id}_consumed_today_count"

    @property
    def native_value(self) -> int | None:
        return (
            self.coordinator.data.consumed_today_count
            if self.coordinator.data
            else None
        )


class CaffeineSleepSafeAtSensor(_CaffeineBase):
    """Timestamp when caffeine drops below the sleep-safe threshold."""

    _attr_device_class = SensorDeviceClass.TIMESTAMP
    _attr_icon = "mdi:sleep"
    _attr_translation_key = "sleep_safe_at"

    def __init__(self, coordinator: CaffeineCoordinator, entry: ConfigEntry) -> None:
        super().__init__(coordinator, entry)
        self._attr_unique_id = f"{entry.entry_id}_sleep_safe_at"

    @property
    def native_value(self) -> datetime | None:
        if not self.coordinator.data:
            return None
        safe_at = self.coordinator.data.sleep_safe_at
        # None means already below threshold — return now so HA shows a valid
        # timestamp and automations can compare against it (it will be in the past).
        return safe_at if safe_at is not None else dt_util.utcnow()


class CaffeinePeakSensor(_CaffeineBase):
    """Estimated peak caffeine level accounting for absorption delay."""

    _attr_native_unit_of_measurement = "mg"
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_icon = "mdi:trending-up"
    _attr_suggested_display_precision = 0
    _attr_translation_key = "peak"

    def __init__(self, coordinator: CaffeineCoordinator, entry: ConfigEntry) -> None:
        super().__init__(coordinator, entry)
        self._attr_unique_id = f"{entry.entry_id}_peak"

    @property
    def native_value(self) -> float | None:
        if not self.coordinator.data:
            return None
        return self.coordinator.data.peak_mg
