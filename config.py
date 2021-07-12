import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path) # take environment variables from .env file

INSTRUMENTATION_KEY = os.getenv("INSTRUMENTATION_KEY")
# INSTRUMENTATION_KEY = "f4789fee-f8dc-47eb-ae64-c3bfc3422422"

print("Instrumentation Key: ", INSTRUMENTATION_KEY)

# if not INSTRUMENTATION_KEY:
#     raise Exception("Missing configuration for Application Insight")

