# V7 Darwin 2 Roboflow
Transfer image or video datasets from V7 Darwin to Roboflow (including annotations).

## 💡 Introduction
The [V7Darwin-2-Roboflow](https://github.com/Jns-M/V7Darwin-2-Roboflow) toolkit is designed to automatically transfer datasets from V7 Labs' Darwin to Roboflow while retaining all annotations. Some common use cases include:
- Part of a dataset has been annotated in Darwin and needs to be merged with the rest of the dataset on Roboflow
- Switching from Darwin to Roboflow
- Missing Export Options in Darwin which Roboflow has (e.g. YOLOv8 for videos/video frames)

The code is flexible and can be utilized across various platforms, including Linux, MacOS, and Windows.

## ⚙️ Requirements

A Python environment running version 3.8 or later with all necessary dependencies is required. The dependencies can be installed by using the [`requirements.txt`](https://github.com/Jns-M/V7Darwin-2-Roboflow/blob/main/requirements.txt) file and executing the following pip command in your terminal:

```bash
$ pip install -r requirements.txt  # Install all required packages
```

Additionally, a **JSON** and **COCO** export version (release) need to be created for your [Darwin](https://darwin.v7labs.com/) dataset in order for the toolkit to work. This can be done by following these steps:

### Create **JSON** release in [V7 Labs Darwin](https://darwin.v7labs.com/):
1. Navigate to your dataset on the [Darwin Website](https://darwin.v7labs.com/).
2. Click on **Export Data**.
3. Click the **+** Icon located at the top right of the Export Page.
4. Enter a name for the version. This name will be needed in the toolkit later.
5. Under *Format*, select **Darwin 2.0 (JSON)**.
6. Under *Items to Export*, select **All Complete**.
7. Click on **Export Items**.
8. The release has now been created.

### Create **COCO** release in [V7 Labs Darwin](https://darwin.v7labs.com/):
1. Navigate to your dataset on the [Darwin Website](https://darwin.v7labs.com/).
2. Click on **Export Data**.
3. Click the **+** Icon located at the top right of the Export Page.
4. Enter a name for the version. This name will be needed in the toolkit later.
5. Under *Format*, select **COCO**.
6. Under *Items to Export*, select **All Complete**.
7. Click on **Export Items**.
8. The release has now been created.

You can either create a new Roboflow dataset or use an existing one in which the data should be uploaded. Make sure that you know the Project ID of this dataset. 
## 🛠️ Usage

Start by pasting your V7 Darwin and Roboflow API Keys and dataset information into [`v7darwin_2_roboflow.py`](https://github.com/Jns-M/V7Darwin-2-Roboflow/blob/main/v7darwin_2_roboflow.py) instead of the placeholder values:
- V7 Darwin API Key
- V7 Darwin Dataset Name
- V7 Darwin JSON Release
- V7 Darwin COCO Release
- Roboflow PRIVATE API Key
- Roboflow Project ID

**ATTENTION:** Make sure that the V7 Darwin API Key has all necessary permissions enabled. Also, the Roboflow Project ID of a dataset does not always match the dataset name!

After that, you can **start using the toolkit** by executing the [`v7darwin_2_roboflow.py`](https://github.com/Jns-M/V7Darwin-2-Roboflow/blob/main/v7darwin_2_roboflow.py) file. This will download all necessary data from Darwin, ensure that all annotations are retained, and upload the data into the specified Roboflow dataset.

### Method Signature

```python
def v7darwin_2_roboflow(
    video=False,
    remove_unannotated=False,
    overwrite_existing_data=False,
    clear_dataset_dir=False,
)
```

### Parameters

- **video (bool, optional):** 
  - Indicates whether the V7 Darwin dataset consists of videos. Videos will be processed as individual frames. Defaults to False.

- **remove_unannotated (bool, optional):**
  - Specifies whether unannotated data should be removed before transferring the dataset to Roboflow. Defaults to False.

- **overwrite_existing_data (bool, optional):**
  - Determines whether existing data and annotations on Roboflow should be overwritten during the transfer process in case of duplicates. Defaults to False.

- **clear_dataset_dir (bool, optional):**
  - Indicates whether the dataset directory on the local computer should be cleared before downloading from V7 Darwin. Defaults to False.


### Example Usage

```python
# Image data:
v7darwin_2_roboflow()

# Image data (with removal of unannotated data):
v7darwin_2_roboflow(remove_unannotated=True)

# Video data:
v7darwin_2_roboflow(video=True)

# Video data (with removal of unannotated frames):
v7darwin_2_roboflow(video=True, remove_unannotated=True)

# Image data (with overwriting existing data/annotations):
v7darwin_2_roboflow(overwrite_existing_data=True)
```

## 📚 Citation

If you find the toolkit useful for your work, please consider citing it.

## ©️ License

[MIT](https://choosealicense.com/licenses/mit/)

## 📬 Contact

For bug reports, feature requests, and contributions, feel free to use [GitHub Issues](https://github.com/Jns-M/V7Darwin-2-Roboflow/issues). For other questions and discussions, you can contact me directly.