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
                   "title": "Willkommen zur Studie zu persönlichen Studienzielen.",
                   "text": """<p> 
                   Im ersten Schritt wirst du zur Einstimmung Fragen zu deiner idealen Zukunft und deinem idealen 
                   Studium beantworten um dann eigene Studienziele zu benennen.
                   <br>
                   Im zweiten Schritt wirst du eines deiner Studienziele in Teilziele zerlegen und ein 
                   System aus konkreteren Teilzielen dazu erstellen.
                   <br><br>
                   Im dritten Schritt wirst du für deine Ziele auf einer Skala einschätzen, inwiefern eine Reihe von 
                   Aussagen auf sie zutrifft. 
                   <br><br>
                   Der gesamte Vorgang dauert ca. 45 Minuten. Um gute Ergebnisse zu bekommen sorgst du am besten für eine
                   störungsfreie Atmosphäre (Handy aus, E-Mail Postfach zu, nur diesen Tab im Browser öffnen) und wählst einen Zeitraum, in dem du 
                   dich ganz auf die Übung konzentrieren kannst.     
                    </p>""",
                   "iframe": True,
                   "show_progress": False,
                   "progress_value": 1,
               }
           }
        )

        self.sequence.append("consent")
        StudyContext.objects.update_or_create(study=self.study, view="consent",
                defaults={
                    "context": {
                        "title": "Einverständniserklärung",
                        "text": """<p> Du hast dich freiwillig zur Teilnahme an dieser Studie gemeldet. Hier erhältst Du nun einige Informationen zu
                            deinen Rechten und zum Ablauf der Studie. Bitte lese die folgenden Abschnitte sorgfältig durch. </p>

                            <h2>1. Zweck der Studie</h2>
                            <p> Ziel dieser Studie ist es, neue Erkenntnisse über Visualisierungen von hierarchischen Zielsystemen zu gewinnen.
                            Die gesammelten Informationen sollen dazu beitragen, Studierende beim Setzen individueller Bildungsziele zu
                            unterstützen. </p>

                            <h2>2. Ablauf der Studie</h2>
                            <p> Du wirst zu einem eigenen Bildungsziel ein hierarchisches Zielsystem erstellen, sowie davor und
                            danach einige Fragen beantworten. Das Zielsystem stellt deine Ziele mit Teilzielen und Aktionen dar,
                            sodass Wege zum Erreichen der Ziele klarer werden. </p>

                            <h2>3. Risiken und Nebenwirkungen</h2>
                            <p> Diese Studie ist nach derzeitigem Wissensstand ungefährlich. Durch deine Teilnahme an dieser Studie setzt Du
                            dich keinen besonderen Risiken aus und es sind keine Nebenwirkungen bekannt. Auswirkungen auf die
                            Lernleistung sind laut derzeitigem Wissensstand eher förderlich. </p>

                            <h2>4. Abbruch des Experiments</h2>
                            <p> Du hast das Recht, diese Studie zu jedem Zeitpunkt und ohne Angabe eines Grundes abzubrechen. Deine
                            Teilnahme ist vollkommen freiwillig und ohne Verpflichtungen. Es entstehen Dir keine Nachteile durch einen
                            Abbruch. </p>

                            <h2>5. Vertraulichkeit</h2>
                            <p> Die Bestimmungen des Datenschutzes werden eingehalten. Personenbezogene Daten werden von uns nicht an
                            Dritte weitergegeben. Die erfassten Daten werden in anonymisierter Form verarbeitet und für wissenschaftliche
                            Zwecke in Forschungsdatenrepositorien publiziert. </p> 

                            <h2>Einverständniserklärung</h2>
                            <p> Bitte bestätige durch Klicken auf den Button die folgende Aussage:
                            “Hiermit bestätige ich, dass ich über Zwecke, Ablauf und nicht auszuschließende Nebenwirkungen der Studie
                            aufgeklärt und informiert worden bin. Ich habe diese Erklärung gelesen und verstanden. Ich stimme jedem der
                            Punkte zu. Ich ermächtige hiermit die von mir in dieser Untersuchung erworbenen Daten zu wissenschaftlichen
                            Zwecken zu analysieren und in wissenschaftlichen Arbeiten anonymisiert zu veröffentlichen. Ich wurde über
                            meine Rechte als Versuchsperson informiert und erkläre mich zu der freiwilligen Teilnahme an dieser Studie
                            bereit.” </p>""",
                        "show_progress": False,
                        "progress_value": 2,
                        }
                    }
                )

        self.sequence.append("userdata")
        StudyContext.objects.update_or_create(study=self.study, view="userdata",
            defaults={
                "context": {
                        "title": "Anmeldung",
                        "introduction": "Fragen zu Studiengang und Vorerfahrungen.",
                        "required": False,
                        "show_progress": True,
                        "progress_value": 1,
                }
            }

        )

        self.sequence.append("open_questions/goal_question_1")
        StudyContext.objects.update_or_create(study=self.study, view="goal_question_1",
           defaults={
               "context": {
                   "title": "Frage 1 zu Deiner idealen Zukunft",
                   "introduction": """<p> Du wirst nun drei Fragen zu Deiner Zukunft sehen und Zeit haben, über sie nachzudenken. 
                   Die Fragen helfen bei der Entwicklung individueller Bildungsziele. Bitte nimm Dir pro Frage ca. <b>2 Minuten</b> Zeit.</p>""",
                   "questions": [
                       {
                           "type": "text",
                           "text": "Wie stellst Du Dir Deine ideale Zukunft bis zu Deinem Lebensende vor? (> 200 Buchstaben)",
                           "rows": 3,
                           "required": True,
                       },
                   ],
                   "min_answer_length": 200,   # minimum textarea char number
                   "iframe": True,
                   "show_progress": True,
                   "progress_value": 5,
               }
           }
        )

        self.sequence.append("open_questions/goal_question_2")
        StudyContext.objects.update_or_create(study=self.study, view="goal_question_2",
           defaults={
               "context": {
                   "title": "Frage 2 zu Deiner idealen Zukunft",
                   "introduction": """<p>Bitte nimm Dir pro Frage ca. <b>2 Minuten</b> Zeit.</p>""",
                   "questions": [
                       {
                           "type": "text",
                           "text": "Was waren die Gründe dafür, dass Du Dich für ein Studium entschieden hast? (> 200 Buchstaben)",
                           "rows": 3,
                           "required": True,
                       },
                   ],
                   "min_answer_length": 200,   # minimum textarea char number
                   "iframe": True,
                   "show_progress": True,
                   "progress_value": 8,
               }
           }
        )

        self.sequence.append("open_questions/goal_question_3")
        StudyContext.objects.update_or_create(study=self.study, view="goal_question_3",
           defaults={
               "context": {
                   "title": "Frage 3 zu Deiner idealen Zukunft",
                   "introduction": """<p>Bitte nimm Dir pro Frage ca. <b>2 Minuten</b> Zeit.</p>""",
                   "questions": [
                       {
                           "type": "text",
                           "text": "Stell' Dir vor Du stehst am Ende Deines Studiums. Wie sollte es verlaufen sein, damit "
                                   "Du zufrieden darauf zurückblicken kannst? (> 200 Buchstaben)",
                           "rows": 3,
                           "required": True,
                       },
                   ],
                   "min_answer_length": 200,   # minimum textarea char number
                   "iframe": True,
                   "show_progress": True,
                   "progress_value": 12,
               }
           }
        )


        self.sequence.append("personal_goals")
        StudyContext.objects.update_or_create(study=self.study, view="personal_goals",
            defaults={
                "context": {
                    "title": """Wichtige Ziele im Studium""",
                    "introduction": """<p>Welche Ziele möchtest Du während Deines Studiums erreichen? 
                                    <br>
                                    Formuliere Deine <b>drei wichtigsten Ziele</b> möglichst als ganze Sätze und möglichst verständlich.</p>""",
                    "max_title_length": 128,
                    "min_number_goals": 1,
                    "iframe": True,
                    "show_progress": True,
                    "progress_value": 13,
                }
            }
        )

        gcq_items = Item.get_gcq(language="de", n_items=1)
        for i in range(len(gcq_items)):
            item = gcq_items[i]
            self.sequence.append("questionnaire/pre_goal_characteristics_questionnaire_item_{}".format(str(i+1)))
            StudyContext.objects.update_or_create(study=self.study, view="pre_goal_characteristics_questionnaire_item_{}".format(str(i+1)),
                defaults={
                    "context": {
                        "title": "",
                        "personal_goal_items": True,        # if true last tree goals are listed in each row as items
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
                        "progress_value": round(13 + (9 / len(gcq_items) * i)),  # calculates progress based on length of items,
                    }
                }
            )

        self.sequence.append("example_tree")
        example_root = self.init_example_tree()
        example_tree = Goal.get_children(example_root.id)
        StudyContext.objects.update_or_create(study=self.study, view="example_tree",
            defaults={
                "context": {
                    "title": "Zielsystem: Ein Beispiel",
                    "text": """<p> Hier siehst Du ein Zielsystem mit einem Hauptziel, welches in konkretere Teilziele aufgegliedert ist.
                              </p>""",
                    "tree_id": example_root.id,
                    "tree": json.dumps(example_tree),
                    "condition": "3",   # show dendrogram
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
                                
                                    <p> Unten rechts ist das nachzubauende Zielsystem abgebildet, links ist Dein Zielsystem, das am Ende
                                    genauso oder ähnlich aussehen sollte. Die Reihenfolge, in der gleichrangige Unterziele geordnet
                                    sind, spielt hierbei keine Rolle. Während der Bearbeitung kann die Visualisierung von Deinem
                                    Zielsystem anders aussehen. Dies wird sich aber zunehmend anpassen, wenn die allgemeine
                                    Struktur mit der Vorlage übereinstimmt. </p>""",
                   "tree_title": "Dein hierarchisches Zielsystem",
                   "example_tree_title": "Vorgegebenes Zielsystem",
                   "example_tree_id": task_example_root.id,
                   "example_tree": json.dumps(task_example_tree),
                   "condition": "3",  # show dendrogram
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
                    "introduction": """<p> Hier kannst Du Dein persönliches Bildungsziel auswählen, für das Du
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
                    "condition": "3",  # show dendrogram
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
            self.sequence.append("questionnaire/post_goal_characteristics_questionnaire_item_{}".format(str(i+1)))
            StudyContext.objects.update_or_create(study=self.study, view="post_goal_characteristics_questionnaire_item_{}".format(str(i+1)),
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
                        "title": "Studie abgeschlossen!",
                        "text": """<p>Glückwunsch! Du hast alle Aufgaben der Studie erledigt. Wir hoffen, Du konntest 
                                    inspirierende und erfüllende Ziele entwickeln.</p>

                            <p>Wenn Du Versuchspersonenstunden bekommen oder an der Verlosung von Amazon 
                            Gutscheinen teilnehmen möchtest, sende eine E-Mail an mit dem Code 
                            <b>VP {timestamp}</b> an <a href='mailto:fweber@uni-osnabrueck.de'>fweber@uni-osnabrueck.de</a> 
                            </p>""",
                        "text_bottom": """<p>Danke für Deine Teilnahme an der Studie und viel Erfolg bei Deinen 
                                        Zielen. Du kannst den Tab nun schließen.</p>""",
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
            title="Erfolgreiches Abitur",  # When title changed, a new sample tree will be created in database
            is_example=True,
            example_id=1,
            study=self.study,
            defaults={
                "tree_id": Goal.objects.aggregate(Max('tree_id'))['tree_id__max'] + 1,
            }
        )[0]
        root.save()

        goal_2 = self.create_node(2, root, title="Einen Notendurchschnitt besser als 2.5 erreichen.")
        goal_3 = self.create_node(3, root, title="fit für's Studium werden")
        goal_4 = self.create_node(4, root, title="Tolle Abiturfeiern organisieren und erleben.")

        goal_5 = self.create_node(5, goal_2, title="Die Matheprüfung mit mindestens 2.2 bestehen.")
        goal_6 = self.create_node(6, goal_2, title="Kursdurchschnitt von besser als 2.5 erreichen")
        goal_7 = self.create_node(7, goal_2, title="die mündliche Prüfung bestehen")

        goal_8 = self.create_node(8, goal_3, title="eigene Lernzeiten einhalten")
        goal_9 = self.create_node(9, goal_3, title="Lerngruppen organisieren")
        goal_10 = self.create_node(10, goal_3, title="eigene Interessen entdecken")

        goal_11 = self.create_node(11, goal_4, title="Die Abiturzeitung mit gestalten")
        goal_12 = self.create_node(12, goal_4, title="Familie einladen")
        goal_13 = self.create_node(13, goal_4, title="Vorbereitungen mit Freunden")

        # delete possible remaining example goals
        Goal.objects.filter(is_example=True, study=self.study, tree_id=root.tree_id, example_id__gt=13).delete()

        return root

    def init_task_example_tree(self):
        """ Creates example tree for practical task """
        # todo: create proper example tree
        root = Goal.objects.get_or_create(
            title="Mein Studienziel",  # When title changed, a new sample tree will be created in database
            is_example=True,
            example_id=1,
            study=self.study,
            defaults={
                "tree_id": Goal.objects.aggregate(Max('tree_id'))['tree_id__max'] + 1,
            }
        )[0]
        root.save()

        goal_2 = self.create_node(2, root, title="Teilziel 1")
        goal_3 = self.create_node(3, root, title="Teilziel 2")

        action_1 = self.create_node(4, goal_2, title="konkrete Aktion 1")
        action_2 = self.create_node(5, goal_2, title="konkrete Aktion 2")
        action_3 = self.create_node(6, goal_2, title="konkrete Aktion 2")

        # delete possible remaining example goals
        Goal.objects.filter(is_example=True, study=self.study, tree_id=root.tree_id, example_id__gt=6).delete()

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
