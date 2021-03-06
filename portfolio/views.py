''' site views '''
from datetime import datetime, timedelta
from flask import render_template
import json

from portfolio import app, flora, models

# ROUTES
@app.route('/')
def index():
    ''' render the basic template for angular '''
    return render_template('index.html')


@app.route('/<path>')
def angular(path):
    ''' render the basic template for angular '''
    return render_template('index.html')


# the fun stuff API
@app.route('/api/flora')
def flower_names():
    ''' returns a made up flower name '''
    name = {'common': flora.get_common_name(), 'scientific': flora.get_scientific_name()}
    return json.dumps(name)


@app.route('/api/activity')
def get_activity():
    ''' load activity from all time '''
    data = []
    limit = datetime.now() - timedelta(days=14)
    activity_data = models.get_activity(limit)

    stats = {'days': []}
    data = [item.serialize() for item in activity_data]

    for day in (limit + timedelta(n) for n in range(15)):
        stats['days'].append({
            'date': day.isoformat()[:10],
            'count': len([i for i in data if \
                i['time'][:10] == day.isoformat()[:10]])
            })
    stats['total'] = sum([day['count'] for day in stats['days']])

    return json.dumps({'stats': stats, 'activity': data})
