import platform
import discord
from discord.utils import get
from discord.ext import commands
from LogLib import Logging
from music_player import Queue
from KateLib import load_json_file, RandomSymbols
from functools import wraps
from asyncio.proactor_events import _ProactorBasePipeTransport
RS = RandomSymbols()


# Windows Development Fix
# https://github.com/aio-libs/aiohttp/issues/4324
def silence_event_loop_closed(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except RuntimeError as e:
            if str(e) != 'Event loop is closed':
                raise
    return wrapper


if platform.system() == 'Windows':
    # Silence the exception here.
    _ProactorBasePipeTransport.__del__ = silence_event_loop_closed(_ProactorBasePipeTransport.__del__)
# End Windows Development Fix


class MyHelpCommand(commands.MinimalHelpCommand):
    async def send_pages(self):
        destination = self.get_destination()
        e = discord.Embed(color=discord.Color.blurple(), description='')
        for page in self.paginator.pages:
            e.description += page
        await destination.send(embed=e)

# Discord.py Bot Extension
class KateBot(commands.Bot):
    def __init__(self, Logger):

        config = load_json_file('config/discord.json')

        intent = discord.Intents.default()
        intent.members = config['members_intent']
        intent.typing = config['typing_intent']
        intent.presences = config['presences_intent']

        commands.Bot.__init__(self,
                              owner_ids=config['owner_ids'],
                              command_prefix=config['prefix'],
                              case_insensitive=config['case_insensitive'],
                              intents=intent)

        self.token = config['token']
        self.logging = Logger
        self.player = Queue(Logger=Logger)

        self.add_commands()
        self.logging.log('KateBot', "Initialized", verbose=True)

    @staticmethod
    async def reaction_role(payload, emoji, role_name, remove=False):
        if payload.emoji.name == emoji:
            role = get(payload.member.guild.roles, name=role_name)
            if role is not None:
                if role not in payload.member.roles:
                    await payload.member.add_roles(role)
                elif remove:
                    await payload.member.remove_roles(role)
            else:
                raise TypeError(f"Role ({role_name}) not found in guild ({payload.member.guild})")

    async def on_ready(self):
        self.logging.log('Discord', f'Logged in as {self.user}! {RS.random_heart()}')

    async def on_command_error(self, ctx, error):
        self.logging.log("Discord", f"{error}\n"
                                    f" Author: [{ctx.author}]\n"
                                    f" Channel: [{ctx.channel}]", error=True)

    # IDE Bug? Self should be purple.
    def add_commands(self):
        @self.command(name="shutdown", aliases=["quit", "logout"])
        @commands.has_permissions(administrator=True)
        async def shutdown(ctx):
            try:
                await self.close()
            except RuntimeError as err:
                self.logging.log("Discord", f"{err}")
            self.logging.log("Discord", "Logging Out!")

        @self.command(category="administrative", name="restart",
                      brief='Restart bot', description='Restarts the discord bot.')
        @commands.has_permissions(administrator=True)
        async def shutdown(ctx):
            try:
                await self.close()
            except RuntimeError as err:
                self.logging.log("Discord", f"{err}")
            self.logging.log("Discord", "Logging Out!")


if __name__ == '__main__':
    from sqlalchemy import Column, Integer, String, ForeignKey, Table
    from sqlalchemy.orm import relationship, backref
    from sqlalchemy.ext.declarative import declarative_base

    Base = declarative_base()

    author_publisher = Table(
        "author_publisher",
        Base.metadata,
        Column("author_id", Integer, ForeignKey("author.author_id")),
        Column("publisher_id", Integer, ForeignKey("publisher.publisher_id")),
    )

    book_publisher = Table(
        "book_publisher",
        Base.metadata,
        Column("book_id", Integer, ForeignKey("book.book_id")),
        Column("publisher_id", Integer, ForeignKey("publisher.publisher_id")),
    )


    class Author(Base):
        __tablename__ = "author"
        author_id = Column(Integer, primary_key=True)
        first_name = Column(String)
        last_name = Column(String)
        books = relationship("Book", backref=backref("author"))
        publishers = relationship(
            "Publisher", secondary=author_publisher, back_populates="authors"
        )


    class Book(Base):
        __tablename__ = "book"
        book_id = Column(Integer, primary_key=True)
        author_id = Column(Integer, ForeignKey("author.author_id"))
        title = Column(String)
        publishers = relationship(
            "Publisher", secondary=book_publisher, back_populates="books"
        )


    class Publisher(Base):
        __tablename__ = "publisher"
        publisher_id = Column(Integer, primary_key=True)
        name = Column(String)
        authors = relationship(
            "Author", secondary=author_publisher, back_populates="publishers"
        )
        books = relationship(
            "Book", secondary=book_publisher, back_populates="publishers"
        )


    engine = create_engine(f"sqlite:///{sqlite_filepath}")
    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()


    Log = Logging()
    Log.debug = True
    Log.bot = True
    Log.verbose = True
    Log.music_player = True
    Log.load()
    KBot = KateBot(Log)
    KBot.load_extension("cogs.reddit")
    KBot.help_command = MyHelpCommand()
    KBot.load_extension("cogs.reaction_roles")
    #KBot.load_extension("cogs.template")
    KBot.run(KBot.token)



