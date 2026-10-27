# Common Emergency Meeting Plugins (CEMP)

Plugins till [Emergency Meeting](https://github.com/xxMrMag1cxx/Emergency-Meeting),
vår egen Among Us-server.

## Plugins

| Fil | Vad den gör | Kommandon |
|-----|-------------|-----------|
| `botplugin.py` | Lägger till bots (låtsasspelare) i lobbyn, bra för att testa | `/bot add`, `/bot remove`, `/help botplugin` |

### Botplugin

Skriv kommandona i chatten när du är i en lobby:

- **`/bot add`** lägger till en bot. Den första heter `Bot_1`, nästa `Bot_2` och så vidare.
- **`/bot remove`** tar bort den senaste boten.
- **`/help botplugin`** visar hjälpen i chatten.

Among Us chatt låter en inte skriva understreck, så kommandona har
mellanslag. `/botadd` och `/bot-add` fungerar också.

Bara värden kan lägga till och ta bort bots. Bots står still i lobbyn men
har namn och färg, räknas som spelare och syns för alla. De kan inte bli
värd: om värden lämnar blir en riktig spelare ny värd, och om bara bots är
kvar stängs spelet.

Kräver Emergency Meeting **0.6.0** eller nyare.

## Installera

1. Klicka på den gröna knappen **Code** och välj **Download ZIP**.
2. Packa upp ZIP-filen.
3. Lägg hela mappen (`Common-Emergency-Meeting-Plugins-main`) i mappen
   `plugins/` i Emergency Meeting.
4. Starta om servern. Den skriver `Laddade pluginet Botplugin` när det fungerar.

```
Emergency-Meeting-main/
  plugins/
    Common-Emergency-Meeting-Plugins-main/
      botplugin.py
```

Vill man bara ha ett av pluginen kan man också kopiera just den `.py`-filen
direkt till `plugins/`.

Filer som börjar med `_` laddas inte. Byt namn på en fil till t.ex.
`_botplugin.py` för att stänga av den utan att ta bort den.

## Göra ett nytt plugin

Hur plugins fungerar, vilka händelser som finns och vad ett plugin kan göra
står i [plugins/README.md i Emergency Meeting](https://github.com/xxMrMag1cxx/Emergency-Meeting/blob/main/plugins/README.md).

Lägg nya plugins som egna `.py`-filer här i repot och skriv in dem i
tabellen ovan.
