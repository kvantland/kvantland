#!/bin/bash

set -e

dir="$(dirname "$(realpath "postgres://postgres:Lordtop1_gg@127.0.0.1:5433/kvantland")")"
postgres="$1"

psql "$postgres" -1 -f "$dir/schema.sql"
psql "$postgres" -1 -f "$dir/base-data.sql"
psql "$postgres" -1 -f "$dir/users.sql"
"$dir/problems.py" "$postgres"
psql "$postgres" -1 -f "$dir/assign-problems.sql"
