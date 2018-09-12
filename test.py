import os
import sys
import yaml
#import ruamel.yaml as yaml
import io
import numpy as np
import struct
from PIL import Image
#import Image


#print "root prints out directories only from what you specified"
#print "dirs prints out sub-directories from root"
#print "files prints out all files from root and directories"
#print "*" * 20
#walk_dir = sys.argv[1]
#print('walk_dir = ' + walk_dir)

#for root, dirs, files in os.walk(walk_dir):
#    print root
#    print dirs
#    print files

# constants ?
yml_name = "/gt.yml"
#yml_name = "/ks.yml"
rgb_name = "/rgb"
labels_name = "/labels"
target_png_folder = "./t-less_v2/aivero_data/PNGImages/"
png_absolute_path = "/home/kunal/tless_data/process_data/t-less_v2/aivero_data/PNGImages/"
target_labels_folder = "./t-less_v2/aivero_data/labels/"
list_file = "./t-less_v2/aivero_data/image_names.txt"

# Function definition
# processes yml file
def process_yml(base_folder,Count,file_name_prefix):
  #print(Count)
  yml_file = base_folder + str(Count).zfill(2) + yml_name;
  rgb_folder =  base_folder + str(Count).zfill(2) + rgb_name;
  labels_folder =  base_folder + str(Count).zfill(2) + labels_name;
  #print("process yml file" + yml_file)
  #print("corresponding rgb files are in " + rgb_folder)
  #print("will generate labels in " + labels_folder)
  #print "now making labels folder"
  cmd = "mkdir " + labels_folder
  os.system(cmd)
  #print "making labels folder done"

  # Read YAML file
  with open(yml_file, 'r') as stream:
    info = yaml.load(stream)
    #print(info)
    for im_id, gts_im in info.items():
      # PNG Image
      rgb_image = rgb_folder + "/" + str(im_id).zfill(4) + ".png"
      #print("rgb image is : " + rgb_image)
      # Get PNG size from rgb_image
      # x_width, y_width
      im = Image.open(rgb_image)
      x_width, y_width = im.size
      #print(x_width)
      #print(y_width)

      # New PNG File Name
      new_rgb_name = target_png_folder + file_name_prefix + str(Count).zfill(2) + str(im_id).zfill(4) + ".png";
      #print("New rgb image is : " + new_rgb_name)

      # Copy file to new folder now
      cmd = "cp " + rgb_image + " " + new_rgb_name
      os.system(cmd)

      full_rgb_name = png_absolute_path + file_name_prefix + str(Count).zfill(2) + str(im_id).zfill(4) + ".png";
      # add to image list
      image_list.write(full_rgb_name + "\n")

      # labels_file = labels_folder + "/" + str(im_id).zfill(4) + ".txt"
      labels_file = target_labels_folder + file_name_prefix + str(Count).zfill(2) + str(im_id).zfill(4) + ".txt";
      #print("label file should be : " + labels_file)
      # Open label file for writing
      out_file = open(labels_file, 'w')

      for gt in gts_im:
        if 'obj_id' in gt.keys():
          object_id = gt['obj_id']
          #print "object id is: "
          #print object_id
        if 'obj_bb' in gt.keys():
          bounding_box = np.array(gt['obj_bb'])
          # for x in np.nditer(bounding_box):
          #print "bounding box is: "
          #for i in range(0,4):
          #  print bounding_box[i]
          x_min = bounding_box[0]
          y_min = bounding_box[1]
          x_size = bounding_box[2]
          y_size = bounding_box[3]
          x_max = x_min + x_size
          y_max = y_min + y_size
          x_avg = (x_min + x_max)/2
          y_avg = (y_min + y_max)/2
          #print(x_min)
          #print(y_min)
          #print(x_max)
          #print(y_max)
          #print(x_avg)
          #print(y_avg)
          #print(x_size)
          #print(y_size)

          # Now write labels to labels_file
          label_0 = object_id
          label_1 = float(x_avg)/x_width
          label_2 = float(y_avg)/y_width
          label_3 = float(x_size)/x_width
          label_4 = float(y_size)/y_width
          #print (label_0)
          #print (label_1)
          #print (label_2)
          #print (label_3)
          #print (label_4)
          out_file.write(str(label_0) + " " + str(label_1) + " " + str(label_2) + " " + str(label_3) + " " + str(label_4) +  "\n")

      # Close the label file now
      out_file.close()

# 1. To start with
# we have following folders
#t-less_v2/train_primesense/01-30
#t-less_v2/test_primesense/01-20
# this is the yml file name


# 2. Prepare
# Create new folders
#t-less_v2/aivero_data/PNGImages
#t-less_v2/aivero_data/labels
cmd = 'mkdir -p ./t-less_v2/aivero_data'
os.system(cmd)
cmd = 'mkdir -p ./t-less_v2/aivero_data/PNGImages'
os.system(cmd)
print "making PNG folder"
cmd = 'mkdir -p ./t-less_v2/aivero_data/labels'
os.system(cmd)
print "making labels folder"

image_list = open(list_file, 'w')

# 3.1 generate labels
#for Count = 1 to 30
#cd t-less_v2/train_primesense/Count/
#mdir labels
#parse gt.yml
#populate labels/XXXX.txt
base_folder = "t-less_v2/train_primesense/"
file_name_prefix = "train_"
for Count in range(1, 31):
#for Count in range(1, 2):
  print ("processing train folder " + str(Count))
  process_yml(base_folder,Count,file_name_prefix)


# 3.2 generate more labels
#for Count = 1 to 20
#cd t-less_v2/test_primesense/Count/
#mdir labels
#parse gt.yml
#populate labels/XXXX.txt
base_folder = "t-less_v2/test_primesense/"
file_name_prefix = "test_"
for Count in range(1, 21):
#for Count in range(1, 2):
  print ("processing test folder " + str(Count))
  process_yml(base_folder,Count,file_name_prefix)

image_list.close()

# SKIP THIS STEP, as we merged this with process_yml
# 4.1 rename and copy files
#for Count = 1 to 30
#cd t-less_v2/train_primesense/Count/
# for each file NAME1 in "ls rgb/*.png"
# cp NAME.png to ../../aivero_data/PNGImages/train_Count_NAME1.png
# for each file NAME2 in "ls labels/*.txt"
# cp NAME.png to ../../aivero_data/labels/train_Count_NAME2.png

# SKIP THIS STEP, as we merged this with process_yml
# 4.2 rename and copy more files
#for Count = 1 to 20
#cd t-less_v2/test_primesense/Count/
# for each file NAME1 in "ls rgb/*.png"
# cp NAME.png to ../../aivero_data/PNGImages/test_Count_NAME1.png
# for each file NAME2 in "ls labels/*.txt"
# cp NAME.png to ../../aivero_data/labels/test_Count_NAME2.png

# 5 now segregate "t-less_v2/aivero_data/PNGImages/*.png" in to TEST & TRAIN

