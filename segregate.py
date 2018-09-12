import random


full = "/home/kunal/tless_data/process_data/t-less_v2/aivero_data/image_names.txt"
train = "/home/kunal/tless_data/process_data/t-less_v2/aivero_data/train.txt"
test = "/home/kunal/tless_data/process_data/t-less_v2/aivero_data/test.txt"

train_file = open(train, 'w')
test_file = open(test, 'w')

with open(full, "r") as ins:
  array = []
  for line in ins:
    #array.append(line.rstrip('\n'))
    array.append(line)


  for data in array:
  #  print data
  #for i in range(len(array)):
    #print array[i]
    value = random.randint(1,100)
    if ( value  > 80 ):
      # use as test data
      test_file.write(data)
    else:
      # use as train data
      train_file.write(data)


train_file.close()
test_file.close()
