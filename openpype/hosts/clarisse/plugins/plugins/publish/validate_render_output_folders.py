import pyblish.api


class ValidateCreateFolderOutput(pyblish.api.InstancePlugin):
    """Check if render output folders are present,
    if not create them
    """

    order = pyblish.api.ValidatorOrder
    label = "Validate Render Folder Output"
    families = ["render"]
    hosts = ["clarisse"]


    def process(self, instance):

        # get layer3d output

        # check if folder exists

        # if doesn not, create output folder
        pass
