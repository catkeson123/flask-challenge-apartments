from flask import Flask, make_response, request
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Apartment, Tenant, Lease

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///apartments.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)


class Home(Resource):

    def get(self):

        response_dict = {
            "message": "Welcome to the Apartments API",
        }

        response = make_response(
            response_dict,
            200
        )

        return response


api.add_resource(Home, '/')


class Apartments(Resource):

    def get(self):
        response_dict_list = [a.to_dict() for a in Apartment.query.all()]

        response = make_response(response_dict_list, 200)

        return response

    def post(self):
        
        new_apartment = Apartment( number = request.form['number'])

        db.session.add(new_apartment)
        db.session.commit()

        response_dict = new_apartment.to_dict()

        response = make_response(response_dict, 201)

        return response

api.add_resource(Apartments, '/apartments')

class ApartmentByID(Resource):

    def get(self, id):
        response_dict = Apartment.query.filter_by(id = id).first().to_dict()

        response = make_response(response_dict, 200)

        return response

    def patch(self, id):
        apt = Apartment.query.filter(Apartment.id == id).first()

        for attr in request.form:
            setattr(apt, attr, request.form[attr])
        
        db.session.add(apt)
        db.session.commit()

        response_dict = apt.to_dict()

        response = make_response(response_dict, 200)

        return response

    def delete(self, id):
        
        apt = Apartment.query.filter_by(id = id).first()

        db.session.delete(apt)
        db.session.commit()

        response_dict = {"message": "Apartment successfully deleted"}

        response = make_response(response_dict, 200)

        return response

api.add_resource(ApartmentByID, '/apartments/<int:id>')


if __name__ == '__main__':
    app.run(port=3000, debug=True)
