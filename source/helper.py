from source.darknet import load_net, load_meta
import os, sys, json, shutil
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

def loadColorsFile():
	color_mapping_json = "/home/ubuntu/darknet/server/source/json/colour_values.json"
	with open(color_mapping_json, 'r') as f:
	    colors_mapping_data = json.load(f)
	return colors_mapping_data
	
def extractRequireColors(product_line, colour):
	main_colour = colour
	colors_mapping_data = loadColorsFile();
	if colors_mapping_data.get(product_line)!=None:
		if colors_mapping_data[product_line].get(main_colour)!=None:
			main_colour = colors_mapping_data[product_line][main_colour]
	return main_colour

def getColorInfo():
	color_mapping_json = "/home/ubuntu/darknet/color_extractor/colour_mapping.json"
	with open(color_mapping_json, 'r') as f:
	    colour_mapping = json.load(f)
	all_colors = []
	color_pixels = []
	for key, value in colour_mapping.items():
	    all_colors.append(key)
	    color_pixels.append(tuple(value["rgb"]))
	return color_pixels, all_colors

CONFIG_DEFAULT = bytes("/home/ubuntu/darknet/config_top/yolo-obj.cfg", encoding='utf-8')
weights = {}
def loadWeights():
	weights_file_path = ROOT_DIR+"/json/weights_path.json"
	with open(weights_file_path, 'r') as f:
		weights_data = json.load(f)
	for weight_type, weights_path in weights_data.items():
		if weights_path["meta"] !='' and weights_path['weights_path']!='':
			TYPE_WEIGHTS = bytes(weights_path["meta"], encoding='utf-8')
			WEIGHTS_DEFAULT = bytes(weights_path["weights_path"], encoding='utf-8')
			weights[weight_type] = {
				"meta":load_meta(TYPE_WEIGHTS),
				"net":load_net(CONFIG_DEFAULT,WEIGHTS_DEFAULT,0)
			}

def getWeights(weight_type):
	if weight_type in weights:
		return weights[weight_type]
	else:
		return None

