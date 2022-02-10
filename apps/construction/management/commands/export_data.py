from django.core.management.base import BaseCommand
from apps.construction import models
import csv
import pandas as pd
import os

EXPORT_PATH = "{}/data".format(os.getcwd())




def write_model_to_csv(model, file_path):
    """
    Writes all data from a model into a csv file in the specified path.
    @param model: Model class to be exported
    @param file_path: File path of the resulting csv file
    """
    model_fields = model._meta.get_fields()
    field_names = list(set([f.name for f in model_fields]))

    objects = model.objects.all()

    df_model = pd.DataFrame(columns=field_names)
    for s in list(objects.values()):
        df_model = df_model.append(s, ignore_index=True)

    df_model.to_csv(path_or_buf=file_path, sep=";",)


class Command(BaseCommand):
    help = 'Exports relations of construction app as csv files'

    def handle(self, *args, **kwargs):

        #df_studies = convert_to_dataframe(models.Study.objects.all())
        #df_studies.to_csv(path_or_buf="{}/studies.csv".format(EXPORT_PATH), sep=";")
        write_model_to_csv((models.Participant), "{}/participants.csv".format(EXPORT_PATH))
        write_model_to_csv(models.Goal, "{}/goals.csv".format(EXPORT_PATH))
        write_model_to_csv(models.PersonalGoal, "{}/personalgoals.csv".format(EXPORT_PATH))
        write_model_to_csv(models.Study, "{}/studies.csv".format(EXPORT_PATH))
        write_model_to_csv(models.Item, "{}/items.csv".format(EXPORT_PATH))
        write_model_to_csv(models.Question, "{}/questions.csv".format(EXPORT_PATH))
        write_model_to_csv(models.StudyContext, "{}/studycontexts.csv".format(EXPORT_PATH))
        write_model_to_csv(models.UserInteraction, "{}/userinteractions.csv".format(EXPORT_PATH))
