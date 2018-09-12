import os
import sys
import yaml
#import ruamel.yaml as yaml
import io
import numpy as np
import struct
from PIL import Image

debug_module = 0


# Background
#
# 1.1 we will keep all data under /home/kunal/tless_data/process_data/
#
working_directory = "/home/kunal/tless_data/process_data/"
#
# 1.2 the downloaded t-less data is under t-less_v2, where we have following 2 folders
#     t-less_v2/train_primesense/01-30
#     t-less_v2/test_primesense/01-20
#
# 1.3 the processed data will go to t-less_v2/aivero_data
#     we have separate folders for PNG Images and labels
#       t-less_v2/aivero_data/PNGImages/
#       t-less_v2/aivero_data/labels/
#
target_png_folder = "./t-less_v2/aivero_data/PNGImages/"
target_labels_folder = "./t-less_v2/aivero_data/labels/"
png_absolute_path = "/home/kunal/tless_data/process_data/t-less_v2/aivero_data/PNGImages/"
#
# 1.4 all the rgb images which have been processed are listed in following file
#
image_list_file = "./t-less_v2/aivero_data/image_names.txt"
#
# 1.5 some other constants
#
yml_name = "/gt.yml"       # this is the yml file name under t-less data set
rgb_folder_name = "/rgb"   # t-less data set stores rgb images under this subfolder


# Function Definition
# processes yml file
def process_yml(base_folder,Count,file_name_prefix):
  yml_file = base_folder + str(Count).zfill(2) + yml_name;
  rgb_folder =  base_folder + str(Count).zfill(2) + rgb_folder_name;
  if (debug_module == 1):
    print("process yml file" + yml_file)
    print("corresponding rgb files are in " + rgb_folder)

  # Read YAML file
  with open(yml_file, 'r') as stream:
    info = yaml.load(stream)

    for im_id, gts_im in info.items():
      rgb_image = rgb_folder + "/" + str(im_id).zfill(4) + ".png"
      if (debug_module == 1):
        print("rgb image is : " + rgb_image)
      # Get PNG size from rgb_image
      # x_width, y_width
      im = Image.open(rgb_image)
      x_width, y_width = im.size

      # New PNG File Name
      new_rgb_name = target_png_folder + file_name_prefix + str(Count).zfill(2) + str(im_id).zfill(4) + ".png";
      if (debug_module == 1):
        print("New rgb image is : " + new_rgb_name)

      # Copy file to new folder now
      cmd = "cp " + rgb_image + " " + new_rgb_name
      os.system(cmd)

      full_rgb_name = png_absolute_path + file_name_prefix + str(Count).zfill(2) + str(im_id).zfill(4) + ".png";
      # add rgb image name to image list
      image_list.write(full_rgb_name + "\n")

      labels_file = target_labels_folder + file_name_prefix + str(Count).zfill(2) + str(im_id).zfill(4) + ".txt";
      #print("label file should be : " + labels_file)
      # Open label file for writing
      out_file = open(labels_file, 'w')

      for gt in gts_im:
        if 'obj_id' in gt.keys():
          object_id = gt['obj_id']
        if 'obj_bb' in gt.keys():
          bounding_box = np.array(gt['obj_bb'])
          x_min = bounding_box[0]
          y_min = bounding_box[1]
          x_size = bounding_box[2]
          y_size = bounding_box[3]
          x_max = x_min + x_size
          y_max = y_min + y_size
          x_avg = (x_min + x_max)/2
          y_avg = (y_min + y_max)/2

          # Now write labels to labels_file
          label_0 = object_id
          label_1 = float(x_avg)/x_width
          label_2 = float(y_avg)/y_width
          label_3 = float(x_size)/x_width
          label_4 = float(y_size)/y_width
          if (debug_module == 1):
            print (label_0)
            print (label_1)
            print (label_2)
            print (label_3)
            print (label_4)
          if (label_0 < 0) or (label_0 > 30):
            print "Fatal: object id is invalid"
          if (label_1 < 0) or (label_1 > 1.0):
            print "Fatal: object x co-ordinate is out of image"
          if (label_2 < 0) or (label_2 > 1.0):
            print "Fatal: object y co-ordinate is out of image"
          if (label_3 < 0) or (label_3 > 1.0):
            print "Fatal: object bounding box is too wide"
          if (label_4 < 0) or (label_4 > 1.0):
            print "Fatal: object bounding box is too high"

          out_file.write(str(label_0) + " " + str(label_1) + " " + str(label_2) + " " + str(label_3) + " " + str(label_4) +  "\n")

      # Close the label file now
      out_file.close()


# 2. Prepare
# Create new folders
#t-less_v2/aivero_data/PNGImages
#t-less_v2/aivero_data/labels
cmd = 'mkdir -p ./t-less_v2/aivero_data'
os.system(cmd)
print "making PNG folder"
cmd = 'mkdir -p ./t-less_v2/aivero_data/PNGImages'
os.system(cmd)
print "making labels folder"
cmd = 'mkdir -p ./t-less_v2/aivero_data/labels'
os.system(cmd)

# 2.1 open file for writing all rgb images name
image_list = open(image_list_file, 'w')

# 3.1 generate labels for train data
base_folder = "t-less_v2/train_primesense/"
file_name_prefix = "train_"
for Count in range(1, 31):
#for Count in range(1, 2):
  print ("processing train folder " + str(Count))
  process_yml(base_folder,Count,file_name_prefix)


# 3.2 generate labels for test data
base_folder = "t-less_v2/test_primesense/"
file_name_prefix = "test_"
for Count in range(1, 21):
#for Count in range(1, 2):
  print ("processing test folder " + str(Count))
  process_yml(base_folder,Count,file_name_prefix)

# close image list
image_list.close()

# 5 now segregate "t-less_v2/aivero_data/PNGImages/*.png" in to TEST & TRAIN
# python segregate.py
