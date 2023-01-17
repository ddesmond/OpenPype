import os
import ix

from openpype.hosts.clarisse.api.pipeline import is_valid_item, tag_creator_object
from openpype.pipeline.context_tools import get_current_project_asset


def create_check_dirs():
    full_path_pdir = ix.application.get_factory().get_vars().get("PDIR").get_string()
    temp_pyblish_filepath = "{}/pyblish".format(full_path_pdir)

    # create folders on disk so we dont have any poping errors for filepaths in clarisse
    if not os.path.isdir(temp_pyblish_filepath):
        os.makedirs(temp_pyblish_filepath)


def check_class_present_in_context(classtype="ProjectItem", ctx=None):
    """Check if class is in a context
    """
    print(classtype)
    print(ctx)
    pass


def export_context_project(creator_type="look", selection=None, pdir=None):
    ctx_select = ix.item_exists(str(selection))
    filename = "{}/pyblish/temp_{}.project".format(pdir, creator_type)
    set_root = ix.item_exists("build://project/EXPORTS/{}".format(creator_type))
    create_check_dirs()
    data_node = ix.item_exists("build://project/EXPORTS/{}/create_{}".format(creator_type, creator_type))
    if not data_node:
        data_node = ix.create_object("create_{}".format(creator_type), "ProjectItem", set_root)
    # tag the object
    tag_creator_object(item=data_node, creator_type=creator_type, selected_context=str(ctx_select), filename=str(filename))

    return data_node



def export_context_alembic(creator_type="camera", selection=None, config_context_export=None, mode="create", item_object=None):
    """Creates a persistent options ui
    in the export context for exporting context as alembic per family
    """

    create_check_dirs()

    if mode == "create":
        options_object = export_setup_options_uiobject(creator_type=creator_type,
                                                       selected_context=selection,
                                                       config_context_export=config_context_export)

        return options_object


    if mode == "trigger":
        """Actual exporting is on the Pyblish part to trigger so we keep in line with Pyblish logic and 
        the extraction step"""
        options = export_setup_options_exporter(options_object=item_object)
        print("Triggering export, please wait.")
        run_export_IOHelper(item_options=options)
        print("Export done.")
        return options




def export_setup_options_uiobject(creator_type=None, selected_context=None, config_context_export=None):
    """Create the UI options_object which feeds option object for exporting
    """
    # get project data
    asset_doc = get_current_project_asset()
    asset_data = asset_doc["data"]
    fps = float(asset_data.get("fps", 25))
    ix.cmds.SetFps(fps)
    frame_start = str(asset_data.get("frameStart", asset_data.get("edit_in")))
    frame_end = str(asset_data.get("frameEnd", asset_data.get("edit_out")))


    set_root = ix.item_exists("build://project/EXPORTS/{}".format(creator_type))

    full_path_pdir = ix.application.get_factory().get_vars().get("PDIR").get_string()
    temp_pyblish_filepath = "{}/pyblish".format(full_path_pdir)
    temp_pyblish_filename = temp_pyblish_filepath + "/temp_{}.abc".format(creator_type)

    create_check_dirs()

    # Create the Alembic Export Options object
    options_class_name = "AbcExportOptionsUi"
    options_object_name = "creator_{}".format(creator_type)
    options_object = ix.item_exists("build://project/EXPORTS/{}/{}".format(creator_type, options_object_name))
    if options_object == None:
        options_object = ix.create_object(options_object_name, options_class_name, set_root)


    # if is_valid_item(options_object):
    selected_context = ix.item_exists(str(selected_context))

    # options_object setup
    options_object.set_private(False)  # hidden
    options_object.set_static(False)  # non-savable
    # Output Alembic file
    options_object.attrs.filename = str(temp_pyblish_filename)
    options_object.attrs.frame_range[0] = frame_start
    options_object.attrs.frame_range[1] = frame_end
    # Write one per frame per file : true/false
    options_object.attrs.write_one_frame_per_file = config_context_export["write_one_frame_per_file"]
    # Transfer data from source Alembic to the output Alembic: true/false
    options_object.attrs.transfer_source_data = config_context_export["transfer_source_data"]
    # Export combiners: true/false
    options_object.attrs.export_combiners = config_context_export["export_combiners"]
    # Export scatterers: true/false
    options_object.attrs.export_scatterers = config_context_export["export_scatterers"]
    # Scatterers export mode: as geometries, or as bounding boxes
    if config_context_export["export_scatterers"] == "1":
        options_object.attrs.scatterer_export_mode = config_context_export["scatterer_export_mode"]
    # Properties option
    options_object.attrs.export_properties = config_context_export["export_properties"]
    options_object.attrs.compatibility_mode = config_context_export["compatibility_mode"]

    # tag the object
    tag_creator_object(item=options_object, creator_type=creator_type, selected_context=selected_context)
    return options_object


def export_setup_options_exporter(options_object=None):
    # options setup
    options = ix.api.AbcExportOptions(ix.application)
    # Context to be exported
    options.export_mode = ix.api.AbcExportOptions.EXPORT_MODE_CONTEXT
    options.context = ix.item_exists(options_object.get_attribute("op_sourced_path").get_string(0))
    # Frame range to be exported
    options.frame_range_mode = ix.api.AbcExportOptions.FRAME_RANGE_MODE_CUSTOM_RANGE
    options.frame_range[0] = options_object.get_attribute("frame_range").get_long(0)
    options.frame_range[1] = options_object.get_attribute("frame_range").get_long(1)
    options.filename = ix.api.CoreString(options_object.get_attribute("filename").get_string())
    options.export_one_frame_per_file = options_object.get_attribute("write_one_frame_per_file").get_bool()
    options.transfer_source_data = options_object.get_attribute("transfer_source_data").get_bool()
    options.export_combiners = options_object.get_attribute("export_combiners").get_bool()
    options.export_scatterers = options_object.get_attribute("export_scatterers").get_bool()
    options.scatterer_export_mode = options_object.get_attribute("scatterer_export_mode").get_long()
    options.export_properties = options_object.get_attribute("export_properties").get_bool()

    compatibility_mode = options_object.get_attribute("compatibility_mode").get_long()
    if compatibility_mode == ix.api.AbcExportOptions.PropertiesCompatibilityMode_Default:
        # use the options values
        options.fill_sparse_properties = options_object.get_attribute("fill_sparse_properties").get_bool()
        options.promote_to_geometry_parameter = options_object.get_attribute("promote_to_geometry_parameter").get_bool()
        options.bake_indexed_properties = options_object.get_attribute("bake_indexed_properties").get_bool()
    else:
        # use the values defined by the mode
        options.fill_sparse_properties = ix.api.AbcExportOptions.get_fill_sparse_properties(compatibility_mode)
        options.promote_to_geometry_parameter = ix.api.AbcExportOptions.get_promote_to_geometry_parameter(compatibility_mode)
        options.bake_indexed_properties = ix.api.AbcExportOptions.get_bake_indexed_properties(compatibility_mode)

    return options



def run_export_IOHelper(item_options=None):
    """Needs options object """
    if item_options:
        ix.api.IOHelpers.export_to_alembic(item_options)
    else:
        print("Didint get the options object")


def run_export_context(ctx_select=None, filename=None):
    create_check_dirs()
    ix.export_context_as_project(ix.get_item(str(ctx_select)), str(filename))

