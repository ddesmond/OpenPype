# -*- coding: utf-8 -*-
"""Extract data as Maya scene (raw)."""
import os

from maya import cmds

from openpype.hosts.maya.api.lib import maintained_selection
from openpype.pipeline import AVALON_CONTAINER_ID, publish


class ExtractMayaSceneRaw(publish.Extractor):
    """Extract as Maya Scene (raw).

    This will preserve all references, construction history, etc.
    """

    label = "Maya Scene (Raw)"
    hosts = ["maya"]
    families = ["mayaAscii",
                "mayaScene",
                "setdress",
                "layout",
                "camerarig"]
    scene_type = "ma"

    def process(self, instance):
        """Plugin entry point."""
        ext_mapping = (
            instance.context.data["project_settings"]["maya"]["ext_mapping"]
        )
        if ext_mapping:
            self.log.debug("Looking in settings for scene type ...")
            # use extension mapping for first family found
            for family in self.families:
                try:
                    self.scene_type = ext_mapping[family]
                    self.log.info(
                        "Using {} as scene type".format(self.scene_type))
                    break
                except KeyError:
                    # no preset found
                    pass
        # Define extract output file path
        dir_path = self.staging_dir(instance)
        filename = "{0}.{1}".format(instance.name, self.scene_type)
        path = os.path.join(dir_path, filename)

        # Whether to include all nodes in the instance (including those from
        # history) or only use the exact set members
        members_only = instance.data.get("exactSetMembersOnly", False)
        if members_only:
            members = instance.data.get("setMembers", list())
            if not members:
                raise RuntimeError("Can't export 'exact set members only' "
                                   "when set is empty.")
        else:
            members = instance[:]

        selection = members
        if set(self.add_for_families).intersection(
                set(instance.data.get("families", []))) or \
                instance.data.get("family") in self.add_for_families:
            selection += self._get_loaded_containers(members)

        # Perform extraction
        self.log.info("Performing extraction ...")
        with maintained_selection():
            cmds.select(selection, noExpand=True)
            cmds.file(path,
                      force=True,
                      typ="mayaAscii" if self.scene_type == "ma" else "mayaBinary",  # noqa: E501
                      exportSelected=True,
                      preserveReferences=True,
                      constructionHistory=True,
                      shader=True,
                      constraints=True,
                      expressions=True)

        if "representations" not in instance.data:
            instance.data["representations"] = []

        representation = {
            'name': self.scene_type,
            'ext': self.scene_type,
            'files': filename,
            "stagingDir": dir_path
        }
        instance.data["representations"].append(representation)

        self.log.info("Extracted instance '%s' to: %s" % (instance.name, path))

    @staticmethod
    def _get_loaded_containers(members):
        # type: (list) -> list
        refs_to_include = {
            cmds.referenceQuery(node, referenceNode=True)
            for node in members
            if cmds.referenceQuery(node, isNodeReferenced=True)
        }

        members_with_refs = refs_to_include.union(members)

        obj_sets = cmds.ls("*.id", long=True, type="objectSet", recursive=True,
                           objectsOnly=True)

        loaded_containers = []
        for obj_set in obj_sets:

            if not cmds.attributeQuery("id", node=obj_set, exists=True):
                continue

            id_attr = "{}.id".format(obj_set)
            if cmds.getAttr(id_attr) != AVALON_CONTAINER_ID:
                continue

            set_content = set(cmds.sets(obj_set, query=True))
            if set_content.intersection(members_with_refs):
                loaded_containers.append(obj_set)

        return loaded_containers
