from apps.construction.studies.STUDY_BASE import STUDY_BASE
from apps.construction.models import Study, StudyContext, Goal, Item

from django.db.models import Max

import json


class STUDY_hgs(STUDY_BASE):
    """
    P3 study
    """

    def __init__(self):
        super().__init__()
        self.name = "hgs_study"
        self.sequence = []
        self.study = Study.objects.update_or_create(
            name=self.name,
            classname=self.get_class_name(),
            defaults={
                "sequence": self.sequence,
                "language": "de",
            },
        )[0]

    def init_contexts(self):
        self.sequence.append("welcome")
        StudyContext.objects.update_or_create(study=self.study, view="welcome",
           defaults={
               "context": {
                   "title": "Willkommen im digitalen Assistenten zu persönlichen Studienzielen.",
                   "text": """<p> Hier bekommst Du Anregungen dazu, dir über deine ganz eigenen Motive und Ziele im 
                   Studium bewusster zu werden um dann zu planen wie du diese in die Tat umsetzen kannst. Darüber hinaus 
                   kannst du Fragen zu deinen Zielen beantworten um Charakteristika deiner Ziele zu erfassen. Im Anschluss 
                   bekommst du Forschungsergebnisse zu Zielcharakteristika und ihre Bedeutung für deine konkreten Ziele
                   zurückgemeldet. 
                   <br><br>
                   Im ersten Schritt wirst du zur Einstimmung Fragen zu deiner idealen Zukunft und deinem idealen 
                   Studium beantworten um dann eigene Studienziele zu benennen.
                   <br>
                   Im zweiten Schritt wirst du eines deiner Studienziele in Teilziele zerlegen und ein hierarchisches 
                   Zielsystem daraus erstellen.
                   <br><br>
                   Im dritten Schritt wirst du für deine Ziele auf einer Skala einschätzen, inwiefern eine Reihe von 
                   Aussagen auf sie zutrifft. Im Anschluss bekommst du quantitative Informationen zu den Charakteristika 
                   deiner Ziele und der Bedeutung davon.
                   <br><br>
                   Der gesamte Vorgang dauert ca. 45 Minuten. Um gute Ergebnisse zu bekommen sorgst du am besten für eine
                   störungsfreie Atmosphäre (Handy aus, E-Mail Postfach aus...) und wählst einen Zeitraum, in dem du 
                   dich ganz auf die Übung konzentrieren kannst.     
                    </p>""",
                   "iframe": True,
                   "show_progress": True,
                   "progress_value": 0,
               }
           }
        )

        self.sequence.append("open_questions/goal_questions")
        StudyContext.objects.update_or_create(study=self.study, view="goal_questions",
           defaults={
               "context": {
                   "title": "Fragen zu deiner idealen Zukunft",
                   "introduction": """<p> Um deine Aufmerksamkeit darauf zu richten, was für dich ganz persönlich im 
                   Leben und im Studium wirklich wichtig ist, beantworte bitte zunächst die folgenden Fragen. 
                   Du kannst dir für jede Frage ca. zwei Minuten Zeit nehmen und deine Überlegungen auf ein Blatt Papier 
                   und/oder in die Textfelder schreiben.</p>""",
                   "questions": [
                       {
                           "type": "text",
                           "text": "Wie stellst du dir deine ideale Zukunft bis zu Deinem Ende ungefähr vor? (min. 200 Buchstaben)",
                           "rows": 3,
                           "required": True,
                       },
                       {
                           "type": "text",
                           "text": "Was waren die Gründe dafür, dass du dich für ein Studium entschieden hast? (min. 200 Buchstaben)",
                           "rows": 3,
                           "required": True,
                       },
                       {
                           "type": "text",
                           "text": "Stell' dir vor du stehst am Ende deines Studiums. Wie sollte es verlaufen sein, damit "
                                   "du zufrieden darauf zurückblicken kannst? (min. 200 Buchstaben)",
                           "rows": 3,
                           "required": True,
                       },
                   ],
                   "min_answer_length": 200,   # minimum textarea char number
                   "iframe": True,
                   "show_progress": True,
                   "progress_value": 2,
               }
           }
        )

        self.sequence.append("personal_goals")
        StudyContext.objects.update_or_create(study=self.study, view="personal_goals",
            defaults={
                "context": {
                    "title": """Meine Ziele im Studium""",
                    "introduction": """<p> Basierend auf deinen vorherigen Überlegungen: Welche (abstrakten) Ziele 
                    möchtest du während deines Studiums erreichen? </p>""",
                    "max_title_length": 128,
                    "min_number_goals": 1,
                    "iframe": True,
                    "show_progress": True,
                    "progress_value": 5,
                }
            }
        )

        self.sequence.append("example_tree")
        example_root = self.init_example_tree()
        example_tree = Goal.get_children(example_root.id)
        StudyContext.objects.update_or_create(study=self.study, view="example_tree",
            defaults={
                "context": {
                    "title": "Ein praktisches Beispiel",
                    "text": """<p> Hier siehst du ein Zielsystem mit einem Hauptziel. Die Teilziele werden konkreter und 
                            detaillierter, bis sie schließlich in konkreten Aktionen und Strategien enden. 
                            Im Idealfall wird jedes Ziel in konkrete Aktionen heruntergebrochen. </p>""",
                    "tree_id": example_root.id,
                    "tree": json.dumps(example_tree),
                    "condition": "3",   # show dendogram
                    "iframe": True,
                    "show_progress": True,
                    "progress_value": 22,
                }
            }
        )

        # create task example tree
        task_example_root = self.init_task_example_tree()
        task_example_tree = Goal.get_children(task_example_root.id)

        # creates new tree with root node
        self.sequence.append("new_tree/{}/{}".format(task_example_root.title, task_example_root.tree_id))

        self.sequence.append("tree_construction/0/practical_task")
        StudyContext.objects.update_or_create(study=self.study, view="practical_task",
           defaults={
               "context": {
                   "title": "Praktisches Beispiel",
                   "introduction": """<p> Als Nächstes wirst Du ein exemplarisches hierarchisches Zielsystem nachbauen. </p> 
                                
                                    <p> Unten rechts ist das nachzubauende Zielsystem abgebildet, links ist dein Zielsystem, das am Ende
                                    genauso oder ähnlich aussehen sollte. Die Reihenfolge, in der gleichrangige Unterziele geordnet
                                    sind, spielt hierbei keine Rolle. Während der Bearbeitung kann die Visualisierung von deinem
                                    Zielsystem anders aussehen. Dies wird sich aber zunehmend anpassen, wenn die allgemeine
                                    Struktur mit der Vorlage übereinstimmt. </p>""",
                   "tree_title": "Dein hierarchisches Zielsystem",
                   "example_tree_title": "Vorgegebenes Zielsystem",
                   "example_tree_id": task_example_root.id,
                   "example_tree": json.dumps(task_example_tree),
                   "condition": "3",  # show dendogram
                   "tree_color": "#28497c",
                   "show_tree_first": True,
                   "description_enabled": False,
                   "iframe": True,
                   "show_progress": True,
                   "progress_value": 25,
               }
           }
        )

        self.sequence.append("personal_goal_selection")
        StudyContext.objects.update_or_create(study=self.study, view="personal_goal_selection",
            defaults={
                "context": {
                    "title": "Persönliches Bildungsziel auswählen",
                    "introduction": """<p> Hier kannst du dein persönliches Bildungsziel auswählen, für das du
                                    auf der nächsten Seite ein Zielsystem erstellen wirst. </p>""",
                    "iframe": True,
                    "show_progress": True,
                    "progress_value": 30,
                }
            }
        )

        self.sequence.append("tree_construction")
        StudyContext.objects.update_or_create(study=self.study, view="tree_construction",
            defaults={
                "context": {
                    "title": "Eigenes Zielsystem",
                    "introduction": """<p> Nun wirst Du zu Deinem ausgewählten Bildungsziel ein hierarchisches Zielsystem erstellen. Bitte
                                    versuche Deine Ziele in erforderliche Teilziele und Aktionen so aufzugliedern, dass die
                                    Wege zum Erreichen der Bildungsziele klarer und zunehmend konkret werden. </p>""",
                    # "condition_selector": True,
                    "max_title_length": 128,
                    "condition": "3",  # show dendogram
                    "description_enabled": False,
                    "show_tree_first": True,
                    "tree_color": "#28497c",
                    "iframe": True,
                    "show_progress": True,
                    "progress_value": 32,
                }
            }
        )

        gcq_items = Item.get_gcq(language="de", n_items=1)
        for i in range(len(gcq_items)):
            item = gcq_items[i]
            self.sequence.append("questionnaire/goal_characteristics_questionnaire_item_{}".format(str(i+1)))
            StudyContext.objects.update_or_create(study=self.study, view="goal_characteristics_questionnaire_item_{}".format(str(i+1)),
                defaults={
                    "context": {
                        "title": "",
                        "tree_goal_items": True,        # if true last tree goals are listed in each row as items
                        "item_text": """<p style='font-weight: bold;font-size: x-large;'>
                                        {} ({}/{})</p>""".format(item.get("item_text", ""), i+1, len(gcq_items)),    # overrides the item text of the goal item
                        "code": item.get("code", ""),                                   # overrides the item code of the goal item
                        "latent_variable": item.get("latent_variable", ""),             # overrides the item latent_variable of the goal item
                        "reverse_coded": item.get("reverse_coded", ""),      # overrides the item reverse_coded
                        "answers": ["Stimme überhaupt nicht zu", "Stimme nicht zu", "Stimme weder zu noch lehne ab", "Stimme zu", "Stimme voll und ganz zu"],
                        "type": "slider",
                        "slider_min": 0,                # minimum slider value
                        "slider_max": 1,                # maximum slider value
                        "slider_step": 0.01,            # slider step length
                        "required": True,
                        "iframe": True,
                        "show_progress": True,
                        "progress_value": round(50 + (50 / len(gcq_items) * i)),  # calculates progress based on length of items,
                    }
                }
            )

        self.sequence.append("thankyou")
        StudyContext.objects.update_or_create(study=self.study, view="thankyou",
            defaults={
                "context": {
                        "title": "Study Completed",
                        "text": """<p>Congratulations! You have completed all tasks of the study. We hope you have found goals that are
                            inspiring and fulfilling.</p>

                            <p>If you want to achieve VP hours, please send an email to 
                            <a href='mailto:fweber@uni-osnabrueck.de'>fweber@uni-osnabrueck.de</a> including your
                            <b>Matrikel-Nr. and major</b> with the subject “<b>VP {timestamp}</b>”</p>

                            <p>If you have any questions about the digital study assistant, contact us at 
                            <a href='mailto:fweber@uni-osnabrueck.de'>fweber@uni-osnabrueck.de</a>.</p>""",
                        "text_bottom": """<p><b>Thank you for participating in our study, and good luck with your goals! You can close the
                                    browser now.</b></p>""",
                        "show_progress": True,
                        "progress_value": 100,
                }
            }
        )

        number_backward_steps = len(gcq_items) + 3  # go back to tree construction
        self.sequence.append("previous_view/" + str(number_backward_steps))

        self.study.sequence = self.sequence
        self.study.save()


    def init_example_tree(self):
        """ Creates example tree """
        root = Goal.objects.get_or_create(
            title="Abitur",  # When title changed, a new sample tree will be created in database
            is_example=True,
            example_id=1,
            study=self.study,
            defaults={
                "tree_id": Goal.objects.aggregate(Max('tree_id'))['tree_id__max'] + 1,
            }
        )[0]
        root.save()

        goal_2 = self.create_node(2, root, title="Notendurchschnitt besser als 2.5")
        goal_3 = self.create_node(3, root, title="fit für's Studium werden")
        goal_4 = self.create_node(4, root, title="tolle Abiturfeiern")

        goal_5 = self.create_node(5, goal_2, title="Matheprüfung mindestens 2.2")
        goal_6 = self.create_node(6, goal_2, title="Kursdurchschnitt besser als 2.5")
        goal_7 = self.create_node(7, goal_2, title="mündliche Prüfung bestehen")

        goal_8 = self.create_node(8, goal_3, title="Lernzeiten einhalten")
        goal_9 = self.create_node(9, goal_3, title="Lerngruppen organisieren")
        goal_10 = self.create_node(10, goal_3, title="eigene Interessen entdecken")

        goal_11 = self.create_node(11, goal_4, title="Abiturzeitung mitgestalten")
        goal_12 = self.create_node(12, goal_4, title="Familie einladen")
        goal_13 = self.create_node(13, goal_4, title="Vorbereitungen mit Freunden")

        # delete possible remaining example goals
        Goal.objects.filter(is_example=True, study=self.study, tree_id=root.tree_id, example_id__gt=13).delete()

        return root

    def init_task_example_tree(self):
        """ Creates example tree for practical task """
        # todo: create proper example tree
        root = Goal.objects.get_or_create(
            title="Beispiel",  # When title changed, a new sample tree will be created in database
            is_example=True,
            example_id=1,
            study=self.study,
            defaults={
                "tree_id": Goal.objects.aggregate(Max('tree_id'))['tree_id__max'] + 1,
            }
        )[0]
        root.save()

        goal_2 = self.create_node(2, root, title="Zweig 1")
        goal_3 = self.create_node(3, root, title="Zweig 2")

        # delete possible remaining example goals
        Goal.objects.filter(is_example=True, study=self.study, tree_id=root.tree_id, example_id__gt=3).delete()

        return root

    def create_node(self, example_id, parent, title):
        return Goal.objects.update_or_create(
            tree_id=parent.tree_id,
            is_example=True,
            example_id=example_id,
            study=self.study,
            defaults={
                "title": title,
                "parent_id": parent.id,
            }
        )[0]
