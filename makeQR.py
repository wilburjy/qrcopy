import qrcode
from PIL import Image, ImageDraw
import imageio
import numpy as np
import base64
import hashlib

lines = []
with open('./file.txt', 'r') as f:
    while True:
        chunk = f.read(800)
        if not chunk:
            break
        encoded_chunk = base64.b64encode(chunk.encode()).decode()
        lines.append(encoded_chunk)


#生成内容MD5

# Combine all lines into one
merged_lines = ''.join(lines)
# Generate MD5 hash for merged lines
md5_hash = hashlib.md5(merged_lines.encode())
md5_txt = md5_hash.hexdigest()


# Create list of QR codes
qrs = []
#md5内容放第一帧
contexts = [md5_txt] + lines
count = len(contexts)

for i, line in enumerate(contexts):
    print(f"<--#{str(i)}/{count-1}-->")
    qr = qrcode.QRCode(version=None, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    qr.add_data(f"<--#{str(i)}/{count-1}-->\n{line}")
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    qrs.append(img)


# Create GIF from QR codes
images = []
for qr in qrs:
    # Convert PIL image to numpy array
    img = qr.convert('RGB')
    arr = np.array(img)
    images.append(arr)


# Save GIF without looping
imageio.mimsave('./output.gif', images, duration=0.2, loop=0)



