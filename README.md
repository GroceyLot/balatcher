# Balatcher

So it's like a balatro patcher, clone this repo, run the main.py (no requirements) and then run build/BalatroMod.exe.

Only windows support. Probably never gonna update this unless a balatro update makes a breaking change.

Mods should copy as much file structure of the game as they want, all files will be copied into the game folder, replacing any if they need. Any Lua will be appended to the end of its file rather than replaced (sorry if you need to edit profile.lua). 
This can achieve 'mixins' by just doing like:

```
local old = Game.dosomething
Game.dosomething = function(self, ...)
  ...
  return old(self, ...)
end
```
