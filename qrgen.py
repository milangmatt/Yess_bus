import csv
import qrcode
from PIL import Image, ImageDraw, ImageFont
import os
import json

# Paths
csv_file = 'Participants.csv'
output_folder = 'qrcards'
os.makedirs(output_folder, exist_ok=True)

# Use Verdana (system font, no need to provide .ttf files)
# Use full paths to Verdana font on Windows
heading_font = ImageFont.truetype("C:/Windows/Fonts/verdanab.ttf", 40)  # bold
text_font = ImageFont.truetype("C:/Windows/Fonts/verdana.ttf", 28)      # regular
id_font = ImageFont.truetype("C:/Windows/Fonts/verdana.ttf", 22)


with open(csv_file, newline='', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    for row in reader:
        student_id = row['ID'].strip()
        name = row['Name'].strip()

        # Encode both ID and name in QR code as JSON
        qr_data = json.dumps({"id": student_id, "name": name})
        qr = qrcode.QRCode(box_size=10, border=2)
        qr.add_data(qr_data)
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white").convert("RGB")

        # Card dimensions
        card_width, card_height = 480, 600
        card = Image.new('RGB', (card_width, card_height), '#121212')
        draw = ImageDraw.Draw(card)

        # Gradient background
        for y in range(card_height):
            shade = int(18 + (y / card_height) * 40)  # from #121212 to lighter grey
            draw.line([(0, y), (card_width, y)], fill=(shade, shade, shade))

        # Border with rounded corners
        border_color = "#ff0400"
        border_radius = 20
        border_width = 6
        border_rect = [(3, 3), (card_width-3, card_height-3)]
        draw.rounded_rectangle(border_rect, radius=border_radius, outline=border_color, width=border_width)

        # Heading "YESS - BUS Card"
        heading_text = "YESS - BUS Card"
        heading_bbox = draw.textbbox((0, 0), heading_text, font=heading_font)
        heading_width = heading_bbox[2] - heading_bbox[0]
        heading_pos = ((card_width - heading_width) // 2, 25)
        draw.text(heading_pos, heading_text, fill=border_color, font=heading_font)

        # Underline bar
        underline_y = heading_pos[1] + heading_bbox[3] + 5
        draw.rectangle([(80, underline_y), (card_width-80, underline_y+4)], fill=border_color)

        # Place QR code
        qr_size = 280
        qr_img = qr_img.resize((qr_size, qr_size))
        qr_pos = ((card_width - qr_size) // 2, 120)
        card.paste(qr_img, qr_pos)

        # Student Name
        name_bbox = draw.textbbox((0, 0), name, font=text_font)
        name_width = name_bbox[2] - name_bbox[0]
        name_pos = ((card_width - name_width) // 2, 420)
        draw.text(name_pos, name, fill="white", font=text_font)

        # Student ID below name
        id_text = f"ID: {student_id}"
        id_bbox = draw.textbbox((0, 0), id_text, font=id_font)
        id_width = id_bbox[2] - id_bbox[0]
        id_pos = ((card_width - id_width) // 2, 470)
        draw.text(id_pos, id_text, fill="#bbbbbb", font=id_font)

        # Accent bar at bottom
        draw.rectangle([(0, card_height-40), (card_width, card_height)], fill=border_color)
        draw.text((card_width//2 - 60, card_height-35), "YESS 2025", font=id_font, fill="white")

        # Save card
        file_name = f"{student_id}_{name}.png".replace(" ", "_")
        card.save(os.path.join(output_folder, file_name))

print("✅ Stylish YESS Bus Cards (Verdana) generated successfully!")
