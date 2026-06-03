"""PostgreSQL client with connection pooling and async operations."""

from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from datetime import datetime
from typing import Any, AsyncGenerator

from psycopg import AsyncConnection
from psycopg_pool import AsyncConnectionPool
from psycopg.rows import dict_row, DictRow

logger = logging.getLogger(__name__)



# SQL statements for creating location tables
CREATE_FREQUENT_LOCATIONS_TABLE = """
CREATE TABLE IF NOT EXISTS frequent_locations (
    id SERIAL PRIMARY KEY,
    vehicle_id VARCHAR(255) NOT NULL,
    location_type VARCHAR(50) NOT NULL CHECK (location_type IN ('home', 'company')),
    name VARCHAR(255),
    address TEXT,
    longitude DECIMAL(12, 8),
    latitude DECIMAL(12, 8),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(vehicle_id, location_type)
)
"""

CREATE_COLLECTED_LOCATIONS_TABLE = """
CREATE TABLE IF NOT EXISTS collected_locations (
    id SERIAL PRIMARY KEY,
    vehicle_id VARCHAR(255) NOT NULL,
    name VARCHAR(255),
    address TEXT,
    longitude DECIMAL(12, 8),
    latitude DECIMAL(12, 8),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
"""

CREATE_COLLECTED_LOCATIONS_INDEX = """
CREATE INDEX IF NOT EXISTS idx_collected_locations_vehicle_id
ON collected_locations(vehicle_id)
"""

async def configure_connection(conn):
    conn.row_factory = dict_row

class PostgresClient:
    """
    Async PostgreSQL client wrapper with connection pooling.
    Use this as the base for all database operations.
    """

    _pool: AsyncConnectionPool | None = None
    _init_queries: list[str] = []

    def __init__(
        self,
        host: str = "localhost",
        port: int = 5432,
        dbname: str = "postgres",
        user: str = "postgres",
        password: str | None = None,
        min_size: int = 1,
        max_size: int = 4,
    ) -> None:
        self._conninfo = f"host={host} port={port} dbname={dbname} user={user}"
        if password:
            self._conninfo += f" password={password}"
        self._min_size = min_size
        self._max_size = max_size

    @classmethod
    async def create_pool(cls, instance: "PostgresClient") -> None:
        cls._pool = AsyncConnectionPool(
            instance._conninfo,
            min_size=instance._min_size,
            max_size=instance._max_size,
            configure=configure_connection # important for fetching data , or kwargs={"row_factory": dict_row}
        )
        await cls._pool.open()
        await cls._run_init_queries()
        logger.info(f"[{cls.__name__}] Pool initialized")

    @classmethod
    async def _run_init_queries(cls) -> None:
        if not cls._init_queries:
            return
        async with cls._pool.connection() as conn:
            for query in cls._init_queries:
                await conn.execute(query)
            await conn.commit()

    @classmethod
    async def close_pool(cls) -> None:
        """Close the connection pool."""
        if cls._pool is not None:
            await cls._pool.close()
            cls._pool = None

    async def execute(
        self,
        query: str,
        params: tuple[Any, ...] | dict[str, Any] | None = None,
    ) -> None:
        """Execute a query with auto-commit."""
        async with self.pool_connection() as conn:
            async with conn.cursor() as cur:
                await cur.execute(query, params)
            await conn.commit()

    async def fetch_one(
        self,
        query: str,
        params: tuple[Any, ...] | dict[str, Any] | None = None,
    ) -> dict | None:
        """Fetch a single row."""
        async with self.pool_connection() as conn:
            async with conn.cursor() as cur:
                await cur.execute(query, params)
                row = await cur.fetchone()
            return dict(row) if row else None

    async def fetch_all(
        self,
        query: str,
        params: tuple[Any, ...] | dict[str, Any] | None = None,
    ) -> list[dict]:
        """Fetch all rows."""
        async with self.pool_connection() as conn:
            async with conn.cursor() as cur:
                await cur.execute(query, params)
                rows = await cur.fetchall()
            return [dict(row) for row in rows]

    async def fetch_value(
        self,
        query: str,
        params: tuple[Any, ...] | dict[str, Any] | None = None,
    ) -> Any:
        """Fetch a single scalar value."""
        async with self.pool_connection() as conn:
            async with conn.cursor() as cur:
                await cur.execute(query, params)
                row = await cur.fetchone()
            return row[0] if row else None

    @asynccontextmanager
    async def pool_connection(
        self,
    ) -> AsyncGenerator[AsyncConnection[DictRow], None]:
        """Get a connection from the pool for transactions."""
        if self._pool is None:
            await self.create_pool(self)
        async with self._pool.connection() as conn:
            yield conn


# FrequentLocationStore - Home/Company addresses
class FrequentLocationStore(PostgresClient):
    """Store for frequent locations (home/company) using PostgreSQL."""

    _init_queries = [
        CREATE_FREQUENT_LOCATIONS_TABLE,
    ]

    async def save(
        self,
        vehicle_id: str,
        location_type: str,
        name: str | None = None,
        address: str | None = None,
        longitude: float | None = None,
        latitude: float | None = None,
    ) -> tuple[bool, str]:
        """
        Save frequent location (home or company). If one already exists, it will be
        replaced and the previous data is returned as info.

        Args:
            vehicle_id: Vehicle identifier
            location_type: 'home' or 'company'
            name: Location name
            address: Full address
            longitude: GPS longitude
            latitude: GPS latitude

        Returns:
            Tuple of (success: bool, info_message: str).
            info_message is empty on pure success, or contains the previous record
            as a JSON string when an existing record was replaced.
        """
        if self._pool is None:
            logger.error("[FrequentLocationStore] Pool not initialized")
            return False, "数据库连接未初始化"
        try:
            existing, _ = await self.get(vehicle_id, location_type)
            replacement_info = ""
            if existing:
                if existing.get("name") == name and existing.get("address") == address:
                    return False, "数据库已存在相同的地址"
                replacement_info = f"[旧地址] {existing.get('name')} | {existing.get('address')} -> [新地址] {name} | {address}"
            await self.execute(
                """
                INSERT INTO frequent_locations (vehicle_id, location_type, name, address, longitude, latitude, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (vehicle_id, location_type)
                DO UPDATE SET
                    name = EXCLUDED.name,
                    address = EXCLUDED.address,
                    longitude = EXCLUDED.longitude,
                    latitude = EXCLUDED.latitude,
                    updated_at = EXCLUDED.updated_at
                """,
                (vehicle_id, location_type, name, address, longitude, latitude, datetime.now()),
            )
            logger.info(f"[FrequentLocationStore] Saved {location_type} for {vehicle_id} (replaced_existing={existing is not None})")
            return True, replacement_info
        except Exception as e:
            logger.error(f"[FrequentLocationStore] Failed to save: {e}")
            return False, str(e)

    async def get(self, vehicle_id: str, location_type: str) -> tuple[dict | None, str]:
        """
        Get frequent location by type.

        Returns:
            Tuple of (result: dict | None, error_message: str)
        """
        try:
            result = await self.fetch_one(
                """
                SELECT * FROM frequent_locations
                WHERE vehicle_id = %s AND location_type = %s
                """,
                (vehicle_id, location_type),
            )
            return result, ""
        except Exception as e:
            logger.error(f"[FrequentLocationStore] Failed to get: {e}")
            return None, str(e)

    async def get_all(self, vehicle_id: str) -> tuple[list[dict], str]:
        """
        Get all frequent locations for a vehicle.

        Returns:
            Tuple of (results: list[dict], error_message: str)
        """
        try:
            results = await self.fetch_all(
                """
                SELECT * FROM frequent_locations
                WHERE vehicle_id = %s
                ORDER BY location_type
                """,
                (vehicle_id,),
            )
            return results, ""
        except Exception as e:
            logger.error(f"[FrequentLocationStore] Failed to get all: {e}")
            return [], str(e)

    async def delete(self, vehicle_id: str, location_type: str) -> tuple[bool, str]:
        """
        Delete frequent location by type.

        Returns:
            Tuple of (success: bool, error_message: str).
            Returns (False, "...") if no matching record exists.
        """
        try:
            existing, _ = await self.get(vehicle_id, location_type)
            if existing is None:
                return False, f"没有找到{location_type}地址"
            await self.execute(
                """
                DELETE FROM frequent_locations
                WHERE vehicle_id = %s AND location_type = %s
                """,
                (vehicle_id, location_type),
            )
            return True, ""
        except Exception as e:
            logger.error(f"[FrequentLocationStore] Failed to delete: {e}")
            return False, str(e)


# CollectedLocationStore - Favorite/collected locations
class CollectedLocationStore(PostgresClient):
    """Store for collected/favorite locations using PostgreSQL."""

    _init_queries = [
        CREATE_COLLECTED_LOCATIONS_TABLE,
        CREATE_COLLECTED_LOCATIONS_INDEX,
    ]

    async def save(
        self,
        vehicle_id: str,
        name: str | None = None,
        address: str | None = None,
        longitude: float | None = None,
        latitude: float | None = None,
    ) -> tuple[bool, str]:
        """
        Save collected/favorite location. If an identical record already exists for this
        vehicle, returns a notification instead of inserting a duplicate.

        Args:
            vehicle_id: Vehicle identifier
            name: Location name
            address: Full address
            longitude: GPS longitude
            latitude: GPS latitude

        Returns:
            Tuple of (success: bool, message: str).
            message is empty on pure success, or contains a notification string when
            a duplicate already exists.
        """
        if self._pool is None:
            logger.error("[CollectedLocationStore] Pool not initialized")
            return False, "数据库连接未初始化"

        try:
            existing = await self.fetch_one(
                """
                SELECT * FROM collected_locations
                WHERE vehicle_id = %s AND name = %s AND address = %s
                """,
                (vehicle_id, name, address),
            )
            if existing:
                logger.info(f"[CollectedLocationStore] Duplicate skipped for {vehicle_id}: {name}")
                return True, f"收藏地点 [{name}] 已存在，无需重复添加"
            await self.execute(
                """
                INSERT INTO collected_locations (vehicle_id, name, address, longitude, latitude)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (vehicle_id, name, address, longitude, latitude),
            )
            logger.info(f"[CollectedLocationStore] Saved for {vehicle_id}: {name}")
            return True, ""
        except Exception as e:
            logger.error(f"[CollectedLocationStore] Failed to save: {e}")
            return False, str(e)

    async def get_all(self, vehicle_id: str) -> tuple[list[dict], str]:
        """
        Get all collected locations for a vehicle.

        Returns:
            Tuple of (results: list[dict], error_message: str)
        """
        try:
            results = await self.fetch_all(
                """
                SELECT * FROM collected_locations
                WHERE vehicle_id = %s
                ORDER BY created_at DESC
                """,
                (vehicle_id,),
            )
            return results, ""
        except Exception as e:
            logger.error(f"[CollectedLocationStore] Failed to get all: {e}")
            return [], str(e)

    async def delete_all(self, vehicle_id: str) -> tuple[bool, str]:
        """
        Delete all collected locations for a vehicle.

        Returns:
            Tuple of (success: bool, error_message: str).
            Returns (False, "...") if no records exist for this vehicle.
        """
        try:
            existing, _ = await self.get_all(vehicle_id)
            if not existing:
                return False, "没有找到收藏地点"
            await self.execute(
                "DELETE FROM collected_locations WHERE vehicle_id = %s",
                (vehicle_id,),
            )
            return True, ""
        except Exception as e:
            logger.error(f"[CollectedLocationStore] Failed to delete all: {e}")
            return False, str(e)

    async def delete_by_name(self, vehicle_id: str, name: str, address: str = "") -> tuple[bool, str]:
        """
        Delete a collected location by name and address (exact match, mirrors save logic).

        Args:
            vehicle_id: Vehicle identifier.
            name: Location name (must match exactly).
            address: Full address (must match exactly).

        Returns:
            Tuple of (success: bool, error_message: str).
            Returns (False, "...") if no matching record exists.
        """
        try:
            existing = await self.fetch_one(
                "SELECT * FROM collected_locations WHERE vehicle_id = %s AND name = %s AND address = %s",
                (vehicle_id, name, address),
            )
            if existing is None:
                return False, f"收藏夹中没有 [{name}]"
            await self.execute(
                "DELETE FROM collected_locations WHERE vehicle_id = %s AND name = %s AND address = %s",
                (vehicle_id, name, address),
            )
            return True, ""
        except Exception as e:
            logger.error(f"[CollectedLocationStore] Failed to delete by name: {e}")
            return False, str(e)
