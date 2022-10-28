import os
import json



def get_local_clarisse_cfg(version="5.0"):
    """"Gets clarisse platform specific path to the local cfg file for the current running clarisse version
    """
    import platform
    # this should be got from the anatomy apps for the correct version to query
    #  we here assume that its the latest clarisse verions 5.0

    # version = ix.application.get_version()[0:3]

    host_os = platform.system().lower()
    if host_os == "windows":
        file = os.path.expanduser("~") + "/AppData/Roaming/Isotropix/Clarisse/" + str(version) + "/clarisse.cfg"
    elif host_os == "macos":
        file = os.path.expanduser("~") + "/Library/Preferences/Isotropix/Clarisse/" + str(version) + "/clarisse.cfg"
    else:
        # linux
        file = os.path.expanduser("~") + "/.isotropix/clarisse/" + str(version) + "/clarisse.cfg"

    if os.path.isfile(file):
        return file
    else:
        print("NO CLARISSE CONFIGURATION FILE FOUND. PLEASE CHECK IN WITH PIPELINE.")


def set_config_type_values(configtype, category, key, value, mode, modetype):
    """Sets config attribute item type class, factory
    """
    import ix
    modes = {
        "mode_app" : {
            "bool" : ix.application.get_prefs(ix.api.AppPreferences.MODE_APPLICATION).set_bool_value,
            "double" : ix.application.get_prefs(ix.api.AppPreferences.MODE_APPLICATION).set_double_value,
            "string": ix.application.get_prefs(ix.api.AppPreferences.MODE_APPLICATION).set_string_value,
            "preset": ix.application.get_prefs(ix.api.AppPreferences.MODE_APPLICATION).set_preset_value,
            "long": ix.application.get_prefs(ix.api.AppPreferences.MODE_APPLICATION).set_long_value
                        },
        "mode_prefs" : {
            "bool" : ix.application.get_prefs().set_bool_value,
            "double" : ix.application.get_prefs().set_double_value,
            "string": ix.application.get_prefs().set_string_value,
            "preset": ix.application.get_prefs().set_preset_value,
            "long": ix.application.get_prefs().set_long_value
                        }
    }

    if configtype in modes[mode]:
        return modes[configtype][modetype]("{}".format(category), "{}".format(key), "{}".format(value))



def load_user_config(json_path=None):
    """Loads user config from a path"""
    with open(json_path, 'r') as filename:
        user_data = json.loads(filename)

    return user_data


def save_user_config(json_data=None, json_path=None):
    """Save user configs to json file
    """
    json_object = json.dumps(json_data, indent=4)
    with open(json_path, "w") as outfile:
        outfile.write(json_object)

    return json_path



def copy_user_config(destination_path=None):
    local_preferences_file = get_local_clarisse_cfg()
    import shutil

    try:
        shutil.copy(local_preferences_file, destination_path)
        print("Preferences copied successfully.")

    except shutil.SameFileError:
        print("Source and destination represents the same file.")
        pass

    except PermissionError:
        print("Permission denied. Check Your folders permissions.")

    except Exception as unknownerror:
        print("Error occurred while copying preferences file: {}.".format(unknownerror))


def load_json_settings():
    """Loads json settings for both modes
    """
    with open("config_manager_presets.json", 'r') as filename:
        data = json.loads(filename)
    return data



def load_json_settings_types():
    """"LOads json settings for pref types
    """

    with open("config_type_definitions.json", 'r') as filename:
        configtypes = json.loads(filename)

    return configtypes



def setup_config():
    """On first run or triggered, load and set common
    preferences options for a project file, clarisse will automaticaly
    save it in the local user folder which we can retrieve and copy for further
    usage
    """
    data = load_json_settings()
    configtypes = load_json_settings_types()

    for d in data:
        print(d)
        # print(data[d])
        for a in data[d]:
            for p in data[d][a]:
                for k in p.keys():
                    print(k, p[k])
                    print(configtypes[k])




def legacy_procees_configmanager_setup():
    """Brute force loading and setting preferences
    """
    from openpype.pipeline.context_tools import get_current_project_asset
    import ix

    asset_doc = get_current_project_asset()
    asset_data = asset_doc["data"]
    project_fps = float(asset_data.get("fps", 25))

    # general settings
    ix.application.get_prefs(ix.api.AppPreferences.MODE_APPLICATION).set_string_value("general", "startup_scene",
                                                                                      "c:/newpipe/projects/develop/cl_layouts/work/layouts/develop_cl_layouts_layouts_v001.project")
    ix.application.get_prefs(ix.api.AppPreferences.MODE_APPLICATION).set_preset_value("Input_Output", "openEXR_compression_method", "DWAB Compression")

    # color managment settings
    ix.application.get_prefs(ix.api.AppPreferences.MODE_APPLICATION).set_bool_value("color_management", "use_ocio_config_file", False)
    ix.application.get_prefs(ix.api.AppPreferences.MODE_APPLICATION).set_string_value("color_management", "ocio_config_file", "")
    ix.application.get_prefs(ix.api.AppPreferences.MODE_APPLICATION).set_preset_value("color_management", "scene_color_space", "Use scene_linear")
    ix.application.get_prefs(ix.api.AppPreferences.MODE_APPLICATION).set_preset_value("color_management", "default_view_transform", "Clarisse.sRGB")
    ix.application.get_prefs(ix.api.AppPreferences.MODE_APPLICATION).set_preset_value("color_management", "color_picker_color_space", "Use Default")

    # caching settings
    ix.application.get_prefs(ix.api.AppPreferences.MODE_APPLICATION).set_double_value("Input_Output", "stream_texture_cache", 10240)
    ix.application.get_prefs(ix.api.AppPreferences.MODE_APPLICATION).set_long_value("image_history", "image_history_cache_max_count", 10)
    ix.application.get_prefs(ix.api.AppPreferences.MODE_APPLICATION).set_string_value("image_history", "image_history_cache_path", "")
    ix.application.get_prefs(ix.api.AppPreferences.MODE_APPLICATION).set_bool_value("image_history", "image_history_autosave", False)
    ix.application.get_prefs(ix.api.AppPreferences.MODE_APPLICATION).set_double_value("image_history", "image_history_cache_max_size", 1024)

    # frames settings
    ix.application.get_prefs().set_double_value("animation", "frames_per_second", project_fps)
    ix.application.get_prefs(ix.api.AppPreferences.MODE_APPLICATION).set_double_value("animation", "frames_per_second", project_fps)

    # resolution settings
    ix.application.get_prefs().set_preset_value("rendering", "default_resolution_preset", "Custom")
    ix.application.get_prefs().set_long_value("rendering", "default_x_resolution", 1920)
    ix.application.get_prefs().set_long_value("rendering", "default_y_resolution", 1080)
    ix.application.get_prefs().set_double_value("rendering", "default_display_aspect_ratio", 1)

    # frame settings
    ix.application.get_prefs().set_double_value("animation", "start_frame", 0.0)
    ix.application.get_prefs().set_double_value("animation", "end_frame", 50)
    ix.application.get_prefs(ix.api.AppPreferences.MODE_APPLICATION).set_double_value("animation", "start_frame", 1001.0)
    ix.application.get_prefs(ix.api.AppPreferences.MODE_APPLICATION).set_double_value("animation", "end_frame", 1100.0)

