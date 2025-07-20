from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Sample initial data
destinations = [
    {'id': 1, 'name': 'Paris', 'region': 'Europe', 'image': 'images/paris.jpg', 'description': 'The City of Light and love.'},
    {'id': 2, 'name': 'Tokyo', 'region': 'Asia', 'image': 'images/tokyo.jpg', 'description': 'A vibrant city blending tradition and technology.'},
    {'id': 3, 'name': 'New York City', 'region': 'North America', 'image': 'images/nyc.jpg', 'description': 'The city that never sleeps.'},
]

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        name = request.form.get('name')
        region = request.form.get('region')
        description = request.form.get('description')
        image = request.form.get('image')  # Image filename expected to be in static/images/
        if name and region and description and image:
            new_id = max(d['id'] for d in destinations) + 1 if destinations else 1
            destinations.append({
                'id': new_id,
                'name': name,
                'region': region,
                'description': description,
                'image': f'images/{image}'
            })
            return redirect(url_for('home'))

    regions = sorted(set(d['region'] for d in destinations))
    selected_region = request.args.get('region')
    filtered = [d for d in destinations if d['region'] == selected_region] if selected_region else destinations
    return render_template('home.html', destinations=filtered, regions=regions, selected_region=selected_region)

@app.route('/destination/<int:dest_id>')
def destination(dest_id):
    dest = next((d for d in destinations if d['id'] == dest_id), None)
    if not dest:
        return "Destination not found", 404
    return render_template('destination.html', destination=dest)



if __name__ == '__main__':
    app.run(debug=True)
