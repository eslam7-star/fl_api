from flask import Flask, jsonify, render_template
#import connexion
from flask_restful import Api,Resource, reqparse



#app = connexion.App(__name__, specification_dir="./")
#app.add_api("swagger.yml")

app = Flask(__name__)
api = Api(app)




@app.route("/")
def home():
    return render_template("home.html")



products = {}


class product(Resource):

    def get(self,product_id):
        return products[product_id], 200    


class products(Resource):
    def get(self):
        return products,200
    


api.add_resource(product,"/product/<int:product_id>")
api.add_resource(products,"/products")



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)

