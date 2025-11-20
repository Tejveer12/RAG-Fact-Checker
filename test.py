import requests
import json

url = "http://127.0.0.1:8000/check_claim"
headers = {"Content-Type": "application/json"}

# True claims
# true_claims = [
#     "India Responding to Global Textile Demand with Strength and Confidence: MoS Pabitra Margherita",
#     "Yoga: India’s Gift to the World",
# ]
#
# # False claims
# false_claims = [
#     "Union Health Minister cancels National One Health Mission Assembly 2025",
#     "Prime Minister moves India’s capital from Delhi to Mumbai",
# ]

# Unverifiable claims
unverifiable_claims = [
    "Aliens spotted at United States of America",
    # "Secret treasure discovered under Rashtrapati Bhavan",
]

all_claims =  unverifiable_claims

for claim in all_claims:
    payload = {"text": claim}
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    if response.status_code == 200:
        print(f"Claim: {claim}")
        print("Verdict:", json.dumps(response.json(), indent=2))
        print("-" * 80)
    else:
        print(f"Error {response.status_code} for claim: {claim}")
