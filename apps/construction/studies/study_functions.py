import importlib
import logging

from apps.construction import models
from os import listdir
from os.path import isfile, join
from goaltrees import settings

STUDYMODULE = "apps.construction.studies"


def check_for_STUDY_existence(study_name):
    """Function to check if an STUDY module already exists in the Database. Workaround to avoid multiple STUDY modules
    beinginstantiated."""
    return models.Study.objects.filter(name=study_name).exists()


def get_studies():
    # path with study modules
    STUDY_path = settings.BASE_DIR + "/apps/construction/studies"

    # only files
    files = [f for f in listdir(STUDY_path) if isfile(join(STUDY_path, f))]
    # only files starting with STUDY

    files = [f for f in files if f[:6] == "STUDY_"]

    studies = []
    for file in files:
        try:
            # remove .py ending
            name = file[:-3]
            study = create_study_by_classname(name)
            studies.append(study)
        except Exception as e:
            print("class instantiation failed for {}: {}".format(name, e))
    return studies


def initialize_studies():
    """
    Create or update all studies and their view contexts in database
    :return:
    """
    studies = get_studies()
    for study in studies:
        # create context foreach study
        try:
            study.init_contexts()
        except Exception as e:
            print("study context initialization failed for {}: {}".format(study.name, e))


def create_study_by_classname(study):
    """
    Create a class instance by constructor call in a string.
    :param study: module name, class name plus arguments in ()
    :return: an instance of the class specified.
    """
    try:
        sm_call = "{}.{}.{}()".format(STUDYMODULE, study, study)

        if "(" in sm_call:
            full_class_name, args = class_name = sm_call.rsplit('(', 1)
            args = '(' + args
        else:
            full_class_name = sm_call
            args = ()

        # Get the class object
        module_path, _, class_name = full_class_name.rpartition('.')
        mod = importlib.import_module(module_path)
        klazz = getattr(mod, class_name)
        alias = class_name + "Alias"
        instance = eval(alias + args, {alias: klazz})
        return instance

    except (ImportError, AttributeError) as e:
        logging.exception(e)
        raise ImportError(sm_call)