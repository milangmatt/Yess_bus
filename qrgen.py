import csv
import qrcode
from PIL import Image, ImageDraw, ImageFont
import os
import json

# Paths
csv_file = 'Participants.csv'
output_folder = 'qrcards'
os.makedirs(output_folder, exist_ok=True)

# Font for the card
font_path = 'arial.ttf'  # replace with a valid font path
font_size = 30
font = ImageFont.truetype(font_path, font_size)

with open(csv_file, newline='', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    for row in reader:
        student_id = row['ID'].strip()
        name = row['Name'].strip()

        # Encode both ID and name in QR code as JSON
        qr_data = json.dumps({"id": student_id, "name": name})
        qr = qrcode.QRCode(box_size=10, border=4)
        qr.add_data(qr_data)
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white")

        # Create card
        card_width, card_height = 400, 400
        card = Image.new('RGB', (card_width, card_height), 'white')
        draw = ImageDraw.Draw(card)

        # Paste QR code in the center
        qr_img = qr_img.resize((250, 250))
        qr_pos = ((card_width - 250) // 2, 50)
        card.paste(qr_img, qr_pos)

        # Add student name below QR
        bbox = draw.textbbox((0, 0), name, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        text_pos = ((card_width - text_width) // 2, 320)
        draw.text(text_pos, name, fill="black", font=font)

        # Save card
        card.save(f'{output_folder}/{student_id}_{name}.png')
