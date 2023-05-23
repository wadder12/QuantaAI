"""
Copyright 2021 Nirlep_5252_

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from nextcord.ext.commands import Converter, Context, BadArgument
from utils.WF2.WadderExceptions import InvalidAutomodModule, InvalidUrl
from utils.WF2.WadderConfigs import DEFAULT_AUTOMOD_CONFIG
import pytz
import validators


class InvalidAddRemoveArgument(BadArgument):
    pass


class InvalidTimeZone(BadArgument):
    pass


class InvalidCategory(BadArgument):
    def __init__(self, category: str):
        self.category = category


class ImportantCategory(BadArgument):
    def __init__(self, category: str):
        self.category = category


class AddRemoveConverter(Converter):
    async def convert(self, ctx: Context, argument: str):
        if argument.lower() in ['add']:
            return True
        elif argument.lower() in ['remove']:
            return False
        else:
            raise InvalidAddRemoveArgument(argument)


class Lower(Converter):
    async def convert(self, ctx: Context, argument: str):
        return argument.lower()


class TimeZone(Converter):
    async def convert(self, ctx: Context, argument: str):
        try:
            timezone = pytz.timezone(argument)
            return timezone
        except pytz.exceptions.UnknownTimeZoneError:
            raise InvalidTimeZone(argument)


class Category(Converter):
    async def convert(self, ctx: Context, argument: str):
        categories: list = [cog for cog in ctx.bot.cogs if cog.lower() == cog and len(ctx.bot.get_cog(cog).get_commands()) != 0]
        imp_categories = ['config', 'user']
        if argument.lower() in imp_categories:
            raise ImportantCategory(argument)
        elif argument.lower() in categories:
            return ctx.bot.get_cog(argument.lower())
        else:
            raise InvalidCategory(argument)


class Url(Converter):
    async def convert(self, ctx: Context, argument: str):
        if validators.url(argument):
            return argument
        else:
            raise InvalidUrl(argument)


class AutomodModule(Converter):
    async def convert(self, ctx: Context, argument: str):
        if argument.lower() in DEFAULT_AUTOMOD_CONFIG:
            return argument.lower()
        else:
            raise InvalidAutomodModule(argument)
