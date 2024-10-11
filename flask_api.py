from flask import Flask, jsonify, redirect, render_template, request ,session, flash
#import connexion
from flask_restful import Api,Resource, reqparse



#app = connexion.App(__name__, specification_dir="./")
#app.add_api("swagger.yml")

app = Flask(__name__, template_folder='templates')
api = Api(app)
app.secret_key ='askfnasfnalksfnd12234'


request_par = reqparse.RequestParser()
request_par.add_argument("name",type=str,help="name of product", required=True)
request_par.add_argument("id",type=int,help="product id", required=True)
request_par.add_argument("pr_count",type=int,help="product count" , required=True)


productss = []
users = {}


@app.route("/")
def home():
    return render_template("home.html")



@app.route("/login", methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    elif request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username in users :
            if password == users[username]['password']:
                flash("loged in successfully")
                session['username'] = username
                session['password'] = password  
                
                return render_template('/dashboard.html' , username = username  , user_type = users[username]['type'] , email = users[username]['email'] )
        else:
            return 'invalid'



@app.route("/register", methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    elif request.method == 'POST':
        user_name = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password') 
        type = request.form.get('type')

        if user_name in users:
            flash("user already found ")
            render_template("register.html")
        else:
            users[user_name] = {
                'email' : email,
                'password' : password,
                'type' : type
            }
            flash('Registration successful! You can log in now.')
            return redirect('/login')
        

@app.route('/logout')
def logout():
    session.clear()
    return render_template('/home.html')



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
    

    def delete(self, product_id):
        args = request_par.parse_args()
        pro = {
            

        }

class products(Resource):
    def get(self):
        return productss,200
    


api.add_resource(product,"/product/<int:product_id>")
api.add_resource(products,"/products")



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)

