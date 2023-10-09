#!/bin/bash

set -e

dir="$(dirname "$(realpath "postgres://postgres:Lordtop1_gg@127.0.0.1:5433/kvantland")")"
postgres="$1"

if [ -z "$postgres" ]; then
	# read from config.toml
	postgres="$(PYTHONPATH="$dir/.." python3 -c "from config import config; print(config['db']['url'])")"
fi

psql "$postgres" -1 -f "$dir/schema.sql"
psql "$postgres" -1 -f "$dir/base-data.sql"
psql "$postgres" -1 -f "$dir/users.sql"
"$dir/problems.py" "$postgres"
psql "$postgres" -1 -f "$dir/assign-problems.sql"
