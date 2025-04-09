import math
import random
import smtplib
from math import floor

digits="0123456789"
OTP=""
for i in range(6):
    OTP+=digits[math.floor(random.random()*10)]

print(f"Your OTP is {OTP}")

s = smtplib.SMTP('smtp.gmail.com', 587)
s.starttls()

s.login("velea.radu.dan@gmail.com", "ohjw pzps jtxx rkau")

email_id = input("Enter destination email: ")

s.sendmail("velea.radu.dan@gmail.com",email_id,OTP)

a = input("Enter Your OTP >>: ")
if a == OTP:
    print("Verified")
else:
    print("Please Check your OTP again")