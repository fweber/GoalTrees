
class STUDY_BASE():
    """
    Study base class.
    """

    def __init__(self):
        self.name = "STUDY_BASE"
        self.description = "Default description"
        self.active = True
        self.duration = 1
        self.sequence = []
        self.context = {}
        self.study = None

    def get_class_name(self):
        return self.__class__.__name__

    def init_contexts(self):
        pass

    def get_csv_dataframe(self, export_name):
        """
        Returns a pandas dataframe for csv export
        :param export_name: name of dataframe
        :return:
        """
        if export_name == "default":
            return self.create_dataframe()
        else:
            return getattr(self, "create_" + export_name + "_dataframe")()

    def create_dataframe(self):
        pass
