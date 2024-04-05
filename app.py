from distutils.log import error
import os
import requests
import datetime
from flask import Flask, session, render_template, request, redirect, jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.sql import text
from datetime import datetime
from werkzeug.utils import secure_filename

#app = Flask(__name__)
app = Flask(__name__, static_folder='static')

app.config['JSON_SORT_KEYS'] = False

# Check for environment variable 
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Manually set up database create_engine(DATABASE_URL) 
# engine = create_engine("DATABASE_URL")

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))

db = scoped_session(sessionmaker(bind=engine))


# Default page redirects
@app.route("/")
def index():
    return redirect("/login")

# Login Page
@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    if request.method == "POST":
        loginUsername = request.form.get("username")
        loginPassword = request.form.get("password")
        
        result = db.execute(text("SELECT * FROM users WHERE username = :username AND password=:password"), {"username":loginUsername, "password":loginPassword}).fetchone()
        if result is None:
            return render_template("login.html", message="Invalid username or password.")
        
        session["user_id"] = result[0]
        session["user_name"] = result[1]

        return redirect("/home")
    
    if request.method == "GET":
        return render_template("login.html")

# Register Page
@app.route("/register", methods=["GET", "POST"])
def register():
    session.clear()
    if request.method == "POST":
        if not request.form.get("username") or not request.form.get("password"):
            return render_template("register.html", message="Username and Password cannot be blank.")
        registerUsername = request.form.get("username")
        registerPassword = request.form.get("password")

        userExists = db.execute(text("SELECT * FROM users WHERE username = :username"), {"username":registerUsername}).fetchone()
        if not userExists:
            db.execute(text("INSERT INTO users (username, password) VALUES (:username, :password)"), {"username":registerUsername, "password":registerPassword})
            db.commit()
            return render_template("register.html", message="Account created successfully.")
        return render_template("register.html", message="User already exists.")
        
    if request.method == "GET":
        return render_template("register.html")

# Logout Page
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

# API to get positions
@app.route('/api/positions', methods=['GET'])
def get_positions():
    print("ajax request")
    if session:
        positions = db.execute(text("SELECT * FROM updates ORDER BY update_time DESC")).fetchall()
        positions_list = [{'latitude': pos.latitude, 'longitude': pos.longitude, 'location': pos.update_location, 'description': pos.comments, 'timestamp': pos.update_time, 'user': pos.update_user} for pos in positions]
        print(positions_list)
        return jsonify(positions_list)
    else:
        return redirect("/login")

#handle image upload
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ['jpg', 'jpeg', 'png'] 


# Map Home Page
@app.route("/home", methods=["GET", "POST"])
def home():
    if request.method == "GET":
        if session:
            results = db.execute(text("SELECT * FROM updates ORDER BY update_time DESC LIMIT 10")).fetchall()
            if len(results) == 0:
                return render_template("home.html", message="No Updates", welcome=("Signed in as: "+ session["user_id"]))

            return render_template("home.html", results = results, welcome=("Signed in as: "+ session["user_id"]))
        else:
            return redirect("/login")
    
    if request.method == "POST":
        if session:

            currentuser = session["user_id"]
            location = request.form.get("locdesc")
            comments = request.form.get("comments")

            file = request.files['cameraInput']
            latitude = request.form.get('latitude')
            longitude = request.form.get('longitude')

            print("latitude: ", latitude)
            print("longitude: ", longitude)
            print("filename: ", file.filename)
            if latitude=="" or longitude=="":
                latitude = 0
                longitude = 0
            
            if location=="" or comments=="":
                results = db.execute(text("SELECT * FROM updates ORDER BY update_time DESC LIMIT 10")).fetchall()
                if len(results) == 0:
                    return render_template("home.html", message="No Updates", error="All fields must be filled in", welcome=("Signed in as: "+ session["user_id"]))
                return render_template("home.html", results = results, error="All fields must be filled in", welcome=("Signed in as: "+ session["user_id"]))      
            
            unique_filename = "No_Image_Available.jpg"
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                unique_filename = f'{datetime.now().strftime("%Y%m%d%H%M%S%f")}_{filename}'
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], unique_filename))
            

            db.execute(text("INSERT INTO updates (update_user, comments, update_location, update_time, photo_filename,longitude,latitude) VALUES(:currentuser, :comments, :location, current_timestamp(0), :unique_filename, :longitude, :latitude)"), {"currentuser": currentuser, "comments":comments, "location": location, "unique_filename": unique_filename, "longitude": longitude, "latitude": latitude})
            db.commit()

            results = db.execute(text("SELECT * FROM updates ORDER BY update_time DESC LIMIT 10")).fetchall()            
            if len(results) == 0:
                return render_template("home.html", message="No Updates", welcome=("Signed in as: "+ session["user_id"]))

            return render_template("home.html", pmessage="Update Posted", results = results, welcome=("Signed in as: "+ session["user_id"]))
        
        else:
            return redirect("/login")

# Updates Page
@app.route("/updates", methods=["GET"])
def updates():
    # Checks if user is logged in
    if request.method == "GET":
        if session:
            results = db.execute(text("SELECT * FROM updates ORDER BY update_time DESC")).fetchall()
            if len(results) == 0:
                return render_template("updates.html", message="No Updates", welcome=("Signed in as: "+ session["user_id"]))

            return render_template("updates.html", results = results, welcome=("Signed in as: "+ session["user_id"]))
        else:
            return redirect("/login")

@app.route('/analytics', methods=['GET'])
def analytics():
    # GET request
    if request.method == 'GET':
        current_month = datetime.now().strftime('%m')
        current_day = datetime.now().strftime('%d')
        current_time = current_month + "/" + current_day
        accidents = db.execute(text("SELECT count(*) FROM accidents2023 WHERE start_dt LIKE '%' || :current_time || '%'"), {"current_time":current_time}).fetchone()
        accidents = accidents[0]

        accidentsNE = db.execute(text("SELECT count(*) FROM accidents2023 WHERE quadrant='NE' AND start_dt LIKE '%' || :current_time || '%'"), {"current_time":current_time}).fetchone()
        accidentsNE = accidentsNE[0]

        accidentsNW = db.execute(text("SELECT count(*) FROM accidents2023 WHERE quadrant='NW' AND start_dt LIKE '%' || :current_time || '%'"), {"current_time":current_time}).fetchone()
        accidentsNW = accidentsNW[0]

        accidentsSE = db.execute(text("SELECT count(*) FROM accidents2023 WHERE quadrant='SE' AND start_dt LIKE '%' || :current_time || '%'"), {"current_time":current_time}).fetchone()
        accidentsSE = accidentsSE[0]

        accidentsSW = db.execute(text("SELECT count(*) FROM accidents2023 WHERE quadrant='SW' AND start_dt LIKE '%' || :current_time || '%'"), {"current_time":current_time}).fetchone()
        accidentsSW = accidentsSW[0]        

        message = {'accidents':accidents, 'accidentsNE':accidentsNE, 'accidentsNW':accidentsNW, 'accidentsSE':accidentsSE, 'accidentsSW':accidentsSW}
        return jsonify(message) 

# if __name__ == '__main__':
#     app.run(debug=True)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')



