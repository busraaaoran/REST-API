from flask import Flask
from flask_restful import reqparse, Api, Resource, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///MyDB.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#database models creation
class ProductModel(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = True)
    price = db.Column(db.Integer, nullable = True)

    def __rep__(self):
        return f"Product(name = {name}, price = {price})"


class CustomerModel(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = True)
    age = db.Column(db.Integer, nullable = True)
    gender = db.Column(db.String(20), nullable = True)

    def __rep__(self):
        return f"Customer(name = {name}, age = {age}, gender = {gender})"


class BrandModel(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = True)

    def __rep__(self):
        return f"Brand(name = {name})"


class ColorModel(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = True)

#db.create_all() it will run just once to create db

#parser creation
product_put_args = reqparse.RequestParser()
product_put_args.add_argument("name", type=str, help="Name of the product")
product_put_args.add_argument("price", type=int, help="Price of the product")

product_post_args = reqparse.RequestParser()
product_post_args.add_argument("name", type=str, help="Name of the product")
product_post_args.add_argument("price", type=int, help="Price of the product")


customer_put_args = reqparse.RequestParser()
customer_put_args.add_argument("name", type=str, help="Name of the customer")
customer_put_args.add_argument("age", type=int, help="Age of the customer")
customer_put_args.add_argument("gender", type=str, help="Gender of the customer")

customer_post_args = reqparse.RequestParser()
customer_post_args.add_argument("name", type=str, help="Name of the customer")
customer_post_args.add_argument("age", type=int, help="Age of the customer")
customer_post_args.add_argument("gender", type=str, help="Gender of the customer")


brand_put_args = reqparse.RequestParser()
brand_put_args.add_argument("name", type=str, help="Name of the brand")

brand_post_args = reqparse.RequestParser()
brand_post_args.add_argument("name", type=str, help="Name of the brand")


color_put_args = reqparse.RequestParser()
color_put_args.add_argument("name", type=str, help="Name of the color")

color_post_args = reqparse.RequestParser()
color_post_args.add_argument("name", type=str, help="Name of the color")

# def abort_if_product_doesnt_exist(product_id):
#     if product_id not in products:
#         abort(404, message="There is no such product with this ID!")

#resource fields creation

product_resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'price': fields.Integer
}

customer_resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'age': fields.Integer,
    'gender': fields.String
}

brand_resource_fields = {
    'id': fields.Integer,
    'name': fields.String
}

color_resource_fields = {
    'id': fields.Integer,
    'name': fields.String
}

#API endpoints creation

class Product(Resource):
    @marshal_with(product_resource_fields)
    def get(self, product_id):
        result = ProductModel.query.filter_by(id=product_id).first()

        if not result:
            abort(404, message="There is no such product with that ID!")

        return result, 200

    @marshal_with(product_resource_fields)
    def post(self, product_id):
        args = product_post_args.parse_args()
        result = ProductModel.query.filter_by(id=product_id).first()

        if result:
            abort(409, message="This product ID is already taken!")
        
        product = ProductModel(id=product_id, name= args['name'], price= args['price'])
        db.session.add(product)
        db.session.commit()

        return product, 201

    @marshal_with(product_resource_fields)
    def put(self, product_id):
        args = product_put_args.parse_args()
        result = ProductModel.query.filter_by(id=product_id).first()

        if not result:
            abort(404, message="This product does not exist!")

        if args['name']:
            result.name = args['name']
        if args['price']:
            result.price = args['price']

        db.session.commit()

        return result, 200

    def delete(self, product_id):
        result = ProductModel.query.filter_by(id=product_id).first()
        if not result:
            abort(404, message="There is no product with that ID to delete!")

        db.session.delete(result)
        db.session.commit()
        return '', 204


class Customer(Resource):
    @marshal_with(customer_resource_fields)
    def get(self, c_id):
        result = CustomerModel.query.filter_by(id=c_id).first()

        if not result:
            abort(404, message="There is no such customer with that ID!")

        return result, 200

    @marshal_with(customer_resource_fields)
    def post(self, c_id):
        args = customer_post_args.parse_args()
        result = CustomerModel.query.filter_by(id=c_id).first()
        if result:
            abort(409, message="Customer already exist with that ID")
        
        customer = CustomerModel(id=c_id, name= args['name'], age= args['age'], gender= args['gender'])
        db.session.add(customer)
        db.session.commit()

        return customer, 201

    @marshal_with(customer_resource_fields)
    def put(self, c_id):
        args = customer_put_args.parse_args()
        result = CustomerModel.query.filter_by(id=c_id).first()
        if not result:
            abort(404, message="This customer does not exist!")
        
        if args['name']:
            result.name = args['name']
        if args['age']:
            result.age = args['age']
        if args['gender']:
            result.gender = args['gender']
        
        db.session.commit()

        return result, 200

    def delete(self, c_id):

        result = CustomerModel.query.filter_by(id=c_id).first()

        if not result:
            abort(404, message="There is no customer with that ID to be deleted!")

        db.session.delete(result)
        db.session.commit()

        return '', 204

class Brand(Resource):

    @marshal_with(brand_resource_fields)
    def get(self, brand_id):

        result = BrandModel.query.filter_by(id=brand_id).first()
        if not result:
            abort(404, message="There is no such brand with that ID!")

        return result, 200

    @marshal_with(brand_resource_fields)
    def post(self, brand_id):
        args = brand_post_args.parse_args()
        result = BrandModel.query.filter_by(id=brand_id).first()

        if result:
            abort(409, message="Brand already exists with that ID!")
        
        brand = BrandModel(id=brand_id, name= args['name'])

        db.session.add(brand)
        db.session.commit()

        return brand, 201

    @marshal_with(brand_resource_fields)
    def put(self, brand_id):
        args = brand_put_args.parse_args()
        result = BrandModel.query.filter_by(id=brand_id).first()

        if not result:
            abort(404, message="This brand does not exist!")

        if args['name']:
            result.name = args['name']
        
        db.session.commit()

        return result, 200

    def delete(self, brand_id):
        result = BrandModel.query.filter_by(id=brand_id).first()
        if not result:
            abort(404, message="There is no brand with that ID to be deleted!")

        db.session.delete(result)
        db.session.commit()

        return '', 204


class Color(Resource):

    @marshal_with(color_resource_fields)
    def get(self, color_id):

        result = ColorModel.query.filter_by(id=color_id).first()

        if not result:
            abort(404, message="There is no such color with that ID!")
        
        return result, 200

    @marshal_with(color_resource_fields)
    def post(self, color_id):
        args = color_post_args.parse_args()
        result = ColorModel.query.filter_by(id=color_id).first()

        if result:
            abort(409, message="Color already exists with that ID!")

        color = ColorModel(id=color_id, name= args['name'])

        db.session.add(color)
        db.session.commit()

        return color, 201

    @marshal_with(color_resource_fields)
    def put(self, color_id):
        args = color_put_args.parse_args()
        result = ColorModel.query.filter_by(id=color_id).first()

        if not result:
            abort(404, message="This color does not exist!")

        if args['name']:
            result.name = args['name']
        
        db.session.commit()

        return result, 200

    def delete(self, color_id):

        result = ColorModel.query.filter_by(id=color_id).first()
        if not result:
            abort(404, "There is no color with that ID to be deleted!")

        db.session.delete(result)
        db.session.commit()

        return '', 204

#endpoints definiton

api.add_resource(Product, "/product/<int:product_id>")
api.add_resource(Customer, "/customer/<int:c_id>")
api.add_resource(Brand, "/brand/<int:brand_id>")
api.add_resource(Color, "/color/<int:color_id>")

if __name__ == "__main__":
    app.run(debug= True)

