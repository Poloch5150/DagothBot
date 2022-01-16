# bot.py
import asyncio
import logging
import os  # for importing env vars for the bot to use
import random
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path

from twitchio import Channel, Client, User
from twitchio.ext import commands, pubsub, routines


class DagothBot(commands.Bot):

    def __init__(self):
        super().__init__(
            token=os.environ['ACCESS_TOKEN'],
            prefix=os.environ['BOT_PREFIX'],
            initial_channels=os.environ['INITIAL_CHANNELS'].split(', '),
            case_insensitive=True
        )
        self.pubsub_client = None
        self.channel = None
        self._cogs_names: t.Dict[str] = [
            p.stem for p in Path(".").glob("./cogs/*.py")
        ]
        self.bot_to_reply = ["wizebot", "streamelements"]

    def setup(self):
        random.seed()

        print("Chargement des cogs...")

        for cog in self._cogs_names:
            logging.info(f"Loading `{cog}` cog.")
            self.load_module(f"cogs.{cog}")

        # logging.info("Starting timers")
        # self.loop.create_task(self.timers())

        logging.info("Chargement terminé")

    def run(self):
        self.setup()
        super().run()

    async def event_ready(self):
        # Notify us when everything is ready!

        # Subscribes through pubsub to topics
        c: Channel = self.connected_channels[0]
        u: List["User"] = await self.fetch_users(names=[c.name])
        uu: User = u[0]

        topics = [
            pubsub.channel_points(self.pubsub_client._http.token)[uu.id],
            pubsub.bits(self.pubsub_client._http.token)[uu.id]
        ]
        await self.pubsub_client.pubsub.subscribe_topics(topics)
        await self.pubsub_client.connect()
        self.channel = self.pubsub_client.get_channel("Payoyo5150")

        # Starting timers
        self.links.start()

        # We are logged in and ready to chat and use commands...
        logging.info(f'Logged in as | {self.nick}')

    async def event_message(self, message):
        # Messages with echo set to True are messages sent by the bot...
        # For now we just want to ignore them...
        if message.echo:
            return

        # Print the contents of our message to console...
        logging.info(
            f'{message.author.name} on channel {message.author.channel.name}: '
            f'{message.content}'
        )

        if "@leixbot" in message.content.lower():
            await self.random_reply(message)

        if "@dagothbot" in message.content.lower():
            await self.random_reply(message)

        if message.author.name.lower() in self.bot_to_reply:
            await self.random_bot_reply(message)

        # Since we have commands and are overriding the default `event_message`
        # We must let the bot know we want to handle and invoke our commands...
        await self.handle_commands(message)

    async def event_raw_usernotice(self, channel, tags):
        if tags["msg-id"] == "sub":
            await channel.send(f"PogChamp {tags['display-name']} fait désormais partie des adeptes de la maison Dagoth. Welcome Moon and Star !")
        elif tags["msg-id"] == "resub":
            await channel.send(
                f"PogChamp Le resuuuub de {tags['display-name']}. Merci de fièrement soutenir la chaine depuis {tags['msg-param-cumulative-months']} T un chad JTM merci"
            )
        elif tags["msg-id"] == "raid":
            await channel.send(
                f"Il faut se défendre SwiftRage ! Nous sommes raid par {tags['msg-param-displayName']} et sa bande de {tags['msg-param-viewerCount']} zinzins")

    ## PUBSUB FUNCTIONS ##
    async def event_pubsub_channel_points(self, event: pubsub.PubSubChannelPointsMessage):
        logging.info(
            f'Redemption by {event.user.name} of reward {event.reward.title} '
            f'with input {event.input} done'
        )
        if event.reward.title == "Hats off to you":
            minutes = 5
            time = datetime.now() + timedelta(minutes=minutes)
            await self.channel.send(f"Met le casque jusqu'à {time.strftime('%H:%M:%S')}")
            await asyncio.sleep(minutes * 60)
            await channel.send("/me @Leix34 tu peux maintenant retirer le casque")

    async def event_pubsub_bits(self, event: pubsub.PubSubBitsMessage):
        logging.info(
            f'{event.user.name} a claqué {event.bits_used} bits sur ce streamer de seconde zone !'
        )
        self.channel.send(
            f'Merci pour les {event.bits_used} bits @{event.user.name} mais vas-y molo sinon Payoyo va gagner assez pour devoir payer des impôts'
        )

    # TODO: add subs, follows, raids... events when twitchio has the classes implemented
    # async def event_pubsub_channel_subscription(self, event: pubsub.PubSubChannelSubscription):
    #     logging.info("Un nouveau sub!")

    ## TIMERS ##
    @routines.routine(minutes=30.0, wait_first=False)
    async def links(self):
        await self.channel.send("Mon YouTube: https://www.youtube.com/channel/UCgkntHnd-v_4KtcmF_sAyFA")
        await asyncio.sleep(60 * 30)
        await self.channel.send("Mes mods : https://www.nexusmods.com/doometernal/users/15899834")
        await asyncio.sleep(60 * 30)

    ## GENERAL FUNCTIONS ##
    @commands.command(name="git")
    async def git(self, ctx: commands.Context):
        await ctx.send(
            f'La légende dit que je suis né du sang de @Leixbot, sinon il y a mon code source (sûrement pas à jour connaissant Payoyo) : https://github.com/Poloch5150/DagothBot/ '
        )

    @commands.command(name="list")
    async def list(self, ctx: commands.Context):
        list = ""
        for command in self.commands:
            list += command + ", "

        # Remove last comma and space
        list = list[:-2]
        await ctx.send(f'Je sais faire tout ça : {list}')

    async def random_leixbot_reply(self, message):
        compiled_msg = re.compile(re.escape("@leixbot"), re.IGNORECASE)
        msg_clean = compiled_msg.sub("", message.content)
        reply_pool = [
            "hé tu parles pas comme ça à mon géniteur", "Tu vas faire quoi",
            "leix34Trigerred",
            "Oui vous l'avez demandé?",
            f"ATTANSION {msg_clean} ??"
        ]
        reply = random.choice(reply_pool)
        await message.author.channel.send(f"@{message.author.name} {reply}")

    async def random_reply(self, message):
        compiled_msg = re.compile(re.escape("@DagothBot"), re.IGNORECASE)
        msg_clean = compiled_msg.sub("", message.content)
        reply_pool = [
            "wsh t ki", "Tu vas faire quoi",
            "SwiftRage SwiftRage SwiftRage",
            "kesta toi",
            f"c moé {msg_clean} ??"
        ]
        reply = random.choice(reply_pool)
        await message.author.channel.send(f"@{message.author.name} {reply}")

    async def random_bot_reply(self, message):
        reply_pool = [
            f"tu vas faire quoi {message.author.name}",
            f"DagothBot > {message.author.name}",
            f"{message.author.name} t'es moche comme le soleil :( ",
            f"{message.author.name} tu pues de la tête",
            f"{message.author.name} t'es moche comme ton père",
            f"{message.author.name} ferme-la, physiquement",
        ]
        reply = random.choice(reply_pool)
        await message.author.channel.send(f"{reply}")


if __name__ == "__main__":
    logging.basicConfig(
        encoding='utf-8',
        level=logging.INFO,
        handlers=[
            logging.FileHandler("debug.log"),
            logging.StreamHandler()
        ]
    )

    client = Client(
        token=os.environ['CHANNEL_ACCESS_TOKEN'],
        initial_channels=['Payoyo5150'],
        client_secret=os.environ['CLIENT_SECRET']
    )

    client.pubsub = pubsub.PubSubPool(client)

    @client.event()
    async def event_pubsub_channel_points(event: pubsub.PubSubChannelPointsMessage):
        await bot.event_pubsub_channel_points(event)

    @client.event()
    async def event_pubsub_bits(event: pubsub.PubSubBitsMessage):
        await bot.event_pubsub_bits(event)

    # @client.event()
    # async def event_channel_subscriptions(event: pubsub.PubSubChannelSubscription):
    #     await bot.event_pubsub_channel_subscription(event)

    bot = DagothBot()
    bot.pubsub_client = client
    bot.run()
