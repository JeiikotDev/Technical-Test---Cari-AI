"""Entrypoint for running the FastAPI application with `uvicorn main:app`."""

from app.main import app

__all__ = ["app"]
