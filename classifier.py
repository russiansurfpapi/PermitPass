import pandas as pd
import openai

# import argparse
# import os
# import sys
# from dotenv import load_dotenv
from openai import OpenAI

# load_dotenv(".env.local")

# # Retrieve the OpenAI API key from environment variables
# api_key = os.getenv("OPENAI_API_KEY1")
# print(api_key)

# # Check if the API key was retrieved successfully
# if not api_key:
#     raise EnvironmentError(
#         "OpenAI API key not found. Please ensure 'OPENAI_API_KEY1' is set in the .env.local file."
#     )

# client = OpenAI(api_key=api_key)


# # Command-line argument parser
# parser = argparse.ArgumentParser(
#     description="Classify Asian-owned restaurants from a CSV file."
# )
# parser.add_argument("input_csv", type=str, help="Path to the input CSV file")
# args = parser.parse_args()

# # Load the CSV file
# file_path = args.input_csv
# df = pd.read_csv(file_path)

# # Output file name
# output_file = "leads.csv"


# # Function to classify whether a restaurant is likely Asian
# def classify_asian(dba, legal_name):
#     prompt = (
#         f"Determine if either of the following names likely indicate an Asian-owned restaurant.\n"
#         f"DBA: {dba}\n"
#         f"Legal Name: {legal_name}\n"
#         f"Respond with 'True' if either name suggests it is Asian-owned, otherwise respond 'False'.\n"
#         f"Also provide a one-line explanation for your classification."
#     )

#     try:
#         # client = openai.OpenAI()
#         response = client.chat.completions.create(
#             model="gpt-4-0613",
#             messages=[
#                 {
#                     "role": "system",
#                     "content": "You are an assistant that classifies restaurant names.",
#                 },
#                 {"role": "user", "content": prompt},
#             ],
#             temperature=0.7,
#             max_tokens=1500,
#             top_p=1,
#             frequency_penalty=0.5,
#             presence_penalty=0,
#         )

#         # Correct way to access the formatted content from the response
#         message_content = response.choices[0].message.content.strip()

#         # Extract boolean and explanation
#         is_asian = "True" in message_content
#         explanation = message_content.replace("True", "").replace("False", "").strip()
#         return is_asian, explanation

#     except Exception as e:
#         print(f"Error processing: {dba}, {legal_name}. Error: {e}")
#         return False, "Error in classification"


# # Apply the function to each row with debug prints
# results = []
# for index, row in df.iterrows():
#     print(
#         f"Processing row {index + 1}/{len(df)}: {row['DBA']} / {row['LegalName']}"
#     )  # Debug line
#     result = classify_asian(row["DBA"], row["LegalName"])
#     results.append(result)

# df["isLikelyAsian"] = [result[0] for result in results]
# df["ClassificationExplanation"] = [result[1] for result in results]

# # Append to leads.csv if it exists, else create a new file
# if os.path.exists(output_file):
#     existing_df = pd.read_csv(output_file)
#     combined_df = pd.concat([existing_df, df], ignore_index=True)
#     combined_df.to_csv(output_file, index=False)
# else:
#     df.to_csv(output_file, index=False)

# # Print explanations
# for index, row in df.iterrows():
#     print(f"{row['DBA']} / {row['LegalName']}: {row['ClassificationExplanation']}")

import pandas as pd
import openai
import argparse
import os
import sys
from dotenv import load_dotenv

# Load environment variables from the .env.local file
load_dotenv(".env.local")

# Retrieve the OpenAI API key from environment variables
api_key = os.getenv("OPENAI_API_KEY1")

# Check if the API key is set correctly
if not api_key:
    sys.exit(
        "Error: OpenAI API key is missing or not set correctly. Please update the API key in the .env.local file."
    )

# Set OpenAI API key
openai.api_key = api_key

client = OpenAI(api_key=api_key)

# Command-line argument parser
parser = argparse.ArgumentParser(
    description="Classify Asian-owned restaurants from a CSV file."
)
parser.add_argument("input_csv", type=str, help="Path to the input CSV file")
args = parser.parse_args()

# Load the CSV file
file_path = args.input_csv
df = pd.read_csv(file_path)

# Output file name
output_file = "leads.csv"


# Function to classify whether a restaurant is likely Asian
def classify_asian(dba, legal_name):
    prompt = (
        f"Determine if either of the following names likely indicate an Asian-owned restaurant.\n"
        f"DBA: {dba}\n"
        f"Legal Name: {legal_name}\n"
        f"Respond with 'True' if either name suggests it is Asian-owned, otherwise respond 'False'.\n"
        f"Also provide a one-line explanation for your classification."
    )

    try:
        # client = openai.OpenAI()
        response = client.chat.completions.create(
            model="gpt-4-0613",
            messages=[
                {
                    "role": "system",
                    "content": "You are an assistant that classifies restaurant names.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
            max_tokens=1500,
            top_p=1,
            frequency_penalty=0.5,
            presence_penalty=0,
        )

        # Correct way to access the formatted content from the response
        message_content = response.choices[0].message.content.strip()

        # Extract boolean and explanation
        is_asian = "True" in message_content
        explanation = message_content.replace("True", "").replace("False", "").strip()
        return is_asian, explanation

    except Exception as e:
        print(f"Error processing: {dba}, {legal_name}. Error: {e}")
        return False, "Error in classification"


# Apply the function to each row with debug prints
for index, row in df.iterrows():
    print(
        f"Processing row {index + 1}/{len(df)}: {row['DBA']} / {row['LegalName']}"
    )  # Debug line
    is_asian, explanation = classify_asian(row["DBA"], row["LegalName"])

    # Append the result directly to leads.csv after each classification
    result_df = pd.DataFrame(
        {
            "DBA": [row["DBA"]],
            "LegalName": [row["LegalName"]],
            "isLikelyAsian": [is_asian],
            "ClassificationExplanation": [explanation],
        }
    )

    if os.path.exists(output_file):
        result_df.to_csv(output_file, mode="a", header=False, index=False)
    else:
        result_df.to_csv(output_file, index=False)

    # Print explanation for immediate feedback
    print(f"{row['DBA']} / {row['LegalName']}: {explanation}")
