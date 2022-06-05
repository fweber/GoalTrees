import copy

from django.core.management.base import BaseCommand
from apps.construction import models
import matplotlib.pyplot as plt
import csv
import pandas as pd
import numpy as np
import seaborn as sns
import os
import json
import datetime
import traceback
import sys
import scipy
from django.db.models import Max
import logging

EXPORT_PATH = "{}/data/hgs_data".format(os.getcwd())
PLOTS_PATH = "{}/plots".format(EXPORT_PATH)

VARIABLES = [
    'Depth',
    'Content Specificity ',
    'Time Specificity',
    'Hierarchy - High Level',
    'Hierarchy - Low Level',
    'Network Congruence',
    'Measurability',
    'Approach/ Avoidance Framing',
    'Process Focus',
    'Outcome Focus',
    'Immediate Actionability',
    'Estimated Effort',
    'Plannability',
    'Controllability',
    'Challenge',
    'Defined Subgoals',
    'Social Support',
    'Informational Support',
    'Instrumental Support',
    'Financial Affordance',
    'Visibility',
    'Time Availability',
    'Competence Adequacy',
    'Self-Congruence',
    'Value Congruence',
    'Importance',
    'Awareness',
    'Vitality',
    'Long-Term Utility',
    'Short-Term Utility',
    'Relative Utility',
    'Self- Improvement Utility',
    'Negative Utility',
]

GCQ_SUBSCALES = [{"scale":"Structural Subscale",
                  "dimensions":[
                        'Content Specificity ',
                        'Time Specificity',
                        'Hierarchy - High Level',
                        'Hierarchy - Low Level',
                        'Network Congruence',
                        'Measurability',]
                  },
                  {"scale":"Framing Subscale",
                  "dimensions":[
                        'Approach/ Avoidance Framing',
                        'Process Focus',
                        'Outcome Focus',
                      ]
                  },
                  {"scale":"Attainability Subscale",
                  "dimensions":[
                        'Immediate Actionability',
                        'Estimated Effort',
                        'Plannability',
                        'Controllability',
                        'Challenge',
                        'Defined Subgoals',
                  ]
                   },
                 {"scale": "Resources Availability Subscale",
                  "dimensions": [
                        'Social Support',
                        'Informational Support',
                        'Instrumental Support',
                        'Financial Affordance',
                        'Visibility',
                        'Time Availability',
                        'Competence Adequacy',
                  ]
                  },
                 {"scale": "Interestingness Subscale",
                  "dimensions": [
                        'Self-Congruence',
                        'Value Congruence',
                        'Importance',
                        'Awareness',
                        'Vitality',
                                  ]
                  },
                 {"scale": "Interestingness Subscale",
                  "dimensions": [
                        'Long-Term Utility',
                        'Short-Term Utility',
                        'Relative Utility',
                        'Self- Improvement Utility',
                        'Negative Utility',
                ]
            }
        ]
def extract_participants():
    """Extracts demographic data"""

    print("Extracting participants from DB...")
    participants = models.Participant.objects.filter(study__name="hgs_study",
                                                     exclude_from_analyses=False,
                                                     ).exclude(finished=None)
    print("Found {} complete participants.".format(len(participants)))
    data = {}
    columns = ["age", "gender", "subject", "semester", "duration", "screen_size", "operating_system",
               "browser_language"]

    for p in participants:
        duration = "%.2f" % ((p.finished - p.created).total_seconds() / 60)
        data[p.pk] = [p.age,
                      p.gender,
                      p.subject,
                      int(p.semester) if p.semester else None,
                      duration,
                      p.screen_size,
                      p.operating_system,
                      p.browser_language,
                      ]
    df_participants = pd.DataFrame.from_dict(data=data,
                                             orient="index",
                                             columns=columns)

    df_participants.to_csv("{}/participants.csv".format(EXPORT_PATH),
                           sep=";")

    return df_participants


def extract_personal_goals():
    """Extracts personal goal data"""
    print("Extracting personal goals from DB...")
    participants = models.Participant.objects.filter(study__name="hgs_study",
                                                     exclude_from_analyses=False,
                                                     ).exclude(finished=None)

    data = {}
    columns = ["participant_id", "goal_id", "goal"]
    gcq = models.Item.get_gcq(n_items=2)
    for item in gcq:
        columns.append(item["code"])
    for p in participants:
        personal_goals = models.PersonalGoal.objects.filter(participant=p)
        for pg in personal_goals:

            data[pg.pk] = [p.id, "pg_{}".format(pg.pk), pg.name]
            for c in columns:
                if c in ["participant_id", "goal_id", "goal"]:
                    continue
                items = models.Item.objects.filter(participant=p,
                                                   code=c,
                                                   personal_goal=pg, )
                if len(items) == 1:
                    data[pg.pk].append(items[0].given_answer)
                elif len(items) == 0:
                    data[pg.pk].append(None)
                elif len(items) == 2:
                    data[pg.pk].append([items[0].given_answer, items[1].given_answer])
                else:
                    print("Found {} items for {}!".format(len(items), items[0].code))

    df_goals = pd.DataFrame.from_dict(data=data,
                                      orient="index",
                                      columns=columns)

    df_goals.to_csv("{}/personal_goals.csv".format(EXPORT_PATH),
                    sep=";")
    return df_goals


def extract_goals():
    """Extracts goal data"""
    print("Extracting goals from DB...")
    participants = models.Participant.objects.filter(study__name="hgs_study",
                                                     exclude_from_analyses=False,
                                                     ).exclude(finished=None)

    data = {}
    columns = ["participant_id", "goal_id", "goal", "tree_id", "depth"]
    gcq = models.Item.get_gcq(n_items=2)
    for item in gcq:
        columns.append(item["code"])
    for p in participants:
        goals = models.Goal.objects.filter(participant=p)
        for g in goals:

            data[g.pk] = [p.id, "g_{}".format(g.pk), g.title, g.tree_id, g.get_depth()]
            for c in columns:
                if c in ["participant_id", "goal_id", "goal", "tree_id", "depth"]:
                    continue
                items = models.Item.objects.filter(participant=p,
                                                   code=c,
                                                   goal=g, )
                if len(items) == 1:
                    data[g.pk].append(items[0].given_answer)
                elif len(items) == 0:
                    data[g.pk].append(None)
                elif len(items) == 2:
                    data[g.pk].append([items[0].given_answer, items[1].given_answer])
                else:
                    print("Found {} items for {}!".format(len(items), items[0].code))

    df_goals = pd.DataFrame.from_dict(data=data,
                                      orient="index",
                                      columns=columns)
    print("Found {} valid goals.".format(len(df_goals)))

    df_goals.to_csv("{}/goals.csv".format(EXPORT_PATH),
                    sep=";")
    return df_goals


def analyze_pre_post():
    """Extracts demographic data"""
    print("Calculating pre- post comparison...")
    participants = models.Participant.objects.filter(study__name="hgs_study",
                                                     exclude_from_analyses=False,
                                                     ).exclude(finished=None)

    data = {}
    columns = ["participant_id", "goal_id", "personal_goal_id", "goal"]
    gcq = models.Item.get_gcq(n_items=1)
    for item in gcq:
        columns.append("pre_{}".format(item["code"]))
        columns.append("post_{}".format(item["code"]))
    for p in participants:
        personal_goals = models.PersonalGoal.objects.filter(participant=p)

        for pg in personal_goals:
            goals = models.Goal.objects.filter(participant=p,
                                               title=pg.name, )
            if len(goals) == 1:
                g = goals[0]
            else:
                print("N goals = {}".format(len(goals)))
                continue

            data[g.pk] = [p.pk, g.pk, pg.pk, g.title]
            for c in gcq:

                # append pre value(s)
                pg_items = models.Item.objects.filter(participant=p,
                                                      code=c,
                                                      personal_goal=pg, )
                if len(pg_items) == 1:
                    data[g.pk].append(pg_items[0].given_answer)
                elif len(pg_items) == 0:
                    data[g.pk].append(None)
                elif len(pg_items) == 2:
                    data[g.pk].append([pg_items[0].given_answer, pg_items[1].given_answer])
                else:
                    print("Found {} items for personal goal {}!".format(len(pg_items), pg_items[0].code))

                # append post value(s)
                g_items = models.Item.objects.filter(participant=p,
                                                     code=c,
                                                     goal=g, )
                if len(g_items) == 1:
                    data[g.pk].append(g_items[0].given_answer)
                elif len(g_items) == 0:
                    data[g.pk].append(None)
                elif len(g_items) == 2:
                    data[g.pk].append([g_items[0].given_answer, g_items[1].given_answer])
                else:
                    print("Found {} items for personal goal {}!".format(len(g_items), g_items[0].code))

    print("columns: {}".format(len(columns)))
    print(columns)
    print("keys: {}".format(len(data[list(data.keys())[0]])))
    print(data[list(data.keys())[0]])
    df_pre_post = pd.DataFrame.from_dict(data=data,
                                         orient="index",
                                         columns=columns)

    df_pre_post.to_csv("{}/pre_post.csv".format(EXPORT_PATH),
                       sep=";")
    return df_pre_post


def extract_items():
    """Extracts all items"""
    print("Extracting items from DB...")
    participants = models.Participant.objects.filter(study__name="hgs_study",
                                                     exclude_from_analyses=False,
                                                     ).exclude(finished=None)

    data = {}
    columns = ["item_id",
               "questionnaire",
               "code",
               "text",
               "latent_variable",
               "answers",
               "participant",
               "created",
               "given_answer",
               "reverse_coded",
               "personal_goal",
               "goal_id",
               "goal",
               ]

    for p in participants:
        items = models.Item.objects.filter(participant=p)
        for i in items:
            data[i.pk] = [i.id,
                          i.questionnaire,
                          i.code,
                          i.text,
                          i.latent_variable,
                          i.answers,
                          i.participant.pk,
                          i.created,
                          i.given_answer,
                          i.reverse_coded,
                          i.personal_goal.pk if i.personal_goal else None,
                          i.goal.pk if i.goal else None,
                          i.goal.title if i.goal else None,
                          ]

    df_items = pd.DataFrame.from_dict(data=data,
                                      orient="index",
                                      columns=columns)

    df_items.to_csv("{}/items.csv".format(EXPORT_PATH),
                    sep=";")
    return df_items


def create_gcq_matrix(df_goals):
    """evaluates gcq answers and calculates a score per gcq dimension"""
    print("Calculating GCQ matrix...")
    gcq_data = models.Item.get_gcq(n_items=2)

    gcq_dictionary = {}
    gcq_items = []
    for gcq_item in gcq_data:

        if gcq_item["latent_variable"] not in gcq_dictionary.keys():
            gcq_dictionary[gcq_item["latent_variable"]] = [{"code": gcq_item["code"],
                                                            "reverse_coded": gcq_item["reverse_coded"]}]
        else:
            gcq_dictionary[gcq_item["latent_variable"]].append({"code": gcq_item["code"],
                                                                "reverse_coded": gcq_item["reverse_coded"]})

        gcq_items.append("{}_{}_reverse_corrected".format(gcq_item["latent_variable"], gcq_item["code"]))

    print(gcq_dictionary.keys())

    data = {}
    columns = ["participant_id", "goal_id", "goal", "tree_id", "Depth"]
    columns.extend(gcq_dictionary.keys())
    columns.extend(gcq_items)

    for index, row in df_goals.iterrows():

        if row["gcq_1"] == None:
            print("NULL ROW")
            continue

        data[row["goal_id"]] = {"participant_id": row["participant_id"],
                                "goal_id": row["goal_id"],
                                "goal": row["goal"],
                                "tree_id": row["tree_id"],
                                "Depth": row["depth"]}

        for dimension in gcq_dictionary.keys():

            # if item not in row keys: skip
            print("items for {}: {}".format(dimension, len(gcq_dictionary[dimension])))

            try:

                if gcq_dictionary[dimension][0]["reverse_coded"] == True:
                    print("dimension {} first item {} is reverse coded".format(dimension,
                                                                               gcq_dictionary[dimension][0]["code"]))
                    first = 1 - float(row[gcq_dictionary[dimension][0]["code"]])
                elif gcq_dictionary[dimension][0]["reverse_coded"] == False:
                    print("dimension {} first item {} is NOT reverse coded".format(dimension,
                                                                                   gcq_dictionary[dimension][0][
                                                                                       "code"]))
                    first = float(row[gcq_dictionary[dimension][0]["code"]])
                else:
                    print("Unknown value for reverse_coded (boolean expected): {}".format(
                        gcq_dictionary[dimension][0]["reverse_coded"]))
            except Exception as e:
                print("error for first")
                if type(row[gcq_dictionary[dimension][0]["code"]]) == list:
                    print("is list")
                    if len(row[gcq_dictionary[dimension][0]["code"]]) == 2:
                        print("length 2")
                        if row[gcq_dictionary[dimension][0]["code"]][0] == row[gcq_dictionary[dimension][0]["code"]][1]:
                            print("both equal")
                            first = float(row[gcq_dictionary[dimension][0]["code"]][0])
                            print("FIXED")

            try:
                print("dimension: {}".format(dimension))
                print("gcq_dictionary[dimension]: {}".format(gcq_dictionary[dimension]))
                print("second item: {}".format(gcq_dictionary[dimension][1]["code"]))
                print("type of row: {}".format(type(row)))
                try:
                    score = row[gcq_dictionary[dimension][1]["code"]]
                    print("second score is: {}".format(score))
                except:
                    print("no score in row")

                if gcq_dictionary[dimension][1]["reverse_coded"] == True:
                    print("dimension {} second item {} is reverse coded".format(dimension,
                                                                                gcq_dictionary[dimension][1]["code"]))
                    second = 1 - float(row[gcq_dictionary[dimension][1]["code"]])
                elif gcq_dictionary[dimension][1]["reverse_coded"] == False:
                    print("dimension {} second item {} is NOT reverse coded".format(dimension,
                                                                                    gcq_dictionary[dimension][1][
                                                                                        "code"]))
                    second = float(row[gcq_dictionary[dimension][1]["code"]])
                else:
                    print("Unknown value for reverse_coded (boolean expected): {}".format(
                        gcq_dictionary[dimension][0]["reverse_coded"]))

            except Exception as e:
                print("error for second")
                if type(row[gcq_dictionary[dimension][1]["code"]]) == list:
                    print("is list")
                    if len(row[gcq_dictionary[dimension][1]["code"]]) == 2:
                        print("length 2")
                        if row[gcq_dictionary[dimension][1]["code"]][0] == row[gcq_dictionary[dimension][1]["code"]][1]:
                            print("both equal")
                            second = float(row[gcq_dictionary[dimension][1]["code"]][0])
                            print("FIXED")

            # write average score for factor
            data[row["goal_id"]][dimension] = (first + second) / 2

            firstcode = gcq_dictionary[dimension][0]["code"]
            secondcode = gcq_dictionary[dimension][1]["code"]

            data[row["goal_id"]]["{}_{}_reverse_corrected".format(dimension, firstcode)] = first
            data[row["goal_id"]]["{}_{}_reverse_corrected".format(dimension, secondcode)] = second

    df_gcq_matrix = pd.DataFrame.from_dict(data=data,
                                           orient="index",
                                           columns=columns)

    df_gcq_matrix.to_csv("{}/gcq_matrix.csv".format(EXPORT_PATH),
                         sep=";")

    return df_gcq_matrix


def plot_correlations(df_gcq_matrix):
    print("Creating correlation plots...")

    df_gcq_matrix.describe()

    plt.clf()

    sns_plot = sns.boxplot(x="variable",
                           y="value",
                           data=pd.melt(df_gcq_matrix[VARIABLES]))

    plt.xticks(rotation=90)

    sns_plot.set(title='Distributions of Goal Characteristics')

    fig = sns_plot.get_figure()
    plt.tight_layout()

    fig.savefig("{}/ALL_characteristics.png".format(PLOTS_PATH), bbox_inches="tight")
    fig.clf()

    for i in range(0, len(VARIABLES)):
        x = VARIABLES[i]
        for j in range(i + 1, len(VARIABLES)):
            y = VARIABLES[j]

            xlabel = x
            ylabel = y
            xlabel = xlabel.replace("/", "").replace(" ", "")
            ylabel = ylabel.replace("/", "").replace(" ", "")

            plt.figure(figsize=(6, 6))

            sns_plot = sns.scatterplot(data=df_gcq_matrix,
                                       x=x,
                                       y=y,
                                       )

            fig = sns_plot.get_figure()

            fig.savefig("{}/scatterplot_{}_{}.png".format(PLOTS_PATH, xlabel, ylabel))
            fig.clf()

        sns_plot = sns.violinplot(data=df_gcq_matrix,
                                  x=x,
                                  cut=0,
                                  )

        fig = sns_plot.get_figure()

        fig.savefig("{}/violinplot_{}.png".format(PLOTS_PATH, xlabel), bbox_inches="tight", )

        fig.clf()


def plot_scatterplot_matrices(df_gcq_matrix=None, ):
    if not df_gcq_matrix:
        df_gcq_matrix = pd.read_csv(filepath_or_buffer="{}/gcq_matrix.csv".format(EXPORT_PATH),
                                    sep=";")

    df_gcq_matrix[VARIABLES].describe()


    for v in VARIABLES:
        variables=copy.deepcopy(VARIABLES)
        variables.remove(v)
        i=1
        for x in range(0, len(variables), 4):
            if x + 4 > len(variables):
                variables_plot = variables[x:]
            else:
                variables_plot = variables[x:x + 4]
            variables_plot = [v]+variables_plot
            dataset = df_gcq_matrix[variables_plot]
            sns_plot = sns.PairGrid(dataset)
            sns_plot.map_diag(plt.hist)
            sns_plot.map_upper(plt.scatter)
            sns_plot.map_lower(sns.kdeplot)

            fig = sns_plot.fig

            fig.savefig("{}/pdfs/correlations_{}_{}.pdf".format(PLOTS_PATH, v.replace("/"," ").replace(" ","")
                                                                .replace("-",""), i),
                        bbox_inches="tight",
                        dpi=75,
                        )
            fig.savefig(
                "{}/pngs/correlations_{}_{}.png".format(PLOTS_PATH, v.replace("/", " ").replace(" ", "").replace("-", ""),
                                                   i), bbox_inches="tight", )
            i += 1

            fig.clf()

def create_latex(header=False):
    if header:
        print("\\documentclass{article}")
        print("")
        print("\\usepackage){graphicx}")
        print("")
        print("\\begin{document}")
        print("")
    even=0
    for variable in VARIABLES:
        variable_original=variable
        variable_original=variable_original.replace("/","")
        variable = variable.replace("/", " ").replace(" ", "").replace("-", "")
        for i in range(1,9):
            even += 1
            even = even % 2

            if even == 0:
                print("\\begin{figure}[b]")
            else:
                print("\\begin{figure}[t]")
            print("\\centering")
            print("\\includegraphics[width=10cm]{{Figures/Appendix_figures/correlations_{}_{}.pdf}}".format(variable,i))
            print("\\caption{{Correlations and KDE for variable {} matrix {}.}}".format(variable_original,i))
            print("\\label{{fig:Corr_and_KDE_{}_{}}}".format(variable,i))
            print("\\end{figure}")
            print("")

            if even == 0:
                print("\\clearpage")
                print("")
    if header:
        print("\\end{document}")

def plot_violinplot_matrix(df_gcq_matrix=None,):

    if not df_gcq_matrix:
        df_gcq_matrix = pd.read_csv(filepath_or_buffer="{}/gcq_matrix.csv".format(EXPORT_PATH),
                                    sep=";")


    df_gcq_matrix[VARIABLES]

    for scale in GCQ_SUBSCALES:
        name=scale["scale"]
        dimensions=scale["dimensions"]

        fig = plt.figure(figsize=(len(dimensions)*2, 6))
        gs = fig.add_gridspec(1, len(dimensions))

        i = 0
        for dimension in dimensions:


            ax = fig.add_subplot(gs[0, i])
            sns.violinplot(data=df_gcq_matrix[dimension])
            ax.set_xlabel(dimension)

            i += 1
        fig.tight_layout()

        fig.savefig("{}/violinplots_{}.png".format(PLOTS_PATH, name))

        fig.clf()

    # ALLINONE

    fig = plt.figure(figsize=(18, 18))
    gs = fig.add_gridspec(6, 7)

    j = 0
    for scale in GCQ_SUBSCALES:
        name=scale["scale"]
        dimensions=scale["dimensions"]

        i = 0
        for dimension in dimensions:


            ax = fig.add_subplot(gs[j, i])
            sns.violinplot(data=df_gcq_matrix[dimension])
            ax.set_xlabel(dimension)

            i += 1
        j += 1
    fig.tight_layout()

    fig.savefig("{}/violinplots_GCQ.png".format(PLOTS_PATH))

    fig.clf()


def plot_correlation_heatmap(df_gcq_matrix):
    """
    Creates a correlation matrix and saves it as png plot.
    """
    print("Saving heatmap plots as .png files... ")

    df_corr = df_gcq_matrix[VARIABLES].corr()

    df_corr.to_csv(path_or_buf="{}/correlation_matrix.csv".format(EXPORT_PATH), sep=";")
    plot_correlation_heatmap(df_corr)

    plt.clf()

    fontsize = 12

    sns.set(style='white')

    mask = np.zeros_like(df_corr, dtype=np.bool)
    mask[np.triu_indices_from(mask)] = True

    f, ax = plt.subplots(figsize=(20, 20))
    cmap = sns.diverging_palette(220, 10, as_cmap=True)

    akws = {"size": fontsize, }

    sns.heatmap(df_corr,
                mask=mask,
                cmap=cmap,
                vmax=0.75,
                vmin=-0.75,
                center=0,
                square=True,
                linewidths=.5,
                cbar_kws={"shrink": .5},
                annot=True,
                annot_kws=akws,
                fmt=".2f",
                xticklabels=True,
                yticklabels=True,
                )

    ax.set_title('Goal Characteristics Correlation Matrix',
                 size=20,
                 )

    plt.xticks(rotation=90,
               horizontalalignment='right',
               rotation_mode='anchor',
               size=fontsize,
               )
    plt.yticks(rotation=0,
               size=fontsize,
               )
    plt.tight_layout()

    plt.savefig("{}/correlation_heatmap_plot.png".format(PLOTS_PATH), bbox_inches="tight")
    plt.clf()


def extract_large_tree_data(size):
    """Extracts all trees with more than n goals and saves them in a csv file.
    @param size : Minimum size of trees to be included
    """
    print("Extracting large tree data...")
    max_tree_id = models.Goal.objects.all().aggregate(Max('tree_id'))['tree_id__max']

    data = {'tree_id': [], "size": []}

    for i in range(max_tree_id):
        goals = models.Goal.objects.filter(tree_id=i,
                                           discarded=False, )
        if len(goals) > size:
            data["tree_id"].append(i)
            data['size'].append(len(goals))

    df_large_trees = pd.DataFrame(columns=['tree_id', 'size'],
                                  data=data)
    df_large_trees.set_index('tree_id')
    df_large_trees.to_csv(path_or_buf="{}/large_trees.csv".format(EXPORT_PATH), sep=";")
    print("Large tree data was saved as csv.")


def create_descriptive_plots_hgs_study():
    """Create plots for descriptive statistics."""
    print("Create descriptive plots for HGS study...")
    max_tree_id = models.Goal.objects.all().aggregate(Max('tree_id'))['tree_id__max']

    hgs_trees = []
    for i in range(1, max_tree_id):
        tree_goals = models.Goal.objects.filter(tree_id=i,
                                                discarded=False,
                                                is_example=False,
                                                participant__study__name="hgs_study", )
        if len(tree_goals) > 2:
            hgs_trees.append(i)

    ### DEPTH ###
    size_data = {}
    valid_hgs = 0
    for i in hgs_trees:
        goals = models.Goal.objects.filter(tree_id=i,
                                           discarded=False,
                                           is_example=False,
                                           participant__study__name="hgs_study", )

        if len(goals) < 2:
            continue
        else:
            size = len(goals)
            valid_hgs += 1
            if size in size_data.keys():
                size_data[size] += 1
            else:
                size_data[size] = 1

    new_data = {"size": [],
                "trees": [],
                }

    for i in size_data.keys():
        new_data["size"].append(i)
        new_data["trees"].append(size_data[i])

    ax = sns.barplot(x="size",
                     y="trees",
                     data=new_data,
                     color="cornflowerblue",
                     )

    xlabel = "size"
    ylabel = "n trees"

    ax.set(xlabel=xlabel, ylabel=ylabel)
    ax.set(title='number of HGS per size (n={})'.format(valid_hgs))

    plt.savefig("{}/HGS_sizes.png".format(PLOTS_PATH), bbox_inches="tight")
    plt.clf()

    ### BRANCHING ###

    branching_data = {}
    goals = models.Goal.objects.filter(discarded=False,
                                       is_example=False,
                                       participant__study__name="hgs_study", )
    counter = {}
    non_leaves = 0
    for g in goals:
        descendants = models.Goal.objects.filter(parent_id=g.id)
        branching = len(descendants)
        if branching > 0:
            non_leaves += 1
            if branching in counter.keys():
                counter[branching] += 1
            else:
                counter[branching] = 1

    branching_data = {"branching_factor": [],
                      "nodes": [],
                      }
    keylist = counter.keys()
    for i in sorted(keylist):
        branching_data["branching_factor"].append(i)
        branching_data["nodes"].append(counter[i])

    plt.clf()

    ax = sns.barplot(x="branching_factor",
                     y="nodes",
                     data=branching_data,
                     color="cornflowerblue",
                     )

    xlabel = "branching"
    ylabel = "n nodes"

    ax.set(xlabel=xlabel, ylabel=ylabel)
    ax.set(title='number of branches per non-leaf goal (n={})'.format(non_leaves))

    plt.savefig("{}/HGS_branching.png".format(PLOTS_PATH),
                bbox_inches="tight")
    plt.clf()

    ### DEPTH ###

    counter = {}
    valid_hgs = 0
    for t_id in hgs_trees:
        tree_properties = models.Goal.get_tree_properties(t_id)
        for p in tree_properties:
            if p["name"] == "maximal depth":
                depth = p["value"]
                break

        if depth > 0:
            valid_hgs += 1
            if depth in counter.keys():
                counter[depth] += 1
            else:
                counter[depth] = 1

    depth_data = {"depth": [],
                  "n": [],
                  }
    keylist = counter.keys()
    for i in sorted(keylist):
        depth_data["depth"].append(i)
        depth_data["n"].append(counter[i])

    plt.clf()

    ax = sns.barplot(x="depth",
                     y="n",
                     data=depth_data,
                     color="cornflowerblue", )

    xlabel = "depth"
    ylabel = "n trees"

    ax.set(xlabel=xlabel, ylabel=ylabel)
    ax.set(title='number of HGS per depth (n={})'.format(valid_hgs))

    plt.savefig("{}/HGS_depths.png".format(PLOTS_PATH), bbox_inches="tight")
    plt.clf()


def create_descriptive_plots():
    """Create plots for descriptive statistics."""
    print("Create descriptive plots...")
    max_tree_id = models.Goal.objects.all().aggregate(Max('tree_id'))['tree_id__max']

    hgs_trees = []
    for i in range(1, max_tree_id):
        goals = models.Goal.objects.filter(tree_id=i,
                                           discarded=False,
                                           is_example=False,
                                           participant__exclude_from_analyses=False)
        if len(goals) > 2:
            hgs_trees.append(i)

    ### SIZES ###

    size_data = {}
    valid_hgs = 0
    for i in hgs_trees:
        goals = models.Goal.objects.filter(tree_id=i,
                                           discarded=False,
                                           is_example=False,
                                           participant__exclude_from_analyses=False, )

        if len(goals) < 2:
            continue
        else:
            valid_hgs += 1
            size = len(goals)
            if size in size_data.keys():
                size_data[size] += 1
            else:
                size_data[size] = 1

    new_data = {"size": [],
                "trees": [],
                }

    for i in size_data.keys():
        new_data["size"].append(i)
        new_data["trees"].append(size_data[i])

    plt.clf()

    ax = sns.barplot(x="size",
                     y="trees",
                     data=new_data,
                     color="cornflowerblue",
                     )

    xlabel = "size"
    ylabel = "n trees"

    ax.set(xlabel=xlabel, ylabel=ylabel)
    ax.set(title='number of HGS per size (n={})'.format(valid_hgs))

    plt.savefig("{}/ALL_sizes.png".format(PLOTS_PATH), bbox_inches="tight")
    plt.clf()

    ### BRANCHING ###

    goals = models.Goal.objects.filter(discarded=False,
                                       is_example=False,
                                       participant__exclude_from_analyses=False,
                                       )
    counter = {}
    nodes = 0
    for g in goals:
        descendants = models.Goal.objects.filter(parent_id=g.id)
        branching = len(descendants)
        if branching > 0:
            nodes += 1
            if branching in counter.keys():
                counter[branching] += 1
            else:
                counter[branching] = 1

    branching_data = {"branching_factor": [],
                      "nodes": [],
                      }

    keylist = counter.keys()
    for i in sorted(keylist):
        branching_data["branching_factor"].append(i)
        branching_data["nodes"].append(counter[i])

    plt.clf()

    ax = sns.barplot(x="branching_factor",
                     y="nodes",
                     data=branching_data,
                     color="cornflowerblue",
                     )

    xlabel = "branching"
    ylabel = "n nodes"

    ax.set(xlabel=xlabel, ylabel=ylabel)
    ax.set(title='branching per non-leaf goal (n={})'.format(nodes))

    plt.savefig("{}/ALL_branching.png".format(PLOTS_PATH), bbox_inches="tight")
    plt.clf()

    ### DEPTH ###

    counter = {}
    valid_hgs = 0
    for t_id in hgs_trees:
        tree_properties = models.Goal.get_tree_properties(t_id)
        for p in tree_properties:
            if p["name"] == "maximal depth":
                depth = p["value"]
                break

        if depth > 0:
            valid_hgs += 1
            if depth in counter.keys():
                counter[depth] += 1
            else:
                counter[depth] = 1

    depth_data = {"depth": [],
                  "n": [],
                  }
    keylist = counter.keys()
    for i in sorted(keylist):
        depth_data["depth"].append(i)
        depth_data["n"].append(counter[i])

    plt.clf()

    ax = sns.barplot(x="depth",
                     y="n",
                     data=depth_data,
                     color="cornflowerblue", )

    xlabel = "depth"
    ylabel = "n trees"

    ax.set(xlabel=xlabel, ylabel=ylabel)
    ax.set(title='number of HGS per depth (n={})'.format(valid_hgs))

    plt.savefig("{}/ALL_depths.png".format(PLOTS_PATH), bbox_inches="tight")
    plt.clf()


def check_attention_checks(studyname="hgs_study"):
    """
    Iterates over participants and checks if attention checks were answered correctly.
    Set participant.exclude_from_analyses to True if checks were not passed.
    @return: List of participants who did not pass.
    """
    print("Filtering out participants based on attention_check...")
    participants = models.Participant.objects.filter(study__name=studyname,
                                                     )
    lst_failed = []
    check_items = models.Item.get_check_items(language="de")

    items = models.Item.objects.filter(participant__in=participants,
                               latent_variable="check",)

    for p in participants:
        my_items=items.filter(participant=p)
        if len(my_items)== 0:
            continue
        failed = 0
        for i in my_items:
            if check_items[0] in i.text:
                if float(i.given_answer)< 0.4 or float(i.given_answer)> 0.6:
                    failed += 1
            elif check_items[1] in i.text:
                if float(i.given_answer)< 0.9:
                    failed += 1
            elif check_items[2] in i.text:
                if float(i.given_answer)> 0.1:
                    failed += 1

        score=(len(my_items)-failed)/len(my_items)
        if score < 0.7:
            lst_failed.append({"id":p.id,
                              "score":score,
                               "n_items":len(my_items),
                              "p_object":p,
                               })

    print("{} participants failed".format(len(lst_failed)))
    for p in lst_failed:
        print("p {} score: {} of: {}".format(p["id"], p["score"], p["n_items"]))
        participant = p["p_object"]
        participant.exclude_from_analyses=True
        participant.save()
    print("Participants were excluded from further analyses!")
    return lst_failed

class Command(BaseCommand):
    help = 'Exports relations of construction app as csv files'

    def handle(self, *args, **kwargs):
        #plot_violinplot_matrix()
        failed=check_attention_checks()
        #print(failed)
        sys.exit()

        create_latex()
        sys.exit()

        plot_violinplot_matrix()
        sys.exit()

        plot_scatterplot_matrices()
        sys.exit()

        create_latex()
        sys.exit()







        df_goals = extract_goals()
        df_gcq_matrix = create_gcq_matrix(df_goals)

        plot_correlations(df_gcq_matrix)
        plot_correlation_heatmap(df_gcq_matrix)

        create_descriptive_plots_hgs_study()
        create_descriptive_plots()

        extract_large_tree_data(12)

        df_participants = extract_participants()
        df_goals = extract_goals()
        df_items = extract_items()
        df_personal_goals = extract_personal_goals()

        # analyze_pre_post()



        print("Analyses completed!")
