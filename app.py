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
import pandas as pd
from keplergl import KeplerGl
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
    # print("ajax request")
    if session:
        positions = db.execute(text("SELECT * FROM reports ORDER BY report_time DESC")).fetchall()
        positions_list = [{'latitude': pos.latitude, 'longitude': pos.longitude, 'location': pos.report_location, 'description': pos.comments, 'timestamp': pos.report_time, 'user': pos.report_user, 'photoname': pos.photo_filename, 'videoname': pos.video_filename} for pos in positions]
        # print(positions_list)
        # for position in positions_list:
        #     print("video filename: ", position.get('video_filename'))
        #     if position.get('video_filename') == "No_Video_Available.mp4":
        #         print("video filename2: ", position.get('video_filename'))
        #         position['video_filename'] = None
        # for position in positions_list:
        #     print("video filename: ", position.get('videoname'))
            # if position.get('videoname') == "No_Video_Available.mp4":
            #     print("Changing 'videoname' to None for: ", position.get('videoname'))
            #     position['videoname'] = None  # Correctly use the key 'videoname'

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
            results = db.execute(text("SELECT * FROM reports ORDER BY report_time DESC LIMIT 10")).fetchall()
            if len(results) == 0:
                return render_template("home.html", message="No Reports", welcome=("Signed in as: "+ session["user_id"]))

            return render_template("home.html", results = results, welcome=("Signed in as: "+ session["user_id"]))
        else:
            return redirect("/login")
    
    if request.method == "POST":
        if session:

            currentuser = session["user_id"]
            location = request.form.get("locdesc")
            comments = request.form.get("comments")

            file = request.files['cameraInput']
            file2 = request.files['videoInput']
            latitude = request.form.get('latitude')
            longitude = request.form.get('longitude')

            # print("latitude: ", latitude)
            # print("longitude: ", longitude)
            # print("filename: ", file.filename)
            print("upload video name: ", file2.filename)
            # print("location: ", location)
            # print("comments: ", comments)
            if latitude=="" or longitude=="":
                latitude = 0
                longitude = 0
            
            if location=="" or comments=="":
                results = db.execute(text("SELECT * FROM reports ORDER BY report_time DESC LIMIT 10")).fetchall()
                if len(results) == 0:
                    return render_template("home.html", message="No Reports", error="All fields must be filled in", welcome=("Signed in as: "+ session["user_id"]))
              
                return render_template("home.html", results = results, error="All fields must be filled in", welcome=("Signed in as: "+ session["user_id"]))      
            
            unique_filename = "No_Image_Available.jpg"
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                unique_filename = f'{datetime.now().strftime("%Y%m%d%H%M%S%f")}_{filename}'
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], unique_filename))
            
            unique_filename2 = "No_Video_Available.mp4"
            if file2:
                filename2 = secure_filename(file2.filename)
                unique_filename2 = f'{datetime.now().strftime("%Y%m%d%H%M%S%f")}_{filename2}'
                file2.save(os.path.join(app.config['UPLOAD_FOLDER'], unique_filename2))
            print("unique_filename2: ", unique_filename2)
            db.execute(text("INSERT INTO reports (report_user, comments, report_location, report_time, photo_filename,video_filename,longitude,latitude) VALUES(:currentuser, :comments, :location, current_timestamp(0), :unique_filename, :unique_filename2, :longitude, :latitude)"), {"currentuser": currentuser, "comments":comments, "location": location, "unique_filename": unique_filename, "unique_filename2": unique_filename2,"longitude": longitude, "latitude": latitude})
            db.commit()

            results = db.execute(text("SELECT * FROM reports ORDER BY report_time DESC LIMIT 10")).fetchall()            
            if len(results) == 0:
                return render_template("home.html", message="No Reports", welcome=("Signed in as: "+ session["user_id"]))
           

            return render_template("home.html", pmessage="Report Posted", results = results, welcome=("Signed in as: "+ session["user_id"]))
        
        else:
            return redirect("/login")

# reports Page
@app.route("/reports", methods=["GET"])
def reports():
    # Checks if user is logged in
    if request.method == "GET":
        if session:
            results = db.execute(text("SELECT * FROM reports ORDER BY report_time DESC")).fetchall()
            if len(results) == 0:
                return render_template("reports.html", message="No Reports", welcome=("Signed in as: "+ session["user_id"]))

            return render_template("reports.html", results = results, welcome=("Signed in as: "+ session["user_id"]))
        else:
            return redirect("/login")

@app.route('/analytics', methods=['GET'])
def analytics():
    # GET request
    if request.method == 'GET':
      
       
        df = pd.read_csv('./Traffic_Incidents.csv')

        # df = pd.DataFrame(data)
        map_config = {
        "mapState": {
            "latitude": 51.0447,
            "longitude": -114.0719,
            "zoom": 9
        }
        }

        map_1 = KeplerGl(height=1000,config=map_config)
        
        map_1.add_data(data=df, name='incidents')
        file_path = os.path.join(app.static_folder, 'kepler_map.html')
        
        map_1.save_to_html(file_name=file_path)

        return render_template('analytics.html')
       



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')



