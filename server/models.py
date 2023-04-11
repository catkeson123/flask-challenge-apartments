from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy

db = SQLAlchemy()

class Apartment(db.Model, SerializerMixin):
    __tablename__ = 'apartments'

    serialize_rules = ('-leases.apartment',)

    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer)

    leases = db.relationship("Lease", backref="apartment")

class Tenant(db.Model, SerializerMixin):
    __tablename__ = 'tenants'

    serialize_rules = ('-leases.tenant',)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer, db.CheckConstraint('age >= 18'))

    __table_args__ = (db.CheckConstraint('age >= 18'),)

    leases = db.relationship("Lease", backref="tenant")

class Lease(db.Model, SerializerMixin):
    __tablename__ = 'leases'

    serialize_rules = ('-apartment.leases', '-tenant.leases',)

    id = db.Column(db.Integer, primary_key=True)
    rent = db.Column(db.Float)
    apartment_id = db.Column(db.Integer, db.ForeignKey('apartments.id'))
    tenant_id = db.Column(db.Integer, db.ForeignKey('tenants.id'))

