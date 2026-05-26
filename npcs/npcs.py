import random
players = {}

starters = [
    "Bulbasaur", "Charmander", "Squirtle",
    "Chikorita", "Cyndaquil", "Totodile",
    "Treecko", "Torchic", "Mudkip",
    "Turtwig", "Chimchar", "Piplup"
]

def give_professor_rewards(user_id):
    if user_id in players:
        return None

    starter = random.choice(starters)

    players[user_id] = {
        "starter": starter,
        "pokeballs": 10,
        "pokedex": True
    }

    return players[user_id]

npc_professor = {
    "name": "Prof. Carvalho",
    "type": "system_npc",
    "functions": [
        "start_game",
        "give_starter",
        "give_items",
        "explain_rules"
    ]
}