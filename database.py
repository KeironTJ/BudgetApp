import csv
from app import db, create_app
from app.models import User, UserRoles, Role, VehicleData, FuelEntryLog
from datetime import datetime
from decimal import Decimal

app=create_app()

app_context = app.app_context()
app_context.push()


def delete_vehicle_data():
    #db.session.query(VehicleData).delete()
    db.session.query(FuelEntryLog).delete()
    db.session.commit()
    print("Vehicle Data Deleted")


def add_entries_from_csv(file_path):
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            entry_date = datetime.strptime(row['Date'], '%d/%m/%Y')
            vrn = row['Vehicle']
            fuel_price = float(row['Price'])
            vehicle_mileage = int(row['Mileage'])
            fuel_cost = float(row['Cost'])

            entry = FuelEntryLog(
                user_id=1,  # Assuming a default user_id for simplicity
                entry_date=entry_date,
                vrn=vrn,
                fuel_price=fuel_price,
                vehicle_mileage=vehicle_mileage,
                fuel_cost=fuel_cost
            )
            
            entry.calculateLitre()
            entry.calculateGallon()
            entry.calculateActualMiles()
            entry.calculateMPG()

            db.session.add(entry)
        db.session.commit()

delete_vehicle_data()
add_entries_from_csv("qafl.csv")