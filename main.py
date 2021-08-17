import asyncio
import asyncpraw as async_praw
import discord
from discord.utils import get
from json import load as load_json
from discord.ext import commands
from datetime import datetime
from os import path
from random import randint
from os import listdir
from os.path import isfile, join
import json
from types import SimpleNamespace


def load_json_file(self, filename):
    with open(filename, 'r', encoding="utf8") as F:
        return load_json(F)


class KateBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        config = load_json_file('discord.json')
        self.discord_config = discord_config
        commands.Bot.__init__(self,
                              owner_ids=config['owner_ids'],
                              command_prefix=discord_config.prefix,
                              case_insensitive=discord_config.case_insensitive,
                              intents=intents)


if __name__ == '__main__':
    KBot = KateBot()



