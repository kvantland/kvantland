from bottle import route
import json
from config import config

@route('/api/dynamic_routes')
def get_dynamic_routes(db):
    current_tournament = config['tournament']['version']
    db.execute('select variant from Kvantland.Problem join Kvantland.Variant using (problem) where tournament=%s', (current_tournament, ))
    problem_routes = list(map(lambda variant: f'/problem/{variant[0]}', db.fetchall()))
    db.execute('select town from Kvantland.Town')
    town_routes = list(map(lambda town: f'/town/{town[0]}', db.fetchall()))
    return json.dumps(problem_routes + town_routes)