from apps.construction.studies.STUDY_BASE import STUDY_BASE
from apps.construction.models import Study, StudyContext, Goal, Item, Participant, UserInteraction, Question

from django.db.models import Max, Sum

import json
import pandas as pd


class STUDY_pilot_study(STUDY_BASE):
    """
    Jana's study
    """

    def __init__(self):
        super().__init__()
        self.name = "pilot_study"
        self.description = "Untersucht Usability und UX."
        self.active = False
        self.duration = 1
        self.sequence = ["welcome", "consent", "userdata", "new_tree/Abitur", "tree_construction/0/practical_task", "questionnaire/after_scenario", "questionnaire/sus", "open_questions/visualization_questions", "personal_goals", "process_personal_goals", "tree_construction", "questionnaire/personal_goals_questionnaire", "process_personal_goals", "open_questions/usability_open_questions", "thankyou"]
        self.study = Study.objects.update_or_create(
            name=self.name,
            classname=self.get_class_name(),
            defaults={
                "sequence": self.sequence,
                "language": "de",
                "conditions": [],
            },
        )[0]

    def init_contexts(self):
        # create view contents
        StudyContext.objects.update_or_create(study=self.study, view="welcome",
           defaults={
               "context": {
                   "title": "Willkommen zur Studie über Zielsysteme!",
                   "text": """<p style="font-weight: bold;"> Diese Studie ist beendet. Vielen Dank an alle, die 
                            teilgenommen haben! Ab jetzt werden die Versuchspersonenstunden nicht mehr vergeben. </p>
                   
                            <p> Uns interessiert welche Bildungsziele Studierende haben und wie diese effektiv strukturiert werden
                            können. Frühere Studien haben gezeigt, dass Klarheit über die eigenen Ziele dabei helfen kann,
                            diese zu erreichen. Du kannst also durch die Teilnahme an unserer Studie nicht nur eine
                            Versuchspersonenstunde erwerben, sondern auch mehr Klarheit über deine Ziele gewinnen und
                            deine Chancen, sie zu erreichen, verbessern. </p> 
                            
                            <p> In der aktuellen Entwicklungsphase geht es darum, die optimale Darstellung für einen Digitalen
                            Assistenten zu finden. Du wirst in der Trainingsphase eine von vier möglichen Darstellungen nutzen
                            und wirst im Anschluss gebeten, diese auszuwerten. In der Praxisphase kannst Du dann Deine
                            eigenen Bildungsziele mittels verschiedener Darstellungen von hierarchischen Zielsystemen
                            formulieren und erneut Fragen zur empfundenen Benutzerfreundlichkeit beantworten. </p>
                            
                            <p> Aus technischen Gründen ist es im Rahmen dieser Studie leider nicht möglich, auf die schon
                            versandten Formulare zuzugreifen. Auch wirst Du den „Zurück“-Button in Deinem Browser nicht
                            nutzen können. Kontrolliere also bitte Deine Eingaben jedes mal bevor Du auf „Weiter“ oder
                            „Absenden“ klickst. </p>
                            
                            <p> Versuche bitte die Fragen möglichst ehrlich zu beantworten und denk daran, dass in dieser Studie
                            nicht Deine Performance, sondern die Benutzerfreundlichkeit der Software untersucht werden soll. 
                            Insgesamt wird die Bearbeitung des Fragebogens ungefähr eine Stunde in Anspruch nehmen. Bitte
                            versuche so wenig Pausen wie möglich zu machen. </p>"""
               }
           }
        )
        StudyContext.objects.update_or_create(study=self.study, view="consent",
           defaults={
               "context": {
                   "title": "Einverständniserklärung",
                   "text": """<p> Du hast Dich freiwillig zur Teilnahme an dieser Studie gemeldet. Hier erhältst Du nun einige
                            Informationen zu Deinen Rechten und zum Ablauf der Studie. Bitte lies die folgenden Abschnitte
                            sorgfältig durch. </p> 
                        
                            <h2>1. Ablauf der Studie </h2> 
                            <p> Deine Aufgabe ist es, ein hierarchisches Zielsystem nachzubauen, sowie davor und danach einige
                            Fragen zu beantworten. In der Trainingsphase wirst Du eine hierarchische Struktur nach einem
                            vorgegeben Muster nachbauen, die den Weg zum exemplarischen Bildungszweck „Abitur“ darstellt.
                            Danach wirst Du zu vier eigenen Bildungszielen jeweils ein hierarchisches Zielsystem erstellen.
                            Dabei sollen diese Ziele so in erforderliche Teilziele und Aktionen aufgegliedert werden, dass die
                            Wege zum Erreichen der Bildungsziele klarer werden. </p>
                        
                            <h2>2. Risiken und Nebenwirkungen</h2>
                            <p> Durch Deine Teilnahme an dieser Studie setzt Du Dich keinen besonderen Risiken aus und es sind
                            keine Nebenwirkungen bekannt. Auswirkungen auf die Lernleistung könnten laut derzeitigem
                            Wissensstand eher positiv sein. </p>
                        
                            <h2>3. Abbruch des Experiments</h2> 
                            <p> Du hast das Recht, diese Studie zu jedem Zeitpunkt und ohne Angabe eines Grundes abzubrechen.
                            Deine Teilnahme ist vollkommen freiwillig und ohne Verpflichtungen. Es entstehen Dir keine
                            Nachteile durch einen Abbruch. </p> 
                        
                            <h2>4. Vertraulichkeit</h2> 
                            <p> Die Bestimmungen des Datenschutzes werden eingehalten. Personenbezogene Daten werden von
                            uns nicht an Dritte weitergegeben. Die erfassten Daten werden in anonymisierter Form verarbeitet
                            und ausschließlich für wissenschaftliche Zwecke in Forschungsdatenrepositorien publiziert. </p>
                        
                            <h2>Einverständniserklärung</h2> 
                            <p> Bitte bestätige durchs Klicken auf den unteren Button die folgende Aussage:
                            “Hiermit bestätige ich, dass ich über Zwecke und Ablauf der Studie aufgeklärt und informiert
                            worden bin. Ich habe diese Erklärung gelesen und verstanden. Ich stimme jedem der Punkte zu. Ich
                            ermächtige hiermit die von mir in dieser Untersuchung erworbenen Daten zu wissenschaftlichen
                            Zwecken zu analysieren und in wissenschaftlichen Arbeiten anonymisiert zu veröffentlichen. Ich
                            wurde über meine Rechte als Versuchsperson informiert und erkläre mich zu der freiwilligen
                            Teilnahme an dieser Studie bereit.” </p> """
               }
           }
        )
        StudyContext.objects.update_or_create(study=self.study, view="userdata",
            defaults={
                "context": {
                    "introduction": "",
                }
            }
        )

        root = self.init_example_tree()

        StudyContext.objects.update_or_create(study=self.study, view="practical_task",
           defaults={
               "context": {
                   "title": "Praktisches Beispiel",
                   "introduction": """<p> Als Nächstes wirst Du ein exemplarisches hierarchisches Zielsystem nachbauen, das die
                                    Teilaufgaben einer Abiturprüfung schildert, das Abitur als Hauptoberziel hat und diverse Teilziele
                                    beinhaltet. </p> 
                                
                                    <p> Unten rechts ist das nachzubauende Zielsystem abgebildet, links ist dein Zielsystem, das am Ende
                                    genauso oder ähnlich aussehen sollte. Die Reihenfolge, in der gleichrangige Unterziele geordnet
                                    sind, spielt hierbei keine Rolle. Während der Bearbeitung kann die Visualisierung von deinem
                                    Zielsystem anders aussehen. Dies wird sich aber zunehmend anpassen, wenn die allgemeine
                                    Struktur mit der Vorlage übereinstimmt. </p>
                                
                                    <p> Tipp: sollte das vorgegebene Zielsystem unter deinem hierarchischen Zielsystem angezeigt werden,
                                    kannst du die Ansicht in deinem Browser verkleinern (herauszoomen) damit beide Systeme
                                    nebeneinander platziert werden. </p> 
                                    
                                    <p> Als erstes Oberziel ist „Abitur“ bereits vordefiniert. Füge zunächst dem Oberziel ein neues Teilziel
                                    im Erstellen-Modus hinzu. Man kann beim Erstellen einem jeweiligen Oberziel nur Teilziele auf der
                                    unmittelbar darunter angeordneten Hierarchieebene zuordnen. Unter dem Begriff „Oberziel“ ist
                                    immer das Ziel zu verstehen, dem man gerade ein neues Unterziel zuordnen will. </p>
                                    
                                    <p> Mithilfe der Optionen „Erstellen“, „Umbenennen“ und „Löschen“ kannst Du dein Zielsystem
                                    verändern. Der aktuelle Status des hierarchischen Zielsystems wird nach jeder Aktion automatisch
                                    aktualisiert. </p>
                                    
                                    <p> Dieser Schritt ist sehr wichtig für die Studie, bitte klicke erst auf „Weiter“ wenn Du mit dem
                                    Nachbauen fertig bist und keine Unterschiede zwischen Deinem und dem vorgegeben Zielsystem
                                    feststellen kannst. </p>
                                    
                                    <p> Tipp: Solltest du Schwierigkeiten haben die Struktur anhand des visuellen Beispiels zu verstehen,
                                    ist diese unten nochmal als Text verfasst. </p>""",
                   "text_bottom": """<p> Für das Abiturbeispiel hier ist zunächst das Bestehen bestimmter Fächer erforderlich. Zu den zu
                                    bestehenden Fächern gehören die für die mündliche Prüfung, die schriftliche Prüfung und den
                                    Wahlbereich relevanten Kurse. Für die mündliche Prüfung muss der „Grundkurs 1“ absolviert
                                    werden; für die schriftliche Prüfung sind die Leistungskurse 1 und 2, sowie der Grundkurs 2
                                    notwendig, für den Wahlbereich sind die Wahlfächer 1 bis 3 zu absolvieren. Dabei sind eine
                                    Notenverbesserung durch Nachhilfeunterricht in zwei Fächern und die sorgfältige Erledigung der
                                    Hausaufgaben von Nutzen. </p>""",
                   "tree_title": "Dein hierarchisches Zielsystem",
                   "example_tree_title": "Vorgegebenes Zielsystem",
                   "example_tree_id": root.tree_id,
                   "example_tree": json.dumps(Goal.get_tree(root.tree_id)),
                   "description_enabled": False,
               }
           }
        )

        StudyContext.objects.update_or_create(study=self.study, view="after_scenario",
           defaults={
               "context": {
                   "introduction": """<p style="font-size:large;font-weight:bold;"> Bitte lies die Fragen aufmerksam durch und beantworte sie ehrlich. Überlege nicht lange, sondern
                                    entscheide dich möglichst spontan für jeweils eine Antwortmöglichkeit. </p>""",
                   "type": "likert",
                   "answers": Item.get_likert_scale(5),
                   "items": [
                       {
                           "item_text": "Die unten stehende Beschreibung der Abitur-Aufgabe war erforderlich um den Aufbau des angestrebten Zielsystems nachvollziehen zu können.",
                           "reverse_coded": False,
                           "code": "after_scenario_1"
                       },
                       {
                           "item_text": "Die Struktur und Inhalte vom vorgegebenen Zielsystem waren verständlich und gut nachvollziehbar.",
                           "reverse_coded": False,
                           "code": "after_scenario_2"
                       },
                       {
                           "item_text": "Der Aufbau und Veränderungen des von mir erstellen Zielsystems waren verständlich und intuitiv.",
                           "reverse_coded": False,
                           "code": "after_scenario_3"
                       },
                   ],
                   "required": True,
               }
           }
        )

        StudyContext.objects.update_or_create(study=self.study, view="sus",
           defaults={
               "context": {
                   "introduction": """<p style="font-size:large;font-weight:bold;"> Bitte lies die Fragen aufmerksam durch und beantworte sie ehrlich. Überlege nicht lange, sondern
                                    entscheide dich möglichst spontan für jeweils eine Antwortmöglichkeit. </p>""",
                   "type": "likert",
                   "answers": Item.get_likert_scale(5),
                   "items": [
                       {
                           "item_text": "Ich kann mir sehr gut vorstellen, das System regelmäßig zu nutzen.",
                           "reverse_coded": False,
                           "code": "sus_1"
                       },
                       {
                           "item_text": "Ich empfinde das System als unnötig komplex.",
                           "reverse_coded": False,
                           "code": "sus_2",
                       },
                       {
                           "item_text": "Ich empfinde das System als einfach zu nutzen.",
                           "reverse_coded": False,
                           "code": "sus_3",
                       },
                       {
                           "item_text": "Ich denke, dass ich technischen Support brauchen würde, um das System zu nutzen.",
                           "reverse_coded": False,
                           "code": "sus_4",
                       },
                       {
                           "item_text": "Ich finde, dass die verschiedenen Funktionen des Systems gut integriert sind.",
                           "reverse_coded": False,
                           "code": "sus_5",
                       },
                       {
                           "item_text": "Ich finde, dass es im System zu viele Inkonsistenzen gibt.",
                           "reverse_coded": False,
                           "code": "sus_6",
                       },
                       {
                           "item_text": "Ich kann mir vorstellen, dass die meisten Leute das System schnell zu beherrschen lernen.",
                           "reverse_coded": False,
                           "code": "sus_7",
                       },
                       {
                           "item_text": "Ich empfinde die Bedienung als sehr umständlich.",
                           "reverse_coded": False,
                           "code": "sus_8",
                       },
                       {
                           "item_text": "Ich habe mich bei der Nutzung des Systems sehr sicher gefühlt.",
                           "reverse_coded": False,
                           "code": "sus_9",
                       },
                       {
                           "item_text": "Ich musste eine Menge Dinge lernen, bevor ich mit dem System arbeiten konnte.",
                           "reverse_coded": False,
                           "code": "sus_10",
                       },
                   ],
                   "required": True,
                   "display_answers_bottom": True,
               }
            }
        )

        StudyContext.objects.update_or_create(study=self.study, view="visualization_questions",
           defaults={
               "context": {
                   "title": None,
                   "introduction": """<p style="font-size:large;font-weight:bold;"> Bitte nimm Dir Zeit, um die Fragen aufmerksam durchzulesen und diese ehrlich und möglichst
                                    ausführlich zu beantworten. </p>""",
                   "questions": [
                       {
                           "type": "text",
                           "text": "Nenne bitte 3 bis 5 Eigenschaften, die Dir bei dieser Zielsystem-Visualisierung besonders gelungen zu sein scheinen.",
                           "required": True,
                           "rows": 4,
                       },
                       {
                           "type": "text",
                           "text": "Nenne bitte 3 bis 5 Eigenschaften, die Dir bei dieser Zielsystem-Visualisierung nicht gelungen zu sein scheinen.",
                           "required": True,
                           "rows": 4,
                       },
                       {
                           "type": "text",
                           "text": "Was würdest Du bei der visuellen Darstellung des Zielsystems verbessern?",
                           "required": True,
                           "rows": 4,
                       },
                       {
                           "type": "text",
                           "text": "Ist Dir bezüglich der Zielsystem-Visualisierung sonst etwas positiv oder negativ aufgefallen?",
                           "required": False,
                           "rows": 4,
                       },
                   ],
               }
           }
        )

        StudyContext.objects.update_or_create(study=self.study, view="personal_goals",
          defaults={
              "context": {
                  "title": """Persönliche Bildungsziele definieren""",
                  "introduction": """<p> Denk bitte an deine vier wichtigsten Studienziele und füge diese nacheinander in das
                                    Eingabefeld ein. Dies können zum Beispiel „Programmieren lernen“ oder „ein Paper
                                    veröffentlichen“ sein. Deine Ziele sollten hier möglichst abstrakt sein und keine konkreten
                                    Lösungsschritte zur Erreichung dieser Ziele beinhalten. </p>
                                    
                                    <p> Formuliere deine Ziele erst einmal stichwortartig (jeweils maximal 20 Symbole). Zu jedem
                                    der Ziele wirst du später eine eigene Zielhierarchie mit jeweils einer anderen
                                    Visualisierung erstellen. Sobald Du vier Ziele hinzugefügt hast, kannst du mit dem
                                    „Speichern“-Button fortfahren. </p>""",
                  "min_number_goals": 4,
                  "max_number_goals": 4,
              }
          }
        )

        StudyContext.objects.update_or_create(study=self.study, view="personal_goals_tree_construction",
          defaults={
              "context": {
                  "introduction": """<p> Nun wirst Du zu einem Deiner Bildungsziele ein hierarchisches Zielsystem erstellen. Bitte
                                    versuche Deine Ziele in erforderliche Teilziele und Aktionen so aufzugliedern, dass die
                                    Wege zum Erreichen der Bildungsziele klarer und zunehmend konkret werden. </p> 

                                    <p> Der aktuelle Status des Zielsystems wird nach jeder Aktion aktualisiert. Ein Oberziel wurde
                                    automatisch aus deiner Wahlliste eingetragen. Füge zunächst dem Oberziel ein neues
                                    Teilziel im Erstellen-Modus hinzu. Unter dem Begriff „Oberziel“ ist immer das Ziel zu
                                    verstehen, dem man gerade ein neues Unterziel zuordnen will. Das Oberziel ist ein
                                    abstraktes Ziel; versuche dein hierarchisches Zielsystem so aufzubauen, dass jede
                                    nächste Hierarchieebene spezifischer formuliert wird, bis du auf der untersten Ebene ganz
                                    konkrete Handlungen formulierst, die direkt unternommen werden könnten. </p>
                                    
                                    <p> Formuliere deine Ziele bitte stichwortartig (jeweils max. 20 Symbole) für eine genauere
                                    Definition kannst du das Beschreibungsfeld nutzen. Mithilfe der Optionen „Erstellen“,
                                    „Umbenennen“ und „Löschen“ kannst Du das Zielsystem verändern. Der aktuelle Status
                                    der Hierarchie wird nach jeder Aktion automatisch aktualisiert. </p>""",
                  "tree_title": "Dein hierarchisches Zielsystem",
                  "example_tree_title": "Vorgegebenes Zielsystem",
                  "description_enabled": True,
                  "identical_nodes_disabled": True,
              }
          }
        )

        StudyContext.objects.update_or_create(study=self.study, view="personal_goals_questionnaire",
           defaults={
               "context": {
                   "introduction": """<p style="font-size:large;font-weight:bold;"> Bitte lies die Fragen aufmerksam durch und beantworte sie ehrlich. Überlege nicht lange, sondern
                                    entscheide dich möglichst spontan für eine Antwortmöglichkeit. <p>""",
                   "type": "likert",
                   "answers": [
                        "trifft überhaupt nicht zu",
                        "trifft überwiegend nicht zu",
                        "trifft eher nicht zu",
                        "teils teils",
                        "trifft eher zu",
                        "trifft überwiegend zu",
                        "trifft vollständig zu"
                   ],
                   "items": [
                       {
                           "item_text": "Insgesamt bin ich damit zufrieden, wie leicht diese Aufgabe zu lösen war.",
                           "reverse_coded": False,
                           "code": "personal_goals_1"},
                       {
                           "item_text": "Insgesamt bin ich damit zufrieden, wie viel Zeit ich für die Lösung der Aufgaben aufwenden musste.",
                           "reverse_coded": False,
                           "code": "personal_goals_2"},
                       {
                           "item_text": "Insgesamt bin ich mit den unterstützenden Informationen (z.B. Formulierungen, Hilfen, Kommentaren) bei der Bearbeitung der Aufgabe zufrieden.",
                           "reverse_coded": False,
                           "code": "personal_goals_3"},
                   ],
                   "required": True,
               }
           }
        )

        StudyContext.objects.update_or_create(study=self.study, view="usability_open_questions",
          defaults={
              "context": {
                  "tree": json.dumps(Goal.get_tree(root.tree_id)),
                  "questions": [
                      {
                          "type": "tree_ranking",
                          "text": "Welche der verwenden Zielsysteme scheint Dir am intuitivsten zu sein? Bitte ordne "
                                  "hierzu die visuellen Darstellungen entsprechend (1 = am wenigsten intuitiv, 4 = besonders intuitiv). "
                                  "Die Auswahl muss eindeutig sein und wird bei einer Mehrfachauswahl automatisch korrigiert.",
                          "conditions": ["1", "2", "3", "4"],
                      },
                  ],
                  "required": True,
              }
          }
        )

        StudyContext.objects.update_or_create(study=self.study, view="thankyou",
           defaults={
               "context": {
                   "text": """<p>Vielen Dank, dass Du Dir die Zeit für die Teilnahme genommen hast!<br>
                            Sollte es noch offene Fragen zum Studienassistenten geben, erreichst Du uns unter 
                            <b>siddata@uni-osnabrueck.de</b>.</p>
                    
                            <p> Um eine <b>Versuchspersonenstunde</b> zu bekommen, schicke bitte eine Email an <b>jkernos@uos.de</b> mit dem <b>Betreff
                            „VP {timestamp}“</b> und mit <b>Matrikelnummer und Studienfach im Inhalt</b>.</p>""",
                   "text_bottom": """<p>Das Browserfenster kann nun geschlossen werden.
                                    <br>
                                    Wir wünschen Dir viel Erfolg beim Erreichen Deiner Ziele!</p>""",
                   "comment_enabled": True,
                   "comment_text": "Hier kannst du gern noch einen abschließenden Kommentar hinzufügen:",
               }
           }
        )

    def init_example_tree(self):
        # create example tree
        root = Goal.objects.get_or_create(
            is_example=True,
            example_id=1,
            study=self.study,
            defaults={
                "tree_id": Goal.objects.aggregate(Max('tree_id'))['tree_id__max'] + 1,
            }
        )[0]
        root.title = "Abitur"
        root.save()

        subjects = self.create_node(2, root, title="Fächer")
        improvement = self.create_node(3, root, title="Notenverbesserung")

        oral = self.create_node(4, subjects, title="Mündliche Prüfung")
        written = self.create_node(5, subjects, title="Schriftliche Prüfung")
        elective = self.create_node(6, subjects, title="Wahlbereich")

        tutoring = self.create_node(7, improvement, title="Nachhilfeunterricht")
        homework = self.create_node(8, improvement, title="Hausaufgaben")

        gk1 = self.create_node(9, oral, title="Grundkurs 1")

        lk1 = self.create_node(10, written, title="Leistungskurs 1")
        lk2 = self.create_node(11, written, title="Leistungskurs 2")
        gk2 = self.create_node(12, written, title="Grundkurs 2")

        wf1 = self.create_node(13, elective, title="Wahlfach 1")
        wf2 = self.create_node(14, elective, title="Wahlfach 2")
        wf3 = self.create_node(15, elective, title="Wahlfach 3")

        subject1 = self.create_node(16, tutoring, title="Nachhilfe Fach 1")
        subject2 = self.create_node(17, tutoring, title="Nachhilfe Fach 2")

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

    def create_dataframe(self):
        """
        Creates the default dataframe of this study
        :return:
        """
        dataframe = pd.DataFrame()
        participants = Participant.objects.filter(study=self.study).order_by("created")
        index = 0
        for participant in participants:
            data = {}

            # collect participant data
            has_additional_data = participant.additional_data is not None
            data.update({
                "id": participant.id,
                "age": participant.age,
                "gender": participant.gender,
                "semester": participant.semester,
                "subject": participant.subject,
                "created": participant.created,
                "finished": participant.finished,
                "abi_condition": participant.condition,
                "studytool_used": participant.additional_data.get("studytool_used") if has_additional_data else "",
                "studytool_name": participant.additional_data.get("studytool_name") if has_additional_data else "",
                "computer_handing": participant.additional_data.get("computer_handling") if has_additional_data else "",
                "consulting_requested": participant.additional_data.get("consulting_requested") if has_additional_data else "",
                "consulting_name": participant.additional_data.get("consulting_form") if has_additional_data else "",
                "screen_size": participant.screen_size,
                "operating_system": participant.operating_system,
                "browser_language": participant.browser_language,
            })

            # collect item data
            participant_items = Item.objects.filter(participant=participant)
            item_data = {}

            after_scenario_codes = [item["code"] for item in
                                    StudyContext.get_context(self.study, "after_scenario")["items"]]
            sus_codes = [item["code"] for item in StudyContext.get_context(self.study, "sus")["items"]]
            for code in after_scenario_codes + sus_codes:
                item_data[code] = participant_items.filter(code=code).latest(
                    "created").given_answer if participant_items.filter(code=code) else "",

            data.update(item_data)

            # collect personal goal items data
            personal_goals_data = {}
            personal_goals_codes = [item["code"] for item in
                                    StudyContext.get_context(self.study, "personal_goals_questionnaire")["items"]]
            personal_items = [participant_items.filter(code=code).order_by("created") for code in personal_goals_codes]
            for i in range(4):
                for j in range(len(personal_items)):
                    if i < len(personal_items[j]):
                        personal_goals_data["personal_goals_{}{}".format(i + 1, j + 1)] = personal_items[j][
                            i].given_answer
                    else:
                        personal_goals_data["personal_goals_{}{}".format(i + 1, j + 1)] = ""

            data.update(personal_goals_data)

            # collect user interaction data
            participant_interactions = UserInteraction.objects.filter(participant=participant).order_by("timestamp")
            abi_tree_interaction_first = participant_interactions.filter(route="/construction/new_tree/Abitur").first()
            abi_goal = Goal.objects.filter(participant=participant, discarded=False).order_by("created").first()
            abi_tree_interactions = None
            abi_duration = 0
            if abi_goal and abi_tree_interaction_first:
                abi_tree_interactions = participant_interactions.filter(goal__tree_id=abi_goal.tree_id).exclude(
                    id=abi_tree_interaction_first.id).order_by("timestamp")

                # search for last abi tree interaction
                last_abi_interaction = None
                for interaction in abi_tree_interactions.filter(
                        timestamp__gte=abi_tree_interaction_first.timestamp).order_by("timestamp"):
                    if interaction.action in ["write goal", "delete goal", "edit goal", "discard goal"]:
                        last_abi_interaction = interaction
                    else:
                        # break if no tree interaction
                        break

                if last_abi_interaction:
                    delta = last_abi_interaction.timestamp - abi_tree_interaction_first.timestamp
                    # milliseconds
                    abi_duration = round(delta.total_seconds() * 1000)

            data.update({
                "clicks": len(abi_tree_interactions) if abi_tree_interactions else "",
                "mseconds": abi_duration
            })

            # collect goal data
            participant_goals = Goal.objects.filter(participant=participant, discarded=False).order_by("tree_id")

            data.update({
                "abi_tree_id": abi_goal.tree_id if abi_goal else "",
                "number_abi_nodes": len(participant_goals.filter(tree_id=abi_goal.tree_id)) if abi_goal else "",
            })

            trees_id = participant_goals
            if abi_goal:
                trees_id = trees_id.exclude(tree_id=abi_goal.tree_id)
            trees_id = trees_id.values_list("tree_id", flat=True).distinct()
            tree_data = {}
            for i in range(4):
                tree_id = trees_id[i] if i < len(trees_id) else ""
                if abi_goal and tree_id == abi_goal.tree_id:
                    continue
                tree_data["own{}_tree_id".format(i + 1)] = tree_id
                tree_data["own{}_nodes".format(i + 1)] = len(
                    participant_goals.filter(tree_id=tree_id)) if tree_id else ""
                tree_data["own{}_condition".format(i + 1)] = participant_goals.get(tree_id=tree_id,
                                                                                   parent_id__isnull=True).condition if tree_id else ""

            data.update(tree_data)

            # collect question data
            question_data = {}
            participant_questions = Question.objects.filter(participant=participant).order_by("created")
            visualization_questions = participant_questions.filter(type="visualization_questions")
            visualization_columns = ["quali_gelungen", "quali_ungelungen", "quali_verbessern", "quali_sonst"]
            for i in range(len(visualization_columns)):
                question_data[visualization_columns[i]] = visualization_questions[i].answer if len(
                    visualization_questions) > i else ""

            usability_questions = participant_questions.filter(type="usability_open_questions")
            usability_columns = ["rank1_sun", "rank2_square", "rank3_tree", "rank4_circles"]
            for i in range(len(usability_columns)):
                question_data[usability_columns[i]] = usability_questions[i].answer if len(
                    usability_questions) > i else ""

            comment = participant_questions.filter(type="thankyou_comment")
            question_data["comment"] = comment.last().answer if comment else "",

            data.update(question_data)

            df_participant = pd.DataFrame(data, index=[index])
            dataframe = pd.concat([dataframe, df_participant])
            index += 1

        return dataframe

    def create_deleted_goals_dataframe(self):
        """
        Creates dataframe of deleted goals_export
        :return:
        """
        dataframe = pd.DataFrame()
        goals = Goal.objects.all().order_by("id")
        deleted_goals = []
        for i in range(len(goals) - 1):
            current_goal = goals[i]
            next_goal = goals[i + 1]
            # subtract ids to get the distance between the ids
            sub_goals = next_goal.id - current_goal.id
            # assume deleted goal if id difference is greater than 1
            for j in range(1, sub_goals):
                deleted_goals.append({
                    "deleted_id": current_goal.id + j,
                    "last_found_id": current_goal.id,
                    "last_found_study": current_goal.participant.study_id,
                    "last_found_tree_id": current_goal.tree_id,
                })

        index = 0
        for deleted_goal in deleted_goals:
            participant = Goal.objects.get(id=deleted_goal["last_found_id"]).participant

            data = deleted_goal

            # check if abi tree
            tree_id = deleted_goal.get("last_found_tree_id")
            abi_root_goal = Goal.objects.filter(tree_id=tree_id, parent_id__isnull=True, title="Abitur")
            data["is_abi_tree"] = abi_root_goal.exists()

            user_interactions = UserInteraction.objects.filter(participant=participant).order_by("timestamp")
            first_abi_interaction = user_interactions.filter(route="/construction/new_tree/Abitur").first()
            # abi tree exist
            last_abi_interaction = first_abi_interaction
            if first_abi_interaction:
                # search for last abi tree interaction
                for interaction in user_interactions.filter(timestamp__gte=first_abi_interaction.timestamp).order_by("timestamp"):
                    if interaction.action in ["write goal", "delete goal", "edit goal", "discard goal"]:
                        last_abi_interaction = interaction
                    else:
                        # break if no tree interaction
                        break

            data["first_click"] = first_abi_interaction.timestamp if first_abi_interaction else ""
            data["last_click"] = last_abi_interaction.timestamp if last_abi_interaction else ""

            # has abi tree 17 nodes
            data["club_17"] = data["is_abi_tree"] and len(Goal.objects.filter(tree_id=tree_id, discarded=False)) == 17

            data["participant_id"] = participant.id
            data["condition"] = participant.condition
            data["experiment_finished"] = participant.finished is not None

            df_deleted_goal = pd.DataFrame(data, index=[index])
            dataframe = pd.concat([dataframe, df_deleted_goal])
            index += 1

        return dataframe
