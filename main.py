import zipfile
import os
import shutil

STEAM_PATH = r"C:\Program Files (x86)\Steam\steamapps\common\Balatro"
BUILD_DIR = "build"


def split_balatro_exe():
    with open(os.path.join(STEAM_PATH, "Balatro.exe"), "rb") as f:
        data = f.read()

    zip_start = data.find(b"PK\x03\x04")
    if zip_start == -1:
        raise Exception("❌ ZIP header not found in the executable.")

    with open("love.exe", "wb") as f:
        f.write(data[:zip_start])

    with open("balatro.zip", "wb") as f:
        f.write(data[zip_start:])

    with zipfile.ZipFile("balatro.zip", "r") as zip_ref:
        zip_ref.extractall("balatro_patch")

    print("✅ Extracted: love.exe, balatro.zip, and balatro_patch")


def patch_initial_lua():
    print("🔧 Patching: globals.lua, main.lua and conf.lua")

    # Patch globals.lua
    globals_path = os.path.join("balatro_patch", "globals.lua")
    with open(globals_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    if len(lines) >= 2:
        lines[1] = "VERSION = VERSION .. '-MOD'\n"
    else:
        raise Exception("globals.lua has fewer than 2 lines.")

    with open(globals_path, "w", encoding="utf-8") as f:
        f.writelines(lines)

    print("🔧 Patched: globals.lua with custom VERSION")

    # Patch main.lua
    main_path = os.path.join("balatro_patch", "main.lua")
    main_patch = "\n\nlove.load = nil\nlove.load = function()\n\tG:start_up()\n\tlove.mouse.setVisible(false)\nend\n"

    with open(main_path, "a", encoding="utf-8") as f:
        f.write(main_patch)

    print("🔧 Patched: main.lua with custom love.load")

    # Patch conf.lua
    conf_path = os.path.join("balatro_patch", "conf.lua")
    conf_patch = (
        "\n\nlocal _old = love.conf\n"
        "love.conf = nil\n"
        "love.conf = function(t)\n"
        "\t_old(t)\n"
        '\tt.identity = "BalatroMod"\n'
        "end\n"
    )

    with open(conf_path, "a", encoding="utf-8") as f:
        f.write(conf_patch)

    print("🔧 Patched: conf.lua with identity override")


def apply_mods():
    print("🔧 Applying mods...")
    for mod in os.listdir("mods"):
        mod_path = os.path.join("mods", mod)
        if os.path.isdir(mod_path):
            print(f"🔧 Applying mod: {mod}")

            for root, dirs, files in os.walk(mod_path):
                rel_path = os.path.relpath(root, mod_path)
                target_root = os.path.join("balatro_patch", rel_path)

                os.makedirs(target_root, exist_ok=True)

                for file in files:
                    src_file = os.path.join(root, file)
                    dst_file = os.path.join(target_root, file)

                    if file.endswith(".lua"):
                        if os.path.exists(dst_file):
                            print(f"🔧 Patching Lua: {dst_file}")
                            with open(dst_file, "r", encoding="utf-8") as f:
                                original = f.read()

                            with open(src_file, "r", encoding="utf-8") as f:
                                patch_code = f.read()

                            merged = original + "\n\n-- MOD: " + mod + "\n" + patch_code

                            with open(dst_file, "w", encoding="utf-8") as f:
                                f.write(merged)
                        else:
                            print(f"🔧 Copying new Lua: {dst_file}")
                            shutil.copy2(src_file, dst_file)
                    else:
                        print(f"🔧 Copying file: {dst_file}")
                        shutil.copy2(src_file, dst_file)

def rejoin_balatro_exe():
    with zipfile.ZipFile("balatro_patch.zip", "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk("balatro_patch"):
            for file in files:
                full_path = os.path.join(root, file)
                arcname = os.path.relpath(full_path, "balatro_patch")
                zipf.write(full_path, arcname)

    os.makedirs(BUILD_DIR, exist_ok=True)

    with open("love.exe", "rb") as love_file, open(
        "balatro_patch.zip", "rb"
    ) as zip_file:
        with open(os.path.join(BUILD_DIR, "BalatroMod.exe"), "wb") as output_file:
            output_file.write(love_file.read())
            output_file.write(zip_file.read())

    print("✅ Rebuilt: BalatroMod.exe")


def copy_dlls_and_license():
    for file in os.listdir(STEAM_PATH):
        if (file.endswith(".dll") or file.lower() == "license.txt") and (file.lower() != "luasteam.dll" and file.lower() != "steam_api64.dll"):
            src = os.path.join(STEAM_PATH, file)
            dst = os.path.join(BUILD_DIR, file)
            shutil.copy2(src, dst)

    print("📦 Copied .dll files and license.txt to build/")

# Run the full build pipeline
split_balatro_exe()
patch_initial_lua()
apply_mods()
rejoin_balatro_exe()
copy_dlls_and_license()
print("🎉 Build complete in ./build/")
