from sklearn.cluster import KMeans
import numpy as np
import cv2
import webcolors

def closest_colour(requested_colour):
    min_colours = {}
    for key, name in webcolors.css3_hex_to_names.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - requested_colour[0]) ** 2
        gd = (g_c - requested_colour[1]) ** 2
        bd = (b_c - requested_colour[2]) ** 2
        min_colours[(rd + gd + bd)] = name
    return min_colours[min(min_colours.keys())]

def get_colour_name(requested_colour):
    try:
        closest_name = actual_name = webcolors.rgb_to_name(requested_colour)
    except ValueError:
        closest_name = closest_colour(requested_colour)
        actual_name = None
    return actual_name, closest_name

def imageColourExtract(pil_img):
    temp_colour_list=[]
    colour1_percentage_list = []
    colour2_percentage_list = []

    img = pil_img.convert('RGB') 
    img = np.array(img)
    img = img[:, :, ::-1].copy()
    
    height, width, dim = img.shape
    img = img[int(height/4):int(3*height/4), int(width/4):int(3*width/4), :]
    height, width, dim = img.shape
    print(height, width, dim)
    img_vec = np.reshape(img, [height * width, dim] )

    kmeans = KMeans(n_clusters=2)
    kmeans.fit( img_vec )
    unique_l, counts_l = np.unique(kmeans.labels_, return_counts=True)
    sort_ix = np.argsort(counts_l)
    sort_ix = sort_ix[::-1]

    track_colour_rgb=[]
    track_colour_hex = []
    color_percentage = [];
    z= {i: np.where(kmeans.labels_ == i)[0] for i in range(kmeans.n_clusters)}
    colour_1_weight = len(z[0])
    colour_2_weight = len(z[1])
    total = colour_1_weight+ colour_2_weight

    print("colour 1 percentage :",float(float(colour_1_weight)/float(total)*100))
    color_percentage += [round(float(float(colour_1_weight)/float(total)*100), 6)]
    print("colour 2 percentage :",float(float(colour_2_weight)/float(total)*100))
    color_percentage += [round(float(float(colour_2_weight)/float(total)*100), 6)]

    for cluster_center in kmeans.cluster_centers_:
        print(cluster_center[2], cluster_center[1], cluster_center[0])
        track_colour_hex+=['#%02x%02x%02x' %(int(cluster_center[2]), int(cluster_center[1]), int(cluster_center[0]))]
        track_colour_rgb+=[[int(cluster_center[2]), int(cluster_center[1]), int(cluster_center[0])]]

    ################################################################################################
    for colour_rgb in track_colour_rgb:
        requested_colour = ( int(colour_rgb[0]), int(colour_rgb[1]), int(colour_rgb[2]))
        actual_name, closest_name = get_colour_name(requested_colour)
        temp_colour_list+=[closest_name]
        print("closest colour name:", closest_name,  "rgb_value", int(colour_rgb[0]), int(colour_rgb[1]), int(colour_rgb[2]))
    print("################################################")

    required_data = []
    max_percentage = max(color_percentage)
    for i in range(len(color_percentage)):
        if color_percentage[i]>=max_percentage-20:
            required_data.append({"colour":temp_colour_list[i],"hexa_code":track_colour_hex[i],"color_percentage" : color_percentage[i], "rgb_values":track_colour_rgb[i]})
    return required_data