from flask import Flask, render_template, redirect, url_for, request, jsonify, make_response
from model.models import db, load_db, Place_obj, Category, Page  # Flask-SQLAlchemy
import service.service
from flask_restplus import Api, Resource, Namespace

app = Flask(__name__)
app_api = Api(app=app,
          version="1.0",
          title="Sights Info App",
          description="Get Information About A Location.")

def getApp():
    return app

# Flask-SQLAlchemy: Initialize
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
db.init_app(app)  # Bind SQLAlchemy to this Flask webapp

"""Define namespace"""
sights_name_space = app_api.namespace("sights", description='Get info about sights')

# Create the database tables and records inside a temporary test context
with app.test_request_context():
    load_db(db)

@app.route('/')
@app.route('/home')
def home():
    return render_template("home.html")

@app.route('/get_info')
def get_info():
    place = request.args.get('place')
    sections = service.service.get_sections_list(place)
    categories = service.service.get_all_categories()
    img_url = service.service.get_image(place)
    return render_template("get_info.html", place = place, sections = sections, categories = categories, image_url = img_url)

# PUT: place + category => add_place_to_db_new_page
@sights_name_space.route("/<string:place>/<string:category>")
class AddPlace(Resource):
    @app_api.doc(responses={200: 'OK'}, description="Add new place")
#    @cross_origin()
    def put(self, place, category):
        service.service.add_place_to_db_new_page(place, category)
        return {"Status": "OK"}

@app.route('/save_page', methods = ['POST'])
def save_page():
    place = request.form['place']
    category = request.form['category']
    print(category)
    if category.strip() not in service.service.get_all_categories():
        service.service.add_category(category)
    service.service.add_place_to_db_new_page(place, category.strip())
    return redirect(url_for('to_visit'))

@sights_name_space.route("/<string:place>/")  # Define the route
class GetCategory(Resource):
    @app_api.doc(responses={200: 'OK', 400: 'Invalid Argument'}, description="Get category of the place")
    def get(self, place):
        titles = service.service.get_all_titles()
        if place in titles:
            category = service.service.get_category(place)
            return {"category": category}
        else:
            sights_name_space.abort(400, status="Place is not the database.", statusCode="400")

@app.route("/to_visit")
def to_visit():
    categories = service.service.get_all_categories()
    places = service.service.get_all_places()
    return render_template("to_visit.html", categories_list=categories, places_list=places)

if __name__ == '__main__':
    app.debug = True  # Turn on auto reloader and debugger
    app.config['SQLALCHEMY_ECHO'] = True  # Show SQL commands created
    app.run()


#https://git.heroku.com/travel-info.git