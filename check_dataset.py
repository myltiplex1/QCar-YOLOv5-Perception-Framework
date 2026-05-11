import os
from PIL import Image

BASE = "dataset"  # change if your folder name is different
DATA_YAML = "data.yaml"  # path to your data.yaml

# Load classes from data.yaml
import yaml
with open(DATA_YAML, "r") as f:
    data_yaml = yaml.safe_load(f)
CLASSES = data_yaml["names"]
NUM_CLASSES = data_yaml["nc"]

def check_split(split):
    img_dir = os.path.join(BASE, "images", split)
    label_dir = os.path.join(BASE, "labels", split)

    img_files = {os.path.splitext(f)[0]: f for f in os.listdir(img_dir)}
    label_files = {os.path.splitext(f)[0]: f for f in os.listdir(label_dir)}

    missing_labels = set(img_files) - set(label_files)
    missing_images = set(label_files) - set(img_files)

    print(f"\n===== {split.upper()} =====")

    # Check for matching images/labels
    if not missing_labels and not missing_images:
        print("✅ All files match perfectly!")
    else:
        if missing_labels:
            print(f"\n❌ Images WITHOUT labels ({len(missing_labels)}):")
            for f in sorted(missing_labels):
                print(f"   {img_files[f]}")
        if missing_images:
            print(f"\n❌ Labels WITHOUT images ({len(missing_images)}):")
            for f in sorted(missing_images):
                print(f"   {label_files[f]}")

    # Check for empty label files
    empty_labels = []
    wrong_class_labels = []
    for f, fname in label_files.items():
        path = os.path.join(label_dir, fname)
        if os.path.getsize(path) == 0:
            empty_labels.append(fname)
        else:
            with open(path, "r") as lf:
                for line in lf:
                    parts = line.strip().split()
                    if len(parts) < 5:
                        print(f"❌ Invalid format in {fname}: {line.strip()}")
                    cls = int(parts[0])
                    if cls >= NUM_CLASSES:
                        wrong_class_labels.append(fname)

    if empty_labels:
        print(f"\n❌ Empty label files ({len(empty_labels)}):")
        for f in empty_labels:
            print(f"   {f}")

    if wrong_class_labels:
        print(f"\n❌ Labels with invalid class indices ({len(wrong_class_labels)}):")
        for f in wrong_class_labels:
            print(f"   {f}")

    # Check if images are valid
    corrupted = []
    for f, fname in img_files.items():
        path = os.path.join(img_dir, fname)
        try:
            with Image.open(path) as im:
                im.verify()  # check if image can be opened
        except Exception as e:
            corrupted.append(fname)
    if corrupted:
        print(f"\n❌ Corrupted images ({len(corrupted)}):")
        for f in corrupted:
            print(f"   {f}")

# Run checks
check_split("train")
check_split("val")
