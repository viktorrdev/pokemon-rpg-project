import discord
from discord.ext import commands
import random
from npcs import players, starters

from data import routes
from pokemon import natures

import os

from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

def generate_pokemon(route_name):
    pokemon_list = routes[route_name]

    weighted_list = []

    for pokemon in pokemon_list:
        weighted_list.extend([pokemon] * pokemon["chance"])

    chosen = random.choice(weighted_list)

    level = random.randint(
        chosen["min_level"],
        chosen["max_level"]
    )

    iv = {
        "hp": random.randint(0, 31),
        "atk": random.randint(0, 31),
        "def": random.randint(0, 31),
        "sp_atk": random.randint(0, 31),
        "sp_def": random.randint(0, 31),
        "speed": random.randint(0, 31)
    }

    iv_total = sum(iv.values())
    iv_percent = round((iv_total / 186) * 100)
    
    gender = random.choice(["♂", "♀"])
    nature = random.choice(natures)
    shiny = random.randint(1, 4096) == 1

    return {
        "name": chosen["name"],
        "level": level,
        "iv": iv,
        "iv_percent": iv_percent,
        "gender": gender,
        "nature": nature,
        "shiny": shiny
    }

@bot.command()
async def procurar(ctx):

    pokemon = generate_pokemon("rota1")

    shiny_text = "✨ SHINY ✨\n" if pokemon["shiny"] else ""

    message = f"""
{shiny_text}
🌿 Um Pokémon apareceu!

Nome: {pokemon['name']} {pokemon['gender']}
Nível: {pokemon['level']}
Natureza: {pokemon['nature']}

IV Total: {pokemon['iv_percent']}%

HP: {pokemon['iv']['hp']}
ATK: {pokemon['iv']['atk']}
DEF: {pokemon['iv']['def']}
SP.ATK: {pokemon['iv']['sp_atk']}
SP.DEF: {pokemon['iv']['sp_def']}
SPD: {pokemon['iv']['speed']}
"""



    await ctx.send(message)
    
@bot.command()
async def professor(ctx, starter=None):

    user_id = str(ctx.author.id)

    if user_id in players:
        await ctx.send("Você já pegou seus itens iniciais.")
        return

    if starter:
        starter = starter.capitalize()
        if starter not in starters:
            await ctx.send("Esse starter não existe.")
            return
    else:
        starter = random.choice(starters)

    players[user_id] = {
        "starter": starter,
        "pokeballs": 10,
        "pokedex": True
    }

    await ctx.send(f"""
👨‍🔬 Prof. Carvalho:

Você recebeu:
🎁 Starter: {starter}
🎒 10 Pokébolas
📘 Pokédex
""")

bot.run(TOKEN)