import asyncio
import functools
from collections.abc import Callable
from typing import Any

import typer
from a8t_tools.db.exceptions import DatabaseError
from loguru import logger

import app.domain
from app.containers import Container
from app.domain.tron.core.schemas import TronDetails


def async_to_sync(fn: Callable[..., Any]) -> Callable[..., Any]:
    if not asyncio.iscoroutinefunction(fn):
        return fn

    @functools.wraps(fn)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        coro = fn(*args, **kwargs)
        return asyncio.get_event_loop().run_until_complete(coro)

    return wrapper


def create_container() -> Container:
    container = Container()
    container.wire(packages=[app.domain])
    container.init_resources()
    return container


container = create_container()
typer_app = typer.Typer()


@typer_app.command()
@async_to_sync
async def noop() -> None:
    pass


# Для тестов
@typer_app.command()
@async_to_sync
async def create_tron(
    address: str = typer.Argument(...),
    bandwidth: str = typer.Argument(...),
    energy: str = typer.Argument(...),
    balance_trx: str = typer.Argument(...),
) -> None:
    command = container.tron.create_command()
    try:
        await command(
            TronDetails(
                address=address,
                bandwidth=bandwidth,
                energy=energy,
                balance_trx=balance_trx,
            ),
        )
    except DatabaseError as err:
        logger.warning(f"Tron creation error: {err}")
