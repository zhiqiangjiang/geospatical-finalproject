

# Project Title
Volunteered Driver Traffic Incidents Platform

# Summary
Our project, the Volunteered Driver Traffic Incidents Platform, is a secure website designed to provide drivers with real-time access to traffic incidents and traffic camera feeds across Calgary. The platform allows drivers to register and log in, enabling them to interact with an interactive map displaying traffic cameras and incidents. From PC or mobile browers, drivers can report and view incidents anywhere, and access incident spatical and temporal analytics for the past year.

# Key Features:
* Interactive Map: drivers can view traffic cameras (camera markers) and official incidents (red markers) and driver-reported incidents (green markers) on a leaflet map. Clicking on markers provides detailed information via pop-ups, including camera feed and driver uploaded images.

* Automatic Refresh: The map refreshes every 10 minutes to display new incident reports and camera images. Drivers can also manually refresh by clicking a button.

* Report Section: From PC and mobile browsers, drivers can post incident reports, with the most recent reports displayed. The page limits the number of reports to 10 to prevent excessive scrolling and provide a link to full report list for driver review.

* Traffic Incident Analytics: The platform provides spatial and temporal statistics on Calgary traffic incidents.

* Incident Data: The driver report data includes incident place information, incident description, on-site image or video, dashboard camera videos and automatically created reporting time & position.

# Webpages:
* Login Page: Handles authentication and credential verification.
* Register Page: Adds new driver records to the database.
* Home Page: Manages incident map and driver report submissions and retrieval.
* Reports Page: Renders full report templates.

# Website Feature:
* Security: The website prioritizes security by implementing SSL (Secure Sockets Layer) and HTTPS (Hypertext Transfer Protocol Secure) protocols. This ensures that all data exchanged between the client (browser) and the server is encrypted, providing a secure connection. SSL and HTTPS are essential, especially since mobile browsers require a secure connection to access location data. By using SSL and HTTPS, the website ensures the protection of sensitive information and enhances user privacy.
* Responsive: The website incorporates AJAX (Asynchronous JavaScript and XML) for incident image and video upload and display. AJAX allows for asynchronous communication between the client and server, enabling seamless updates to web content without reloading the entire page. This enhances the user experience by providing faster and more dynamic interactions. Users can upload incident images and videos without experiencing delays or interruptions, resulting in a responsive and efficient website.
* Interactive: The website utilizes Kepler map technology to display incident spatial and temporal statistics. By integrating Kepler maps, the website enhances interactivity and engagement, enabling users to interact with incident data in meaningful ways. Users can zoom in/out, pan, and filter data on the map, providing valuable insights into driver incidents' spatial distribution and temporal patterns.

# Program Key Files:
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
* pip/pip3 install requests
* set FLASK_APP=app.py
* set FLASK_DEBUG=1
* set DATABASE_URL="postgresql://myuser:mypassword@localhost:5432/finalproject"
* python import.py
* python app.py

# Datasets Used:
* Calgary Traffic Incidents-online real-time
* Calgary Traffic Cameras-online real-time
* Traffic_incidents.csv contains past-year traffic incidents

# Example Use Cases:
* Drivers can preview road and traffic incident conditions before leaving home by viewing traffic cameras.
* If drivers experience or witness an incident, they can record/report/share it on the platform.
* View Calgary incident spatial and temporal statistics for the past year
