#!/bin/bash
clear; clear
cd ~ || exit

# shellcheck source=~
. ~/.profile
failed=0

while read -r line; do
  if [ "$line" == "exit \$failed" ]; then skip=0; continue; fi
  if [ ${skip=1} -eq 1 ]; then continue; fi
  if $line
  then
    echo "$line...success."
    success=$((${success=0}+1))
  else
    echo "$line...failed."
    failed=$((failed+1))
  fi
done < "$0"

echo "total: $((success+failed))"
echo "success: ${success=0}"
echo "failed: $failed"

exit $failed
python3.9 arclight.py
python3.9 bungeecord.py
python3.9 nukkitx.py
python3.9 paperspigot.py
python3.9 pocketmine.py
python3.9 purpur.py
python3.9 spongeforge.py
python3.9 spongevanilla.py
python3.9 velocity.py
python3.9 waterfall.py
python3.9 lightfall.py
python3.9 lightfallclient.py
docker start sync_spigot_jdk8 && docker attach sync_spigot_jdk8
docker start sync_spigot_jdk16 && docker attach sync_spigot_jdk16
docker start sync_spigot_jdk17 && docker attach sync_spigot_jdk17