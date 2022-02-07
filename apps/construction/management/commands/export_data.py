from django.core.management.base import BaseCommand
from apps.construction import models
import csv
import pandas as pd
import os

EXPORT_PATH = "{}/data".format(os.getcwd())

def get_model_field_names(model, ignore_fields=['content_object']):
    """
    ::param model is a Django model class
    ::param ignore_fields is a list of field names to ignore by default
    This method gets all model field names (as strings) and returns a list
    of them ignoring the ones we know don't work (like the 'content_object' field)
    """
    model_fields = model._meta.get_fields()
    model_field_names = list(set([f.name for f in model_fields if f.name not in ignore_fields]))
    return model_field_names


def get_lookup_fields(model, fields=None):
    """
    ::param model is a Django model class
    ::param fields is a list of field name strings.
    This method compares the lookups we want vs the lookups
    that are available. It ignores the unavailable fields we passed.
    """
    model_field_names = get_model_field_names(model)
    if fields is not None:
        """
        we'll iterate through all the passed field_names
        and verify they are valid by only including the valid ones
        """
        lookup_fields = []
        for x in fields:
            if "__" in x:
                # the __ is for ForeignKey lookups
                lookup_fields.append(x)
            elif x in model_field_names:
                lookup_fields.append(x)
    else:
        """
        No field names were passed, use the default model fields
        """
        lookup_fields = model_field_names
    return lookup_fields


def qs_to_dataset(qs, fields=None):
    """
    ::param qs is any Django queryset
    ::param fields is a list of field name strings, ignoring non-model field names
    This method is the final step, simply calling the fields we formed on the queryset
    and turning it into a list of dictionaries with key/value pairs.
    """

    lookup_fields = get_lookup_fields(qs.model, fields=fields)
    return list(qs.values(*lookup_fields))

def convert_to_dataframe(qs, fields=None, index=None):
    """
    ::param qs is an QuerySet from Django
    ::fields is a list of field names from the Model of the QuerySet
    ::index is the preferred index column we want our dataframe to be set to

    Using the methods from above, we can easily build a dataframe
    from this data.
    """
    lookup_fields = get_lookup_fields(qs.model, fields=fields)
    index_col = None
    if index in lookup_fields:
        index_col = index
    elif "id" in lookup_fields:
        index_col = 'id'
    values = qs_to_dataset(qs, fields=fields)
    df = pd.DataFrame.from_records(values, columns=lookup_fields, index=index_col)
    return df

def write_model_to_csv(model, file_path):

    field_names = get_model_field_names(model)

    objects = model.objects.all()

    df_model = pd.DataFrame(columns=field_names)
    for s in list(objects.values()):
        df_model = df_model.append(s, ignore_index=True)

    df_model.to_csv(path_or_buf=file_path, sep=";")


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
