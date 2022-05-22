from django.core.management.base import BaseCommand
from apps.construction import models
import csv
import pandas as pd
import numpy as np
import os
import json
import datetime
import traceback
import sys
import scipy.stats
import statistics
import matplotlib.pyplot as plt
import scikit_posthocs
from autorank import autorank, plot_stats, create_report, latex_table

EXPORT_PATH = "{}/data/visualization_data".format(os.getcwd())


def analyze_study(study):
    """Extracts demographic data"""
    participants = models.Participant.objects.filter(study__name=study,
                                                     exclude_from_analyses=False,
                                                     finished__isnull=False)

    print("{} participants: {}".format(study, participants.count()))

    data = {}
    columns = ["participant_id", "age", "gender", "semester", "subject", "degree", "screen_size", "operating_system",
               "browser_language"]

    questions = models.Question.objects.filter(participant=participants[10])

    for q in questions:
        columns.append(q.question)

    ids = []
    for p in participants:
        ids.append(p.pk)
        data[p.pk] = {"participant_id": p.pk,
                      "age": p.age,
                      "gender": p.gender,
                      "semester": p.semester,
                      "subject": p.subject,
                      "degree": p.degree,
                      "screen_size": p.screen_size,
                      "operating_system": p.operating_system,
                      "browser_language": p.browser_language,
                      }
        for q in models.Question.objects.filter(participant=p):
            if p.study.name == "big5_study" and ("condition" in q.question):
                for c in columns:
                    if c[-10:] == q.question[-10:]:
                        data[p.pk][c] = q.answer
            else:
                data[p.pk][q.question] = q.answer

    df_study_data = pd.DataFrame.from_dict(data=data,
                                           orient="index",
                                           columns=columns)

    df_study_data.to_csv("{}/{}.csv".format(EXPORT_PATH, study),
                         sep=";")


def summarize_studies(studies):
    """Extracts demographic data"""
    participants = models.Participant.objects.filter(study__name__in=studies,
                                                     exclude_from_analyses=False,
                                                     finished__isnull=False)

    n = 0
    for p in participants:
        n += 1

    data = {}
    columns = ["participant_id", "age", "gender", "semester", "subject", "degree", "screen_size", "operating_system",
               "browser_language"]

    conditions = ["ranking condition: {}".format(x) for x in range(1, 5)]

    for c in conditions:
        columns.append(c)

    ids = []
    for p in participants:
        ids.append(p.pk)
        data[p.pk] = {"participant_id": p.pk,
                      "age": p.age,
                      "gender": p.gender,
                      "semester": p.semester,
                      "subject": p.subject,
                      "degree": p.degree,
                      "screen_size": p.screen_size,
                      "operating_system": p.operating_system,
                      "browser_language": p.browser_language,
                      }
        for q in models.Question.objects.filter(participant=p):
            if "condition" in q.question:
                for c in columns:
                    if c[-10:] == q.question[-10:]:
                        if p.study.name == "pilot_study":
                            translation = [0, 4, 3, 2, 1]
                            data[p.pk][c] = translation[int(q.answer)]
                        elif p.study.name == "big5_study":
                            data[p.pk][c] = q.answer

    df_study = pd.DataFrame.from_dict(data=data,
                                      orient="index",
                                      columns=columns)
    print(df_study.describe())
    print("total: {}".format(len(df_study)))
    print("male: {}".format(len(df_study.loc[df_study['gender'] == "male"])))
    print("female: {}".format(len(df_study.loc[df_study['gender'] == "female"])))

    for s in df_study["subject"].unique():
        print("{}: {}".format(s, len(df_study.loc[df_study['subject'] == s])))

    df_study.to_csv("{}/merged_visu_data.csv".format(EXPORT_PATH),
                    sep=";")


    condition_1 = [int(x) for x in df_study["ranking condition: 1"]]
    condition_2 = [int(x) for x in df_study["ranking condition: 2"]]
    condition_3 = [int(x) for x in df_study["ranking condition: 3"]]
    condition_4 = [int(x) for x in df_study["ranking condition: 4"]]

    samples = {"condition 1": condition_1,
               "condition 2": condition_2,
               "condition 3": condition_3,
               "condition 4": condition_4,
               }

    visualizations = {"condition 1": "sunburst",
                      "condition 2": "treemap",
                      "condition 3": "dendrogram",
                      "condition 4": "circlepacking",
                      }

    columns = ["participant"]
    data = {}
    for v in visualizations.values():
        columns.append(v)
    for i in range(0, len(samples["condition 1"])):
        data[i] = {"participant": i,
                   visualizations["condition 1"]: samples["condition 1"][i],
                   visualizations["condition 2"]: samples["condition 2"][i],
                   visualizations["condition 3"]: samples["condition 3"][i],
                   visualizations["condition 4"]: samples["condition 4"][i], }

    df_rankings = pd.DataFrame.from_dict(data=data,
                                         orient="index",
                                         columns=columns)

    df_rankings.to_csv("{}/rankings.csv".format(EXPORT_PATH),
                       sep=";")


    columns = ["visu 1", "visu 2", "first", "second"]
    data = {}
    for i in range(1, 5):

        for j in range(i + 1, 5):
            # if s1==s2:
            #    continue
            print("{}{}".format(i, j))
            s1 = "condition {}".format(i)
            s2 = "condition {}".format(j)

            data["{}{}".format(s1, s2)] = {"visu 1": visualizations[s1],
                                           "visu 2": visualizations[s2], }

            print("T-Test for {} and {}".format(visualizations[s1], visualizations[s2]))
            result = scipy.stats.ttest_rel(samples[s1],
                                           samples[s2],
                                           axis=0,
                                           nan_policy='raise',
                                           )
            print("statistic: {:,.8f}".format(result[0]))
            print("p-value: {:,.8f}".format(result[1]))

            measure = "t-test"
            stat = "{}_statistic".format(measure)
            p = "{}_p".format(measure)
            if stat not in columns:
                columns.append(stat)
            if p not in columns:
                columns.append(p)
            data["{}{}".format(s1, s2)][stat] = "{:,.8f}".format(result[0])
            data["{}{}".format(s1, s2)][p] = "{:,.8f}".format(result[1])



            # percentage

            first = 0
            second = 0
            for x in range(0, len(samples[s1])):
                if samples[s1][x] > samples[s2][x]:
                    second += 1
                elif samples[s1][x] < samples[s2][x]:
                    first += 1

            data["{}{}".format(s1, s2)]["first"] = "{:,.8f}".format(first / len(samples[s1]))
            data["{}{}".format(s1, s2)]["second"] = "{:,.8f}".format(second / len(samples[s1]))

    df_post_hoc = pd.DataFrame.from_dict(data=data,
                                         orient="index",
                                         columns=columns)

    df_post_hoc.to_csv("{}/post_hoc.csv".format(EXPORT_PATH),
                       sep=";")

    # Nemenyi

    print("Nemenyi post-hoc Test for {} and {}".format(visualizations[s1], visualizations[s2]))

    data = np.array([samples["condition 1"],
                     samples["condition 2"],
                     samples["condition 3"],
                     samples["condition 4"],
                     ])

    result = scikit_posthocs.posthoc_nemenyi_friedman(data.T)

    print("Nemenyi post-hoc test")
    print(result)

    ############### descriptive statistics ############

    columns = ["visualization", "R 1", "R 2", "R 3", "R 4", "rank sum", "average", "SD", "z score"]
    data = {}

    for s in samples.keys():
        R1 = 0
        R2 = 0
        R3 = 0
        R4 = 0
        sum = 0
        for value in samples[s]:
            sum += value
            if value == 1:
                R1 += 1
            elif value == 2:
                R2 += 1
            elif value == 3:
                R3 += 1
            elif value == 4:
                R4 += 1
            else:
                print("ERROR: value is {}".format(value))

        data[visualizations[s]] = {}
        data[visualizations[s]]["visualization"] = visualizations[s]
        data[visualizations[s]]["R 1"] = "{0:.0%}".format(R1 / len(samples[s]))
        data[visualizations[s]]["R 2"] = "{0:.0%}".format(R2 / len(samples[s]))
        data[visualizations[s]]["R 3"] = "{0:.0%}".format(R3 / len(samples[s]))
        data[visualizations[s]]["R 4"] = "{0:.0%}".format(R4 / len(samples[s]))
        data[visualizations[s]]["average"] = "{:,.2f}".format(statistics.mean(samples[s]))
        data[visualizations[s]]["rank sum"] = sum
        data[visualizations[s]]["SD"] = "{:,.2f}".format(statistics.stdev(samples[s]))
        data[visualizations[s]]["z score"] = statistics.mean(scipy.stats.zscore(samples[s]))

    df_sample = pd.DataFrame.from_dict(data=data,
                                       orient="index",
                                       columns=columns)

    df_sample.to_csv("{}/merged_visu_data_statistics.csv".format(EXPORT_PATH),
                     sep=";")

    result = scipy.stats.friedmanchisquare(condition_1,
                                           condition_2,
                                           condition_3,
                                           condition_4)

    print("Friedmann statistic: {:,.4f}".format(result[0]))
    print("Friedmann p: {:,.12f}".format(result[1]))

    questions = models.Question.objects.filter(participant__study__name__in=studies)

    columns = ["participant", "question", "answer"]
    data = {}

    ###  export open questions ###
    for q in questions:
        if "condition" not in q.question and q.answer:
            data[q.pk] = {"participant": q.participant.pk,
                          "question": q.question,
                          "answer": q.answer, }

    df_questions = pd.DataFrame.from_dict(columns=columns,
                                          orient="index",
                                          data=data, )

    df_questions.to_csv("{}/questions.csv".format(EXPORT_PATH),
                        sep=";")


    data = pd.DataFrame()
    for c in samples.keys():
        data[visualizations[c]] = [np.float64(x) for x in samples[c]]

    result = autorank(data, alpha=0.05, verbose=False)
    print(result)

    result = autorank(data, alpha=0.05, verbose=False, approach='bayesian')
    print(result)

    create_report(result)

    latex_table(result)


class Command(BaseCommand):
    help = 'Exports relations of construction app as csv files'

    def handle(self, *args, **kwargs):
        analyze_study("pilot_study")
        analyze_study("big5_study")
        summarize_studies(["pilot_study", "big5_study"])
