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

