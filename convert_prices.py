import re
import os

filepath = 'backend/app/tools/booking_tools.py'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

def convert_to_inr(match):
    val = float(match.group(1))
    inr_val = int(val * 83)
    return f'\"₹{inr_val:,}\"'

# Convert hotel prices
content = re.compile(r'\"\$([0-9\.]+)\s*USD\"').sub(convert_to_inr, content)

def convert_estimate(match):
    val1 = int(match.group(1)) * 83
    val2 = int(match.group(2)) * 83
    return f'\"₹{val1:,}‑₹{val2:,}\"'

content = re.compile(r'\"\$(\d+)[-‑]\$(\d+)\"').sub(convert_estimate, content)

def convert_pound(match):
    val1 = int(match.group(1)) * 105
    val2 = int(match.group(2)) * 105
    return f'\"₹{val1:,}‑₹{val2:,}\"'

content = re.compile(r'\"£(\d+)[-‑]£(\d+)\"').sub(convert_pound, content)

content = content.replace('f\"${price}.00 USD\"', 'f\"₹{price * 83:,}\"')
content = content.replace('f\"${random.randint(100, 300)}.00 USD\"', 'f\"₹{random.randint(100, 300) * 83:,}\"')

content = content.replace('\"$12 CAD\"', '\"₹730\"')
content = content.replace('\"$1.75\"', '\"₹145\"')
content = content.replace('\"$2.50\"', '\"₹207\"')
content = content.replace('\"$0.30\"', '\"₹25\"')

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Prices converted to INR successfully!")
