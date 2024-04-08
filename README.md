

# Project Title
Volunteered Driver Traffic Incidents Platform

# Summary
Our project, the Volunteered Driver Traffic Incidents Platform, is a web application designed to provide drivers with real-time access to traffic incidents and traffic camera feeds across Calgary. The platform allows drivers to register and log in, enabling them to interact with an interactive map displaying traffic cameras and incidents. Drivers can report and view incidents, and access incident spatical and temporal analytics for the past year.

# Key Features:
* Interactive Map: drivers can view traffic cameras (camera markers) and official incidents (red markers) and driver-reported incidents (green markers) on a leaflet map. Clicking on markers provides detailed information via pop-ups, including camera feed and driver uploaded images.

* Automatic Refresh: The map refreshes every 10 minutes to display new incident reports and camera images. Drivers can also manually refresh by clicking a button.

* Report Section: From website and mobile phone, drivers can post incident reports, with the most recent reports displayed. The page limits the number of reports to 10 to prevent excessive scrolling and provide a link to full report list for driver review.

* Traffic Incident Analytics: The platform provides statistics on traffic incidents on spatical and temporal.

* Incident Data: The driver report data includes incident place information, incident description, on-site image or video, dashboard camera videos and automatically created reporting time & position.

# RESTful API Backend
* Login Page: Handles authentication and credential verification.
* Register Page: Adds new driver records to the database.
* Home Page: Manages incident map and driver report submissions and retrieval.
* Reports Page: Renders full report templates.

# Example Use Cases:
* Drivers can preview road and traffic incident conditions before leaving home by viewing traffic cameras.
* If drivers experience or witness an incident, they can record/report/share it on the platform.
* View Calgary incident spatial and temporal statistics for the past year

# Program-related Key Files:
* app.py: Flask framework including GET/POST request logic for each page.
* mapScripts.js: Contains logic for map creation, population, and analytics on the home page.
* home.html, login.html, register.html, reports.html: HTML templates for different pages.
* import.py: Used for importing historical incident data.

# Database Tables:
* CREATE TABLE "public"."accidents2023" (
    "incident_info" text NOT NULL,
    "description" text NOT NULL,
    "start_dt" text NOT NULL,
    "modified_dt" text NOT NULL,
    "quadrant" text NOT NULL,
    "longitude" text NOT NULL,
    "latitude" text NOT NULL
) WITH (oids = false);

* CREATE TABLE "public"."reports" (
    "report_user" text NOT NULL,
    "comments" text NOT NULL,
    "report_id" integer DEFAULT nextval('reports_report_id_seq') NOT NULL,
    "report_time" timestamp NOT NULL,
    "report_location" text NOT NULL,
    "longitude" text,
    "latitude" text,
    "photo_filename" text,
    "video_filename" text,
    CONSTRAINT "reports_pkey" PRIMARY KEY ("report_id")
) WITH (oids = false);

* CREATE TABLE "public"."users" (
    "username" text NOT NULL,
    "password" text NOT NULL,
    "user_id" integer DEFAULT nextval('users_user_id_seq') NOT NULL,
    CONSTRAINT "users_pkey" PRIMARY KEY ("user_id")
) WITH (oids = false);

# Setting up the Web Application:
pip/pip3 install requests
set FLASK_APP=app.py
set FLASK_DEBUG=1
set DATABASE_URL="postgresql://myuser:mypassword@localhost:5432/finalproject"
python import.py
python app.py

# Datasets Used:
* Calgary Traffic Incidents-online real-time
* Calgary Traffic Cameras-online real-time
* Traffic_incidents.csv contains past-year traffic incidents


