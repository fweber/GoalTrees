from apps.construction.studies.STUDY_BASE import STUDY_BASE
from apps.construction.models import Study, StudyContext, Goal, Item

from apps.construction import models


class STUDY_prestudy(STUDY_BASE):
    """
    Jana's study
    """

    def __init__(self):
        super().__init__()
        self.name = "prestudy"
        self.description = "Vorstudie zu Usability und UX."
        self.active = False
        self.duration = 1
        self.sequence = ["welcome", "consent", "userdata", "questionnaire/big_five", "instructions", "example_tree", "tree_construction", "nasa_tlx", "questionnaire/utility_measure", "thankyou"]
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
                   "title": "Willkommen zur Studie über Zielsysteme",
                   "text": """<p>Uns interessiert welche Bildungsziele
                            Studierende haben und wie diese effectiv strukturiert werden können.
                            Studien haben gezeigt, dass Klarheit über die eigenen Ziele dabei helfen kann, sie auch zu erreichen.
                            Du kannst also durch die Teilnahme an unserer Studie nicht nur eine Versuchspersonenstunde erwerben, sondern
                            auch mehr Klarheit über deine Ziele gewinnen und deine Chancen, sie zu erreichen, verbessern.
                            </p>
                            <p> Insgesamt wird die Bearbeitung des Fragebogens ungefähr eine Stunde in Anspruch nehmen. Versuche so wenig Pausen
                            wie möglich zu machen.</p>"""
               }
           }
        )
        StudyContext.objects.update_or_create(study=self.study, view="consent",
           defaults={
               "context": {
                   "title": "Einverständniserklärung",
                   "text": """<p> Du hast dich freiwillig zur Teilnahme an dieser Studie gemeldet. Hier erhältst du 
                            nun einige Informationen zu deinen Rechten und zum Ablauf der Studie. Bitte lese die folgenden 
                            Abschnitte sorgfältig durch. </p> 
                        
                            <h2>1. Zweck der Studie </h2> 
                            <p> Ziel dieser Studie ist es, 
                            neue Erkenntnisse über Visualisierungen von hierarchischen Zielsystemen zu gewinnen. Die 
                            gesammelten Informationen sollen dazu beitragen, Studierende beim Setzen individueller 
                            Bildungsziele zu unterstützen. </p> 
                        
                            <h2>2. Ablauf der Studie</h2> 
                            <p> Deine Aufgabe ist es, 
                            hierarchische Zielsysteme zu erstellen sowie davor und danach einige Fragen zu beantworten.<br> 
                            Zum Ablauf:<br> Du wirst zu drei eigenen Bildungszielen jeweils ein hierarchisches Zielsystem 
                            erstellen. Diese stellen deine Ziele mit Teilzielen und Aktionen, die zur Zielerreichung führen, 
                            dar. Dabei sollen die Ziele so zerlegt werden, dass Wege zum Erreichen der Ziele klarer werden. 
                            </p> 
                        
                            <h2>3. Risiken und Nebenwirkungen</h2> 
                            <p> Diese Studie ist nach derzeitigem Wissensstand 
                            ungefährlich. Durch deine Teilnahme an dieser Studie setzt du dich keinen besonderen Risiken aus 
                            und es sind keine Nebenwirkungen bekannt. Da diese Studie in Ihrer Gesamtheit neu ist, 
                            kann das Auftreten von noch unbekannten Nebenwirkungen allerdings nicht ausgeschlossen werden. 
                            Auswirkungen auf die Lernleistung sind laut derzeitigem Wissensstand eher förderlich. </p> 
                        
                            <h2>4. Abbruch des Experiments</h2> 
                            <p> Du hast das Recht, diese Studie zu jedem Zeitpunkt und ohne 
                            Angabe eines Grundes abzubrechen. Deine Teilnahme ist vollkommen freiwillig und ohne 
                            Verpflichtungen. Es entstehen Dir keine Nachteile durch einen Abbruch. </p>
                        
                            <h2>5. Vertraulichkeit</h2> 
                            <p> Die Bestimmungen des Datenschutzes werden eingehalten. Personenbezogene 
                            Daten werden von uns nicht an Dritte weitergegeben. Die verfassten Daten werden in anonymisierter 
                            Form verarbeitet und für wissenschaftliche Zwecke in Forschungsdatenrepositorien publiziert. </p> 
                        
                            <h2>Einverständniserklärung</h2> 
                            <p> Bitte bestätige durch Klicken auf den Button die folgende 
                            Aussage: <br> “Hiermit bestätige ich, dass ich über Zwecke, Ablauf und nicht auszuschließende 
                            Nebenwirkungen der Studie aufgeklärt und informiert worden bin. Ich habe diese Erklärung gelesen 
                            und verstanden. Ich stimme jedem der Punkte zu. Ich ermächtige hiermit die von mir in dieser 
                            Untersuchung erworbenen Daten zu wissenschaftlichen Zwecken zu analysieren und in 
                            wissenschaftlichen Arbeiten anonymisiert zu veröffentlichen. Ich wurde über meine Rechte als 
                            Versuchsperson informiert und erkläre mich zu der freiwilligen Teilnahme an dieser Studie 
                            bereit.” </p> """
               }
           }
        )
        StudyContext.objects.update_or_create(study=self.study, view="userdata",
           defaults={
               "context": {
               }
           }
        )

        items = models.Item.get_big_five_items()
        StudyContext.objects.update_or_create(study=self.study, view="big_five",
           defaults={
               "context": {
                    "title": "Selbsteinschätzung",
                    "introduction": "<p>Inwieweit treffen die folgenden Aussagen auf dich zu? Antworte möglichst spontan. "
                                    "Es gibt keine richtigen oder falschen Antworten.</p>",
                    "type": "likert",
                    "answers": items[0].get("answers"),
                    "items": items,
               }
           }
        )

        items = models.Item.get_utility_measure_items()
        StudyContext.objects.update_or_create(study=self.study, view="utility_measure",
              defaults={
                  "context": {
                        "title": "Bewerte bitte inwieweit die folgenden Aussagen zutreffen.",
                        "type": "likert",
                        "answers": items[0].get("answers"),
                        "items": models.Item.get_utility_measure_items(),
                  }
              }
        )

        StudyContext.objects.update_or_create(study=self.study, view="instructions",
           defaults={
               "context": {
                   "title": "Instruktionen",
                   "text": """<p>Als nächstes wirst du selbst hierarchische Zielsysteme erstellen. Du beginnst ganz 
                            einfach mit einem Studienziel, dass Dir wichtig ist und das Du genauer unter die Lupe nehmen 
                            möchtest. Bitte formuliere Deine Ziele und Teilziele so, dass ein Außenstehender sie ebenfalls 
                            verstehen kann. Statt Stichworten wie "Plan" kannst du zum Beispiel "Lernplan erstellen" 
                            ausführen. <br>
                            <ol> 
                            <li>Du beginnst mit einem, sozusagen die Äste des Baumes. </li> 
                            <li>Dies setzt Du so lange fort, bis sich Aktionen, also ausführbare Handlungen oder 
                            Strategien ergeben. Das sind sozusagen die Blätter des Zielbaumes. </li>
                            </ol> 
                            Wenn du startklar bist, kannst Du auf der nächsten Seite loslegen und mindestens drei 
                            Zielbäume erstellen. Gerne kannst du auch noch mehr erstellen. </p>"""
               }
           }
        )

        StudyContext.objects.update_or_create(study=self.study, view="example_tree",
            defaults={
                 "context": {
                      "title": "Ein praktisches Beispiel",
                      "text": """<p> Du siehst hier einen Zielbaum mit einem <b>Hauptziel</b> von dem <b>Teilziele</b> 
                                abgeleitet werden. Die Teilziele werden konkreter und detaillierter, bis sie schließlich 
                                in konkrete <b>Aktionen und Strategien</b>. Im Idealfall wird jedes Ziel in konkrete 
                                Aktionen heruntergebrochen. </p>"""
                 }
            }
        )

        StudyContext.objects.update_or_create(study=self.study, view="thankyou",
            defaults={
                "context": {
                    "text": """<p>Vielen Dank, dass Du Dir die Zeit für die Teilnahme genommen hast!<br>
                            Sollte es noch offene Fragen zum Studienassistenten geben, erreichst Du uns unter 
                            <b>siddata@uni-osnabrueck.de</b>.</p>""",
                    "text_bottom": """<p>Das Browserfenster kann nun geschlossen werden.<br>
                                    Wir wünschen Dir viel Erfolg beim Erreichen Deiner Ziele!</p>""",
                }
            }
        )
