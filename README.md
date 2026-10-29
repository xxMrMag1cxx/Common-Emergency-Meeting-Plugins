# Common Emergency Meeting Plugins (CEMP)

Plugins for [Emergency Meeting](https://github.com/xxMrMag1cxx/Emergency-Meeting),
our own Among Us server.

## Plugins

| File | What it does | Commands |
|------|--------------|----------|
| `botplugin.py` | Adds bots (pretend players) to the lobby, good for testing | `/bot add`, `/bot remove`, `/help botplugin` |

### Botplugin

Type the commands in the chat when you are in a lobby:

- **`/bot add`** adds a bot. The first one is called `Bot_1`, the next `Bot_2` and so on.
- **`/bot remove`** removes the latest bot.
- **`/help botplugin`** shows the help in the chat.

Among Us's chat doesn't let you type underscores, so the commands have
spaces. `/botadd` and `/bot-add` work too.

Only the host can add and remove bots. Bots have a name and a color, count
as players and show up for everyone. They walk around in the lobby and on
the map. During a round they walk to their tasks and do them on the spot
(impostor bots only pretend), and in meetings they vote skip when the
discussion time is over. That way you can test whole matches, and practice
killing as an impostor.

At the top of `botplugin.py` there are two settings:

- `BOTS_PLAY_ALONG = False`: the bots don't do tasks and don't vote.
- `BOTS_WALK = False`: the bots stand still.

Bots can't become the host: if the host leaves, a real player becomes the new
host, and if only bots are left the game closes.

Requires Emergency Meeting **0.6.0** or newer (**0.7.0** for the bots to do
tasks and vote, **0.8.0** for them to walk around). With **0.12.1** or newer
the plugin's log messages are in Swedish in the server's Terminal window if
the server's language is Swedish.

## Installing

1. Click the green **Code** button and choose **Download ZIP**.
2. Unpack the ZIP file.
3. Put the whole folder (`Common-Emergency-Meeting-Plugins-main`) in the
   `plugins/` folder in Emergency Meeting.
4. Restart the server. The box **LOADING PLUGINS** shows `Botplugin` when it works.

```
Emergency-Meeting-main/
  plugins/
    Common-Emergency-Meeting-Plugins-main/
      botplugin.py
```

If you only want one of the plugins, you can also copy just that `.py` file
directly to `plugins/`.

Files that start with `_` aren't loaded. Rename a file to for example
`_botplugin.py` to turn it off without deleting it.

## Making a new plugin

How plugins work, which events there are and what a plugin can do is in
[plugins/README.md in Emergency Meeting](https://github.com/xxMrMag1cxx/Emergency-Meeting/blob/main/plugins/README.md).

Put new plugins as their own `.py` files here in the repo and add them to
the table above. Write everything in English, and add Swedish translations
of the log messages in a `TRANSLATIONS` dictionary (see botplugin.py).
