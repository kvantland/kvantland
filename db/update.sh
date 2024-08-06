#!/bin/bash

set -e

dir="$(dirname "$(realpath "$0")")"
postgres="$1"

if [ -z "$postgres" ]; then
	# read from config.toml
	postgres="$(PYTHONPATH="$dir/.." python3 -c "from config import config; print(config['db']['url'])")"
fi
 
"$dir/set-current-tournament.py" "$postgres"
psql "$postgres" -1 -f "$dir/update-score.sql"
"$dir/insert-new-tournament.py" "$postgres"
"$dir/problems.py" "$postgres"
psql "$postgres" -1 -f "$dir/assign-problems.sql"

