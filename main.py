from quotexapi.stable_api import Quotex
import os

email = os.getenv("QX_EMAIL")
password = os.getenv("QX_PASSWORD")

qx = Quotex(email, password)
if qx.login():
    print("✅ Login Successful")
else:
    print("❌ Login Failed")