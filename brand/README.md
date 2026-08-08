# Parlami brand kit

The mark: a speech bubble ("parlami" = Italian for "talk to me") holding three rising
bars — a voice speaking and a growth chart in one shape. Colors and font come from
the live site: cyan `#22d3ee` → violet `#8b5cf6` gradient, navy `#1a1a2e`, Quicksand Bold.

## Which file to use where

| File | Use |
|---|---|
| `parlami-avatar-400.png` | X/Twitter profile picture (400×400) |
| `parlami-avatar-800.png` | YouTube + Facebook profile picture |
| `parlami-avatar-1024.png` | LinkedIn + anywhere wanting high-res |
| `parlami-logo-dark-1660x512.png` | Banners/headers on dark backgrounds (navy baked in) |
| `parlami-logo-light-1660x512.png` | Documents, invoices, light backgrounds (transparent) |
| `parlami-mark-1024.png` | Icon only, transparent — watermarks, favicons, stickers |
| `*.svg` | Masters. Lockup SVGs have Quicksand embedded — render anywhere. |

## Regenerating PNGs

Headless Chromium (snap) renders the SVGs directly. Gotchas learned the hard way:
- snap chromium can't read /tmp or ~/.local/share/fonts — hence fonts embedded in the SVGs
- `--default-background-color` is RGBA hex (`1A1A2EFF` = opaque navy), not ARGB

```sh
chromium-browser --headless --disable-gpu --no-sandbox --hide-scrollbars \
  --default-background-color=00000000 --window-size=1024,1024 \
  --screenshot=out.png "file://$PWD/parlami-mark.svg"
```
