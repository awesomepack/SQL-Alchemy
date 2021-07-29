# importing flask
#localhost:500<url>
from flask import Flask
from flask import jsonify

# Defining an app
app = Flask(__name__);

# List the availible routes
@app.route('/')
def home():
    precip_route = '/api/v1.0/precipitation';
    station_route = '/api/v1.0/stations';
    tobs_route = '/api/v1.0/tobs';
    date_route = '/api/v1.0/<start>'
    date_range_route = '/api/v1.0/<start>/<end>'

    route_dict = {
        'precipitation': precip_route ,
        'stations': station_route , 
        'temp': tobs_route ,
        'date' : date_route ,
        'date_range': date_range_route
    }

    return jsonify(route_dict)


# Defining a new route for my homepage
@app.route('/about')
def about():
    print('Request received for about page...');
    return 'Welcome to my about page'

if __name__ == '__main__':
    app.run(debug = True)

