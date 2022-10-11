# -*- coding: utf-8 -*-
import os
import logging
import contextlib
from pyblish import api as pyblish

import ix
from . import command
from . import lib
import pyblish.api

from openpype.pipeline import (
    register_loader_plugin_path,
    register_inventory_action_path,
    register_creator_plugin_path,
    AVALON_CONTAINER_ID,
)
from openpype.host import HostBase, ILoadHost, IWorkfileHost

from openpype.hosts.clarisse import CLARISSE_ROOT_DIR


HOST_DIR = os.path.dirname(CLARISSE_ROOT_DIR)
PLUGINS_DIR = os.path.join(HOST_DIR, "plugins")
PUBLISH_PATH = os.path.join(PLUGINS_DIR, "publish")
LOAD_PATH = os.path.join(PLUGINS_DIR, "load")
CREATE_PATH = os.path.join(PLUGINS_DIR, "create")
INVENTORY_PATH = os.path.join(PLUGINS_DIR, "inventory")


class ClarisseHost(HostBase, IWorkfileHost, ILoadHost):
    name = "clarisse"

    def __init__(self):
        super(ClarisseHost, self).__init__()
        self._op_events = {}

    def install(self):
        pyblish.api.register_plugin_path(PUBLISH_PATH)
        pyblish.api.register_host("clarisse")

        register_loader_plugin_path(LOAD_PATH)
        register_creator_plugin_path(CREATE_PATH)
        register_inventory_action_path(INVENTORY_PATH)

        _install_menu()

    def open_workfile(self, filepath):
        return ix.load_project(str(filepath))

    def save_workfile(self, filepath=None):
        return ix.save_project(filepath)

    def work_root(self, session):
        work_dir = session.get("AVALON_WORKDIR")
        scene_dir = session.get("AVALON_SCENEDIR")
        if scene_dir:
            return os.path.join(work_dir, scene_dir)
        else:
            return work_dir

    def get_current_workfile(self):
        return get_current_clarisseproject()

    def workfile_has_unsaved_changes(self):
        return ix.check_need_save()

    def get_workfile_extensions(self):
        return [".project"]

    def get_containers(self):

        contexts = ix.api.OfContextSet()
        ix.application.get_factory().get_root().resolve_all_contexts(contexts)
        for context in contexts:
            # print(context)
            if context.is_reference() and not context.is_disabled():
                try:
                    id = context.get_attribute("id").get_string()
                    name = context.get_attribute("name").get_string()
                    # ix.log_info("{}: {}".format(context.get_name(), name))
                    # yielding only referenced files ""
                    print(id, name, context)
                    yield context
                except:
                    pass

    @contextlib.contextmanager
    def maintained_selection(self):
        with lib.maintained_selection():
            yield


class clarisse_project_fileLogHandler(logging.Handler):
    def emit(self, record):
        entry = self.format(record)
        clarisse_project_file = get_current_clarisseproject()
        if clarisse_project_file:
            clarisse_project_file.Print(entry)


def _install_menu():
    ix.application.get_main_menu().add_command("OpenPype>")
    ix.application.get_main_menu().add_command("OpenPype>Create")
    ix.application.get_main_menu().add_command("OpenPype>Load")
    ix.application.get_main_menu().add_command("OpenPype>Publish")
    ix.application.get_main_menu().add_command("OpenPype>Manage")
    ix.application.get_main_menu().add_command("OpenPype>Work file")
    ix.application.get_main_menu().add_command("OpenPype>Project manager")
    ix.application.get_main_menu().add_command("OpenPype>Reset resolution")
    ix.application.get_main_menu().add_command("OpenPype>Reset frame range")



def _uninstall_menu():
    ix.application.get_main_menu().remove_command("OpenPype>Create")
    ix.application.get_main_menu().remove_command("OpenPype>Load")
    ix.application.get_main_menu().remove_command("OpenPype>Publish")
    ix.application.get_main_menu().remove_command("OpenPype>Manage")
    ix.application.get_main_menu().remove_command("OpenPype>Work file")
    ix.application.get_main_menu().remove_command("OpenPype>Project manager")
    ix.application.get_main_menu().remove_command("OpenPype>Reset resolution")
    ix.application.get_main_menu().remove_command("OpenPype>Reset frame range")
    ix.application.get_main_menu().remove_command("OpenPype>")


def imprint_container(tool,
                      name,
                      namespace,
                      context,
                      loader=None):
    """Imprint a Loader with metadata

    Containerisation enables a tracking of version, author and origin
    for loaded assets.

    Arguments:
        tool (object): The node in clarisse to imprint as container, usually a
            Loader.
        name (str): Name of resulting assembly
        namespace (str): Namespace under which to host container
        context (dict): Asset information
        loader (str, optional): Name of loader used to produce this container.

    Returns:
        None

    """

    data = [
        ("schema", "avalon-core:container-2.0"),
        ("id", AVALON_CONTAINER_ID),
        ("name", str(name)),
        ("namespace", str(namespace)),
        ("loader", str(loader)),
        ("representation", str(context["representation"]["_id"])),
    ]

    keys = []
    values = []
    for key, value in data:
        keys.append("{}.{}[0]".format(tool, key))
        values.append(value)

    ix.cmds.SetValues(keys, values)


def parse_container(tool):
    """Returns imprinted container data of a tool

    This reads the imprinted data from `imprint_container`.

    """
    container = command.ix_select(tool)

    keys = ["id", "name", "namespace", "loader", "representation"]
    values = {}
    for key in keys:
        values[key] = container.get_attribute(key).get_string()

    return values


def get_current_clarisseproject():
    """Hack to get current clarisse_project_file in this session"""
    current_filepath = ix.application.get_factory().get_vars().get("PNAME").get_string() + ".project"  # noqa
    # current_filepath = ix.application.get_current_project_filename()
    return current_filepath


@contextlib.contextmanager
def clarisse_project_file_lock_and_undo_chunk(clarisse_project_file, undo_queue_name="Script CMD"):
    """Lock clarisse_project_file and open an undo chunk during the context"""
    try:
        ix.begin_command_batch("Avalon: project undo")
        yield
    finally:
        ix.end_command_batch()
