# Importing necessary libraries
from PIL import Image
import os
from pyzbar.pyzbar import decode
import re 
import base64
import hashlib


# Opening the GIF file using Image module
with Image.open("./output.gif") as im:
    txt_file = open("abc.txt", "w")  # Open file to write
    # iterating through each frame of the GIF
    lines = [''] * im.n_frames
    for frame_num in range(int(im.n_frames)):

        #Selecting the current frame
        im.seek(frame_num)
        current_frame = im.copy().convert('RGB')
        d = decode(current_frame)
        context = d[0].data.decode()
        #匹配正则格式
        match = re.search(r'<--#([0-9])+/([0-9])+-->\n(.*)', context)
        if match :
            lines[int(match.group(1))] = match.group(3)
            print(f"found page: {match.group(1)}/{match.group(2)}")

            #txt_file.write(content)

          # Write decoded data to file

    
    md5 = lines[0]
    context = ''.join(lines[1:])
    #计算MD5
    md5_hash = hashlib.md5(context.encode()).hexdigest()

    if md5 == md5_hash:
        print("MD5 检查正确.")
        for txt in lines[1:]:
            txt_file.write(base64.b64decode(txt).decode('utf8'))
    
    else:
        print("MD5 检查错误~！")
    txt_file.close()  # Close file after writing all data


