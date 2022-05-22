from apps.construction.studies.STUDY_BASE import STUDY_BASE
from apps.construction.models import Study, StudyContext, Goal, Item

from django.db.models import Max

import json

class STUDY_big5_study(STUDY_BASE):
    """
    Mae's study
    """

    def __init__(self):
        super().__init__()
        self.name = "big5_study"
        self.description = "Investigates correlations between OCEAN personality traits and visualization type preferences."
        self.active = False
        self.duration = 1
        self.sequence = ["welcome", "consent", "userdata", "questionnaire/big_five", "questionnaire/complexity_assessment_1", "questionnaire/complexity_assessment_2", "questionnaire/complexity_assessment_3", "questionnaire/complexity_assessment_4", "instructions", "example_tree", "goal_definition", "tree_construction", "questionnaire/sus", "open_questions/goalsystem_questions", "open_questions/ranking", "thankyou"]
        self.study = Study.objects.update_or_create(
            name=self.name,
            classname=self.get_class_name(),
            defaults={
                "sequence": self.sequence,
                "language": "de",
            },
        )[0]

    def init_contexts(self):
        # create view contents
        StudyContext.objects.update_or_create(study=self.study, view="welcome",
           defaults={
               "context": {
                   "title": "Willkommen zur Studie über Zielsysteme!",
                   "text": """<p style="font-weight: bold;"> Diese Studie ist abgeschlossen, vielen Dank für Ihre Teilnahme. 
                            Für diese Studie werden keine VP-Stunden mehr vergeben. </p>
                   
                            <p> Uns interessiert, welche Bildungsziele Studierende haben und wie diese effektiv strukturiert werden können.
                            Studien haben gezeigt, dass Klarheit über die eigenen Ziele dabei helfen kann, diese auch zu erreichen. Du
                            kannst also durch die Teilnahme an unserer Studie nicht nur eine Versuchspersonenstunde erwerben (Studenten
                            der Cognitive Science und der Psychologie), sondern auch mehr Klarheit über deine Ziele gewinnen und deine
                            Chancen, sie zu erreichen, verbessern. </p>
                            
                            <p> Diese Studie soll die Effekte von Persönlichkeitseigenschaften auf die Präferenz für verschiedene
                            Visualisierungen der Zielsysteme erforschen. Dazu wirst Du zu Beginn einige Fragen zu deiner Persönlichkeit
                            beantworten und die Komplexität der dargestellten Zielsysteme bewerten. Im Anschluss konstruierst Du dein
                            eigenes Zielsystem und beantwortest einige weitere Fragen dazu. </p>
                            
                            <p> Insgesamt wird die Bearbeitung der Studie ungefähr 35 bis 45 Minuten in Anspruch nehmen. Aus technischen
                            Gründen kannst Du den „Zurück“-Button deines Browsers leider nicht verwenden, um getätigte Eingaben der
                            vorherigen Seite zu verändern. Prüfe deine Antworten dementsprechend bevor Du mit der Studie fortfährst. </p>
                            
                            <p> Versuche so wenig Pausen wie möglich zu machen. </p>"""
               }
           }
        )

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
                            bereit.” </p>"""
               }
           }
        )

        StudyContext.objects.update_or_create(study=self.study, view="userdata",
            defaults={
                "context": {
                    "title": "Anmeldung",
                    "introduction": "Die Beantwortung folgender Fragen ist optional:",
                    "required": False,
                }
            }
        )

        items = Item.get_big_five_items()
        StudyContext.objects.update_or_create(study=self.study, view="big_five",
              defaults={
                  "context": {
                      "title": "Selbsteinschätzung",
                      "introduction": "<p>Inwieweit treffen die folgenden Aussagen auf dich zu? Antworte möglichst spontan. "
                                      "Es gibt keine richtigen oder falschen Antworten.</p>",
                      "type": "likert",
                      "answers": Item.get_likert_scale(4),
                      "items": [
                          {
                              "code": "neuro1",
                              "item_text": "Ich bin ein ängstlicher Typ.",
                          },
                          {
                              "code": "neuro2",
                              "item_text": "Ich fühle mich oft unsicher.",
                          },
                          {
                              "code": "neuro3",
                              "item_text": "Ich verspüre oft eine große innere Unruhe.",
                          },
                          {
                              "code": "neuro4",
                              "item_text": "Ich mache mir oft unnütze Sorgen.",
                          },
                          {
                              "code": "neuro5",
                              "item_text": "Ich grübele viel über meine Zukunft nach.",
                          },
                          {
                              "code": "neuro6",
                              "item_text": "Oft überwältigen mich meine Gefühle.",
                          },
                          {
                              "code": "neuro7",
                              "item_text": "Ich bin oft ohne Grund traurig.",
                          },
                          {
                              "code": "neuro8",
                              "item_text": "Ich bin oft nervös.",
                          },
                          {
                              "code": "neuro9",
                              "item_text": "Oft werde ich von meinen Gefühlen hin-und her gerissen.",
                          },
                          {
                              "code": "neuro10",
                              "item_text": "Ich bin mir in meinen Entscheidungen oft unsicher.",
                          },
                          {
                              "code": "extra1",
                              "item_text": "Ich bin gerne mit anderen Menschen zusammen.",
                          },
                          {
                              "code": "extra2",
                              "item_text": "Ich kann schnell gute Stimmung verbreiten.",
                          },
                          {
                              "code": "extra3",
                              "item_text": "Ich bin unternehmungslustig.",
                          },
                          {
                              "code": "extra4",
                              "item_text": "Ich stehe gerne im Mittelpunkt.",
                          },
                          {
                              "code": "extra5",
                              "item_text": "Im Grunde bin ich oft lieber für mich allein.",
                          },
                          {
                              "code": "extra6",
                              "item_text": "Ich bin ein Einzelgänger.",
                          },
                          {
                              "code": "extra7",
                              "item_text": "Ich gehe gerne auf Partys.",
                          },
                          {
                              "code": "extra8",
                              "item_text": "Ich bin in vielen Vereinen aktiv.",
                          },
                          {
                              "code": "extra9",
                              "item_text": "Ich bin ein gesprächiger und kommunikativer Mensch.",
                          },
                          {
                              "code": "extra10",
                              "item_text": "Ich bin sehr kontaktfreudig.",
                          },
                          {
                              "code": "gewissen1",
                              "item_text": "Ich bin sehr pflichtbewusst.",
                          },
                          {
                              "code": "gewissen2",
                              "item_text": "Meine Aufgaben erledige ich immer sehr genau.",
                          },
                          {
                              "code": "gewissen3",
                              "item_text": "Ich war schon als Kind sehr ordentlich.",
                          },
                          {
                              "code": "gewissen4",
                              "item_text": "Ich gehe immer planvoll vor.",
                          },
                          {
                              "code": "gewissen5",
                              "item_text": "Ich habe meine festen Prinzipien und halte daran auch fest.",
                          },
                          {
                              "code": "gewissen6",
                              "item_text": "Auch kleine Bußgelder sind mir sehr unangenehm.",
                          },
                          {
                              "code": "gewissen7",
                              "item_text": "Auch kleine Schlampereien stören mich.",
                          },
                          {
                              "code": "gewissen8",
                              "item_text": "Ich achte sehr darauf, dass Regeln eingehalten werden.",
                          },
                          {
                              "code": "gewissen9",
                              "item_text": "Wenn ich mich einmal entschieden habe, dann weiche ich davon auch nicht mehr ab.",
                          },
                          {
                              "code": "gewissen10",
                              "item_text": "Ich mache eigentlich nie Flüchtigkeitsfehler.",
                          },
                          {
                              "code": "offen1",
                              "item_text": "Ich will immer neue Dinge ausprobieren.",
                          },
                          {
                              "code": "offen2",
                              "item_text": "Ich bin ein neugieriger Mensch.",
                          },
                          {
                              "code": "offen3",
                              "item_text": "Ich reise viel, um andere Kulturen kennenzulernen.",
                          },
                          {
                              "code": "offen4",
                              "item_text": "Am liebsten ist es mir, wenn alles so bleibt, wie es ist.",
                          },
                          {
                              "code": "offen5",
                              "item_text": "Ich diskutiere gerne.",
                          },
                          {
                              "code": "offen6",
                              "item_text": "Ich lerne immer wieder gerne neue Dinge.",
                          },
                          {
                              "code": "offen7",
                              "item_text": "Ich beschäftige mich viel mit Kunst, Musik und Literatur.",
                          },
                          {
                              "code": "offen8",
                              "item_text": "Ich interessiere mich sehr für philosophische Fragen.",
                          },
                          {
                              "code": "offen9",
                              "item_text": "Ich lese viel über wissenschaftliche Themen, neue Entdeckungen oder historische Begebenheiten.",
                          },
                          {
                              "code": "offen10",
                              "item_text": "Ich habe viele Ideen und viel Fantasie.",
                          },
                          {
                              "code": "vertrag1",
                              "item_text": "Ich achte darauf, immer freundlich zu sein.",
                          },
                          {
                              "code": "vertrag2",
                              "item_text": "Ich bin ein höflicher Mensch.",
                          },
                          {
                              "code": "vertrag3",
                              "item_text": "Ich helfe anderen, auch wenn man mir es nicht dankt.",
                          },
                          {
                              "code": "vertrag4",
                              "item_text": "Ich habe immer wieder Streit mit anderen.",
                          },
                          {
                              "code": "vertrag5",
                              "item_text": "Ich bin ein Egoist.",
                          },
                          {
                              "code": "vertrag6",
                              "item_text": "Wenn mir jemand hilft, erweise ich mich immer als dankbar.",
                          },
                          {
                              "code": "vertrag7",
                              "item_text": "Ich würde meine schlechte Laune nie an anderen auslassen.",
                          },
                          {
                              "code": "vertrag8",
                              "item_text": "Es fällt mir sehr leicht, meine Bedürfnisse für andere zurückzustellen.",
                          },
                          {
                              "code": "vertrag9",
                              "item_text": "Ich kann mich gut in andere Menschen hinein versetzen.",
                          },
                          {
                              "code": "vertrag10",
                              "item_text": "Ich komme immer gut mit anderen aus, auch wenn sie nicht meiner Meinung sind.",
                          },
                          {
                              "code": "leistung1",
                              "item_text": "Ich habe schon immer ein starkes Bedürfnis verspürt nach meinen eigenen Maßstäben der Beste zu sein.",
                          },
                          {
                              "code": "leistung2",
                              "item_text": "Ich habe schon immer ein starkes Bedürfnis nach Anerkennung und Bewunderung verspürt.",
                          },
                          {
                              "code": "leistung3",
                              "item_text": "Für mehr Anerkennung würde ich auf vieles verzichten.",
                          },
                          {
                              "code": "leistung4",
                              "item_text": "Am glücklichsten bin ich dann, wenn viele Menschen mich bewundern und das toll finden, was ich mache.",
                          },
                          {
                              "code": "leistung5",
                              "item_text": "Tief in meinem Innersten gibt es eine Sehnsucht danach der Beste sein zu wollen.",
                          },
                          {
                              "code": "leistung6",
                              "item_text": "Ich träume oft davon, berühmt zu sein.",
                          },
                          {
                              "code": "macht1",
                              "item_text": "Ich träume oft davon, wichtige Entscheidungen für Politiker oder andere mächtige Menschen zu treffen.",
                          },
                          {
                              "code": "macht2",
                              "item_text": "Wenn ich die Wahl hätte, würde ich in meinem Leben gerne weltbewegende Entscheidungen treffen.",
                          },
                          {
                              "code": "macht3",
                              "item_text": "Tief in meinem Innersten gibt es eine Sehnsucht nach Einfluss und Macht.",
                          },
                          {
                              "code": "macht4",
                              "item_text": "Für mehr Einfluss würde ich auf vieles verzichten.",
                          },
                          {
                              "code": "macht5",
                              "item_text": "Am glücklichsten bin ich dann, wenn ich Verantwortung übernehmen kann und wichtige Entscheidungen treffen darf.",
                          },
                          {
                              "code": "macht6",
                              "item_text": "Ich kann Menschen verstehen, die sagen, dass andere Dinge wichtiger sind als Einfluss und Politik.",
                          },
                          {
                              "code": "sicher1",
                              "item_text": "Ich habe schon immer ein starkes Bedürfnis nach Sicherheit und Ruhe verspürt.",
                          },
                          {
                              "code": "sicher2",
                              "item_text": "Wenn ich die Wahl hätte, würde ich ein Leben in Sicherheit und Frieden wählen.",
                          },
                          {
                              "code": "sicher3",
                              "item_text": "Für ein sicheres Leben ohne böse Überraschungen würde ich auf vieles verzichten.",
                          },
                          {
                              "code": "sicher4",
                              "item_text": "Tief in meinem Innersten gibt es eine Sehnsucht nach Ruhe und Geborgenheit.",
                          },
                          {
                              "code": "sicher5",
                              "item_text": "Ich träume oft von einem ruhigen Leben ohne böse Überraschungen.",
                          },
                          {
                              "code": "sicher6",
                              "item_text": "Am glücklichsten bin ich dann, wenn ich mich geborgen fühle.",
                          },
                          {
                              "code": "ehrlich1",
                              "item_text": "Ich habe schon mal etwas unterschlagen oder nicht gleich zurückgegeben.",
                          },
                          {
                              "code": "ehrlich2",
                              "item_text": "Im privaten Bereich habe ich schon mal Dinge gemacht, die besser nicht an die Öffentlichkeit kommen sollten.",
                          },
                          {
                              "code": "ehrlich3",
                              "item_text": "Ich habe schon mal Dinge weitererzählt, die ich besser für mich behalten hätte.",
                          },
                          {
                              "code": "ehrlich4",
                              "item_text": "Ich habe schon mal über andere gelästert oder schlecht über sie gedacht.",
                          },
                      ],
                      "required": True,
                  },
              }
        )

        root = self.init_example_tree()
        tree = Goal.get_children(root.id)
        answers= ["trifft überhaupt nicht zu", "trifft nicht zu", "trifft eher nicht zu", "teils-teils",
                  "trifft eher zu", "trifft zu", "trifft vollkommen zu"]
        StudyContext.objects.update_or_create(study=self.study, view="complexity_assessment_1",
           defaults={
               "context": {
                   "title": "Komplexitätseinschätzung",
                   "introduction": """<p> Bitte gib an, inwieweit Du mit folgenden Aussagen übereinstimmst: <p>""",
                   "type": "likert",
                   "answers": answers,
                   "items": [
                       {
                           "item_text": "Die Visualisierung kann als komplex beschrieben werden.",
                           "reverse_coded": False,
                           "code": "complexity_assessment_1_1"},
                       {
                           "item_text": "Die Visualisierung hat eine logische Struktur, der leicht zu folgen ist.",
                           "reverse_coded": False,
                           "code": "complexity_assessment_1_2"},
                       {
                           "item_text": "Die Visualisierung ist überfordernd.",
                           "reverse_coded": False,
                           "code": "complexity_assessment_1_3"},
                       {
                           "item_text": "Die Visualisierung erscheint mir intuitiv.",
                           "reverse_coded": False,
                           "code": "complexity_assessment_1_4"},
                   ],
                   # shows example tree with given condition under introduction
                   "tree_text": "<p> Hier siehst Du nun eine Visualisierung eines Beispiel Zielsystems. </p>",
                   "tree": json.dumps(tree),
                   "tree_condition": 1,
                   "required": True,
               }
           }
        )

        StudyContext.objects.update_or_create(study=self.study, view="complexity_assessment_2",
            defaults={
                "context": {
                    "title": "Komplexitätseinschätzung",
                    "introduction": """<p> Bitte gib an, in wie weit du mit folgenden Aussagen übereinstimmst: <p>""",
                    "type": "likert",
                    "answers": answers,
                    "items": [
                    {
                      "item_text": "Die Visualisierung kann als komplex beschrieben werden.",
                      "reverse_coded": False,
                      "code": "complexity_assessment_2_1"},
                    {
                      "item_text": "Die Visualisierung hat eine logische Struktur, der leicht zu folgen ist.",
                      "reverse_coded": False,
                      "code": "complexity_assessment_2_2"},
                    {
                      "item_text": "Die Visualisierung ist überfordernd.",
                      "reverse_coded": False,
                      "code": "complexity_assessment_2_3"},
                    {
                      "item_text": "Die Visualisierung erscheint mir intuitiv.",
                      "reverse_coded": False,
                      "code": "complexity_assessment_2_4"},
                    ],
                    # shows example tree with given condition under introduction
                    "tree_text": "<p> Hier siehst Du nun eine Visualisierung eines Beispiel Zielsystems. </p>",
                    "tree": json.dumps(tree),
                    "tree_condition": 2,
                    "required": True,
                }
            }
        )

        StudyContext.objects.update_or_create(study=self.study, view="complexity_assessment_3",
            defaults={
                "context": {
                    "title": "Komplexitätseinschätzung",
                    "introduction": """<p> Bitte gib an, in wie weit du mit folgenden Aussagen übereinstimmst: <p>""",
                    "type": "likert",
                    "answers": answers,
                    "items": [
                    {
                        "item_text": "Die Visualisierung kann als komplex beschrieben werden.",
                        "reverse_coded": False,
                        "code": "complexity_assessment_3_1"},
                    {
                        "item_text": "Die Visualisierung hat eine logische Struktur, der leicht zu folgen ist.",
                        "reverse_coded": False,
                        "code": "complexity_assessment_3_2"},
                    {
                        "item_text": "Die Visualisierung ist überfordernd.",
                        "reverse_coded": False,
                        "code": "complexity_assessment_3_3"},
                    {
                        "item_text": "Die Visualisierung erscheint mir intuitiv.",
                        "reverse_coded": False,
                        "code": "complexity_assessment_3_4"},
                    ],
                    # shows example tree with given condition under introduction
                    "tree_text": "<p> Hier siehst Du nun eine Visualisierung eines Beispiel Zielsystems. </p>",
                    "tree": json.dumps(tree),
                    "tree_condition": 3,
                    "required": True,
                }
            }
        )

        StudyContext.objects.update_or_create(study=self.study, view="complexity_assessment_4",
            defaults={
                "context": {
                    "title": "Komplexitätseinschätzung",
                    "introduction": """<p> Bitte gib an, in wie weit du mit folgenden Aussagen übereinstimmst: <p>""",
                    "type": "likert",
                    "answers": answers,
                    "items": [
                    {
                        "item_text": "Die Visualisierung kann als komplex beschrieben werden.",
                        "reverse_coded": False,
                        "code": "complexity_assessment_4_1"},
                    {
                        "item_text": "Die Visualisierung hat eine logische Struktur, der leicht zu folgen ist.",
                        "reverse_coded": False,
                        "code": "complexity_assessment_4_2"},
                    {
                        "item_text": "Die Visualisierung ist überfordernd.",
                        "reverse_coded": False,
                        "code": "complexity_assessment_4_3"},
                    {
                        "item_text": "Die Visualisierung erscheint mir intuitiv.",
                        "reverse_coded": False,
                        "code": "complexity_assessment_4_4"},
                    ],
                    # shows example tree with given condition under introduction
                    "tree_text": "<p> Hier siehst Du nun eine Visualisierung eines Beispiel Zielsystems. </p>",
                    "tree": json.dumps(tree),
                    "tree_condition": 4,
                    "required": True,
                }
            }
        )

        StudyContext.objects.update_or_create(study=self.study, view="instructions",
            defaults={
                "context": {
                    "title": "Dein eigenes Zielsystem",
                    "text": """<p>Deine nächste Aufgabe ist, ein eigenes Zielsystem zu erstellen. Dazu kannst Du dir auf der nächsten
                            Seite nochmal ein Beispiel Zielsystem zum Ziel „Fristen einhalten“ anschauen. Im Anschluss daran
                            wirst Du selbst ein hierarchisches Zielsysteme zu einem Ziel deiner Wahl erstellen.
                            Schaue dir nun das Beispiel System an. </p>"""
                }
            }
        )

        StudyContext.objects.update_or_create(study=self.study, view="example_tree",
            defaults={
                "context": {
                    "title": "Ein praktisches Beispiel",
                    "text": """<p> Du siehst hier ein Zielsystem mit einem Hauptziel von dem Teilziele abgeleitet werden. Die Teilziele
                            werden konkreter und detaillierter, bis sie schließlich in konkreten Aktionen und Strategien enden. 
                            Im Idealfall wird jedes Ziel in konkrete Aktionen heruntergebrochen. Solltest Du das dargestellte System
                            nicht verstehen, sind die Ziele unter der Visualisierung nochmal in schriftlicher Form verfasst. </p>""",
                    "text_bottom": """<p> Um Fristen einzuhalten, ist ein gutes Zeitmanagement essentiell. Dieses kann durch eine gute
                                    Zeiteinteilung, Übersicht und Priorisierung erreicht werden. Im Sinne der Zeiteinteilung sollte die Zeit
                                    pro Aufgabe eingeplant werden. Eine gute Übersicht lässt sich durch einen Kalender und eine To-do
                                    Liste erreichen. Die Priorisierung sollte nach Datum und Wichtigkeit der Aufgabe erfolgen. </p>""",
                    "tree_id": root.id,
                    "tree": json.dumps(tree),
                }
            }
        )

        StudyContext.objects.update_or_create(study=self.study, view="goal_definition",
            defaults={
                "context": {
                    "title": "Deine Bildungsziele definieren",
                    "introduction": """<p> Formuliere hier nun dein eigenes Bildungsziel, zu dem Du auf der nächsten Seite dein Zielsystem
                            erstellen wirst. Dein Ziel sollte möglichst abstrakt sein, zum Beispiel „Programmieren lernen“ oder
                            „Studium abschließen“ . </p>
                            
                            <p> Bitte verwende eine stichpunktartige Formulierung (max. 20 Zeichen) deines Ziels. Nachdem Du dein
                            Ziel hinzugefügt hast, kannst Du mit dem „Speichern“-Button fortfahren. </p>"""
                }
            }
        )

        StudyContext.objects.update_or_create(study=self.study, view="tree_construction",
          defaults={
              "context": {
                  "title": "Dein Zielsystem erstellen",
                  "introduction": """<p> Bitte erstelle jetzt dein eigenes Zielsystem. </p>
                                    
                                    <p> Starte damit, ein Studienziel zu wählen, das dir wichtig ist und das Du genauer unter die Lupe nehmen 
                                    möchtest. </p>
                                    
                                    <p> Danach fügst Du mit der „Erstellen“ Option ein neues Teilziel hinzu. Das „Oberziel“ bezeichnet dabei
                                    das Ziel, zu dem Du das Unterziel („Teilziel“) erstellst. Mit der Option „umbenennen“ kannst Du ein
                                    schon hinzugefügtes Ziel umbenennen und mit der Option „verwerfen“ entfernst Du das ausgewählte
                                    Ziel mitsamt all seiner Unterziele. </p>
                                    
                                    <p> Bitte formuliere deine Ziele und Teilziele stichpunktartig (max. 20 Zeichen). Damit diese ein
                                    Außenstehender auch verstehen kann, kannst Du deinen Zielen eine Beschreibung hinzufügen, solltest
                                    Du das als erforderlich erachten. </p>
                                    
                                    <p> Versuche deine Ziele so aufzubauen, dass die Teilziele, die von den Oberzielen abgeleitet werden,
                                    immer konkreter werden, bis sie schließlich in spezifischen Aktionen enden. Die Teilziele werden also
                                    pro Hierarchieebene spezifischer formuliert bis in der untersten Ebene ausführbare Handlungen stehen.
                                    Somit sollen die Wege zum Erreichen des abstrakten Oberziels klarer werden. </p>""",
                  "tree_title": "Dein hierarchisches Zielsystem",
                  "example_tree_title": "Vorgegebenes Zielsystem",
                  "description_enabled": True,
                  "min_node_number": 3,
              }
          }
        )

        StudyContext.objects.update_or_create(study=self.study, view="sus",
           defaults={
               "context": {
                   "title": "Weitere Fragen",
                   "introduction": "<p> Bitte bewerte nun die Nutzung der Zielsystemanwendung („System“). </p>",
                   "type": "likert",
                   "answers": Item.get_likert_scale(5),
                   "items": [
                       {
                           "item_text": "1. Ich denke, dass ich das System gerne benutzen würde.",
                           "reverse_coded": False,
                           "code": "sus_1"
                       },
                       {
                           "item_text": "2. Ich empfand das System als unnötig komplex.",
                           "reverse_coded": False,
                           "code": "sus_2",
                       },
                       {
                           "item_text": "3. Ich empfand das System als einfach zu benutzen.",
                           "reverse_coded": False,
                           "code": "sus_3",
                       },
                       {
                           "item_text": "4. Ich glaube, ich würde die Hilfe einer technisch versierten Person benötigen, um das System benutzen zu können.",
                           "reverse_coded": False,
                           "code": "sus_4",
                       },
                       {
                           "item_text": "5. Ich fand, die verschiedenen Funktionen waren in dem System gut integriert.",
                           "reverse_coded": False,
                           "code": "sus_5",
                       },
                       {
                           "item_text": "6. Ich denke, das System enthielt zu viele Inkonsistenzen.",
                           "reverse_coded": False,
                           "code": "sus_6",
                       },
                       {
                           "item_text": "7. Ich kann mir vorstellen, dass die meisten Menschen den Umgang mit dem System sehr schnell lernen.",
                           "reverse_coded": False,
                           "code": "sus_7",
                       },
                       {
                           "item_text": "8. Ich empfand das System als sehr umständlich zu nutzen.",
                           "reverse_coded": False,
                           "code": "sus_8",
                       },
                       {
                           "item_text": "9. Ich fühlte mich bei der Benutzung des Systems sehr sicher.",
                           "reverse_coded": False,
                           "code": "sus_9",
                       },
                       {
                           "item_text": "10. Ich musste eine Menge lernen, bevor ich anfangen konnte das System zu verwenden.",
                           "reverse_coded": False,
                           "code": "sus_10",
                       },
                   ],
                   "required": True,
               }
            }
        )

        StudyContext.objects.update_or_create(study=self.study, view="goalsystem_questions",
          defaults={
              "context": {
                  "title": """Weitere Fragen""",
                  "introduction": """<p> Die Beantwortung der folgenden Fragen ist optional: </p>""",
                  "questions": [
                      {
                          "type": "text",
                          "text": "Was hat dir besonders an dem Zielsystem gefallen?",
                      },
                      {
                          "type": "text",
                          "text": "Was hat dir am wenigsten am Zielsystem gefallen?",
                      },
                      {
                          "type": "text",
                          "text": "Weitere Anmerkungen zu dem Zielsystem?",
                      },
                  ],
              }
          }
        )

        StudyContext.objects.update_or_create(study=self.study, view="ranking",
            defaults={
                "context": {
                    "title": "Ranking",
                    "questions": [
                        {
                            "type": "tree_ranking",
                            "text": "Bitte betrachte nun dein persönliches Zielsystem in verschiedenen Visualisierungen. "
                                    "Anschließend kannst Du die verschiedenen Visualisierungen gemäß deiner Präferenz, "
                                    "diese zu nutzen, anordnen. (1 – am stärksten präferiert bis 4 – am wenigsten präferiert)",
                            "conditions": ["1", "2", "3", "4"],
                            # if no tree is set use the current tree
                        },
                    ],
                    "zoomable": True,
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
                    
                            <p> Um eine <b>Versuchspersonenstunde</b> zu bekommen, schicke bitte eine Email an <b>mgrenz@uni-osnabrueck.de</b> mit dem <b>Betreff
                            „VP {timestamp}“</b> und mit <b>Matrikelnummer und Studienfach im Inhalt</b>.</p>""",
                   "text_bottom": """<p>Das Browserfenster kann nun geschlossen werden.
                                    <br>
                                    Wir wünschen Dir viel Erfolg beim Erreichen Deiner Ziele!</p>""",
                   "comment_enabled": False,
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
        root.title = "Fristen einhalten"
        root.save()

        time = self.create_node(2, root, title="Zeitmanagement")

        priority = self.create_node(3, time, title="Priorisierung")
        timedivision = self.create_node(4, time, title="Zeiteinteilung")
        overview = self.create_node(5, time, title="Übersicht")

        date = self.create_node(6, priority, title="Datum")
        important = self.create_node(7, priority, title="Wichtigkeit")

        tasktime = self.create_node(8, timedivision, title="Zeit pro Aufgabe")

        calendar = self.create_node(9, overview, title="Kalender")
        todo = self.create_node(10, overview, title="To-do Liste")

        # delete possible remaining example goals
        Goal.objects.filter(is_example=True, study=self.study, tree_id=root.tree_id, example_id__gt=10).delete()

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

