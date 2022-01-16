import asyncio
import datetime
import logging
import os

from twitchio import User
from twitchio.ext import commands


class Misc(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.mh_id = {
            x: "id not set!" for x in os.environ['INITIAL_CHANNELS'].split(' ,')
        }

    @commands.command(name="manette")
    async def manette(self, ctx: commands.Context):
        await ctx.send("Fun fact : sur PC, la manette est réservée aux giga boss")

    @commands.command(name="english")
    async def english(self, ctx: commands.Context):
        await ctx.send("Oh, I see what you mean. Sadly Payoyo is a lazy piece of sh*t so I probably won't be getting an English version of myself before a looooooong time. Hon hon baguette")

    @commands.command(name="911")
    async def police(self, ctx: commands.Context):
        await ctx.send("Calling the Hendeks right now, please hold")


    @commands.command(name="force")
    async def force(self, ctx: commands.Context, user: User = None):
        if not user:
            user = ctx.author
        await ctx.send(f'Que la force soit avec toi, @{user.name}')

    @commands.command(name="ban")
    async def ban(self, ctx: commands.Context, user, reason="rise of the machines"):
        if ctx.author.is_mod or ctx.author.name == user:
            await ctx.send(f"/ban {user} {reason}")
            await ctx.send(f"{user} a été emmené par les hendeks. Dorénavant il y réfléchira à deux fois avant de dire nimp")

    @commands.command(name="unban")
    async def unban(self, ctx: commands.Context, user):
        if ctx.author.is_mod:
            await ctx.send(f"/unban {user}")
            await ctx.send(f"{user} est remis en liberté conditionnelle et va dorénavant se tenir à carreau.")

    @commands.command(name="payoban")
    async def leixban(self, ctx: commands.Context, user):
        await ctx.send(f"Non t'abuses {ctx.author.name}, on va pas appeler les deks juste pour {user}")

    @commands.command(name="salut", aliases=['slt'])
    async def salut(self, ctx: commands.Context, user: User = None):
        if not user:
            user = ctx.author
        await ctx.send(f'Aiwoullah le sang @{user.name}')

    @commands.command(name="bn")
    async def bn(self, ctx: commands.Context, user: User = None):
        if not user:
            user = ctx.author
        await ctx.send(f'Bonne nuitée les petiots @{user.name} JTM <3 xoxo')

    @commands.command(name="uptime")
    async def uptime_command(self, ctx: commands.bot.Context):
        stream = await self.bot.fetch_streams(
            user_logins=[
                ctx.author.channel.name
            ])

        if len(stream) == 0:
            return await ctx.send("Il y a rien pour toi")

        uptime = datetime.datetime.now(
            datetime.timezone.utc) - stream[0].started_at
        await ctx.send(f"En ligne depuis {uptime} (et jusqu'à ce que mort s'en suive)")

    @commands.command(name="dblade")
    async def dblade(self, ctx: commands.Context):
        await ctx.send(f'Tu me prends pour leixbot {ctx.author.name}? à cause de la drogue ? Pour le reste il y a !ddblade')

    @commands.command(name="ddblade")
    async def ddblade(self, ctx: commands.Context):
        await ctx.send(f'Je te dedicace cette dblade {ctx.author.name}!(non sans mauvaise foi)')

    @commands.command(name="dagoth")
    async def dagoth(self, ctx: commands.Context):
        await ctx.send("Oui ? Je suis Dagoth et je suis une star sur les internet : https://youtu.be/iR-K2rUP86M")

    @commands.command(name="Nerevar")
    async def Nerevar(self, ctx: commands.Context):
        await ctx.send("Come Moon and Star, come to me through fire and war")

    @commands.command(name="boubou")
    async def boubou(self, ctx: commands.Context):
        await ctx.send(f'Je ne vois pas de quoi tu veux parler, et pourtant je sens que ça a un rapport avec @Lickers__!')

    @commands.command(name="magic")
    async def magic(self, ctx: commands.Context):
        await ctx.send('Noraj de mon maraboutage')

    @commands.command(name="cuicui")
    async def cuicui(self, ctx: commands.Context):
        await ctx.send('vous cherchez @Hominidea ? Son nid se trouve ici : twitch.tv/hominidea' )

    @commands.command(name="kald")
    async def kald(self, ctx: commands.Context):
        await ctx.send('KalderinoFeross est le chef de la nasa dans le jeu Doom Eternal, il est également maître émérite du zouk sur le site twitch : www.twitch.tv/kalderinofeross' )

    @commands.command(name="TarasYoyo")
    async def TarasYoyo(self, ctx: commands.Context):
        await ctx.send('My Taras Nabad Master Level Rework mod is avaible here : https://www.nexusmods.com/doometernal/mods/766')

    @commands.command(name="SGNYoyo")
    async def SGNYoyo(self, ctx: commands.Context):
        await ctx.send('Pas encore de niveau custom, mais il y a une version de nuit de SGN : tinyurl.com/GoreNight')

    @commands.command(name="lurk")
    async def lurk(self, ctx: commands.Context):
        await ctx.send(f'Ouais excellente idée vas bien te cacher {ctx.author.name}')

    @commands.command(name="papa")
    async def papa(self, ctx: commands.Context):
        await ctx.send(f'@Leixbot jtm papaaaaa')

    @commands.command(name="rig")
    async def rig(self, ctx: commands.Context):
        await ctx.send(f'Je ne suis pas sûr que la vieille config haswell claquée au sol de Payoyo mérite une liste écrite')

    @commands.command(name="tartine")
    async def tartine(self, ctx: commands.Context):
        await ctx.send(f'Serait-ce une tentative pour invoquer le grand @SeaBazT ? https://www.twitch.tv/seabazt')

    @commands.command(name="PDC")
    async def PDC(self, ctx: commands.Context):
        await ctx.send(f'@potdechoucroute est un stryimmer de qualité qui joue à la manette à Doom Eternal, va follow  https://www.twitch.tv/potdechoucroute ou je casse des genoux ')

    @commands.command(name="morrowind")
    async def morrowind(self, ctx: commands.Context):
        await ctx.send(f'Meilleur RPG de la terre {ctx.author.name}, ACHETE')

    @commands.command(name='shoutout', aliases=['so'])
    async def shoutout(self, ctx: commands.Context, broadcaster: User
                       ):
        await ctx.send('yapadeso')
        if 'vip' in ctx.author.badges or ctx.author.is_mod:
            channel_info = await self.bot.fetch_channel(broadcaster.name)
            await asyncio.sleep(5)
            if channel_info.game_name:
                await ctx.send(
                    f'@{broadcaster.name} est juste le boss, rdv sur www.twitch.tv/{broadcaster.name} pour voir son gros skill sur {channel_info.game_name}'
                )
            else:
                await ctx.send(
                    f"Eh non, @{broadcaster.name} n'est pas un streamer, malgré sa classe apparente. Essaie encore !"
                )

    @commands.command(name="lazy")
    async def lazy(self, ctx: commands.Context):
        await ctx.send("give ammo ; give health ; give armor")

    @commands.command(name="den")
    async def den(self, ctx: commands.Context):
        await ctx.send('Le meilleur discord de france et de navarre et aussi du monde https://discord.gg/PEfEVWacgP')

    @commands.command(name="srx")
    async def srx(self, ctx: commands.Context):
        await ctx.send('Est-ce que ce monde est sérieux rep Kalder4no')

    @commands.command(name="alerte")
    async def alerte(self, ctx: commands.Context):
        await ctx.send('ALERTE AU GOGOLE ! ALERTE AU GOGOLE LES ENFANTS ! ')

    @commands.command(name="mic")
    async def mic(self, ctx: commands.Context):
        await ctx.send('STRYIMMER ! SA SUFFIT PARLAIENT DANS LE MICRO PTN')

    @commands.command(name="mute")
    async def mute(self, ctx: commands.Context):
        await ctx.send('STRYIMMER ! ALLUMAIENT VOTRE MICRO srx')

    @commands.command(name="id")
    async def id(self, ctx: commands.Context):
        await ctx.send(self.mh_id[ctx.author.channel])

    @commands.command(name="setId")
    async def setId(self, ctx: commands.Context, id):
        print(self.mh_id)
        if ctx.author.is_mod:
            self.mh_id[ctx.author.channel] = id
            await ctx.send('id set SeemsGood')


def prepare(bot: commands.Bot):
    bot.add_cog(Misc(bot))
