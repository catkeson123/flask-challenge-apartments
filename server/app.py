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

        # status code messages 
        if response_dict_list:
            response = make_response(response_dict_list, 200)
        
        else:
            response = make_response( {"error": "no apartments found"}, 404)
        
        return response

    def post(self):
        
        # status code messages 
        try:
            new_apartment = Apartment( number = request.form['number'])

            db.session.add(new_apartment)
            db.session.commit()

            response_dict = new_apartment.to_dict()

            response = make_response(response_dict, 201)
        
        except: 
            response = make_response( { 'error': 'could not create apartment, must be a number'}, 400)


        return response

api.add_resource(Apartments, '/apartments')

class ApartmentByID(Resource):

    def get(self, id):

         
        apt = Apartment.query.filter_by(id = id).first()

        # status code messages 
        if apt:
            response_dict = apt.to_dict()
            response = make_response(response_dict, 200)
        else:
            response = make_response( {"error": "no apartment found"}, 404)

        return response

    def patch(self, id):
        apt = Apartment.query.filter(Apartment.id == id).first()
        
        # status code messages 
        if apt:
            for attr in request.form:
                setattr(apt, attr, request.form[attr])
        else:
            response = make_response( {"error": "no apartment found"}, 404)
        
        try:
            db.session.add(apt)
            db.session.commit()
        except:
            db.session.rollback()
            return make_response( {'error': 'failed to update apartment'}, 400 )
 
        response_dict = apt.to_dict()

        response = make_response(response_dict, 200)

        return response

    def delete(self, id):
        
        apt = Apartment.query.filter_by(id = id).first()

        if apt:
            db.session.delete(apt)
            db.session.commit()

            response_dict = {"message": "Apartment successfully deleted"}

            response = make_response(response_dict, 200)

        else:
            response = make_response( {"error": "could not delete apartment"}, 404) 


        return response

api.add_resource(ApartmentByID, '/apartments/<int:id>')

### tenants ###

class Tenants(Resource):

    def get(self):

        response_dict_list = [t.to_dict() for t in Tenant.query.all()]

        response = make_response(response_dict_list, 200)

        return response

    # circle back to this to fix 
    # potential solution: LAG / add an s and run it, and then remove s 
    # potential solution: restart postman  
    def post(self):
        
        try:
            new_tenant = Tenant(
                name = request.form['name'], 
                age = request.form['age'],
            )

            db.session.add(new_tenant)
            db.session.commit()

            response_dict = new_tenant.to_dict()

            # successful creation 201
            response = make_response(response_dict, 201)

        except:
            db.session.rollback()
            response = make_response({"error": "username required and age must be greater than or equal to 18"}, 400)

        return response

api.add_resource(Tenants, '/tenants')

class TenantByID(Resource):

    def get(self, id):
        response_dict = Tenant.query.filter_by(id = id).first().to_dict()

        response = make_response(response_dict, 200)

        return response

    # circle back to this to fix 
    # potential solution: LAG / add an s and run it, and then remove s 
    # potential solution: restart postman  
    def patch(self, id):
        tenant = Tenant.query.filter(Tenant.id == id).first()

        for attr in request.form:
            setattr(tenant, attr, request.form[attr])
        
        db.session.add(tenant)
        db.session.commit()

        response_dict = tenant.to_dict()

        response = make_response(response_dict, 200)

        return response

    def delete(self, id):
        
        tenant = Tenant.query.filter_by(id = id).first()

        db.session.delete(tenant)
        db.session.commit()

        response_dict = {"message": "Tenant successfully deleted"}

        response = make_response(response_dict, 200)

        return response

api.add_resource(TenantByID, '/tenants/<int:id>')

### leases ###

class Leases(Resource):

     def post(self):
        
        new_lease = Lease(rent = request.form['rent'], tenant_id = request.form['tenant_id'], apartment_id = request.form['apartment_id'],)

        db.session.add(new_lease)
        db.session.commit()

        response_dict = new_lease.to_dict()

        response = make_response(response_dict, 201)

        return response

api.add_resource(Leases, '/leases')

class LeaseByID (Resource):

    def delete(self, id):
            
        lease = Lease.query.filter_by(id = id).first()

        db.session.delete(lease)
        db.session.commit()

        response_dict = {"message": "Lease successfully deleted"}

        response = make_response(response_dict, 200)

        return response

api.add_resource(LeaseByID, '/leases/<int:id>')


if __name__ == '__main__':
    app.run(port=3000, debug=True)
