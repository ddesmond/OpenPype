# -*- coding: utf-8 -*-
import openpype.api
import pyblish.api
import hou


class ValidateWorkfilePaths(pyblish.api.InstancePlugin):
    """Validate workfile paths so they are absolute."""

    order = pyblish.api.ValidatorOrder
    families = ["workfile"]
    hosts = ["clarisse"]
    label = "Validate Workfile Paths"
    actions = [openpype.api.RepairAction]
    optional = True

    node_types = ["file", "alembic"]
    prohibited_vars = ["$HIP", "$JOB"]

    def process(self, instance):
        invalid = self.get_invalid()
        self.log.info(
            "node types to check: {}".format(", ".join(self.node_types)))
        self.log.info(
            "prohibited vars: {}".format(", ".join(self.prohibited_vars))
        )
        if invalid:
            for param in invalid:
                self.log.error(
                    "{}: {}".format(param.path(), param.unexpandedString()))

            raise RuntimeError("Invalid paths found")

    @classmethod
    def get_invalid(cls):
        invalid = []

        return invalid

    @classmethod
    def repair(cls, instance):
        invalid = cls.get_invalid()
        for param in invalid:
            cls.log.info("processing: {}".format(param.path()))
            cls.log.info("TODO")
