import ix
import contextlib


@contextlib.contextmanager
def maintained_selection():
    selection = ix.selection
    try:
        yield
    finally:
        ix.selection = selection


@contextlib.contextmanager
def command_batch(name):
    ix.begin_command_batch(name)
    try:
        yield
    finally:
        ix.end_command_batch()


def get_imports_context():
    """Get import context or create one so we can load files"""
    _get_root_imports = ix.item_exists("build://project/IMPORTS")

    if _get_root_imports:
        return _get_root_imports
    else:
        return ix.cmds.CreateContext("IMPORTS", "Global", "build://project/")


def check_ctx(ctx):
    """Check if context exists"""
    # check for context creation
    if ix.item_exists(str("build://project/IMPORTS/"+str(ctx))):
        return True

def gather_all_filenames_projectitems():
    """Gathers all objects/ project item class to a list
    gets all items - enabled and disabled"""

    all_files = []
    class_names = ix.api.CoreStringArray(1)
    class_names[0] = "ProjectItem"

    empty_mask = ix.api.CoreBitFieldHelper()

    all_objects = ix.api.OfObjectArray()
    root_context = ix.application.get_factory().get_root()
    root_context.get_all_objects(class_names, all_objects, empty_mask)

    for f in all_objects:
        # check for allowed, or parent context is a reference and if is read only
        if not ix.get_item(str(f.get_parent_item())).is_reference():
            try:
                if f.attrs.filename:
                    check_file = f.get_attribute("filename")
                    if f.attrs.filename != "":
                        all_files.append(f)
            except:
                pass

    return all_files


def gather_all_images(filter=True):
    """Gathers all objects/ project item class to a list
    gets all items - enabled and disabled
    filter can be Enabled or disabled, True or false
    """

    all_files = []
    class_names = ix.api.CoreStringArray(1)
    class_names[0] = "Image"

    empty_mask = ix.api.CoreBitFieldHelper()

    all_objects = ix.api.OfObjectArray()
    root_context = ix.application.get_factory().get_root()
    root_context.get_all_objects(class_names, all_objects, empty_mask)

    for f in all_objects:
        if filter and f.is_disabled():
            pass
        else:
            all_files.append(f)

    return all_files


def gather_all_layers_from_image(image=None):
    """Gathers all layer3d in the image
    """
    included_layers = []
    sourced_image = ix.get_item(str(image)).get_module()

    for a in range(sourced_image.get_all_layers().get_count()):
        layer = ix.get_item(str(image)).get_module().get_layers()[a].get_object()
        included_layers.append(layer)

    return included_layers


def create_import_contexts():
    """Create ctxs in IMPORT for asset types"""
    ctx_import_types = ["geometry", "cameras", "volumes"]
    ctx_list = []
    for ctx in ctx_import_types:
        if not check_ctx(str(ctx)):
            ctx = ix.cmds.CreateContext(str(ctx), "Global", "build://project/IMPORTS/")
            ctx_list.append(str(ctx))

    return ctx_list


def get_raw_item_filename(itemobject):
    """Returns a raw string for the object
    takes clarisse object or gets one"""
    itemobject = ix.item_exists(str(itemobject))
    return itemobject.get_attribute("filename").get_raw_string()


def make_all_contexts_local():
    """Make all referenced context as local"""
    ix.application.check_for_events()

    # get all contexts
    all_ctxs = ix.api.OfContextSet()
    ix.application.get_factory().get_root().resolve_all_contexts(all_ctxs)

    # gather all localizable reference contexts
    loc_ctxs = []
    for ctx in all_ctxs:
        engine = ctx.get_engine()
        if (engine.is_file_reference_engine() and engine.supports_localize()) or engine.is_usd_reference_engine():
            loc_ctxs.append(ctx)

    # localize them
    for ctx in loc_ctxs:
        ix.cmds.MakeLocalContext(ctx)

    ix.application.check_for_events()



def popsup(info_text=None):
    app = ix.application
    clarisse_window = app.get_event_window()
    box = ix.api.GuiMessageBox(app, 0, 0, "Pipeline Information",  info_text)
    box.set_resizable(True)
    box.resize(350,350,400,200)
    box.show()