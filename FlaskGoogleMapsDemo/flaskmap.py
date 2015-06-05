from flask import Flask
from flask import render_template
from flask.ext.googlemaps import GoogleMaps
from flask.ext.googlemaps import Map

app = Flask(__name__)
GoogleMaps(app)

@app.route('/')
def mapdemo():
    # creating a map in the view
    flaskmap = Map(
        identifier="test",
        lat=37.4419,
        lng=-122.1419,
        markers=[(37.4419, -122.1419)],
        style="width:100%;height:100%;"
    )
    return render_template('map.html',mymap=flaskmap)

if __name__=='__main__':
    app.run(debug=True)
