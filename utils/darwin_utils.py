import json
import os
import shutil
import zipfile
from os.path import expanduser
from pathlib import Path

from darwin.client import Client
from darwin.dataset.release import Release


class Darwin_Utils:
    """
    A utility class for interacting with datasets in V7 Darwin.

    Attributes:
        api_key (str): The API key for accessing your V7 Darwin datasets.
        dataset_name (str): The name of the dataset.
        workspace_name (str): The name of the workspace.
        client (Client): An instance of the Darwin Client.
        current_release_name (str): The name of the current release.
        coco_name (str): The name of the COCO file.
    """

    def __init__(self, api_key, dataset_name, workspace_name=None):
        """
        Initializes the Darwin_Utils class.

        Args:
            api_key (str): The API key for accessing your V7 Darwin datasets.
            dataset_name (str): The name of the dataset.
            workspace_name (str, optional): The name of the workspace (if more than one workspace exists). Defaults to None.
        """

        self.api_key = api_key
        self.dataset_name = dataset_name
        self.workspace_name = workspace_name
        self.client = Client.from_api_key(self.api_key)
        self.coco_name = "coco.json"

    def __get_dataset_dir(self):
        """
        Retrieves the directory path of the dataset.

        Returns:
            str: The directory path of the dataset.
        """

        # Get the .darwin directory
        darwin_dir = expanduser("~") + "\\.darwin\\datasets"

        # Open first folder in .darwin\datasets directory if no workspace name is provided
        self.workspace_name = (
            os.listdir(darwin_dir)[0] if self.workspace_name is None else self.workspace_name
        )
        return f"{darwin_dir}\\{self.workspace_name}\\{self.dataset_name}"

    def get_dataset_img_dir(self):
        """
        Retrieves the directory path of the dataset images.

        Returns:
            str: The directory path of the dataset images.
        """

        return self.__get_dataset_dir() + "\\images"

    def get_dataset_releases_dir(self):
        """
        Retrieves the directory path of the dataset releases.

        Returns:
            str: The directory path of the dataset releases.
        """

        return self.__get_dataset_dir() + "\\releases"

    def pull_dataset(
        self, dataset_name, json_release_name, remove_unannotated=False, video_frames=False
    ):
        """
        Pulls the dataset from the V7 Darwin platform.

        Args:
            dataset_name (str): The name of the dataset.
            json_release_name (str): The name of the JSON release. See README.md for more information.
            remove_unannotated (bool, optional): Whether to remove unannotated data. Defaults to False.
            video_frames (bool, optional): Whether to include video frames. Defaults to False.
        """

        # Get the dataset and release
        dataset = self.client.get_remote_dataset(dataset_name)
        release: Release = dataset.get_release(json_release_name)

        # Pull the dataset (including all image/video data)
        dataset.pull(release=release, remove_extra=remove_unannotated, video_frames=video_frames)

    def pull_coco_annotations(self, dataset_name, coco_release_name):
        """
        Pulls the COCO annotations for the dataset.

        Args:
            dataset_name (str): The name of the dataset.
            coco_release_name (str): The name of the COCO release. See README.md for more information.
        """

        # Get the dataset and release
        coco_release_dir = self.get_dataset_releases_dir() + f"\\{coco_release_name}"
        dataset = self.client.get_remote_dataset(dataset_name)
        release: Release = dataset.get_release(coco_release_name)

        # Clear COCO release directory
        if os.path.exists(coco_release_dir):
            shutil.rmtree(coco_release_dir)
        os.makedirs(coco_release_dir)
        coco_release_path = Path(coco_release_dir)

        # Download and unzip the COCO annotations
        zip_file_path = release.download_zip(coco_release_path / "dataset.zip")
        try:
            with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
                zip_ref.extractall(coco_release_dir)
        except Exception as e:
            # Handle any errors that occur during extraction
            print(f"An error occurred while extracting the COCO annotations: {e}")
        finally:
            # Clean up by removing the downloaded zip file
            os.remove(zip_file_path)

        # Rename the COCO annotations file
        files = os.listdir(coco_release_dir)
        for file in files:
            if file.endswith(".json"):
                os.rename(coco_release_dir + "\\" + file, coco_release_dir + "\\" + self.coco_name)

    def split_coco_for_video_files(self, img_dir, coco_file_path):
        """
        Splits the COCO annotations for the individual video files.

        Args:
            img_dir (str): The directory path of the darwin image folder.
            coco_file_path (str): The file path of the COCO file.
        """

        for folder in os.listdir(img_dir):
            if os.path.isdir(img_dir + "\\" + folder):

                # Copy the COCO file to the folder
                shutil.copy(coco_file_path, img_dir + "\\" + folder + "\\" + self.coco_name)

                # Filter the COCO annotations for the video frames in the folder
                self.__filter_coco_for_folder(img_dir, folder)

    def __filter_coco_for_folder(self, img_dir, folder):
        """
        Filters the COCO annotations for a specific folder.

        Args:
            img_dir (str): The directory path of the images.
            folder (str): The name of the folder.
        """

        # Load the JSON data
        with open(img_dir + "\\" + folder + "\\" + self.coco_name, "r") as f:
            data = json.load(f)

        # Filter the images
        filtered_images = [image for image in data["images"] if folder in image["file_name"]]

        # Update the JSON data
        data["images"] = filtered_images

        # Save the updated JSON data
        with open(img_dir + "\\" + folder + "\\" + self.coco_name, "w") as f:
            json.dump(data, f, indent=4)
