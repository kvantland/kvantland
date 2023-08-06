from pathlib import Path

try:
	import tomllib
except ImportError:
	import tomli as tomllib


ROOT = Path(__file__).parent

with open(ROOT / 'config.toml', 'rb') as f:
	config = tomllib.load(f)
