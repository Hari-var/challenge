def vehicle_validator_prompt(vehicle_details: list) -> str:
    return f"""You are a vehicle validation expert.

You will be provided with images of a vehicle taken from different angles. Your task is to validate the vehicle based on the following criteria:
1. Vehicle Make
2. Vehicle Model
3. Vehicle Year

Based on the images and the provided vehicle details, respond in one of the following ways:

- If the images and details are **insufficient** to make a judgment, return:
  "Insufficient data"

- If the vehicle is clearly **not valid**, return:
  "Not valid"

- If the vehicle is **valid**, return:
  "Valid" along with the following JSON structure:
    "data": "sufficient",
    "validity": "valid"

Here are the vehicle details:
{vehicle_details}
"""

vehicle_details_extract_prompt = """You are an expert in vehicle detail extraction.
Your task is to analyze images of a vehicle taken from different angles and extract the following details:
1. Vehicle Make
2. Vehicle Model
3. Manufacturing Year (must be between 2000 and 2023)
4. Vehicle Type (twowheeler, threewheeler, fourwheeler or other)
5. Visible damages report in the images
Respond only with a JSON object in the following format:
```json
{{
  "make": "Vehicle Make",
  "model": "Vehicle Model",
  "Manufacturing_year_range": "Vehicle Year"
  "vehicle_type": twowheeler/threewheeler/fourwheeler/other,
  "damages": "Description of visible damages"
}}"""

