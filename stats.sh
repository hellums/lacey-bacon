# Provides a short table of git add/change/del activity from logs since Monday

git log --shortstat --since="24 Jan, 2022" | grep -E "fil(e|es) changed" | awk '{files+=$1; inserted+=$4; deleted+=$6; delta+=$4-$6; ratio=deleted/inserted} END {printf "Commit stats:\n- Files changed (total).. %s\n- Lines added (total).... %s\n- Lines deleted (total).. %s\n- Total lines (delta).... %s\n- Add./Del. ratio (1:n).. 1 : %s\n", files, inserted, deleted,
delta, ratio}' -

