"""Location context store with Redis backend.

This module provides ephemeral location storage that auto-expires after 60 seconds
without GPS updates. NO personal addresses (home, work) are stored - only
transient vehicle position data.
"""

import logging
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Optional

logger = logging.getLogger(__name__)


# Redis key format for vehicle location
LOCATION_KEY_PREFIX = "vehicle:location:"
LOCATION_TTL_SECONDS = 60  # Auto-expire after 60s without update


@dataclass
class LocationContext:
    """
    Transient vehicle location data.
    
    NOTE: This stores ONLY current position data that auto-expires.
    NO personal information (home address, work address, city name) is stored.
    """
    latitude: float
    longitude: float
    timestamp: str = ""   # ISO format timestamp

    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.now().isoformat()

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "LocationContext":
        """Create from dictionary."""
        return cls(**data)

    def format_for_query(self) -> str:
        """
        Format location as a human-readable string for query injection.
        
        Returns a concise format suitable for LLM prompts.
        """
        return f"GPS坐标: {self.latitude:.6f}, {self.longitude:.6f}"


class LocationStore:
    """
    Redis-based ephemeral location storage.
    
    Stores current vehicle position with auto-expiry (60 seconds).
    This is NOT persistent storage - location data is transient.
    """
    
    def __init__(self, redis_client):
        """
        Initialize location store with Redis client.
        
        Args:
            redis_client: RedisClient instance
        """
        self._redis = redis_client

    def _get_key(self, vehicle_id: str) -> str:
        """Generate Redis key for vehicle location."""
        return f"{LOCATION_KEY_PREFIX}{vehicle_id}"

    async def save(self, vehicle_id: str, location: LocationContext) -> bool:
        """
        Save vehicle location to Redis with TTL.
        
        Args:
            vehicle_id: Vehicle identifier
            location: LocationContext with current position
            
        Returns:
            True if saved successfully
        """
        try:
            key = self._get_key(vehicle_id)
            await self._redis.set(
                key,
                location.to_dict(),
                ex=LOCATION_TTL_SECONDS
            )
            logger.debug(f"[LocationStore] Saved location for {vehicle_id}: {location}")
            return True
        except Exception as e:
            logger.error(f"[LocationStore] Failed to save location: {e}")
            return False

    async def get(self, vehicle_id: str) -> Optional[LocationContext]:
        """
        Get current vehicle location.
        
        Args:
            vehicle_id: Vehicle identifier
            
        Returns:
            LocationContext if available and not expired, None otherwise
        """
        try:
            key = self._get_key(vehicle_id)
            data = await self._redis.get(key)
            
            if data is None:
                logger.debug(f"[LocationStore] No location found for {vehicle_id}")
                return None
            
            return LocationContext.from_dict(data)
        except Exception as e:
            logger.error(f"[LocationStore] Failed to get location: {e}")
            return None

    async def delete(self, vehicle_id: str) -> bool:
        """
        Delete vehicle location from Redis.
        
        Args:
            vehicle_id: Vehicle identifier
            
        Returns:
            True if deleted successfully
        """
        try:
            key = self._get_key(vehicle_id)
            await self._redis.unlink(key)
            logger.debug(f"[LocationStore] Deleted location for {vehicle_id}")
            return True
        except Exception as e:
            logger.error(f"[LocationStore] Failed to delete location: {e}")
            return False

    async def exists(self, vehicle_id: str) -> bool:
        """
        Check if vehicle has valid location data.
        
        Args:
            vehicle_id: Vehicle identifier
            
        Returns:
            True if location exists and is valid
        """
        location = await self.get(vehicle_id)
        return location is not None
