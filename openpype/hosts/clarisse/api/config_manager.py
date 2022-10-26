from openpype.pipeline.context_tools import get_current_project_asset



config_definition_mode_app = {
    "Input_Output": [
        {"openEXR_compression_method": "DWAB Compression"},
        {"stream_texture_cache":  10240}
                    ],
    "color_management": [
        {"use_ocio_config_file":  False},
        {"ocio_config_file":  ""},
        {"scene_color_space":  "Use scene_linear"},
        {"default_view_transform":  "Clarisse.sRGB"},
        {"color_picker_color_space":  "Use Default"}
                        ],
    "image_history": [
        {"image_history_cache_max_count":  40},
        {"image_history_cache_path":  ""},
        {"image_history_autosave":  False},
        {"image_history_cache_max_size":  8096}
                    ],
    "animation": [
        {"frames_per_second":  "25"},
        {"start_frame": 1001.0},
        {"end_frame": 1100.0}
                ]
}


def set_config_type_values(configtype, category, key, value, mode):
    """Setsconfig attribute item type class
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
        return mode[configtype]("{}".format(category), "{}".format(key), "{}".format(value))

def load_user_config(json_path=None):
    """Loads user config from a path"""
    pass

def save_user_config(json_path=None):
    pass

def copy_user_config(json_path=None, destination_json_path=None):
    pass

def procees_configmanager_setup():
    import ix
    asset_doc = get_current_project_asset()
    asset_data = asset_doc["data"]
    project_fps = float(asset_data.get("fps", 25))

    # general settings
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

