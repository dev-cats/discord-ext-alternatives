"""An experiment that allows using bitwise OR (``|``) with checks

It is equivalent to calling ``check_any``

Example (Python 3.9):

```py
def is_guild_owner():
    def predicate(ctx):
        return ctx.guild is not None and ctx.guild.owner_id == ctx.author.id
    return commands.check(predicate)

@bot.command()
@commands.is_owner() | is_guild_owner()
async def only_for_owners(ctx):
    await ctx.send('Hello mister owner!')
```
"""

from discord.ext import commands
from discord.ext.commands import core

old_check = core.check


class Check:
    def __init__(self, predicate):
        self.__dec = old_check(predicate)

    def __or__(self, other: "Check"):
        return core.check_any(self.__dec, other.__dec)

    def __call__(self, *args, **kwargs):
        return self.__dec(*args, **kwargs)

    def __getattr__(self, attr):
        return getattr(self.__dec, attr)


core.check = Check
commands.check = Check
