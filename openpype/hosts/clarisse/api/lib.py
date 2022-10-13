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
    # check for context creation
    if ix.item_exists(str("build://project/IMPORTS/"+str(ctx))):
        return True

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