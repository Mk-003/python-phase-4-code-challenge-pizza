#!/usr/bin/env python3
from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)


@app.route("/")
def index():
    return "<h1>Code challenge</h1>"



class Pizzas(Resource):

    def get(self):

        response_dict_list = [pizza.serialize() for pizza in Pizza.query.all()]

        response = make_response(
            response_dict_list,
            200,
        )

        return response

    def post(self):

        new_record = Pizza(
            title=request.form['title'],
            body=request.form['body'],
        )

        db.session.add(new_record)
        db.session.commit()

        response_dict = new_record.to_dict()

        response = make_response(
            response_dict,
            201,
        )

        return response

api.add_resource(Pizzas, '/pizzas')



class PizzaByID(Resource):
    

    def get(self, id):

        response_dict = Pizza.query.filter_by(id=id).first().to_dict()

        response = make_response(
            response_dict,
            200,
        )

        return response

    def patch(self, id):

        record = Pizza.query.filter_by(id=id).first()
        for attr in request.form:
            setattr(record, attr, request.form[attr])

        db.session.add(record)
        db.session.commit()

        response_dict = record.to_dict()

        response = make_response(
            response_dict,
            200
        )

        return response

    def delete(self, id):

        record = Pizza.query.filter_by(id=id).first()

        db.session.delete(record)
        db.session.commit()

        response_dict = {"message": "record successfully deleted"}

        response = make_response(
            response_dict,
            200
        )

        return response

api.add_resource(PizzaByID, '/pizzas/<int:id>')

class Restaurants(Resource):

    def get(self):

        response_dict_list = [restaurant.to_dict() for restaurant in Restaurant.query.all()]

        response = make_response(
            response_dict_list,
            200,
        )

        return response

    def post(self):

        new_record = Restaurant(
            title=request.form['title'],
            body=request.form['body'],
        )

        db.session.add(new_record)
        db.session.commit()

        response_dict = new_record.to_dict()

        response = make_response(
            response_dict,
            201,
        )

        return response

api.add_resource(Restaurants, '/restaurants')


class RestaurantByID(Resource):
    

    def get(self, id):

        response_dict = Restaurant.query.filter_by(id=id).first().to_dict()

        response = make_response(
            response_dict,
            200,
        )

        return response

    def patch(self, id):

        record = Restaurant.query.filter_by(id=id).first()
        for attr in request.form:
            setattr(record, attr, request.form[attr])

        db.session.add(record)
        db.session.commit()

        response_dict = record.to_dict()

        response = make_response(
            response_dict,
            200
        )

        return response

    def delete(self, id):

        record = Restaurant.query.filter_by(id=id).first()

        db.session.delete(record)
        db.session.commit()

        response_dict = {"message": "record successfully deleted"}

        response = make_response(
            response_dict,
            200
        )

        return response

api.add_resource(RestaurantByID, '/restaurants/<int:id>')



if __name__ == "__main__":
    app.run(port=5555, debug=True)
