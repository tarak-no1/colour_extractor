import os, sys, uuid
import numpy as np
from PIL import Image
import webcolors
import json,shutil
from source.darknet import detect
from source.helper import loadWeights, getWeights, getColorInfo, extractRequireColors
import time,requests
from source.image_colour_detect import imageColourExtract

loadWeights()

def join_l(l, sep):
    li = iter(l)
    string = str(next(li))
    for i in li:
        string += str(sep) + str(i)
    return string

def downloadImages(image_links):
    millis = int(round(time.time() * 1000))
    image_folder_path = "/home/ubuntu/darknet/server/source/images/"+str(millis)
    url_to_path_map = {}
    try:
        for url in image_links:
            extn = os.path.splitext(url)[1]
            extn = extn.strip()
            extn = extn.lower()
            print("Extn : ",extn)
            print(url)
            image_name='';
            if extn!='':
                image_name = str(uuid.uuid4())+extn
            else:
                image_name = str(uuid.uuid4())+'.jpg'
            
            image_path = image_folder_path+"/"+image_name
            url_to_path_map[url] = image_path
            if not os.path.exists(image_path):
                if not os.path.exists(image_folder_path):
                    try:
                        os.makedirs(image_folder_path)
                    except OSError as exc: # Guard against race condition
                        if exc.errno != errno.EEXIST:
                            raise
                with open(image_path, "wb") as fh:
                    fh.write(requests.get(url).content)
    except:
        print("Error while downloading images")
    return image_folder_path, url_to_path_map

def getColorTag(product_line, weights_type, image_links):
    colors_data = {}
    image_folder_path, url_to_path_map = downloadImages(image_links)
    try:
        files = os.listdir(image_folder_path)
        print("Weights type : ",weights_type);
        weights_model = getWeights(weights_type)
        if weights_model:
            meta = weights_model["meta"]
            net = weights_model["net"]

            for url, f in url_to_path_map.items():
                colors_data[url] = {}
                try:
                    if f.endswith(".jpg") or f.endswith(".jpeg") or f.endswith(".png"):
                        path = bytes(f,encoding="utf-8")
                        
                        r = detect(net, meta, path)

                        if len(r)>0:
                            name = r[0][0]
                            predict = r[0][1]

                            x = r[0][2][0]
                            y = r[0][2][1]
                            w = r[0][2][2]
                            z = r[0][2][3]

                            x_max = (2*x+w)/2
                            x_min = (2*x-w)/2
                            y_min = (2*y-z)/2
                            y_max = (2*y+z)/2

                            image = Image.open(path)
                            cropped = image.crop((x_min, y_min, x_max, y_max))
                            required_colors = imageColourExtract(cropped)
                            #main_colors = [extractRequireColors(product_line, cols) for cols in required_colors]
                            #print(required_colors)
                            for col_idx in range(len(required_colors)):
                                required_colors[col_idx]["colour"] = extractRequireColors(product_line, required_colors[col_idx]["colour"])
                            colors_data[url] = {"attribute_value": required_colors, "crop_cordinates":{"x_axis":x/10, "y_axis": y/10, "width":w, "height":z}} 
                except Exception as e:
                    print("Error", e)
            
        try:
            shutil.rmtree(image_folder_path, ignore_errors=False, onerror=None)
        except:
            print("Error while deleting folder")
    except:
        print("Error")
    return json.dumps(colors_data)

