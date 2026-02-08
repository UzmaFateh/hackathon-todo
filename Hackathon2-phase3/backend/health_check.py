"""
Health check and monitoring endpoints for uptime monitoring.
"""
from fastapi import FastAPI, HTTPException, status
from typing import Dict, Any
import time
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global state for health checks
startup_time = time.time()
last_healthy_check = time.time()


class HealthChecker:
    """
    Health checker for monitoring service availability and performance.
    """

    def __init__(self):
        self.startup_time = time.time()
        self.last_healthy_check = time.time()
        self.health_status = True
        self.performance_metrics = {}

    def check_health(self) -> Dict[str, Any]:
        """
        Perform a comprehensive health check.

        Returns:
            Dictionary with health status and details
        """
        global last_healthy_check

        # Calculate uptime
        uptime_seconds = time.time() - self.startup_time

        # Perform basic health checks
        checks = {
            "database": self._check_database_connection(),
            "llm_api": self._check_llm_connection(),
            "memory_usage": self._check_memory_usage(),
            "response_time": self._check_response_time()
        }

        # Overall health status
        overall_healthy = all(check.get("status") == "healthy" for check in checks.values())

        if overall_healthy:
            self.last_healthy_check = time.time()

        health_report = {
            "status": "healthy" if overall_healthy else "unhealthy",
            "timestamp": datetime.utcnow().isoformat(),
            "uptime_seconds": uptime_seconds,
            "checks": checks,
            "version": "1.0.0"
        }

        return health_report

    def check_readiness(self) -> Dict[str, Any]:
        """
        Check if the service is ready to serve traffic.

        Returns:
            Dictionary with readiness status
        """
        # For now, readiness is the same as health
        # In the future, this could check for specific startup conditions
        return {
            "status": "ready",
            "timestamp": datetime.utcnow().isoformat(),
            "message": "Service is ready to accept traffic"
        }

    def _check_database_connection(self) -> Dict[str, Any]:
        """
        Check database connectivity.

        Returns:
            Dictionary with database check results
        """
        try:
            # In a real implementation, this would test the actual database connection
            # For now, we'll simulate a healthy connection
            import random
            # Simulate occasional failures for testing
            if random.random() < 0.01:  # 1% failure rate for simulation
                return {
                    "status": "unhealthy",
                    "message": "Database connection failed",
                    "details": "Could not connect to database server"
                }

            return {
                "status": "healthy",
                "message": "Database connection successful",
                "details": "Connected to PostgreSQL database"
            }
        except Exception as e:
            logger.error(f"Database health check failed: {str(e)}")
            return {
                "status": "unhealthy",
                "message": "Database connection failed",
                "details": str(e)
            }

    def _check_llm_connection(self) -> Dict[str, Any]:
        """
        Check LLM API connectivity.

        Returns:
            Dictionary with LLM connection check results
        """
        try:
            # In a real implementation, this would test the actual LLM API connection
            # For now, we'll simulate a healthy connection
            import random
            # Simulate occasional failures for testing
            if random.random() < 0.02:  # 2% failure rate for simulation
                return {
                    "status": "unhealthy",
                    "message": "LLM API connection failed",
                    "details": "Could not connect to LLM service"
                }

            return {
                "status": "healthy",
                "message": "LLM API connection successful",
                "details": "Connected to LLM service endpoint"
            }
        except Exception as e:
            logger.error(f"LLM connection health check failed: {str(e)}")
            return {
                "status": "unhealthy",
                "message": "LLM API connection failed",
                "details": str(e)
            }

    def _check_memory_usage(self) -> Dict[str, Any]:
        """
        Check memory usage.

        Returns:
            Dictionary with memory usage check results
        """
        try:
            import psutil
            memory_percent = psutil.virtual_memory().percent

            if memory_percent > 90:
                return {
                    "status": "warning",
                    "message": "High memory usage detected",
                    "details": f"Memory usage: {memory_percent}%"
                }
            elif memory_percent > 95:
                return {
                    "status": "unhealthy",
                    "message": "Critical memory usage detected",
                    "details": f"Memory usage: {memory_percent}%"
                }
            else:
                return {
                    "status": "healthy",
                    "message": "Memory usage within normal range",
                    "details": f"Memory usage: {memory_percent}%"
                }
        except ImportError:
            # psutil not available in some environments
            return {
                "status": "unknown",
                "message": "Memory check unavailable",
                "details": "psutil module not installed"
            }
        except Exception as e:
            logger.error(f"Memory health check failed: {str(e)}")
            return {
                "status": "unhealthy",
                "message": "Memory check failed",
                "details": str(e)
            }

    def _check_response_time(self) -> Dict[str, Any]:
        """
        Check response time metrics.

        Returns:
            Dictionary with response time check results
        """
        try:
            # Calculate approximate response time based on the last health check
            time_since_last_check = time.time() - self.last_healthy_check

            if time_since_last_check > 5:  # More than 5 seconds since last check
                return {
                    "status": "warning",
                    "message": "Potential performance issue detected",
                    "details": f"Last health check was {time_since_last_check:.2f}s ago"
                }
            else:
                return {
                    "status": "healthy",
                    "message": "Response time within acceptable range",
                    "details": f"Last check was {time_since_last_check:.2f}s ago"
                }
        except Exception as e:
            logger.error(f"Response time health check failed: {str(e)}")
            return {
                "status": "unhealthy",
                "message": "Response time check failed",
                "details": str(e)
            }


# Global health checker instance
health_checker = HealthChecker()


def get_health_status() -> Dict[str, Any]:
    """
    Get the current health status.

    Returns:
        Dictionary with health status
    """
    return health_checker.check_health()


def get_readiness_status() -> Dict[str, Any]:
    """
    Get the current readiness status.

    Returns:
        Dictionary with readiness status
    """
    return health_checker.check_readiness()


# For use in FastAPI app
def add_health_routes(app: FastAPI):
    """
    Add health check routes to the FastAPI application.

    Args:
        app: FastAPI application instance
    """

    @app.get("/health", tags=["health"])
    async def health_check():
        """Health check endpoint for uptime monitoring."""
        return health_checker.check_health()

    @app.get("/ready", tags=["health"])
    async def readiness_check():
        """Readiness check endpoint."""
        return health_checker.check_readiness()


# Export for easy import
__all__ = ['health_checker', 'get_health_status', 'get_readiness_status', 'add_health_routes']