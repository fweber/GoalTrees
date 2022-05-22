import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.views.decorators.clickjacking import xframe_options_exempt

import random

from . import models
from . import views


def next_view(request):
    """
    redirects the participant to next view in study sequence
    :param request:
    :return:
    """
    study = models.Study.get_current_study(request)
    return redirect(study.get_next_view(request))


@xframe_options_exempt
def previous_view(request, offset=1):
    """
    redirects the participant to previous view in study sequence
    :param offset: Specifies how many views to go back.
    :param request:
    :return:
    """
    study = models.Study.get_current_study(request)
    study.set_sequence_position(request, study.get_sequence_position(request) - offset)
    return redirect("/" + study.get_current_view(request))


@xframe_options_exempt
def answer_questionnaire(request):
    """
    processes the generic questionnaire form
    :param request:
    :return:
    """
    post = request.POST

    questionnaire = post["questionnaire"]
    # the get items function must have following structure: "get_"+questionnaire+"_items"
    study = models.Study.get_current_study(request)
    study_context = models.StudyContext.get_context(study=study, view=questionnaire)

    # collect personal goals as items if personal_goal_items is true
    if study_context.get("personal_goal_items", False) is True:
        study_context["items"] = models.Item.get_personal_goal_items(request)
    # collect last tree goals ordered by their depth if tree_goal_items is true
    elif study_context.get("tree_goal_items", False) is True:
        study_context["items"] = models.Item.get_tree_goal_items(request)

    items = study_context["items"] if "items" in study_context else []
    items_texts = [item["item_text"] for item in items]

    participant = models.Participant.get_current_participant(request)

    for key in post.keys():

        if key in items_texts:
            item_text = key
        else:
            continue

        answer = post[item_text]

        for item in items:
            if item["item_text"] == item_text:
                stored_item = models.Item.objects.create(
                    questionnaire=questionnaire,
                    code=item["code"] if "code" not in study_context else study_context["code"],
                    # use code in study context if exists
                    text=item["item_text"] if "item_text" not in study_context else study_context["item_text"],
                    # goal items have only one item_text
                    answers=item["answers"] if "answers" in item else study_context["answers"],
                    participant=participant,
                    given_answer=answer,
                    reverse_coded=item.get("reverse_coded", False) if "reverse_coded" not in study_context else
                    study_context["reverse_coded"],  # use reverse_coded in study context if exists
                    latent_variable=item.get("latent_variable", "") if "latent_variable" not in study_context else
                    study_context["latent_variable"],  # use latent_variable in study context if exists
                    personal_goal=item["personal_goal"] if "personal_goal" in item else None,
                    goal=item["goal"] if "goal" in item else None,
                )
                stored_item.save()
                models.UserInteraction.create_interaction(request, "answer item", stored_item)

    # get next view from Item model
    response = redirect(participant.study.get_next_view(request))
    return response


def register_participant(request):
    post = request.POST
    study = models.Study.get_current_study(request)

    additional_data = {}
    if "tool" in post:
        additional_data["studytool_used"] = post["tool"]
        if post["tool"] == "yes" and "tool_name" in post:
            additional_data["studytool_name"] = post["tool_name"]

    if "consulting" in post:
        additional_data["consulting_requested"] = post["consulting"]
        if post["consulting"] == "yes" and "consulting_form" in post:
            additional_data["consulting_form"] = post["consulting_form"]

    if "handling" in post:
        additional_data["computer_handling"] = post["handling"]

    if "english" in post:
        additional_data["english"] = post["english"]

    p = models.Participant.get_current_participant(request)

    # update participant fields
    p.age = (None if post["age"] == "" else post["age"])
    p.gender = (None if "gender" not in post else post["gender"])
    p.subject = (None if post["subject"] == "" else post["subject"])
    p.degree = (None if "degree" not in post or post["degree"] == "" else post["degree"])
    p.semester = (None if post["semester"] == "" else post["semester"])
    p.study = study
    p.additional_data = additional_data
    p.screen_size = (None if post["screen_size"] == "" else post["screen_size"])
    p.operating_system = (None if post["operating_system"] == "" else post["operating_system"])
    p.browser_language = (None if post["browser_language"] == "" else post["browser_language"])

    # if study has defined conditions
    if study.conditions:
        p.condition = study.conditions[p.id % len(study.conditions)]
    else:
        p.condition = (p.id % 4) + 1

    p.save()

    request.session['participant_id'] = p.id
    request.session['condition'] = p.condition

    models.UserInteraction.create_interaction(request, "create participant", p)

    response = redirect(study.get_next_view(request))
    return response


def write_feedback(request):
    post = request.POST
    default_participant = models.Participant.get_default_participant()
    question_templates = models.Question.objects.filter(participant=default_participant,
                                                        type="feedback")
    questions = []
    for question in question_templates:
        questions.append(question.question)
    participant = models.Participant.get_participant(request)
    for key in post.keys():
        if key in questions:
            id = models.Participant.get_next_question_id()
            q = models.Question.objects.create(id=id,
                                               question=key,
                                               answer=post[key],
                                               type="feedback",
                                               participant=participant)
            q.save()
            models.UserInteraction.create_interaction(request, "write question", q)
    return views.next_view(request)


def write_root(request):
    goal = models.Goal.get_current_root(request)
    goal.title = request.POST["goal_text"]
    goal.save()
    return views.tree_generation_new(request)


def change_functionality(request):
    f = request.POST["function"]
    if f == "new":
        return views.tree_generation_new(request)
    elif f == "edit":
        return views.tree_generation_edit(request)
    elif f == "delete":
        return views.tree_generation_delete(request)
    else:
        return HttpResponse("change functionality, function {} unknown!".format(f))


@xframe_options_exempt
def write_goal(request):
    participant = models.Participant.get_current_participant(request)
    parent_id = int(request.POST["parent_id"])
    title = request.POST["goal_title"]
    description = request.POST["goal_description"] if "goal_description" in request.POST else None
    parent = models.Goal.objects.get(id=parent_id)
    tree_id = parent.tree_id
    replicated_tree_id = parent.replicated_tree_id
    g = models.Goal.objects.create(
        participant=participant,
        parent_id=parent_id,
        title=title,
        description=description,
        tree_id=tree_id,
        replicated_tree_id=replicated_tree_id,
    )
    g.save()
    tree = models.Goal.get_tree(tree_id)
    models.UserInteraction.create_interaction(request, "write goal", g)
    goals = models.Goal.get_tree_goals(tree_id).order_by("title")
    response = {
        "tree": json.dumps(tree),
        "goals": [goal.serialize() for goal in goals],
    }
    return JsonResponse(response)


@xframe_options_exempt
def edit_goal(request):
    id = request.POST["goal_id"]
    title = request.POST["goal_title"]
    description = request.POST["goal_description"] if "goal_description" in request.POST else None
    g = models.Goal.objects.get(id=id)
    # if new title empty retain old title
    g.title = title if title else g.title
    g.description = description if description else g.description
    g.save()
    tree = models.Goal.get_tree(g.tree_id)
    models.UserInteraction.create_interaction(request, "edit goal", g)
    goals = models.Goal.get_tree_goals(g.tree_id).order_by("title")
    response = {
        "tree": json.dumps(tree),
        "goals": [goal.serialize() for goal in goals],
    }
    return JsonResponse(response)


@xframe_options_exempt
def discard_goal(request):
    id = request.POST["goal_id"]
    g = models.Goal.objects.get(id=id)
    tree_id = g.tree_id
    models.UserInteraction.create_interaction(request, "discard goal", g)
    models.Goal.discard_goal(g.id)
    tree = models.Goal.get_tree(tree_id)
    goals = models.Goal.get_tree_goals(tree_id).order_by("title")
    response = {
        "tree": json.dumps(tree),
        "goals": [goal.serialize() for goal in goals],
    }
    return JsonResponse(response)


def mark_goal(request):
    id = request.POST["goal_id"]
    g = models.Goal.objects.get(id=id)
    g.done = True
    g.save()
    tree_id = g.tree_id
    models.UserInteraction.create_interaction(request, "mark goal", g)
    tree = models.Goal.get_tree(tree_id)
    goals = models.Goal.get_tree_goals(tree_id).order_by("title")
    response = {
        "tree": json.dumps(tree),
        "goals": [goal.serialize() for goal in goals],
    }
    return JsonResponse(response)


def change_condition(request):
    condition = request.POST["selected_condition"]
    participant = models.Participant.get_current_participant(request)
    participant.condition = condition
    participant.save()
    models.UserInteraction.create_interaction(request, "change condition", participant)
    return redirect("tree_construction/{}/{}".format(condition, request.POST["view"]))


def answer_nasa_tlx(request):
    post = request.POST

    nasa_tlx = models.Item.get_nasa_tlx()

    # override items if study context exists
    study = models.Study.get_current_study(request)
    study_context = models.StudyContext.get_context(study=study, view="nasa_tlx")
    if "nasa_tlx_items" in study_context:
        nasa_tlx = study_context["nasa_tlx_items"]

    items = ["{}    {}".format(item["deutsch"][0], item["deutsch"][1]) for item in nasa_tlx]

    participant = models.Participant.get_current_participant(request)

    for key in post.keys():

        if key in items:
            item_text = key
        else:
            continue

        answer = post[item_text]

        for item in nasa_tlx:

            if item["deutsch"][1] == item_text:
                stored_item = models.Item.objects.create(
                    questionnaire="nasa_tlx",
                    code=item["code"],
                    text=answer,
                    answers=item["answers"],
                    participant=participant,
                    given_answer=answer, )
                stored_item.save()
                models.UserInteraction.create_interaction(request, "answer item", stored_item)
    response = redirect(participant.study.get_next_view(request))
    return response


@xframe_options_exempt
def new_tree(request, title="Mein Studienziel", replicated_tree_id=None):
    if request.method == 'POST' and "goal" in request.POST:
        title = request.POST["goal"]

    models.Goal.create_new_tree(request, title, replicated_tree_id)
    participant = models.Participant.get_current_participant(request)

    return redirect("/" + participant.study.get_next_view(request))


@xframe_options_exempt
def answer_open_questions(request):
    participant = models.Participant.get_current_participant(request)

    questions = models.Question.get_open_questions()
    open_questions = request.POST["open_questions"]

    study = models.Study.get_current_study(request)
    study_context = models.StudyContext.get_context(study=study, view=open_questions)
    if "questions" in study_context:
        questions = study_context["questions"]

    for question in questions:
        if question["type"] == "text" or question["type"] == "radio" or question["type"] == "goal":
            if question["text"] in request.POST.keys():
                q = models.Question.objects.create(
                    participant=participant,
                    question=question["text"],
                    answer=request.POST.get(question["text"]),
                    type=open_questions,
                    tree_id=(request.session["current_tree"] if "current_tree" in request.session else None),
                )
                q.save()
                models.UserInteraction.create_interaction(request, "write question", q)
        elif question["type"] == "tree_ranking":
            for condition in question["conditions"]:
                if condition in request.POST.keys():
                    q = models.Question.objects.create(
                        participant=participant,
                        question="{}, condition: {}".format(question["text"], condition),
                        answer=request.POST.get(condition),
                        type=open_questions,
                        tree_id=(request.session["current_tree"] if "current_tree" in request.session else None),
                    )
                    q.save()
                    models.UserInteraction.create_interaction(request, "write question", q)

        # save personal goal
        if question["type"] == "goal":
            if question["text"] in request.POST.keys():
                pg = models.PersonalGoal.objects.create(
                    name=request.POST.get(question["text"]),
                    participant=participant,
                )
                pg.save()

    # single view
    if study_context.get("single_view", False):
        request.session.pop("current_question_index")
        # remaining questions exist
        remaining_questions_indices = request.session.get("remaining_questions_indices", [])
        if len(remaining_questions_indices) > 0:
            response = redirect("open_questions/" + open_questions)
        else:
            request.session.pop("remaining_questions_indices")
            response = redirect(participant.study.get_next_view(request))
    else:
        response = redirect(participant.study.get_next_view(request))
    return response


def write_comment(request):
    """
    Saves final user thankyou comment
    :param request:
    :return:
    """
    participant = models.Participant.get_current_participant(request)

    q = models.Question.objects.get_or_create(
        participant=participant,
        question=request.POST.get("comment_text"),
        type=request.POST.get("open_questions"),
    )[0]
    q.answer = request.POST.get("thankyou_comment")
    q.save()

    models.UserInteraction.create_interaction(request, "write comment", q)

    return redirect(participant.study.get_current_view(request))


@xframe_options_exempt
def write_personal_goal(request):
    participant = models.Participant.get_current_participant(request)

    models.PersonalGoal.objects.create(
        name=request.POST["personal_goal"],
        participant=participant,
    )

    return HttpResponse("Personal goal saved.")


@xframe_options_exempt
def delete_personal_goal(request):
    participant = models.Participant.get_current_participant(request)

    models.PersonalGoal.objects.filter(
        name=request.POST["personal_goal"],
        participant=participant,
    ).delete()

    return HttpResponse("Personal goal deleted.")


def process_personal_goals(request):
    participant = models.Participant.get_current_participant(request)
    study = models.Study.get_current_study(request)

    if "remaining_tree_conditions" not in request.session:
        # if first call
        request.session["remaining_tree_conditions"] = ["1", "2", "3", "4"]
        request.session["personal_goal_index"] = 0

    # tree already constructed
    remaining_conditions = request.session["remaining_tree_conditions"]

    if not remaining_conditions:
        # remove current tree
        request.session.pop("current_tree")
        # if remaining conditions empty continue sequence
        return redirect(participant.study.get_next_view(request))

    if len(remaining_conditions) < 4 and participant.study.get_current_view(request) == "process_personal_goals":
        # if remaining conditions available go three views back
        participant.study.set_sequence_position(request, study.get_sequence_position(request) - 3)

    # pick random condition
    tree_condition = random.choice(remaining_conditions)
    # delete condition from remaining conditions
    remaining_conditions.remove(tree_condition)
    request.session["remaining_tree_conditions"] = remaining_conditions

    # pick random personal goal
    goal_index = request.session["personal_goal_index"]
    personal_goals = models.PersonalGoal.objects.filter(participant=participant).order_by("created")
    root_title = personal_goals[goal_index].name
    # increment goal index
    request.session["personal_goal_index"] = goal_index + 1

    # create new tree and save condition on root node
    tree = models.Goal.create_new_tree(request, root_title)
    tree.condition = tree_condition
    tree.save()
    request.session["current_tree"] = tree.tree_id

    return redirect(
        participant.study.get_next_view(request) + "/" + tree_condition + "/personal_goals_tree_construction")


def random_views(request):
    """Shows all in study context containing views randomly"""
    participant = models.Participant.get_current_participant(request)
    study = models.Study.get_current_study(request)
    study_context = models.StudyContext.get_context(study=study, view="random_views")

    if "remaining_views" not in request.session:
        if "sequences" in study_context:
            # pick sequence iteratively
            sequence = study_context["sequences"][participant.id % len(study_context["sequences"])]
            request.session["remaining_views"] = [study_context["views"][i] for i in sequence]
        else:
            # sort views randomly
            random.shuffle(study_context["views"])
            request.session["remaining_views"] = study_context["views"]

    remaining_views = request.session["remaining_views"]
    # remaining views available
    if len(remaining_views) > 0:
        next_view = remaining_views.pop(0)
        request.session["remaining_views"] = remaining_views
        study.set_sequence_position(request, study.get_sequence_position(request) - 1)
        return redirect("/" + next_view)
    else:
        # remove remaining views from session
        request.session.pop("remaining_views")

    return redirect(study.get_next_view(request))


@xframe_options_exempt
def filter_participants(request):
    post = request.POST
    for x in post.keys():
        print(x)
        if x[:12] == "participant_":
            p_id = x[12:]
            participant = models.Participant.objects.get(pk=p_id)
            participant.exclude_from_analyses = True
            participant.save()

    return views.participants(request)


@xframe_options_exempt
def filter_trees(request):

    post = request.POST
    for x in post.keys():
        print(x)
        if x[:16] == "tree_is_example_":
            tree_id = x[16:]
            goals = models.Goal.objects.filter(tree_id=tree_id)
            for goal in goals:
                goal.is_example = True
                goal.save()
        elif x[:15] == "tree_discarded_":
            tree_id = x[15:]
            goals = models.Goal.objects.filter(tree_id=tree_id)
            for goal in goals:
                goal.discarded = True
                goal.save()

    return views.trees(request)
