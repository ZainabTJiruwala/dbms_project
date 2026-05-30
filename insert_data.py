from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")

db = client["GeneVaultDB"]

patients = [
    {
        "patient_id":"PT101",
        "mutations":[
            {"chr":"17","pos":12345},
            {"chr":"7","pos":45678}
        ]
    },
    {
        "patient_id":"PT102",
        "mutations":[
            {"chr":"17","pos":11111},
            {"chr":"1","pos":22222}
        ]
    },
    {
        "patient_id":"PT103",
        "mutations":[
            {"chr":"7","pos":33333}
        ]
    }
]

db.patients.insert_many(patients)

print("Data Inserted")