import os
import shutil

from utils.darwin_utils import Darwin_Utils
from utils.roboflow_utils import Roboflow_Utils


# Define your V7 Darwin API KEY (ensure that it has all necessary permissions) and dataset details
# The JSON and COCO exports have to be created online (https://darwin.v7labs.com/), for more information see README.md
V7DARWIN_API_KEY = "YOUR_V7DARWIN_API_KEY"
V7DARWIN_DATASET_NAME = "YOUR_DATASET_NAME"
V7DARWIN_JSON_EXPORT_NAME = "YOUR_JSON_EXPORT_NAME"
V7DARWIN_COCO_EXPORT_NAME = "YOUR_COCO_EXPORT_NAME"
V7DARWIN_WORKSPACE_NAME = None  # only edit this line if you have more than one workspace

# Define your Roboflow API KEY and project details
# ATTENTION: Roboflow Project ID can be different from the dataset name
ROBOFLOW_PRIVATE_API_KEY = "YOUR_PRIVATE_ROBOFLOW_API_KEY"
ROBOFLOW_PROJECT_ID = "YOUR_PROJECT_ID"
ROBOFLOW_WORKSPACE_NAME = None  # only edit this line if you have more than one workspace


def v7darwin_2_roboflow(
    video=False,
    remove_unannotated=False,
    overwrite_existing_data=False,
    clear_dataset_dir=False,
):
    """Transfers a dataset from V7 Darwin to Roboflow by uploading the data (including annotations).

    Args:
        video (bool, optional): Whether the V7 Darwin dataset consists of videos (will be converted to individual frames). Defaults to False.
        remove_unannotated (bool, optional): Whether to remove unannotated data. Defaults to False.
        overwrite_existing_data (bool, optional): Whether to overwrite existing data/annotations when uploading to Roboflow. Defaults to False.
        clear_dataset_dir (bool, optional): Whether to clear the dataset directory on the computer before downloading from V7 Darwin. Defaults to False.
    """

    # Initialize the Darwin and Roboflow utilities
    print("\nInitializing Darwin and Roboflow Utilities...")
    darwin_utils = Darwin_Utils(api_key=V7DARWIN_API_KEY, dataset_name=V7DARWIN_DATASET_NAME)
    roboflow_utils = Roboflow_Utils(
        api_key=ROBOFLOW_PRIVATE_API_KEY, project_id=ROBOFLOW_PROJECT_ID
    )

    # Get the dataset image and release directories
    darwin_dataset_img_dir = darwin_utils.get_dataset_img_dir()
    darwin_dataset_releases_dir = darwin_utils.get_dataset_releases_dir()

    # Clear the dataset directory on computer if specified
    if clear_dataset_dir and os.path.exists(darwin_dataset_releases_dir):
        shutil.rmtree(darwin_dataset_releases_dir)
    if clear_dataset_dir and os.path.exists(darwin_dataset_img_dir):
        shutil.rmtree(darwin_dataset_img_dir)

    # Pull the dataset data from V7 Darwin
    print(f"\nDownloading Dataset from V7 Darwin dataset '{V7DARWIN_DATASET_NAME}'...\n")
    darwin_utils.pull_dataset(
        V7DARWIN_DATASET_NAME,
        V7DARWIN_JSON_EXPORT_NAME,
        remove_unannotated,
        video_frames=True,
    )

    # Download the COCO annotations from V7 Darwin
    print(f"\nDownloading COCO Annotations from V7 Darwin dataset '{V7DARWIN_DATASET_NAME}'...")
    darwin_utils.pull_coco_annotations(V7DARWIN_DATASET_NAME, V7DARWIN_COCO_EXPORT_NAME)
    coco_path = f"{darwin_dataset_releases_dir}\\{V7DARWIN_COCO_EXPORT_NAME}\\coco.json"

    print(f"\nUploading Data and Annotations to Roboflow dataset '{ROBOFLOW_PROJECT_ID}'...\n")
    # Upload video data (as individual frames) including annotations to Roboflow
    if video:

        # Split COCO annotations for the individual video files
        darwin_utils.split_coco_for_video_files(
            img_dir=darwin_dataset_img_dir, coco_file_path=coco_path
        )

        # Upload the frames of each video file to Roboflow
        for file in os.listdir(darwin_dataset_img_dir):
            roboflow_utils.upload_images_and_annotations(
                img_dir=darwin_dataset_img_dir + "\\" + file,
                annotation_file=coco_path,
                overwrite=overwrite_existing_data,
            )

    # Upload image data including annotations to Roboflow
    else:

        roboflow_utils.upload_images_and_annotations(
            img_dir=darwin_dataset_img_dir,
            annotation_file=coco_path,
            overwrite=overwrite_existing_data,
        )

    print(
        f"\nData and Annotations successfully uploaded to Roboflow dataset '{ROBOFLOW_PROJECT_ID}'.\n"
    )


if __name__ == "__main__":

    # Transfer dataset from V7 Darwin to Roboflow
    v7darwin_2_roboflow()

    ### Example Usage ###

    # Image data:
    # v7darwin_2_roboflow()

    # Image data (with removal of unannotated data):
    # v7darwin_2_roboflow(remove_unannotated=True)

    # Video data:
    # v7darwin_2_roboflow(video=True)

    # Video data (with removal of unannotated frames):
    # v7darwin_2_roboflow(video=True, remove_unannotated=True)

    # Image data (with overwriting existing data/annotations):
    # v7darwin_2_roboflow(overwrite_existing_data=True)
