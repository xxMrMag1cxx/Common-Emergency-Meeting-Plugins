"""
Botplugin: lägg till och ta bort bots i lobbyn med chattkommandon.

Bots är låtsasspelare som servern styr. De är bra för att testa saker
när man inte har så många riktiga spelare. De har namn och färg och syns
för alla som vanliga spelare. De går runt i lobbyn och på kartan. Under en
runda går de till sina uppdrag och gör dem (impostor-bots låtsas bara) och
röstar skip på möten när diskussionstiden är slut.

Kommandon (skrivs i chatten i lobbyn):

    /bot add          lägger till en bot (Bot_1, Bot_2, ...)   bara värden
    /bot remove       tar bort den senaste boten                bara värden
    /help botplugin   visar hjälpen

Among Us chatt låter en inte skriva understreck, så kommandona använder
mellanslag. Varianter som "/botadd" och "/bot-add" fungerar också.

Kräver Emergency Meeting version 0.6.0 eller nyare. Med 0.7.0 eller nyare
gör botarna uppdrag och röstar, och med 0.8.0 eller nyare går de runt.
"""

import logging
import re

NAME = "Botplugin"
VERSION = "1.3"
AUTHOR = "CEMP"
DESCRIPTION = "/bot add, /bot remove och /help botplugin"

log = logging.getLogger("plugin.botplugin")

BOT_PREFIX = "Bot_"

# Ska botarna göra uppdrag och rösta skip under en runda? (True/False)
BOTS_PLAY_ALONG = True

# Ska botarna gå runt? (True/False) Med False står de still.
BOTS_WALK = True

HELP = [
    "--- Botplugin ---",
    "/bot add : lägger till en bot (Bot_1, Bot_2 ...)",
    "/bot remove : tar bort den senaste boten",
    "/help botplugin : visar den här hjälpen",
    "Bara värden kan lägga till och ta bort bots.",
    "Bots går runt och räknas som spelare.",
    "I en runda går de till sina uppdrag och röstar skip.",
]


def on_chat(lobby, player, text):
    command = simplify(text)

    if command == "/helpbotplugin":
        for line in HELP:
            player.send_chat(line)
        return False  # visa inte kommandot för de andra

    if command == "/botadd":
        add_bot(lobby, player)
        return False

    if command == "/botremove":
        remove_bot(lobby, player)
        return False

    return True  # vanliga meddelanden skickas vidare som vanligt


def simplify(text):
    """
    Gör om t.ex. "/Bot Add", "/bot-add" och "/bot_add" till "/botadd",
    så att det inte spelar någon roll hur man skriver.
    """
    return re.sub(r"[\s_\-]+", "", text.strip().lower())


def add_bot(lobby, player):
    if not player.is_host:
        player.send_chat("Bara värden kan lägga till bots.")
        return
    if not hasattr(lobby, "add_bot"):
        player.send_chat("Servern är för gammal för bots. Uppdatera Emergency Meeting.")
        return

    name = next_bot_name(lobby)
    try:
        bot = lobby.add_bot(name, do_tasks=BOTS_PLAY_ALONG, walk=BOTS_WALK)
    except TypeError:
        try:
            bot = lobby.add_bot(name, do_tasks=BOTS_PLAY_ALONG)  # server äldre än 0.8.0
        except TypeError:
            bot = lobby.add_bot(name)  # server äldre än 0.7.0
    if bot is None:
        if lobby.is_started:
            player.send_chat("Det går inte att lägga till bots under en runda.")
        else:
            player.send_chat("Det gick inte att lägga till en bot. Är lobbyn full?")
        return

    # Spelet visar själv "Bot_1 joined the game", så vi behöver inte skriva något.
    log.info("%s lade till %s i %s", player.name, name, lobby.code)


def remove_bot(lobby, player):
    if not player.is_host:
        player.send_chat("Bara värden kan ta bort bots.")
        return
    if not hasattr(lobby, "remove_bot"):
        player.send_chat("Servern är för gammal för bots. Uppdatera Emergency Meeting.")
        return

    bots = lobby.bots
    if not bots:
        player.send_chat("Det finns inga bots att ta bort.")
        return

    bot = bots[-1]
    name = bot.name
    lobby.remove_bot(bot)
    log.info("%s tog bort %s i %s", player.name, name, lobby.code)


def next_bot_name(lobby):
    """Bot_1, Bot_2, ... Tar det lägsta lediga numret."""
    taken = {p.name for p in lobby.player_list}
    number = 1
    while f"{BOT_PREFIX}{number}" in taken:
        number += 1
    return f"{BOT_PREFIX}{number}"
