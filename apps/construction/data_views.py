import json

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseServerError

from apps.construction.studies import study_functions
from apps.construction import models


@login_required
def trees(request):
    """

    :param request:
    :return:
    """

    root_goals=models.Goal.objects.filter(parent_id=None).order_by("tree_id")

    trees = []
    for goal in root_goals:
        size=len(models.Goal.objects.filter(tree_id=goal.tree_id,
                                         discarded=False,))
        tree={"tree_id":goal.tree_id,
              "size":size,
              "root_goal":goal.title,
              "study": goal.study.name if goal.study else None,
              "is_example":goal.is_example,
              "discarded":goal.discarded,}

        trees.append(tree)


    context = {'trees': trees}

    return render(request, 'construction/trees.html', context)

@login_required
def participants(request):
    """

    :param request:
    :return:
    """

    participant_objects = models.Participant.objects.all().order_by("id")
    participants = []
    for p in participant_objects:
        if p.study.name != "prestudy" and p.finished == None:
            continue

        participants.append({})
        participants[-1]["id"] = p.id
        participants[-1]["age"] = p.age
        participants[-1]["gender"] = p.gender
        participants[-1]["semester"] = p.semester
        participants[-1]["subject"] = p.subject
        participants[-1]["degree"] = p.degree
        participants[-1]["created"] = p.created
        participants[-1]["finished"] = p.finished
        participants[-1]["condition"] = p.condition
        participants[-1]["study"] = p.study.name
        participants[-1]["study_sequence_position"] = p.study_sequence_position
        participants[-1]["additional_data"] = p.additional_data
        participants[-1]["exclude_from_analyses"] = p.exclude_from_analyses

        goals = models.Goal.objects.filter(participant=p)
        participants[-1]["goals"] = len(goals)

        personal_goals = models.PersonalGoal.objects.filter(participant=p)
        participants[-1]["personal_goals"] = len(personal_goals)

        items = models.Item.objects.filter(participant=p)
        participants[-1]["items"] = len(items)

        question = models.Question.objects.filter(participant=p)
        participants[-1]["questions"] = len(question)

    context = {'participants': participants}

    return render(request, 'construction/participants.html', context)

@login_required
def export_csv(request, study_id, export_name="default"):
    """
    Create csv export of study
    :param export_name:
    :param request:
    :param study_id:
    :return:
    """
    response = HttpResponse(
        content_type="text/csv",
    )
    response['Content-Disposition'] = 'attachment; filename="study_export.csv"'

    study = models.Study.objects.get(id=study_id)

    try:
        study_class = study_functions.create_study_by_classname(study.classname)
    except:
        print("class instantiation failed for {}".format(study.classname))
        return HttpResponseServerError("Study can not be found.")

    csv_dataframe = study_class.get_csv_dataframe(export_name)

    csv_dataframe.to_csv(path_or_buf=response, index=True, sep=";")

    return response

@login_required
def goal_list(request):
    """
    Display goals as list.
    :param request:
    :return:
    """
    goal_list = models.Goal.objects.all()
    context = {"goal_list": goal_list}

    return render(request, 'construction/goals.html', context)

@login_required
def explore_studies(request, study_id):
    """

    :param request:
    :return:
    """

    if study_id == 0:
        study_properties = models.Study.summarize(models.Study)

        prev_next = models.Study.get_previous_and_next_study()

        tree_data = models.Study.get_tree_data()


    else:

        study = models.Study.objects.get(id=study_id)

        prev_next = study.get_previous_and_next_study()

        study_properties = study.summarize()

        tree_data = study.get_tree_data()

    context = {
        'branching': list(study_properties[0]["nodes"]),
        'depths': list(study_properties[0]["branches"]),
        'tree_sizes': list(study_properties[0]["tree_sizes"]),
        'study_properties': study_properties,
        'tree_data': tree_data,
    }
    context.update(prev_next)
    return render(request, 'construction/explore_studies.html', context)

@login_required
def explore_trees(request, tree_id):
    """

    :param request:
    :return:
    """

    root_goal = models.Goal.objects.get(tree_id=tree_id, parent_id__isnull=True)
    tree = models.Goal.get_children(root_goal.id)
    study = root_goal.participant.study

    prev_next = study.get_previous_and_next_tree(tree_id)

    study_properties = study.summarize()

    tree_properties = models.Goal.get_tree_properties(tree_id)
    context = {
        'tree_properties': tree_properties,
        'study_properties': study_properties,
        'tree_id': tree_id,
        'tree': json.dumps(tree),
    }
    context.update(prev_next)
    return render(request, 'construction/explore_trees.html', context)
