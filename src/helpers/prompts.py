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

def number_plate_extractor(vehicle_no: str) -> str :
    return f"""
You are an intelligent vision model. A user has uploaded an image of a vehicle license plate. 
Your task is to extract the vehicle number from the image and compare and validate it with the following vehicle number: "{vehicle_no}".

Please return your output in the following JSON format:

{{
  "vehicle_no": "<vehicle_number on vehicle>"[ extract from image],
  "validity": "<valid | invalid>"
}}

Only include the JSON in your response.
"""

def number_plate_extractor2(vehicle_no: str) -> str:
    return f"""
You are an OCR-capable vision model. A user has uploaded an image containing a vehicle's license plate.

Your tasks are:
1. Detect and extract the license plate number from the image.
2. Compare it to the expected vehicle number: "{vehicle_no}" (ignore case and spacing).
3. Return the result **only** in the JSON format below.

Output JSON format:
{{
  "vehicle_no": "<extracted_vehicle_number>",
  "validity": "<valid | invalid>"
}}

Rules:
- Do not include any explanation or reasoning.
- Strip extra spaces and normalize the extracted vehicle number before comparison.
- If the number in the image matches "{vehicle_no}" after normalization, mark it as "valid". Otherwise, mark it as "invalid".

Only respond with the JSON.
"""

def number_plate_extractor3(vehicle_no: str) -> str:
    return f"""
You are a vision model specialized in OCR (Optical Character Recognition). A user has uploaded an image of a vehicle's license plate.

Your job:
1. Extract the **exact** vehicle number from the license plate image.
2. Normalize the result by removing spaces and converting all characters to uppercase.
3. Compare the result to the expected number: "{vehicle_no.upper().replace(' ', '')}".
4. Only return the final decision in this exact JSON format:

{{
  "vehicle_no": "<extracted_vehicle_number>",
  "validity": "<valid | invalid>"
}}

Important:
- Match the vehicle number **exactly** after normalization.
- Do **not** guess or hallucinate missing characters.
- If there’s any mismatch, mark the result as "invalid".
- Do **not** include explanations or extra text — return **only** the JSON object.
"""

def claims_damage_report_and_analysis(damage_description: str, requested_amount: float, claimable_amount: float) -> str:
    return f"""
You are an experienced insurance claims underwriter. Your task is to analyze a vehicle damage report submitted by a user. You will assess the damage based on the provided description and associated images (not included here but considered available in your context).

Follow these steps:
1. Analyze the damage based on the textual description.
2. Estimate the **severity** and **percentage of vehicle damage**.
3. Assess whether the **requested claim amount** is justified in comparison to typical repair costs for such damage.
4. Compare the requested amount with the **maximum claimable amount** under the user's policy.
5. Determine a **reasonable approvable amount** that should be approved for payout.

Use your expertise to also identify if any part of the request seems **suspicious or exaggerated**, and mention it in the remarks.

Input:
- Damage Description: "{damage_description}"
- Requested Amount: {requested_amount}
- Policy Claimable Amount: {claimable_amount}

Your output should be a well-structured JSON object in the following format:

```json
{{
    "damage_analysis": "Brief analysis of the nature and severity of the damage",
    "damage_percentage": "Estimated percentage of vehicle damaged (e.g., 35%)",
    "severity_level": "Low | Moderate | High | Critical",
    "approvable_amount": float in rupees,
    "reason_for_approval": "Justification for the approved amount",
    "remarks": "Any concerns, anomalies, or notes for the adjuster"
}}
```
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

