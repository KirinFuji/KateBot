# KateBot

![Sample](LogExample.png)

## Setup

Fill out the .json files and copy them into the root of the config folder, then run the bot.  
You will need both a Discord Application Token, and a bunch of reddit data, look up "AsyncPraw" quick start for an explanation on the data needed.  


## Features:
- MemeStream (Reddit FeedBot)
- MusicBot 
- ReactionRoles (Dynamically from .json)


## Commands

#### Administration  
- !Cleanup \<all|Username> -- Starts deleting messages in the channel it is run in.  
- !Restart -- Restart the bot and reconnect to reddit and discord api's. (Not yet implemented)  
- !Shutdown -- Gracefully shutdown.  
- !Status - Is the bot still alive test command.  
#### CryptoCoins  
- !Price \<coin> -- Fetchs cryptocurrency information. (Not yet implemented)  
#### MusicPlayer   
- !Join \<Channel_ID> -- Joins a voice channel and creates a voice_client.  
- !Leave -- Leaves all voice channels  
- !Next -- Plays next song in queue.
- !Pause -- Pauses music playback.
- !Play \<MP3 Filename> -- Plays/queues an mp3 file. (Requires setup in discord.json)  
- !Random_music <n of songs> -- Generates a queue of n random songs.
- !Resume -- Resume music playback.
- !Stop -- Stops music playback and empties queue.  
#### ReactionRoles  
- !rr_disable
- !rr_enable
- !rr_reload  
#### RedditCog  
- !meme_stream \<on|off> -- Creates/Cancels background tasks for pulling Reddit submission streams.
#### No Category  
- !help <command|category> -- Use !help [command|category] for more info on a command or category.


## Dependencies
- asyncpraw  
- discord.py  
- PyNaCl (Required for music streaming over voice.)
