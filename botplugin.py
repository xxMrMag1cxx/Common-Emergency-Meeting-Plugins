"""
Botplugin: add and remove bots in the lobby with chat commands.

Bots are pretend players that the server controls. They are good for testing
things when you don't have that many real players. They have a name and a
color and show up for everyone like ordinary players. They walk around in
the lobby and on the map. During a round they walk to their tasks and do
them (impostor bots only pretend) and vote skip in meetings when the
discussion time is over.

Commands (typed in the chat in the lobby):

    /bot add          adds a bot (Bot_1, Bot_2, ...)   only the host
    /bot remove       removes the latest bot           only the host
    /help botplugin   shows the help

Among Us's chat doesn't let you type underscores, so the commands use
spaces. Variants like "/botadd" and "/bot-add" work too.

Requires Emergency Meeting version 0.6.0 or newer. With 0.7.0 or newer the
bots do tasks and vote, and with 0.8.0 or newer they walk around. With
0.12.1 or newer the server's Terminal window shows the log messages in
Swedish if the server's language is Swedish (see TRANSLATIONS below).
"""

import logging
import re

NAME = "Botplugin"
VERSION = "1.4"
AUTHOR = "CEMP"
DESCRIPTION = "/bot add, /bot remove and /help botplugin"

log = logging.getLogger("plugin.botplugin")

BOT_PREFIX = "Bot_"

# Should the bots do tasks and vote skip during a round? (True/False)
BOTS_PLAY_ALONG = True

# Should the bots walk around? (True/False) With False they stand still.
BOTS_WALK = True

HELP = [
    "--- Botplugin ---",
    "/bot add : adds a bot (Bot_1, Bot_2 ...)",
    "/bot remove : removes the latest bot",
    "/help botplugin : shows this help",
    "Only the host can add and remove bots.",
    "Bots walk around and count as players.",
    "In a round they walk to their tasks and vote skip.",
]

# Translations for the server's Terminal window (only the log messages and
# DESCRIPTION, the chat messages above are always in English).
TRANSLATIONS = {
    "sv": {
        "/bot add, /bot remove and /help botplugin": "/bot add, /bot remove och /help botplugin",
        "%s added %s to %s": "%s lade till %s i %s",
        "%s removed %s from %s": "%s tog bort %s i %s",
    },
}


def on_chat(lobby, player, text):
    command = simplify(text)

    if command == "/helpbotplugin":
        for line in HELP:
            player.send_chat(line)
        return False  # don't show the command to the others

    if command == "/botadd":
        add_bot(lobby, player)
        return False

    if command == "/botremove":
        remove_bot(lobby, player)
        return False

    return True  # ordinary messages are passed on as usual


def simplify(text):
    """
    Turns for example "/Bot Add", "/bot-add" and "/bot_add" into "/botadd",
    so that it doesn't matter how you type it.
    """
    return re.sub(r"[\s_\-]+", "", text.strip().lower())


def add_bot(lobby, player):
    if not player.is_host:
        player.send_chat("Only the host can add bots.")
        return
    if not hasattr(lobby, "add_bot"):
        player.send_chat("The server is too old for bots. Update Emergency Meeting.")
        return

    name = next_bot_name(lobby)
    try:
        bot = lobby.add_bot(name, do_tasks=BOTS_PLAY_ALONG, walk=BOTS_WALK)
    except TypeError:
        try:
            bot = lobby.add_bot(name, do_tasks=BOTS_PLAY_ALONG)  # server older than 0.8.0
        except TypeError:
            bot = lobby.add_bot(name)  # server older than 0.7.0
    if bot is None:
        if lobby.is_started:
            player.send_chat("Bots can't be added during a round.")
        else:
            player.send_chat("A bot could not be added. Is the lobby full?")
        return

    # The game shows "Bot_1 joined the game" by itself, so we don't need to write anything.
    log.info("%s added %s to %s", player.name, name, lobby.code)


def remove_bot(lobby, player):
    if not player.is_host:
        player.send_chat("Only the host can remove bots.")
        return
    if not hasattr(lobby, "remove_bot"):
        player.send_chat("The server is too old for bots. Update Emergency Meeting.")
        return

    bots = lobby.bots
    if not bots:
        player.send_chat("There are no bots to remove.")
        return

    bot = bots[-1]
    name = bot.name
    lobby.remove_bot(bot)
    log.info("%s removed %s from %s", player.name, name, lobby.code)


def next_bot_name(lobby):
    """Bot_1, Bot_2, ... Takes the lowest free number."""
    taken = {p.name for p in lobby.player_list}
    number = 1
    while f"{BOT_PREFIX}{number}" in taken:
        number += 1
    return f"{BOT_PREFIX}{number}"
