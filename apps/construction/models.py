import csv
import math
import statistics
import pandas as pd
import random

from goaltrees import settings

from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models import Max, JSONField

class Study(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=512, unique=True)
    sequence = ArrayField(models.CharField(max_length=128), default=list)
    classname = models.CharField(max_length=256)
    conditions = ArrayField(models.IntegerField(), default=list)
    language = models.CharField(max_length=16, default="de")

    def set_current_study(request, study_name="default"):
        try:
            study = Study.objects.get(name=study_name)
        except Study.DoesNotExist:
            # if study not exist
            return False

        request.session["study_name"] = study_name
        return study

    def get_current_study(request):
        # if no study is set in session
        if "study_name" not in request.session:
            # use prestudy_ld as default study
            request.session["study_name"] = "prestudy"
        return Study.objects.get(name=request.session["study_name"])

    def get_next_view(self, request, position=None):
        """
        Returns the next view in sequence
        :param request:
        :param position: sets the position of the sequence and returns the next view
                         negative values return the first view
        :return:
        """
        self.set_sequence_position(request, position)

        # if no sequence available
        if not self.sequence:
            # return to default url
            return "/"

        # if first call
        if "sequence_position" not in request.session:
            # return second view
            request.session["sequence_position"] = 0
        elif request.session["sequence_position"] < 0:
            # return first view
            request.session["sequence_position"] = -1

        next_position = request.session["sequence_position"]
        # if not last study element
        if next_position + 1 < len(self.sequence):
            next_position = next_position + 1

        request.session["sequence_position"] = next_position
        Participant.save_sequence_position(request, request.session["sequence_position"])
        return self.sequence[next_position]

    def get_current_view(self, request):
        # if no sequence available
        if not self.sequence:
            return False

        position = self.get_sequence_position(request)
        return self.sequence[position]

    def set_sequence_position(self, request, position):
        if position is not None and position < len(self.sequence):
            request.session["sequence_position"] = position
            Participant.save_sequence_position(request, request.session["sequence_position"])

    def get_sequence_position(self, request):
        # return first position if not set
        if "sequence_position" not in request.session:
            request.session["sequence_position"] = 0
            Participant.save_sequence_position(request, request.session["sequence_position"])

        return request.session["sequence_position"]

    def get_valid_tree_ids(self):
        goals = Goal.objects.filter(participant__study=self, discarded=False)
        valid_tree_ids=[]
        for goal in goals:
            # if there are less than 3 goals in the tree
            if len(goals.filter(tree_id=goal.tree_id))>2:
                if goal.tree_id not in valid_tree_ids:
                    valid_tree_ids.append(goal.tree_id)
        return valid_tree_ids

    def get_goals_from_valid_trees(self):
        goals = Goal.objects.filter(participant__study=self, discarded=False)
        to_exclude=[]
        for goal in goals:
            # if there are less than 3 goals in the tree
            if len(goals.filter(tree_id=goal.tree_id, discarded=False))<3:
                to_exclude.append(goal.tree_id)
        goals = Goal.objects.filter(participant__study=self, discarded=False).exclude(tree_id__in=to_exclude)
        return goals

    def get_previous_and_next_tree(self,tree_id):
        goals=self.get_goals_from_valid_trees().order_by('tree_id').values('tree_id').distinct()
        minus_2=0
        minus_1=0
        current=0
        for goal in goals:
            minus_2=minus_1
            minus_1=current
            current=goal['tree_id']
            if minus_1==tree_id:
                break
        prev_next= {
            'last_tree_id': minus_2,
            'next_tree_id': current,
        }
        return prev_next

    def get_previous_and_next_study(self):
        studies = Study.objects.all().order_by("id")
        if len(studies)==1:
            return {'last_study_id': self.id,
                    'next_study_id': self.id,
            }
        minus_2=0
        minus_1=0
        current=0
        for study in studies:
            minus_2=minus_1
            minus_1=current
            current = study.id
            if minus_1==self.id:
                break
        prev_next= {
            'last_study_id': minus_2,
            'next_study_id': current,
        }
        return prev_next

    def summarize(self):
        study_properties=[]

        goals=self.get_goals_from_valid_trees()

        participants = len(goals.order_by().values('participant').distinct())
        study_properties.append({"name":"Name","value":self.name})
        if self.sequence:
            study_properties.append({"name":"Sequence","value":self.sequence})
        study_properties.append({"name":"Number of participants","value":participants},)
        study_properties.append({"name": "Number of trees", "value": len(goals.order_by().values('tree_id').distinct())}, )
        study_properties.append({"name": "Number of goals", "value": len(goals)}, )


        branch_depths = []
        parents = {}
        trees = {}
        actions = 0
        roots = 0
        for goal in goals:

            if goal.tree_id in trees.keys():
                trees[goal.tree_id] += 1
            else:
                trees[goal.tree_id] = 1

            if goal.parent_id is None:
                roots += 1
            elif goal.parent_id in parents.keys():
                parents[goal.parent_id] += 1
            else:
                parents[goal.parent_id] = 1
            # if goal is not a parent itself, it is a leaf node
            if not goals.filter(parent_id=goal.id).exists():
                actions += 1
                depth = 0
                parent = goal
                # probably a node is deleted
                while parent.parent_id is not None and goals.filter(id=parent.parent_id).exists():
                    parent = goals.get(id=parent.parent_id)
                    depth += 1
                branch_depths.append(depth)
        if len(branch_depths) == 0:
            max_depth = 0
            min_depth = 0
            average_depth = 0
        else:
            max_depth = max(branch_depths)
            min_depth = min(branch_depths)
            average_depth = statistics.mean(branch_depths)


        average_depth = "%.2f" % average_depth

        if len(parents.values())==0:
            min_branching = 0
            max_branching = 0
            average_branching = 0
        else:
            min_branching = min(parents.values())
            max_branching = max(parents.values())
            average_branching = statistics.mean(parents.values())

        study_properties.append({'name': 'minimal depth', "value": min_depth, })
        study_properties.append({'name': 'maximal depth', "value": max_depth, })
        study_properties.append({'name': 'average depth', "value": average_depth, })
        study_properties.append({'name': 'minimal branching', "value": min_branching, })
        study_properties.append({'name': 'maximal branching', "value": max_branching, })
        study_properties.append({'name': 'average branching', "value": average_branching,})
        study_properties.append({'name': 'actions', "value": actions, })
        study_properties.append({'name': 'intermediate goals', "value": len(goals)-roots-actions, })
        study_properties.append({'name': 'root goals', "value": roots, })

        study_properties.append({'name': 'nodes', "value": len(parents.keys()),"nodes":parents.values() })
        study_properties.append({'name': 'branches', "value": len(branch_depths),"branches":branch_depths })
        study_properties.append({'name': 'trees', "value": len(trees.keys()), "tree_sizes": trees.values()})
        print(parents.keys())

        return study_properties

    def get_tree_data(self):
        tree_ids = self.get_valid_tree_ids()
        tree_data={}
        for tree_id in tree_ids:
            tree_properties = Goal.get_tree_properties(tree_id)
            for tree_property in tree_properties:
                if tree_property["name"] in tree_data.keys():

                    tree_data[tree_property["name"]].append(float(tree_property["value"]))
                else:

                    tree_data[tree_property["name"]]=[float(tree_property["value"])]

        return tree_data


class StudyContext(models.Model):
    """
    Contains all view contexts of a study like welcome texts, questionnaire texts etc.
    """
    id = models.AutoField(primary_key=True)
    view = models.CharField(max_length=256)
    study = models.ForeignKey(Study, on_delete=models.CASCADE)
    context = JSONField()

    def get_context(study, view):
        try:
            return StudyContext.objects.get(study=study, view=view).context
        except StudyContext.DoesNotExist:
            return {}


# Create your models here.
class Participant(models.Model):
    id = models.AutoField(primary_key=True)
    age = models.IntegerField(null=True)
    gender = models.CharField(max_length=256, null=True)
    semester = models.IntegerField(null=True)
    subject = models.CharField("Studienfach", max_length=256, null=True)
    degree = models.CharField(max_length=256, null=True)
    created = models.DateTimeField(auto_now_add=True)
    finished = models.DateTimeField(null=True)
    condition = models.CharField(max_length=256, null=True)
    study = models.ForeignKey(Study,on_delete=models.CASCADE)
    study_sequence_position = models.IntegerField(null=True)
    additional_data = JSONField(null=True)
    # structure of screen_size: screen_width x screen_height (e.g. 1920x1080)
    screen_size = models.CharField(max_length=128, null=True)
    operating_system = models.CharField(max_length=256, null=True)
    browser_language = models.CharField(max_length=128, null=True)
    siddata_user_id = models.CharField(max_length=256, null=True)

    def __str__(self):
        return "{}".format(self.id)

    def get_trees(self):
        """
        Get goals for Participant instance and structure as trees.
        :return:
        """
        data = {"trees": [{"goal": "my goal 1", "sub_goals": []},
                          {"goal": "my goal 2", "sub_goals": []},
                          ]
                }
        return data

    def get_current_participant(request):
        if "participant_id" in request.session:
            return Participant.objects.get(id=request.session["participant_id"])
        else:
            # create new participant with minimal information
            participant = Participant.objects.create(
                study=Study.get_current_study(request),
            )
            participant.condition = (participant.id % 4) + 1
            participant.save()
            request.session["participant_id"] = participant.id
            return participant


    def get_default_participant():
        return Participant.objects.get(subject="Testfach")

    def get_or_create_siddata_participant(request, userid):
        participant, created = Participant.objects.get_or_create(
            siddata_user_id=userid,
            study=Study.get_current_study(request),
        )
        if created:
            participant.condition = 3   # only dendogram visualisation
            participant.save()
        request.session["participant_id"] = participant.id
        return participant

    def save_sequence_position(request, position):
        # save sequence position in participant object if exists
        try:
            participant = Participant.get_current_participant(request)
            participant.study_sequence_position = position
            participant.save()
        except KeyError:
            # do nothing if participant is not created (e.g. in welcome view)
            pass


class Goal(models.Model):
    """
    Represents tree goals
    Attributes:
        is_example: Indicates example tree which are defined in the study classes.
        example_id: Is set during the creation of example trees so that goals can be clearly distinguished.
        replicated_tree_id: Indicates which tree was recreated by the user.
    """
    id = models.AutoField(primary_key=True)
    tree_id = models.IntegerField("Zielbaum ID")
    parent_id = models.IntegerField("Oberziel", null=True, default=None)
    title = models.CharField("Zieltext", max_length=256)
    description = models.CharField("Beschreibung", null=True, max_length=512)
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE, null=True)
    condition = models.CharField(max_length=256, null=True)
    created = models.DateTimeField(auto_now_add=True)
    is_example = models.BooleanField(default=False)
    example_id = models.IntegerField(null=True, default=None)
    replicated_tree_id = models.IntegerField(null=True)
    study = models.ForeignKey(Study, on_delete=models.CASCADE, null=True)
    discarded = models.BooleanField(default=False)
    done = models.BooleanField(null=True)

    def __str__(self):
        return "{} {}".format(self.id, self.title)

    def get_children(goal_id):
        """
        recursively returns subtrees or nodes as anchor
        :param goal_id:
        :return:
        """
        children = Goal.objects.filter(parent_id=goal_id, discarded=False)
        root = Goal.objects.get(id=goal_id)
        if len(children) == 0:
            return {'name': root.title, 'done': root.done, 'size': 1000}
        else:
            children_json = []
            for child in children:
                children_json.append(Goal.get_children(child.id))
            return {'name': root.title, 'done': root.done, 'children': children_json}


    def get_current_tree(request):
        return Goal.objects.get(id=request.session["current_root"])

    def get_tree_goals(tree_id):
        """
        Returns all not discarded tree goals
        :param tree_id:
        :return:
        """
        return Goal.objects.filter(tree_id=tree_id, discarded=False)

    def get_tree(tree_id):
        try:
            root_goal = Goal.objects.get(
                tree_id=tree_id,
                parent_id=None,
            )
            tree = Goal.get_children(root_goal.id)
            tree['parent'] = 'null'
            # tree = [tree]
            return tree
        except Exception as e:
            print(e)
            return None

    def get_current_tree_id(request):
        participant = Participant.get_current_participant(request)
        return Goal.objects.filter(participant=participant).aggregate(Max('tree_id'))['tree_id__max']

    def create_new_tree(request, root_title="Mein Studienziel", replicated_tree_id=None):
        participant = Participant.get_current_participant(request)
        if len(Goal.objects.all()) == 0:
            tree_id = 1
        else:
            tree_id = Goal.objects.aggregate(Max('tree_id'))['tree_id__max'] + 1
        new_tree_root = Goal.objects.create(
            participant=participant,
            tree_id=tree_id,
            title=root_title,
            replicated_tree_id=replicated_tree_id,
        )
        UserInteraction.create_interaction(request, "write goal", new_tree_root)
        new_tree_root.save()
        return new_tree_root

    def get_gcq_goal(request):
        # todo: Improve the choice mechanism
        participant = Participant.get_current_participant(request)
        return Goal.objects.filter(participant=participant)[0]

    def get_tree_properties(tree_id):
        # Tree Data
        goals_in_tree=Goal.get_tree_goals(tree_id)
        goals_n=len(goals_in_tree)
        discarded_goals_n=len(Goal.objects.filter(tree_id=tree_id, discarded=True))
        branch_depths=[]
        parents={}
        for goal in goals_in_tree:
            if goal.parent_id in parents.keys():
                parents[goal.parent_id]+=1
            else:
                parents[goal.parent_id]=1
            # if goal is not a parent itself, it is a leaf node
            if not goals_in_tree.filter(parent_id=goal.id).exists():
                depth=0
                parent=goal
                while parent.parent_id is not None and goals_in_tree.filter(id=parent.parent_id).exists():
                    parent=goals_in_tree.get(id=parent.parent_id)
                    depth+=1
                branch_depths.append(depth)

        max_depth=max(branch_depths)
        min_depth=min(branch_depths)
        average_depth=statistics.mean(branch_depths)
        average_depth="%.2f" % average_depth

        min_branching=min(parents.values())
        max_branching=max(parents.values())
        average_branching=statistics.mean(parents.values())
        average_branching = "%.2f" % average_branching

        tree_properties=[
                {'name':'Number_of_goals',"value": goals_n,},
                {'name':'Number_of_discarded_goals',"value": discarded_goals_n},
                {'name':'minimal_depth',"value": min_depth,},
                {'name':'maximal_depth',"value": max_depth,},
                {'name':'average_depth',"value": average_depth,},
                {'name':'minimal_branching',"value": min_branching,},
                {'name':'maximal_branching',"value": max_branching,},
                {'name':'average_branching',"value": average_branching,},
            ]
        return tree_properties

    def discard_goal(goal_id):
        """
        Discards recursively a goal and his children
        :return:
        """
        goal = Goal.objects.get(id=goal_id)
        children = Goal.objects.filter(parent_id=goal_id)
        for c in children:
            Goal.discard_goal(c.id)
        goal.discarded = True
        goal.save()

    def serialize(self):
        return {
            "id": self.id,
            "tree_id": self.tree_id,
            "parent_id": self.parent_id,
            "title": self.title,
            "description": self.description,
            "discarded": self.discarded,
            "done": self.done,
        }


class PersonalGoal(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField("Zieltext", max_length=256)
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)


class Item(models.Model):
    id = models.AutoField(primary_key=True)
    questionnaire = models.CharField(max_length=256)
    code = models.CharField(max_length=256)
    text = models.CharField(max_length=256)
    latent_variable = models.CharField(max_length=256)
    answers = ArrayField(models.CharField(max_length=256))
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    given_answer = models.CharField(max_length=256, null=True)
    reverse_coded = models.BooleanField(default=False)
    personal_goal = models.ForeignKey(PersonalGoal, null=True, on_delete=models.SET_NULL)
    goal = models.ForeignKey(Goal, null=True, on_delete=models.SET_NULL)

    def get_big_five_items():
        with open(
                '{}/apps/construction/static/construction/data/questionnaires/big_five.csv'.format(settings.BASE_DIR),
                'r',
                encoding="utf-8") as file:
            reader = csv.reader(file, delimiter=";")

            big_five = []
            for row in reader:
                big_five.append({"code": row[0],
                                 "item_text": row[1],
                                 "answers": Item.get_likert_scale(4),
                                 })

        return big_five



    def get_gcq(n_items=3, language="en", version="V3", attention_checks=False, exclude_dimensions=[]):
        """
        Returns a list of dictionaries with GCQ items.
        @param n_items: Number of items per dimension to be returned
        @param language: "english" or "german", defining the language of items to be returned
        @param version: GCQ version, V2 or V3
        @param exclude_dimensions: list of gcq dimensions to be excluded
        """
        if language == "en":
            language="english"
            check_items=["Choose the answering option in the middle for all items.",
                     "Choose the answering option at the right for all items.",
                     "Choose the answering option at the left for all items.",]
        elif language == "de":
            language="german"
            check_items=["Wähle immer die mittlere Antwortoption aus.",
                     "Wähle immer die Anwortoption ganz rechts.",
                     "Wähle immer die Antwortoption ganz links."]


        gcq_file='{}/apps/construction/static/construction/data/questionnaires/2022_GCQ_full_goaltrees.csv'.format(settings.BASE_DIR)

        df_items=pd.read_csv(filepath_or_buffer=gcq_file,
                             sep=";",
                             )
        gcq_items = []

        item_label = "{}_item_{}".format(version, language)
        dimension_label = "factor_{}".format(language)
        description_label = "explanation_{}".format(language)

        for index, row in df_items.iterrows():

            # skip items higher than n_items
            if row["priority"] > int(n_items):
                continue

            # skip excluded dimensions
            elif row[dimension_label] in exclude_dimensions:
                continue

            gcq_items.append(
                {"code": "gcq_{}".format(row["id"]),
                "item_text": row[item_label],
                "answers": Item.get_likert_scale(7),
                "reverse_coded": bool(row["reverse_coded"]),
                "latent_variable": row[dimension_label],
                "latent_variable_description": row[description_label],
             })

            if attention_checks and (index % 10 == 0):
                gcq_items.append(
                    {"code": "attention_check_{}".format(index/10),
                     "item_text": random.choice(check_items),
                     "answers": Item.get_likert_scale(7),
                     "reverse_coded": False,
                     "latent_variable": "check",
                     "latent_variable_description": "check",
                     })

        return gcq_items


    # todo: deprecated, remove when studies done
    def get_gcq_items(file="gcq.csv", language="de"):
        print('{}/apps/construction/static/construction/data/questionnaires/{}'.format(settings.BASE_DIR, file))
        with open(
                '{}/apps/construction/static/construction/data/questionnaires/{}'.format(settings.BASE_DIR, file),
                'r',
                encoding="utf-8") as file:
            reader = csv.reader(file, delimiter=";")

            gcq_items = []
            latent_variable = ""
            for row in reader:
                if row[6]:
                    if language == "en":
                        latent_variable = row[1]
                    else:
                        latent_variable = row[6]
                if language == "en":
                    item_text = row[4]
                else:
                    item_text = row[7]
                gcq_items.append(
                    {"code": "gcq_{}".format(row[2]),
                     "item_text": item_text,
                     "answers": Item.get_likert_scale(7),
                     "reverse_coded": (True if row[3] == "R" else False),
                     "latent_variable": latent_variable,
                     })

        return gcq_items

    # todo: deprecated, remove when studies done
    def get_gcq_short_items():
        with open(
                '{}/apps/construction/static/construction/data/questionnaires/gcq_short.csv'.format(settings.BASE_DIR),
                'r',
                encoding="utf-8") as file:
            reader = csv.reader(file, delimiter=";")

            gcq_items = []
            latent_variable = ""
            for index, row in enumerate(reader):
                # skip first row
                if index == 0:
                    continue
                gcq_items.append(
                    {"code": "gcq_{}".format(row[1]),
                     "item_text": row[5],
                     "answers": Item.get_likert_scale(7),
                     "reverse_coded": (True if row[2] == "1" else False),
                     "latent_variable": row[3],
                     "latent_variable_description": row[6],
                     })
        return gcq_items

    def get_utility_measure_items():
        items = [
            # Intuitives Verständnis
            {"item_text": "Die Visualisierung war leicht verständlich.",
             "reverse_coded": False,
             "code": "utility_1"},
            {"item_text": "Es war schwierig die Visualisierung zu verstehen.",
             "reverse_coded": True,
             "code": "utility_2"},
            {"item_text": "Ich konnte mit gut vorstellen wo neue Ziele in der Visualisierung auftauchen würden.",
             "reverse_coded": False,
             "code": "utility_3"},
            # Nützlichkeit
            {"item_text": "Die Visualisierung hat mir geholfen zu verstehen wie meine Ziele zusammenhängen.",
             "reverse_coded": False,
             "code": "utility_4"},
            {"item_text": "Ich habe die Visualisierung als hilfreich empfunden.",
             "reverse_coded": False,
             "code": "utility_5"},
            {"item_text": "Die Visualisierung war übersichtlich.",
             "reverse_coded": False,
             "code": "utility_6"},
            {"item_text": "Die Visualisierung hat es mir leicht gemacht Teilziele anzulegen.",
             "reverse_coded": False,
             "code": "utility_7"},
            {"item_text": "Die Visualisierung ist hilfreich um die nächste Aktion auszuwählen.",
             "reverse_coded": False,
             "code": "utility_8"},
            {"item_text": "Die Visualisierung ist geeignet um Ziele zu priorisieren.",
             "reverse_coded": False,
             "code": "utility_9"},
            {"item_text": "Die Visualisierung kann helfen Zeit, Aufmerksamkeit und Arbeit zu lenken.",
             "reverse_coded": False,
             "code": "utility_10"},
            # Interesse an Nutzung
            {"item_text": "Ich könnte mir vorstellen eine solche Visualisierung zur Selbstorganisation zu nutzen.",
             "reverse_coded": False,
             "code": "utility_6"},
        ]
        utility_items = []
        for item in items:
            item["answers"] = Item.get_likert_scale(4)
            utility_items.append(item)
        return utility_items

    def get_nasa_tlx():
        lst = list(range(1, 21))
        nasa_tlx = [
            {
                "english": ["Mental Demand", "How mentally demanding was the task?"],
                "deutsch": ["Mentale Anforderung", "Wie anspruchsvoll war die Aufgabe mental?"],
                "left": "Sehr Niedrig",
                "right": "Sehr Hoch",
                "range": lst,
            },
            {
                "english": ["Physical Demand", "How physically demanding was the task?"],
                "deutsch": ["Physischer Anforderung", "Wie anspruchsvoll war die Aufgabe physisch?"],
                "left": "Sehr Niedrig",
                "right": "Sehr Hoch",
                "range": lst,
            },
            {
                "english": ["Temporal Demand", "How hurried was the pace of the task?"],
                "deutsch": ["Zeitliche Anforderung",
                            "Als wie stressig oder eilig hast Du den Zeitrahmen der Aufgabe erlebt?"],
                "left": "Sehr Niedrig",
                "right": "Sehr Hoch",
                "range": lst,
            },
            {
                "english": ["Performance", "How successful were you in accomplishing what you were asked to do?"],
                "deutsch": ["Performance", "Wie erfolgreich warst Du in der Bewältigung der Aufgabe?"],
                "left": "Perfekt",
                "right": "Versagen",
                "range": lst,
            },
            {
                "english": ["Effort", "How hard did you have to work to accomplish your level of performance?"],
                "deutsch": ["Anstrengung", "Wie sehr musstest Du Dich anstrengen um Dein Ergebnis zu erreichen?"],
                "left": "Sehr Niedrig",
                "right": "Sehr Hoch",
                "range": lst,
            },
            {
                "english": ["Frustration", "How insecure, discouraged, irritated, stressed and annoyed were you?"],
                "deutsch": ["Frustration", "Wie unsicher, entmutigt, irritiert, gestresst und verärgert warst Du?"],
                "left": "Sehr Niedrig",
                "right": "Sehr Hoch",
                "range": lst,
            },
        ]
        return nasa_tlx

    def get_personal_goal_items(request):
        """
        Return personal goals of a participant as items
        :return:
        """
        participant = Participant.get_current_participant(request)
        personal_goals = PersonalGoal.objects.filter(participant=participant)
        personal_goal_items = []
        for personal_goal in personal_goals:
            # each personal goal is represented as item
            personal_goal_items.append(
                {
                    "item_text": personal_goal.name,
                    "code": personal_goal.name,
                    "personal_goal": personal_goal,
                }
            )
        return personal_goal_items

    def get_tree_goal_items(request):
        """
        Return last tree goals ordered by depth of a participant as items
        :return:
        """
        tree_id = Goal.get_current_tree_id(request)
        root_goal = Goal.objects.get(
            tree_id=tree_id,
            parent_id=None,
        )
        goal_items = []
        children = [root_goal]
        while len(children) > 0:
            first_child = children.pop(0)
            goal_items.append(
                {
                    "item_text": first_child.title,
                    "code": first_child.title,
                    "goal": first_child,
                }
            )
            children.extend(Goal.objects.filter(parent_id=first_child.id, discarded=False).order_by("title"))
        return goal_items

    def get_goal_scores(participant, latent_variable, tree_id, min, max):
        """
        Calculates the normalized goal scores between 0 and 1 for the passed latent_variable
        :param min: minimum value
        :param max: maximum value
        :return:
        """
        latent_variable_items = Item.objects.filter(participant=participant, latent_variable=latent_variable, goal__tree_id=tree_id).order_by("created")

        # collect goals ordered by item creation date to preserve depth order
        goals = []
        for item in latent_variable_items:
            if item.goal not in goals:
                goals.append(item.goal)

        # calc score for each goal
        goal_scores = []
        for goal in goals:
            goal_items = latent_variable_items.filter(goal=goal)
            sum = 0
            for goal_item in goal_items:
                answer = float(goal_item.given_answer)
                sum += answer if not goal_item.reverse_coded else 1-answer
            score = sum / goal_items.count()
            normalized_score = (score - min) / (max - min)
            goal_scores.append({
                "id": goal.id,
                "title": goal.title,
                "score": normalized_score,
            })

        return goal_scores

    def get_scale_value(items):
        """
        transfer the value of likert scale from words into numbers
        """
        if items == 4:
            scale_value_dic_4 = {
                "trifft nicht zu": 1,
                "trifft eher nicht zu": 2,
                "trifft eher zu": 3,
                "trifft zu": 4}
            return scale_value_dic_4

        elif items == 5:
            scale_value_dic_5 = {
                "trifft nicht zu": 1,
                "trifft eher nicht zu": 2,
                "teils - teils": 3,
                "trifft eher zu": 4,
                "trifft zu": 5}
            return scale_value_dic_5

        elif items == 7:
            scale_value_dic_7 = {
                "trifft überhaupt nicht zu": 1,
                "trifft wenig zu": 2,
                "trifft eher nicht zu": 3,
                "teils teils": 4,
                "trifft eher zu": 5,
                "trifft viel zu": 6,
                "trifft vollständig zu": 7}
            return scale_value_dic_7

        else:
            return "no scale for {}".format(items)

    def get_likert_scale(items):

        if items == 4:
            likert_scale_answers_4 = [
                "trifft nicht zu",
                "trifft eher nicht zu",
                "trifft eher zu",
                "trifft zu"]
            return likert_scale_answers_4

        elif items == 5:
            likert_scale_answers_5 = [
                "trifft nicht zu",
                "trifft eher nicht zu",
                "teils - teils",
                "trifft eher zu",
                "trifft zu"]
            return likert_scale_answers_5

        elif items == 7:
            likert_scale_answers_7 = [
                "trifft überhaupt nicht zu",
                "trifft wenig zu",
                "trifft eher nicht zu",
                "teils teils",
                "trifft eher zu",
                "trifft viel zu",
                "trifft vollständig zu"]
            return likert_scale_answers_7

        else:
            return "no scale for {}".format(items)

    def get_next_view(questionnaire):
        """
        provides the redirection views for the different questionnaires
        """
        next_view = {
            "big_five": "/instructions",
            "utility_measure": "/thankyou",
            "gcq": "/open_questions",
        }
        return next_view.get(questionnaire, "/welcome")


class Question(models.Model):
    id = models.AutoField(primary_key=True)
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    question = models.CharField(max_length=512)
    answer = models.CharField(max_length=2048)
    type = models.CharField(max_length=128, null=True)
    created = models.DateTimeField(auto_now_add=True)
    tree = models.ForeignKey(Goal, on_delete=models.CASCADE, null=True)

    def get_open_questions():
        questions = [
            {
                "type": "text",
                "text": "Was für ein Endgerät hast du verwendet (Tablet, Notebook, PC, Smartphone..)?",
            },
            {
                "type": "text",
                "text": "Was ist Dir noch aufgefallen?",
            },
            {
                "type": "text",
                "text": "Möchtest Du uns ein technisches Problem mitteilen?"
            },
        ]
        return questions


class UserInteraction(models.Model):
    """
    Logs all user actions
    duration: timespan between last two actions in milliseconds
    """
    id = models.AutoField(primary_key=True)
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    duration = models.IntegerField(null=True)
    route = models.CharField(max_length=128)
    action = models.CharField(max_length=256)
    target_id = models.CharField(max_length=256, null=True)
    goal = models.ForeignKey(Goal, on_delete=models.SET_NULL, null=True)
    item = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True)
    question = models.ForeignKey(Question, on_delete=models.SET_NULL, null=True)

    def create_interaction(request, action, item):
        participant = Participant.get_current_participant(request)
        participant_actions = UserInteraction.objects.filter(participant=participant)
        last_action = None
        if participant_actions:
            # get last created action
            last_action = participant_actions.latest("timestamp")

        action = UserInteraction.objects.create(
            participant=participant,
            route=request.path,
            action=action,
        )

        # save item id
        if item and hasattr(item, "id"):
            action.target_id = item.id

        if item.__class__.__name__ == "Goal":
            action.goal = item
        elif item.__class__.__name__ == "Item":
            action.item = item
        elif item.__class__.__name__ == "Question":
            action.question = item

        if last_action:
            delta = action.timestamp - last_action.timestamp
            # milliseconds
            action.duration = delta.total_seconds() * 1000
        action.save()
        return action


