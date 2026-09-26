#!/bin/bash
# One scripted drive of the driver test: FORK=<the fork's checkout> ./run_drive.sh SEED LABEL [sim]
# The fork at the column's commit (README, "The arms"); "sim" starts sim_a_server.py (option A swapped in) instead
# of the plain dev server. Temporary settings on top of the fork's dev settings.yaml (the seed, calls at 20-40 s,
# contacts of exactly 3 answers), the dev server on 8010 for this drive only, then the settings restored and
# checked, even on failure. Into raw/: the driver's output, the server's log, and a copy of the run record.
set -u
FORK=${FORK:?set FORK to the TalkWithZombies checkout}
HERE=$(cd "$(dirname "$0")" && pwd)
RAW=$HERE/raw
SEED=$1
LABEL=$2
OUT=$RAW/drive-$LABEL-$SEED.txt
[ -e "$OUT" ] && { echo "$OUT exists (the record); use a new label"; exit 1; }
cd "$FORK" || exit 1
[ "$(tail -2 settings.yaml)" = "$(printf 'show:\n  seed: 42')" ] \
    || { echo "settings.yaml must end with a show: section holding only seed: 42; stopping"; exit 1; }
BACKUP=$(mktemp)
cp settings.yaml "$BACKUP"
restore() {
    [ -n "${PID:-}" ] && kill "$PID" 2>/dev/null && wait "$PID" 2>/dev/null
    cp "$BACKUP" settings.yaml
    cmp settings.yaml "$BACKUP" && echo "settings.yaml restored" && rm "$BACKUP"
}
trap restore EXIT
sed "s/^  seed: 42$/  seed: $SEED/" "$BACKUP" > settings.yaml
printf '  interaction_min_s: 20\n  interaction_max_s: 40\n  contact_jitter: 0\n' >> settings.yaml
mkdir -p "$RAW/runs"
if [ "${3:-}" = sim ]; then
    .venv/bin/python "$HERE/sim_a_server.py" > "$RAW/dev-server-8010-$LABEL-$SEED.log" 2>&1 &
else
    .venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8010 > "$RAW/dev-server-8010-$LABEL-$SEED.log" 2>&1 &
fi
PID=$!
curl -s -o /dev/null --retry 20 --retry-connrefused --retry-delay 1 http://127.0.0.1:8010/show || exit 1
python3 scripts/drive_show.py --rounds 40 \
    --heard "Hello? Is anyone there?" --heard "My name is Alfredo." \
    --heard "I'm in Austin, Texas, and I have a pickup truck." \
    --heard "This is Maria, from Dallas." --heard "We have a doctor with us." --heard "Do you need medicine?" \
    --heard "Hello again, lab." --heard - \
    --heard "It's me, Alfredo, from Austin. I still have the truck." --heard "Where should I drive?" \
    --heard - --heard - \
    > "$OUT" 2>&1
echo "drive exit $? -> raw/drive-$LABEL-$SEED.txt"
RUN=$(sed -n 's|^record: runs/\(.*\)/script.json$|\1|p' "$OUT")
[ -n "$RUN" ] && mkdir -p "$RAW/runs/$RUN" && cp "runs/$RUN/script.json" "$RAW/runs/$RUN/" \
    && echo "record copied -> raw/runs/$RUN/script.json"
