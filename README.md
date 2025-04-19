# Balatcher

So it's like a balatro patcher, clone this repo, run the main.py (no requirements) and then run build/BalatroMod.exe (all necessary DLLs and the license.txt are copied to build).

Only windows support. Probably never gonna update this unless a balatro update makes a breaking change. It also removes all connection to steam and saves in a different folder.

Mods should copy as much file structure of the game as they want, all files will be copied into the game folder, replacing any if they need. Any Lua will be appended to the end of its file rather than replaced (sorry if you need to edit profile.lua). 
This can achieve 'mixins' by just doing like:

```
local old = Game.dosomething
Game.dosomething = function(self, ...)
  ...
  return old(self, ...)
end
```

If you don't understand, just look at my example mod which removes pixel art from the shaders (overwriting them) and the UIElement.draw_pixelated_rect function.

I really hope this is allowed because I'm not sharing any source code.
