"""Location provider service for managing vehicle GPS data.

This service:
1. Subscribes to GPS updates from vehicle (via Socket.IO event)
2. Stores location context in Redis
3. Provides location when requested by query enhancer
"""

import logging
from typing import Optional

from src.context.location_store import LocationStore, LocationContext

logger = logging.getLogger(__name__)


class LocationProvider:
    """
    Service for managing vehicle location data.
    
    Handles:
    - Receiving GPS updates from vehicle clients
    - Storing location in Redis with auto-expiry
    - Providing location context to query processor
    """
    
    def __init__(self, redis_client):
        """
        Initialize location provider.
        
        Args:
            redis_client: RedisClient instance
        """
        self._store = LocationStore(redis_client)

    async def update_location(
        self,
        vehicle_id: str,
        latitude: float,
        longitude: float,
    ) -> bool:
        """
        Update vehicle's current location.
        
        Called when vehicle sends GPS update via Socket.IO.
        
        Args:
            vehicle_id: Vehicle identifier
            latitude: GPS latitude (GCJ-02)
            longitude: GPS longitude (GCJ-02)
            
        Returns:
            True if location was saved successfully
        """
        location = LocationContext(
            latitude=latitude,
            longitude=longitude
        )
        
        success = await self._store.save(vehicle_id, location)
        
        if success:
            logger.info(
                f"[LocationProvider] Updated location for {vehicle_id}: "
                f"({latitude:.6f}, {longitude:.6f})"
            )
        
        return success

    async def get_current_location(self, vehicle_id: str) -> Optional[LocationContext]:
        """
        Get vehicle's current location.
        
        Args:
            vehicle_id: Vehicle identifier
            
        Returns:
            LocationContext if available, None otherwise
        """
        location = await self._store.get(vehicle_id)
        
        if location:
            logger.debug(
                f"[LocationProvider] Retrieved location for {vehicle_id}: "
                f"({location.latitude:.6f}, {location.longitude:.6f})"
            )
        else:
            logger.debug(f"[LocationProvider] No location available for {vehicle_id}")
        
        return location

    async def has_location(self, vehicle_id: str) -> bool:
        """
        Check if vehicle has valid location data.
        
        Args:
            vehicle_id: Vehicle identifier
            
        Returns:
            True if location is available
        """
        return await self._store.exists(vehicle_id)

    async def clear_location(self, vehicle_id: str) -> bool:
        """
        Clear vehicle's cached location.
        
        Args:
            vehicle_id: Vehicle identifier
            
        Returns:
            True if location was cleared
        """
        return await self._store.delete(vehicle_id)

    async def deactivate_gps(self, vehicle_id: str) -> bool:
        """
        Deactivate GPS by clearing the location.
        
        Args:
            vehicle_id: Vehicle identifier
            
        Returns:
            True if deactivated successfully
        """
        return await self.clear_location(vehicle_id)


# Global singleton instance
_location_provider: Optional[LocationProvider] = None


def get_location_provider() -> LocationProvider:
    """Get the global location provider instance."""
    if _location_provider is None:
        raise RuntimeError("LocationProvider not initialized. Call init_location_provider first.")
    return _location_provider


def init_location_provider(redis_client) -> LocationProvider:
    """Initialize the global location provider."""
    global _location_provider
    _location_provider = LocationProvider(redis_client)
    logger.info("[LocationProvider] Initialized")
    return _location_provider
