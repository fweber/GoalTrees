import json
import statistics
import random

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse, HttpResponseServerError
from django.utils import timezone
from django.views.decorators.clickjacking import xframe_options_exempt

from django.conf import settings
from django.utils import translation
from apps.construction.studies import study_functions
from apps.construction import models


@xframe_options_exempt
def welcome(request):
    """
    Welcome page is returned.
    :param request:
    :return:
    """
    study = models.Study.get_current_study(request)
    study_context = models.StudyContext.get_context(study=study, view="welcome")

    context = {}
    context["key"] = "value"
    context.update(study_context)
    return render(request, 'construction/welcome.html', context)


def consent(request):
    """
    Consent page is returned.
    :param request:
    :return:
    """
    study = models.Study.get_current_study(request)
    study_context = models.StudyContext.get_context(study=study, view="consent")

    context = {}
    context["key"] = "value"
    context.update(study_context)
    return render(request, 'construction/consent.html', context)


def userdata(request):
    """
    Participant registration page is returned.
    :param request:
    :return:
    """
    study = models.Study.get_current_study(request)
    study_context = models.StudyContext.get_context(study=study, view="userdata")

    context = {
        "title": "Anmeldung",
        "introduction": "<p> Die folgenden Angaben sind freiwillig und optional. </p>",
        "ask_english_proficiency": False,
        "required": True,   # required inputs as default
        "key": "value",
    }
    context.update(study_context)
    return render(request, 'construction/userdata.html', context)


@xframe_options_exempt
def example_tree(request):
    """
    Html showing an example tree is returned.
    :param request:
    :return:
    """
    study = models.Study.get_current_study(request)
    study_context = models.StudyContext.get_context(study=study, view="example_tree")

    #tree_id = 2
    #root_goal = models.Goal.objects.get(tree_id=tree_id,parent_id__isnull=True)
    #tree = models.Goal.get_children(root_goal.id)
    condition = models.Participant.get_current_participant(request).condition
    #print(tree)
    #print("condition is {}".format(condition))
    context = {#'tree_id': tree_id,
               #'tree': json.dumps(tree),
               'condition': models.Participant.get_current_participant(request).condition,
               }
    context.update(study_context)
    return render(request, 'construction/example_tree.html', context)


def instructions(request, view="instructions"):
    """
    Html giving instructions is returned.
    :param view: name of view used in context
    :param request:
    :return:
    """
    study = models.Study.get_current_study(request)
    study_context = models.StudyContext.get_context(study=study, view=view)

    context = {}
    context.update(study_context)
    return render(request, 'construction/instructions.html', context)


@xframe_options_exempt
def goal_definition(request):
    """
    HTML defining root tree goal
    :param request:
    :return:
    """
    study = models.Study.get_current_study(request)
    study_context = models.StudyContext.get_context(study=study, view="goal_definition")

    context = {
        "max_title_length": 20,
    }
    context.update(study_context)
    return render(request, 'construction/goal_definition.html', context)


@xframe_options_exempt
def tree_construction(request, condition=0, view="tree_construction"):
    """
    Html allowing tree generation.
    :param view: determines the view of the context
    :param condition: sets the condition of the tree
    :param request:
    :return:
    """
    participant = models.Participant.get_current_participant(request)

    study = models.Study.get_current_study(request)
    # gets the example tree
    study_context = models.StudyContext.get_context(study=study, view=view)

    if len(models.Goal.objects.filter(participant=participant, discarded=False)) == 0:
        models.Goal.create_new_tree(request)

    tree_id = models.Goal.get_current_tree_id(request)
    tree = models.Goal.get_tree(tree_id)
    number_of_trees = len(models.Goal.objects.filter(participant=participant, parent_id=0, discarded=False))

    if not condition:
        condition = models.Participant.get_current_participant(request).condition

    context = {}
    context['condition'] = str(condition)
    context['view'] = view
    context['tree_id'] = tree_id
    context['tree'] = json.dumps(tree)
    context["number_of_trees"] = number_of_trees
    context["goals"] = models.Goal.get_tree_goals(tree_id).order_by("title")
    context["max_title_length"] = 20
    context["description_enabled"] = True
    context.update(study_context)

    return render(request, 'construction/tree_construction.html', context)


def gcq(request):
    """
    Landing Page
    :param request:
    :return:
    """
    items = models.Item.get_gcq_items()
    goal = models.Goal.get_gcq_goal(request)
    context = {
        "title": goal,
        "introduction": "Bewerte inwiefern die folgenden Aussagen auf Dein Ziel <em>{}</em> zutreffen.".format(goal),
        "answers": items[0].get("answers"),
        "items": items,
        "questionnaire": "gcq"
    }
    return render(request, 'construction/gcq.html', context)


@xframe_options_exempt
def explore_gcq(request, tree_id=None):
    """
    HTML with statistics of gcq
    :param request:
    :return:
    """
    participant = models.Participant.get_current_participant(request)
    study = models.Study.get_current_study(request)
    study_context = models.StudyContext.get_context(study=study, view="explore_gcq")

    if tree_id is None:
        tree_id = models.Goal.get_current_tree_id(request)
    tree = models.Goal.get_tree(tree_id)

    items = models.Item.get_gcq_short_items()

    # get first latent variable
    latent_variable = items[0]["latent_variable"]

    # collect all latent variables ordered by created to preserve item order
    latent_variables = []
    latent_variables_descriptions = []
    for item in items:
        if item["latent_variable"] not in latent_variables:
            latent_variables.append(item["latent_variable"])
            latent_variables_descriptions.append(item["latent_variable_description"])

    # collect goal scores of each latent variable
    latent_scores = []
    for index in range(len(latent_variables)):
        latent_scores.append({
            "latent_variable": latent_variables[index],
            "latent_variable_description": latent_variables_descriptions[index],
            "score_goals": models.Item.get_goal_scores(participant, latent_variables[index], tree_id, 0, 1)
        })

    # collect all user trees / root goals
    root_goals = models.Goal.objects.filter(participant=participant, parent_id__isnull=True, replicated_tree_id__isnull=True)

    context = {
        "root_goals": root_goals,
        "latent_variables": latent_variables,
        "current_latent_variable": latent_variable,
        "latent_scores": latent_scores,
        "condition": str(participant.condition),
        'tree_id': tree_id,
        'tree': json.dumps(tree),
    }
    context.update(study_context)
    return render(request, 'construction/explore_gcq.html', context)


def nasa_tlx(request):
    """
    Html with Nasa TLX questionnaire is returned.
    :param request:
    :return:
    """
    study = models.Study.get_current_study(request)
    study_context = models.StudyContext.get_context(study=study, view="nasa_tlx")

    items = models.Item.get_nasa_tlx()
    # override items if study context exists
    if "nasa_tlx_items" in study_context:
        items = study_context["nasa_tlx_items"]

    nasa_tlx_items = []
    for item in items:
        nasa_tlx_items.append({"text": "{}    {}".format(item["deutsch"][0], item["deutsch"][1]),
                               "left": item["left"],
                               "right": item["right"],
                               "range": item["range"]})

    context = {"nasa_tlx_items": nasa_tlx_items,
               "current_view": "welcome",
               }
    return render(request, 'construction/nasa_tlx.html', context)


@xframe_options_exempt
def open_questions(request, open_questions="open_questions"):
    """
    Html with open questions is returned.
    :param request:
    :return:
    """
    study = models.Study.get_current_study(request)
    study_context = models.StudyContext.get_context(study=study, view=open_questions)

    # tree ranking
    tree_id = models.Goal.get_current_tree_id(request)
    tree = models.Goal.get_tree(tree_id)

    # single view
    if study_context.get("single_view", False):
        if "remaining_questions_indices" not in request.session or len(request.session["remaining_questions_indices"]) == 0:
            # if first call
            if study_context.get("random_order", False):
                random_questions_indices = []
                non_random_questions_indices = []
                # separate between random and non random questions
                for index, question in enumerate(study_context["questions"]):
                    if question.get("random", True):
                        random_questions_indices.append(index)
                    else:
                        non_random_questions_indices.append(index)
                random.shuffle(random_questions_indices)
                questions_indices = random_questions_indices + non_random_questions_indices  # non random questions last
            else:
                questions_indices = range(len(study_context["questions"]))
            request.session["remaining_questions_indices"] = questions_indices
        remaining_questions_indices = request.session["remaining_questions_indices"]

        if "current_question_index" not in request.session:
            # get first remaining question
            question_index = remaining_questions_indices.pop(0)
            request.session["current_question_index"] = question_index
            request.session["remaining_questions_indices"] = remaining_questions_indices
        else:
            question_index = request.session["current_question_index"]
        # set single selected question
        study_context["questions"] = [study_context["questions"][question_index]]

    # sort questions randomly
    if study_context.get("random_order", False):
        random.shuffle(study_context["questions"])

    context = {
        "title": "Teile uns Deine Erfahrungen mit",
        "tree": json.dumps(tree),
        "open_questions": open_questions,
        "max_answer_length": 2048,          # model field is limited to 2048 chars
        "max_goal_length": 256,
    }
    if "questions" not in study_context:
        context["questions"] = models.Question.get_open_questions()

    context.update(study_context)
    return render(request, 'construction/open_questions.html', context)


def thankyou(request):
    """
    Html with open Outro is returned.
    :param request:
    :return:
    """
    study = models.Study.get_current_study(request)
    study_context = models.StudyContext.get_context(study=study, view="thankyou")

    participant = models.Participant.get_current_participant(request)
    if not participant.finished:
        participant.finished = timezone.now()
    participant.save()

    # set timestamp
    timestamp = participant.finished.timestamp()
    if "text" in study_context:
        study_context["text"] = study_context["text"].format(timestamp=timestamp)

    context = {
        "title": "Studienteilnahme abgeschlossen - Danke!",
        "timestamp": timestamp,
    }
    context.update(study_context)

    # set timestamp in text
    if "text" in context:
        context["text"] = context["text"].format(timestamp=context["timestamp"])

    return render(request, 'construction/thankyou.html', context)


@xframe_options_exempt
def questionnaire(request, questionnaire="questionnaire"):
    """
        Html with questionnaire of the passed questionnaire name
        :param questionnaire: name of questionnaire
        :param request:
        :return:
        """
    study = models.Study.get_current_study(request)
    study_context = models.StudyContext.get_context(study=study, view=questionnaire)

    # collect personal goals as items if personal_goal_items is true
    if study_context.get("personal_goal_items", False) is True:
        study_context["items"] = models.Item.get_personal_goal_items(request)
    # collect last tree goals ordered by their depth if tree_goal_items is true
    elif study_context.get("tree_goal_items", False) is True:
        study_context["items"] = models.Item.get_tree_goal_items(request)

    context = {
        "questionnaire": questionnaire,
        "type": "likert",                # default type
        "slider_min": 0,                 # default minimum
        "slider_max": 1,                 # default maximum
        "slider_step": 0.01,             # default step
    }
    context.update(study_context)
    return render(request, 'construction/questionnaire.html', context)


@xframe_options_exempt
def personal_goals(request):
    """
    Html with personal goals is returned.
    :param request:
    :return:
    """
    participant = models.Participant.get_current_participant(request)
    study = models.Study.get_current_study(request)
    study_context = models.StudyContext.get_context(study=study, view="personal_goals")

    goals = models.PersonalGoal.objects.filter(participant=participant)

    context = {
        "title": "Persönliche Bildungsziele",
        "max_title_length": 20,
        "personal_goals": [goal.name for goal in goals],
    }
    context.update(study_context)
    return render(request, 'construction/personal_goals.html', context)


@xframe_options_exempt
def personal_goal_selection(request):
    """
    Html with selection of one personal goal
    :param request:
    :return:
    """
    participant = models.Participant.get_current_participant(request)
    study = models.Study.get_current_study(request)
    study_context = models.StudyContext.get_context(study=study, view="personal_goal_selection")

    personal_goals = models.PersonalGoal.objects.filter(participant=participant)

    context = {
        "title": "Persönliches Bildungsziel auswählen",
        "personal_goals": personal_goals,
    }
    context.update(study_context)
    return render(request, 'construction/personal_goal_selection.html', context)


@xframe_options_exempt
def study(request, study_name, userid=None):
    """
    Study entry point view
    :param userid: backend user_origin_id
    :param request:
    :param study_name
    :return:
    """
    # clear session
    request.session.flush()

    study = models.Study.set_current_study(request, study_name)
    # if study doesn't exist
    if not study:
        raise Http404

    # set position to first view
    position = -1
    # create participant for external siddata user
    if userid:
        participant = models.Participant.get_or_create_siddata_participant(request, userid)
        # restore study position / last view of siddata participant
        if participant.study_sequence_position is not None:
            position = participant.study_sequence_position-1
    response = redirect("/"+study.get_next_view(request, position=position))

    # set study language
    translation.activate(study.language)
    response.set_cookie(settings.LANGUAGE_COOKIE_NAME, study.language)
    return response


def index(request):
    """
    Landing Page
    :param request:
    :return:
    """
    context = {"key": "value"}
    return render(request, 'construction/index.html', context)


# @login_required
def explore_trees(request, tree_id):
    """

    :param request:
    :return:
    """

    root_goal = models.Goal.objects.get(tree_id=tree_id, parent_id__isnull=True)
    tree = models.Goal.get_children(root_goal.id)
    study=root_goal.participant.study

    prev_next = study.get_previous_and_next_tree(tree_id)


    study_properties=study.summarize()

    tree_properties=models.Goal.get_tree_properties(tree_id)
    context = {
                'tree_properties':tree_properties,
                'study_properties':study_properties,
               'tree_id': tree_id,
               'tree': json.dumps(tree),
               }
    context.update(prev_next)
    return render(request, 'construction/explore_trees.html', context)

# @login_required
def explore_studies(request, study_id):
    """

    :param request:
    :return:
    """

    study=models.Study.objects.get(id=study_id)

    prev_next = study.get_previous_and_next_study()

    study_properties = study.summarize()

    context = {
                'branching':list(study_properties[-3]["nodes"]),
                'depths':list(study_properties[-2]["branches"]),
                'tree_sizes':list(study_properties[-1]["tree_sizes"]),
                'study_properties':study_properties,
                'tree_data':study.get_tree_data(),
               }
    print("branching")
    print(context["branching"])
    print("tree_sizes")
    print(context["tree_sizes"])
    print("depths")
    print(context["depths"])
    context.update(prev_next)
    return render(request, 'construction/explore_studies.html', context)

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


def condition1(request):
    """
    Display tree.
    :param request:
    :return:
    """

    tree_id = 1
    context = {'tree_id': tree_id,
               'tree': json.dumps(models.Goal.get_tree(0)),
               }

    return render(request, 'construction/condition1.html', context)


def condition2(request):
    """
    Display tree.
    :param request:
    :return:
    """

    tree_id = 1
    context = {'tree_id': tree_id,
               'tree': json.dumps(models.Goal.get_tree(0)),
               }

    return render(request, 'construction/condition2.html', context)


def condition3(request):
    """
    Display tree.
    :param request:
    :return:
    """
    tree_id = 1
    context = {'tree_id': tree_id,
               'tree': json.dumps(models.Goal.get_tree(0)),
               }

    return render(request, 'construction/condition3.html', context)


def condition4(request):
    """
    Display tree.
    :param request:
    :return:
    """
    tree_id = 1
    context = {'tree_id': tree_id,
               'tree': json.dumps(models.Goal.get_tree(0)),
               }

    return render(request, 'construction/condition4.html', context)
