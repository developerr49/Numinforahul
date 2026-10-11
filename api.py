from fastapi import FastAPI, Query
import pandas as pd

app = FastAPI(title="NumInfo API")

# CSV Load
df = pd.read_csv("database.csv", dtype=str)

# Column names ko clean karna
df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
)

# Phone clean
df["phone"] = df["phone"].astype(str).str.strip()

print("Database Loaded:", len(df))
print(df.columns.tolist())


@app.get("/")
def home():
    return {
        "developer": "@Mr_rahul_dev",
        "api_by": "@Rahuls_Portal",
        "status": "online",
        "records": len(df),
        "credits": "Developer @Mr_rahul_dev | API by @Rahuls_Portal"
    }


@app.get("/lookup")
def lookup(num: str = Query(None, description="Phone number to lookup")):
    if not num:
        return {
            "developer": "@Mr_rahul_dev",
            "api_by": "@Rahuls_Portal",
            "success": False,
            "error": "Please provide phone number",
            "credits": "Developer @Mr_rahul_dev | API by @Rahuls_Portal"
        }

    phone = num.strip()
    result = df[df["phone"] == phone]

    if result.empty:
        return {
            "developer": "@Mr_rahul_dev",
            "api_by": "@Rahuls_Portal",
            "success": False,
            "message": "Number not found",
            "credits": "Developer @Mr_rahul_dev | API by @Rahuls_Portal"
        }

    row = result.iloc[0].fillna("")

    return {
        "developer": "@Mr_rahul_dev",
        "api_by": "@Rahuls_Portal",
        "success": True,
        "data": {
            "first_name": row["first_name"],
            "last_name": row["last_name"],
            "address": row["address"],
            "city": row["city"],
            "county": row["county"],
            "state": row["state"],
            "zip": row["zip"],
            "phone": row["phone"],
            "carrier": row["carrier"],
            "gender": row["gender"],
            "ethnicity": row["ethnicity"],
            "ownrent": row["ownrent"],
            "latitude": row["latitude"],
            "longitude": row["longitude"]
        },
        "credits": "Developer @Mr_rahul_dev | API by @Rahuls_Portal"
    }
