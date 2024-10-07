from flask import Flask, jsonify, render_template
#import connexion
from flask_restful import Api,Resource, reqparse



#app = connexion.App(__name__, specification_dir="./")
#app.add_api("swagger.yml")

app = Flask(__name__)
api = Api(app)


request_par = reqparse.RequestParser()
request_par.add_argument("name",type=str,help="name of product", required=True)
request_par.add_argument("id",type=int,help="product id", required=True)
request_par.add_argument("pr_count",type=int,help="product count" , required=True)


@app.route("/")
def home():
    return render_template("home.html")



productss = []


class product(Resource):

    def get(self, product_id):
        if 0 <= product_id < len(productss):
            return productss[product_id], 200
        return {"message": "Product not found"}, 404

    def put(self, product_id):
        if 0 <= product_id < len(productss):
            args = request_par.parse_args()
            productss[product_id] = {
                "id": args["id"],
                "name": args["name"],
                "pr_count": args["pr_count"]
            }
            return {"message": "Product updated successfully"}, 200
        return {"message": "Product not found"}, 404
    

    def post(self,product_id):
        args = request_par.parse_args()
        pro = {
            "id": args["id"],
            "name": args["name"],
            "pr_count": args["pr_count"]
        }
        productss.append(pro)
        return {"response": "done"}, 200
    



class products(Resource):
    def get(self):
        return productss,200
    


api.add_resource(product,"/product/<int:product_id>")
api.add_resource(products,"/products")



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)

