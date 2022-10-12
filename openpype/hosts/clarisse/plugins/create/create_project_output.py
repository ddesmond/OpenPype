import ix


class CreateContextProjectOutput():
    """Bake a context into a project file"""

    label = "Clarisse project file"
    family = "project"
    icon = "magic"
    defaults = ["Main"]

    def __init__(self, *args, **kwargs):
        super(CreateContextProjectOutput, self).__init__(*args, **kwargs)


    def _process(self, instance):
        """Creator main entry point.

        Args:
            instance (pyContext): selected context

        """

        pname = ix.application.get_factory().get_vars().get("PNAME").get_string() + ".project"
        pdir = ix.application.get_factory().get_vars().get("PDIR").get_string()

        _app = ix.application
        if _app.get_selection().get_count() > 0:
            item = _app.get_selection().get_item(0)
            if item.is_context():
                context_selected = item.to_context()
                if context_selected:

                    if pname != "untitled.project":
                        context_name = str(context_selected).split("/")[-1]

                        filename = "$PDIR/pyblish/%s.project" % self.context_name

                        print("Saving cache filename as {}".format(filename))
                        try:
                            os.makedirs(str(pdir + "/pyblish/"))
                        except:
                            pass


                        ix.export_context_as_project(context_selected, filename)

                    else:
                        ix.log_info("Please save you project first!\nUntitled files are not able to export.")

            else:
                ix.log_info("Only Contexts can be exported!\nPlease select a context to export.")

        else:
            ix.log_info("No Context selected!\nPlease select a context to export.")





