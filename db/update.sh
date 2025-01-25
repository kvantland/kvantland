#!/bin/bash

set -e

dir="$(dirname "$(realpath "$0")")"
postgres="$1"

if [ -z "$postgres" ]; then
	# read from config.toml
	postgres="$(PYTHONPATH="$dir/.." python3 -c "from config import config; print(config['db']['url'])")"
fi
 
python3 "$dir/set-current-tournament.py" "$postgres"
psql "$postgres" -1 -f "$dir/update-score.sql"

# only for first use in each tournament type (math, IT, etc), if column classes is not in table
psql "$postgres" -1 -f "$dir/fill-classes.sql" 

python3 "$dir/problems.py" "$postgres"
psql "$postgres" -1 -f "$dir/assign-problems.sql"

