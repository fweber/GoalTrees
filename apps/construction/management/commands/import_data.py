from django.core.management.base import BaseCommand
from apps.construction import models
import csv
import pandas as pd
import numpy
import os
import json
import datetime
import traceback

EXPORT_PATH = "{}/data".format(os.getcwd())
ID_FILE="{}/id_table.json".format(EXPORT_PATH)


def get_or_create_id_table():
    if os.path.isfile(ID_FILE):
        print("Loaded ID table")
        id_table=json.load(open(ID_FILE))
    else:
        print("Created ID table")
        id_table = {"participants": {},
                    "goals": {},
                    "personalgoals": {},
                    "studies": {},
                    "items": {},
                    "questions": {},
                    "studycontexts": {},
                    "userinteractions": {},
                    }
    return id_table


def import_participants():
    try:
        id_table=get_or_create_id_table()

        df_participants = pd.read_csv(filepath_or_buffer="{}/participants.csv".format(EXPORT_PATH),
                                      sep=";",
                                      )

        for index, row in df_participants.iterrows():

            if str(row["id"]) in id_table["participants"].keys():
                print("Participant {} already exists!".format(row["id"]))
            else:
                study = get_or_create_study(row["study_id"], id_table)
                participant = models.Participant.objects.create(
                    age=row["age"] if not numpy.isnan(row["age"]) else None,
                    gender=row["gender"] if not numpy.isnan(row["gender"]) else None,
                    semester=row["semester"] if not numpy.isnan(row["semester"]) else None,
                    subject=row["subject"] if row["subject"] else None,
                    degree=row["degree"] if not row["degree"] else None,
                    created=datetime.datetime.fromisoformat(row["created"]) if row["created"] else None,
                    # finished= datetime.datetime.fromisoformat(row["finished"]) if row["finished"] else None,
                    condition=row["condition"] if row["condition"] else None,
                    study=study,
                    study_sequence_position=row["study_sequence_position"] if not numpy.isnan(
                        row["study_sequence_position"]) else None,
                    additional_data=row["additional_data"] if not numpy.isnan(row["additional_data"]) else None,
                    screen_size=row["screen_size"] if not numpy.isnan(row["screen_size"]) else None,
                    operating_system=row["operating_system"] if not numpy.isnan(row["operating_system"]) else None,
                    browser_language=row["browser_language"] if not numpy.isnan(row["browser_language"]) else None,
                    siddata_user_id=row["siddata_user_id"] if not row["siddata_user_id"] else None,
                )
                id_table["participants"][str(row["id"])] = participant.pk
                print("Participant {} copied with new id {}!".format(row["id"], participant.pk))
    except Exception as e:
        print(e)
        track = traceback.format_exc()
        print(track)

    json.dump(id_table, open(ID_FILE, 'w'))


def import_study_contexts():
    try:
        id_table = get_or_create_id_table()

        df_studycontexts = pd.read_csv(filepath_or_buffer="{}/studycontexts.csv".format(EXPORT_PATH),
                                      sep=";",
                                      )

        for index, row in df_studycontexts.iterrows():
            if str(row["id"]) in id_table["studycontexts"].keys():
                print("Studycontext {} already exists!".format(row["id"]))
            else:
                study = get_or_create_study(row["study_id"], id_table)

                context = row["context"]
                context = str(context).strip("'<>() ").replace('\"', '\*').replace('\'', '\"').replace('True','true').replace('False','false').replace('\*', '\'')
                context = json.loads(context)

                studycontext = models.StudyContext.objects.create(
                    view=row["view"],
                    study=study,
                    context=context,
                )
                id_table["studycontexts"][str(int(row["id"]))] = studycontext.pk
                print("Studycontext {} copied with new id {}!".format(row["id"], studycontext.pk))
    except Exception as e:
        print(e)
        track = traceback.format_exc()
        print(track)

    json.dump(id_table, open(ID_FILE, 'w'))


def import_goals():
    try:
        id_table = get_or_create_id_table()

        df_goals = pd.read_csv(filepath_or_buffer="{}/goals.csv".format(EXPORT_PATH),
                               sep=";",
                               )

        for index, row in df_goals.iterrows():

            if str(row["id"]) in id_table["goals"].keys():
                print("Goal {} already exists!".format(row["id"]))
            else:
                study = get_or_create_study(row["study_id"], id_table)

                if not numpy.isnan(row["participant_id"]):
                    participant=models.Participant.objects.get(id=id_table["participants"][str(int(row["participant_id"]))])
                else:
                    participant=None
                goal = models.Goal.objects.create(
                    tree_id=row["tree_id"],
                    parent_id=row["parent_id"] if not numpy.isnan(row["parent_id"]) else None,
                    title=row["title"],
                    description=row["description"],
                    participant=participant,
                    condition=row["condition"],
                    created=datetime.datetime.fromisoformat(row["created"]) if row["created"] else None,
                    is_example=row["is_example"],
                    example_id=row["example_id"] if not numpy.isnan(row["example_id"]) else None,
                    replicated_tree_id=row["replicated_tree_id"] if not numpy.isnan(row["replicated_tree_id"]) else None,
                    study=study,
                    discarded=row["discarded"],
                    done=False if numpy.isnan(row["done"]) else True,
                )
                goal.save()

                id_table["goals"][str(row["id"])] = goal.pk
                print("Goal {} copied with new id {}!".format(row["id"], goal.pk))

        # parent correction
        goal_ids = list(df_goals["id"])
        for index, row in df_goals.iterrows():
                goal=models.Goal.objects.get(pk=id_table["goals"][str(row["id"])])
                if goal.parent_id==None:
                    continue
                parent=models.Goal.objects.get(pk=id_table["goals"][str(goal.parent_id)])
                goal.parent_id=parent.pk
                goal.save()
                print("Changed goal {} parent_id to {}".format(goal.pk,parent.pk))

    except Exception as e:
        print(e)
        track = traceback.format_exc()
        print(track)

    json.dump(id_table, open(ID_FILE, 'w'))


def import_personalgoals():
    try:
        id_table = get_or_create_id_table()

        df_personalgoals = pd.read_csv(filepath_or_buffer="{}/personalgoals.csv".format(EXPORT_PATH),
                               sep=";",
                               )

        for index, row in df_personalgoals.iterrows():

            if str(row["id"]) in id_table["personalgoals"].keys():
                print("Personaloal {} already exists!".format(row["id"]))
            else:
                if not numpy.isnan(row["participant_id"]):
                    participant=models.Participant.objects.get(id=id_table["participants"][str(int(row["participant_id"]))])
                else:
                    participant=None
                personalgoal = models.PersonalGoal.objects.create(
                    name=row["name"],
                    participant=participant,
                    created=datetime.datetime.fromisoformat(row["created"]) if row["created"] else None,
                )
                personalgoal.save()

                id_table["personalgoals"][str(row["id"])] = personalgoal.pk
                print("Personalgoal {} copied with new id {}!".format(row["id"], personalgoal.pk))


    except Exception as e:
        print(e)
        track = traceback.format_exc()
        print(track)

    json.dump(id_table, open(ID_FILE, 'w'))

def parse_strange_answers(answers):
    answers = str(answers).replace('\"', '\*').strip("'<>() ").replace('\'', '\"').replace('\*', '\"')

    lst = []
    word = ""
    input = 0
    for i in answers:
        if i == "[":
            pass
        elif i == "\"":
            if input == 0:
                input = 1
            elif input == 1:
                input = 2
            elif input == 2:
                input = 0
        elif i == ",":
            if input == 0:
                pass
            elif input == 1:
                if len(word) > 0:
                    lst.append(word)
                    word = ""
                    input = 2
            elif input == 2:
                pass

        elif i == "]":
            pass
        elif i == " ":
            if input == 1:
                word = "{}{}".format(word, i)
                input = 2
        else:
            word = "{}{}".format(word, i)
            input = 2

    lst.append(word)
    return lst


def import_items():
    try:
        id_table = get_or_create_id_table()

        df_items = pd.read_csv(filepath_or_buffer="{}/items.csv".format(EXPORT_PATH),
                               sep=";",
                               )

        for index, row in df_items.iterrows():

            if str(row["id"]) in id_table["items"].keys():
                print("Item {} already exists!".format(row["id"]))
            else:
                if numpy.isnan(row["personal_goal_id"]):
                    personal_goal=None
                else:
                    personal_goal = models.PersonalGoal.objects.get(pk=id_table["personalgoals"][str(row["personal_goal_id"])])

                if numpy.isnan(row["goal_id"]):
                    goal=None
                else:
                    goal=models.Goal.objects.get(pk=id_table["goals"][str(int(row["goal_id"]))])

                if not numpy.isnan(row["participant_id"]):
                    participant=models.Participant.objects.get(id=id_table["participants"][str(int(row["participant_id"]))])
                else:
                    participant=None

                answers=row["answers"]
                answers=parse_strange_answers(answers)

                item = models.Item.objects.create(
                    questionnaire=row["questionnaire"],
                    code=row["code"],
                    text=row["text"],
                    latent_variable=row["latent_variable"],
                    answers=answers,
                    participant=participant,
                    created=datetime.datetime.fromisoformat(row["created"]) if row["created"] else None,
                    given_answer=row["given_answer"],
                    reverse_coded=row["reverse_coded"],
                    personal_goal=personal_goal,
                    goal=goal,
                )
                item.save()

                id_table["items"][str(row["id"])] = item.pk
                print("Item {} copied with new id {}!".format(row["id"], item.pk))

    except Exception as e:
        print(e)
        track = traceback.format_exc()
        print(track)

    json.dump(id_table, open(ID_FILE, 'w'))


def get_or_create_study(id, id_table):
    df_studies = pd.read_csv(filepath_or_buffer="{}/studies.csv".format(EXPORT_PATH),
                             sep=";",
                             )

    if numpy.isnan(id):
        print("Study id is NaN")
        return

    study_series= df_studies.loc[df_studies["id"]==id].iloc[0]

    sequence=study_series["sequence"]
    sequence = str(sequence).strip("'<>() ").replace('\'', '\"')
    sequence=json.loads(sequence)

    study, created = models.Study.objects.get_or_create(
        name=study_series["name"],
    )
    if created:
        study.sequence=sequence
        study.classname=study_series["classname"]
        study.conditions=json.loads(study_series["conditions"])
        study.language=study_series["language"]
        study.save()
        print("Study {} created!".format(study.pk))
    else:
        print("Study {} already exists!".format(study.pk))
    id_table["studies"][str(study_series["id"])] = study.pk
    return study


def import_questions():
    try:
        id_table = get_or_create_id_table()

        df_questions = pd.read_csv(filepath_or_buffer="{}/questions.csv".format(EXPORT_PATH),
                               sep=";",
                               )

        for index, row in df_questions.iterrows():

            if str(row["id"]) in id_table["questions"].keys():
                print("Question {} already exists!".format(row["id"]))
            else:

                if not numpy.isnan(row["participant_id"]):
                    participant=models.Participant.objects.get(id=id_table["participants"][str(int(row["participant_id"]))])
                else:
                    participant=None

                if numpy.isnan(row["tree_id"]):
                    goal = None
                else:
                    goal = models.Goal.objects.get(pk=id_table["goals"][str(int(row["tree_id"]))])

                question = models.Question.objects.create(
                    participant=participant,
                    question=row["question"],
                    answer=row["answer"],
                    type=row["type"],
                    created=datetime.datetime.fromisoformat(row["created"]) if row["created"] else None,
                    tree=goal,
                )
                question.save()

                id_table["questions"][str(row["id"])] = question.pk
                print("Question {} copied with new id {}!".format(row["id"], question.pk))

    except Exception as e:
        print(e)
        track = traceback.format_exc()
        print(track)

    json.dump(id_table, open(ID_FILE, 'w'))


class Command(BaseCommand):
    help = 'Exports relations of construction app as csv files'


    def handle(self, *args, **kwargs):

        import_participants()

        import_study_contexts()

        import_goals()

        import_personalgoals()

        import_items()

        import_questions()


