"""Redis client with connection pooling and async operations."""

from __future__ import annotations

import json
import redis.asyncio as aioredis
from typing import Any


class RedisClient:
    """Async Redis client wrapper with connection pooling support."""

    _pool: aioredis.ConnectionPool | None = None

    def __init__(self, host: str = "localhost", port: int = 6379, db: int = 0, password: str | None = None) -> None:
        """
        Initialize Redis client.

        Args:
            host: Redis server hostname.
            port: Redis server port.
            db: Redis database number.
            password: Optional Redis password.
        """
        self._host = host
        self._port = port
        self._db = db
        self._password = password
        self._client: aioredis.Redis | None = None

    @classmethod
    async def create_pool(
        cls,
        host: str = "localhost",
        port: int = 6379,
        db: int = 0,
        password: str | None = None,
        max_connections: int | None = None,
    ) -> aioredis.ConnectionPool:
        """
        Create and store a shared Redis connection pool.

        Args:
            host: Redis server hostname.
            port: Redis server port.
            db: Redis database number.
            password: Optional Redis password.
            max_connections: Maximum number of connections in the pool.

        Returns:
            The created ConnectionPool instance.
        """
        cls._pool = aioredis.ConnectionPool(
            host=host,
            port=port,
            db=db,
            password=password,
            max_connections=max_connections,
            decode_responses=False,
        )
        return cls._pool

    @property
    def client(self) -> aioredis.Redis:
        """Get or create a Redis client instance."""
        if self._client is not None:
            return self._client

        if self._pool is not None:
            self._client = aioredis.Redis(connection_pool=self._pool)
        else:
            self._client = aioredis.Redis(
                host=self._host,
                port=self._port,
                db=self._db,
                password=self._password,
                decode_responses=False,
            )
        return self._client

    async def get(self, key: str) -> Any | None:
        """
        Get a value from Redis.

        Args:
            key: The key to retrieve.

        Returns:
            The stored value, or None if the key does not exist.
        """
        value = await self.client.get(key)
        if value is None:
            return None
        try:
            return json.loads(value)
        except (json.JSONDecodeError, TypeError):
            return value.decode("utf-8") if isinstance(value, bytes) else value

    async def set(
        self,
        key: str,
        value: Any,
        ex: int | None = None,
        px: int | None = None,
        nx: bool = False,
        xx: bool = False,
    ) -> bool:
        """
        Set a value in Redis.

        Args:
            key: The key to set.
            value: The value to store. Objects are JSON-serialized.
            ex: Expiration time in seconds.
            px: Expiration time in milliseconds.
            nx: Only set if the key does not exist.
            xx: Only set if the key already exists.

        Returns:
            True if the value was set, False otherwise.
        """
        if not isinstance(value, (str, bytes, int, float)):
            value = json.dumps(value)
        return bool(await self.client.set(key, value, ex=ex, px=px, nx=nx, xx=xx))

    async def close(self) -> None:
        """Close the Redis client connection."""
        if self._client is not None:
            await self._client.aclose()
            self._client = None
