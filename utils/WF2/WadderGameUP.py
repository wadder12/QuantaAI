from __future__ import annotations

from typing import (
    Optional,
    Coroutine,
    Callable,
    Final,
    Union,
    TypeVar,
    TYPE_CHECKING,
    Any,
)

import functools
import asyncio

import nextcord
from nextcord.ext import commands

if TYPE_CHECKING:
    from typing_extensions import ParamSpec, TypeAlias

    P = ParamSpec("P")
    T = TypeVar("T")

    A = TypeVar("A", bound=bool)
    B = TypeVar("B", bound=bool)

__all__: tuple[str, ...] = (
    "DiscordColor",
    "DEFAULT_COLOR",
    "executor",
    "chunk",
    "BaseView",
    "double_wait",
    "wait_for_delete",
)

DiscordColor: TypeAlias = Union[nextcord.Color, int]

DEFAULT_COLOR: Final[nextcord.Color] = nextcord.Color(0x2F3136)


def chunk(iterable: list[T], *, count: int) -> list[list[T]]:
    return [iterable[i : i + count] for i in range(0, len(iterable), count)]


def executor() -> Callable[[Callable[P, T]], Callable[P, asyncio.Future[T]]]:
    def decorator(func: Callable[P, T]) -> Callable[P, asyncio.Future[T]]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs):
            partial = functools.partial(func, *args, **kwargs)
            loop = asyncio.get_event_loop()
            return loop.run_in_executor(None, partial)

        return wrapper

    return decorator


async def wait_for_delete(
    ctx: commands.Context[commands.Bot],
    message: nextcord.Message,
    *,
    emoji: str = "⏹️",
    bot: Optional[nextcord.Client] = None,
    user: Optional[
        Union[nextcord.User, nextcord.Member, tuple[nextcord.User, ...]]
    ] = None,
    timeout: Optional[float] = None,
) -> bool:

    if not user:
        user = ctx.author
    try:
        await message.add_reaction(emoji)
    except nextcord.DiscordException:
        pass

    def check(reaction: nextcord.Reaction, _user: nextcord.User) -> bool:
        if reaction.emoji == emoji and reaction.message == message:
            if isinstance(user, tuple):
                return _user in user
            else:
                return _user == user
        else:
            return False

    resolved_bot: nextcord.Client = bot or ctx.bot
    try:
        await resolved_bot.wait_for("reaction_add", timeout=timeout, check=check)
    except asyncio.TimeoutError:
        return False
    else:
        await message.delete()
        return True


async def double_wait(
    task1: Coroutine[Any, Any, A],
    task2: Coroutine[Any, Any, B],
    *,
    loop: Optional[asyncio.AbstractEventLoop] = None,
) -> tuple[
    set[Union[asyncio.Task[A], asyncio.Task[B]]],
    set[Union[asyncio.Task[A], asyncio.Task[B]]],
]:

    if not loop:
        loop = asyncio.get_event_loop()

    return await asyncio.wait(
        [
            loop.create_task(task1),
            loop.create_task(task2),
        ],
        return_when=asyncio.FIRST_COMPLETED,
    )


if hasattr(nextcord, "ui"):

    class BaseView(nextcord.ui.View):
        def disable_all(self) -> None:
            for button in self.children:
                if isinstance(button, nextcord.ui.Button):
                    button.disabled = True

        async def on_timeout(self) -> None:
            return self.stop()
