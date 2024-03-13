import os

from roboflow import Roboflow


class Roboflow_Utils:
    """A utility class for interacting with the Roboflow API to manage datasets and upload images with annotations.

    This class provides a mathod to upload images (including annotations) to a Roboflow dataset
    It requires a valid API key and allows for the specification of the workspace and dataset names.

    Attributes:
        api_key (str): The API key used to authenticate requests to the Roboflow API (has to be private key).
        project_id (str): The id of the project within the Roboflow platform.
        workspace_name (str, optional): The name of the workspace (if more than one workspaces exist) where the dataset resides.
    """

    def __init__(self, api_key, project_id, workspace_name=None):
        """Initialize a Roboflow_Utils object with the specified API key, dataset name, and optional workspace name.

        Args:
            api_key (str): The API key used to authenticate requests to the Roboflow API (has to be private key).
            project_id (str): The id of the project within the Roboflow platform.
            workspace_name (str, optional): The name of the workspace (if more than one workspaces exist) where the dataset resides.
        """

        self.api_key = api_key
        self.project_id = project_id
        self.workspace_name = workspace_name
        self.client = Roboflow(api_key=self.api_key)

    def upload_images_and_annotations(self, img_dir, annotation_file, overwrite=False):
        """Uploads images and annotations to Roboflow.

        Args:
            img_dir (str): Directory containing the image files.
            annotation_file (str): Path to the annotation file (COCO format).
            overwrite (bool, optional): Whether to overwrite existing annotations. Defaults to False.
        """

        # Get Roboflow project
        rf_project = self.client.workspace(the_workspace=self.workspace_name).project(
            self.project_id
        )

        # Supported image file extensions by Roboflow
        file_extension_types = [".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff"]
        image_files = []

        # Get the current working directory
        original_dir = os.getcwd()

        # Change directory to img_dir to avoid issues with special characters in the roboflow upload method
        try:
            os.chdir(img_dir)

            # Iterate over all files in the directory
            for file in os.listdir():

                # Check if the file has a supported file extension
                if any(file.lower().endswith(extension) for extension in file_extension_types):
                    image_files.append(file)

            # Upload the images and annotations to Roboflow
            for image in image_files:
                print(
                    rf_project.single_upload(
                        image_path=image,
                        annotation_path=annotation_file,
                        annotation_overwrite=overwrite,
                    )
                )

        finally:

            # Revert the current working directory back to its original state
            os.chdir(original_dir)
