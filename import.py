import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.sql import text

# Set up database from environment variable
engine = create_engine(os.getenv("DATABASE_URL"))

# Or manually set up DATABASE_URL
#DATABASE_URL = 'postgresql://myuser:mypassword@localhost:5432/finalproject'
#engine = create_engine(DATABASE_URL)

db = scoped_session(sessionmaker(bind=engine))

def main():
    f = open("Traffic_Incidents.csv")
    reader = csv.reader(f)
    
    #for incident_info, description, start_dt, modified_dt, quadrant, longitude, latitude in reader:
    for row in reader:
        incident_info, description, start_dt, modified_dt, quadrant, longitude, latitude = row[:7]
#         db.execute("INSERT INTO accidents2023 (incident_info, description, start_dt, modified_dt, quadrant, longitude, latitude) VALUES (:incident_info, :description, :start_dt, :modified_dt, :quadrant, :longitude, :latitude)",
#         {
#             "incident_info": incident_info, "description": description, "start_dt": start_dt, "modified_dt": modified_dt, "quadrant": quadrant, "longitude": longitude, "latitude": latitude 
#         })

        db.execute(text("INSERT INTO accidents2023 (incident_info, description, start_dt, modified_dt, quadrant, longitude, latitude) VALUES (:incident_info, :description, :start_dt, :modified_dt, :quadrant, :longitude, :latitude)"),
        {
            "incident_info": incident_info, "description": description, "start_dt": start_dt, "modified_dt": modified_dt, "quadrant": quadrant, "longitude": longitude, "latitude": latitude
        })
        print(f"Added accident record: {incident_info}, {description}, {start_dt}, {modified_dt}, {quadrant}, {longitude}, {latitude}")
    db.commit()

if __name__ == "__main__":
    main()