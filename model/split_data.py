import os
import shutil
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

# path to main/original dataset folder containing ~200k images
path = "dataset/CCPD_2019_first_part/"
source_dir = path + "ccpd_base/"

# path to output folders
train_dir = path + "train/"
test_dir = path + "test/"
valid_dir = path + "validation/"

folders = [train_dir, test_dir, valid_dir]

# get file names
files = sorted(os.listdir(source_dir))

# separate filename into sections and extract license plate area
areas = []
for i, f in enumerate(files):
    f = f.split("-")
    area = f[0].ljust(4, "0")

    areas.append(int(area))

# bin the data into percentage ranges (e.g. 200 - 300 = 2% - 3% area)
bins = [0, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 3500]
binned = pd.cut(areas, bins=bins)
print(f"Binned:\n{binned.describe()}\n")

df = pd.DataFrame({"Area": areas, "Bin": binned, "Filename": files})

# shuffle the data using sample frac=1, group by bins and take the first 100 of each bin
groups = df.sample(frac=1, random_state=19).groupby(["Bin"]).head(100)
print(groups.groupby(["Bin"]).describe())

# split into train/test/validation sets
train_data, test_data = train_test_split(groups, test_size=0.3, random_state=19)
test_data, valid_data = train_test_split(test_data, test_size=0.5, random_state=19)

# move files into corresponding dataset folders
data_list = [train_data, test_data, valid_data]

for folder, data in zip(folders, data_list):
    if not os.path.isdir(folder):
        os.mkdir(folder)
    
    for f in data["Filename"]:
        shutil.move(source_dir + f, folder)
    
    print(f"Moved {len(os.listdir(folder))} files to {folder}")

print("Finished")

