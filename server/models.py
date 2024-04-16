from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(
    naming_convention={
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    }
)

db = SQLAlchemy(metadata=metadata)


class Restaurant(db.Model, SerializerMixin):
    __tablename__ = "restaurants"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    address = db.Column(db.String)

    # add relationship
 # add relationship
    pizzas = db.relationship("RestaurantPizza", back_populates="restaurant")
    # add serialization rules
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "address": self.address,
            "pizzas": [pizza.serialize() for pizza in self.pizzas]
        }

    def __repr__(self):
        return f"<Restaurant {self.name}>"


class Pizza(db.Model, SerializerMixin):
    __tablename__ = "pizzas"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    ingredients = db.Column(db.String)

    # add relationship
    restaurant_pizzas = db.relationship("RestaurantPizza", back_populates="pizza")

    # add serialization rules
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "ingredients": self.ingredients
        }

    def __repr__(self):
        return f"<Pizza {self.name}, {self.ingredients}>"


class RestaurantPizza(db.Model, SerializerMixin):
    __tablename__ = "restaurant_pizzas"

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer, nullable=False)

    pizza_id=db.Column(db.Integer,db.ForeignKey('restaurants.id', ondelete='CASCADE'))
    restaurant_id=db.Column(db.Integer,db.ForeignKey('pizzas.id', ondelete='CASCADE'))

    # add relationships
    pizza = db.relationship("Pizza", back_populates="restaurant_pizzas")
    restaurant = db.relationship("Restaurant", back_populates="pizzas")

    # add serialization rules
    def serialize(self):
        return {
            "id": self.id,
            "price": self.price,
            "pizza": self.pizza.serialize(),
            "restaurant": self.restaurant.serialize()
        }

    # add validation
@validates("price")
def validate_price(self, key, price):
        if price <= 0:
            raise ValueError("Price must be greater than zero.")
        return price

def __repr__(self):
        return f"<RestaurantPizza ${self.price}>"
