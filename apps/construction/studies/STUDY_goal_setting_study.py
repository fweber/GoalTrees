from apps.construction.studies.STUDY_BASE import STUDY_BASE
from apps.construction.models import Study, StudyContext, Goal, Item

from django.templatetags.static import static


class STUDY_goal_setting_study(STUDY_BASE):
    """
    Jueun's study
    """

    def __init__(self):
        super().__init__()
        self.name = "goal_setting_study"
        self.sequence = []
        self.study = Study.objects.update_or_create(
            name=self.name,
            classname=self.get_class_name(),
            defaults={
                "sequence": self.sequence,
                "language": "en",
            },
        )[0]

    def init_contexts(self):
        # create view contents
        self.sequence.append("welcome")
        StudyContext.objects.update_or_create(study=self.study, view="welcome",
            defaults={
                "context": {
                    "title": "Welcome to our study on academic goal setting!",
                    "text": """<p> We are interested in what academic goals students have and how these can be effectively structured.
                            Previous studies have shown that having clear goals can help you achieve them. By participating in
                            our study, you can not only acquire VP hours but also gain more clarity about your goals and improve
                            your chances of achieving them. </p>
                            
                            <p> This study is part of the formative studies on hierarchical goal-setting intervention in a digital assistant
                            and aims to investigate the relation between task-related experiences and goal characteristics. You will be asked 
                            to answer questions about your experience, and then to set your academic goals.
                            After having set personal goals, you will be asked to rate and compare those goals in relation to
                            diverse goal characteristics which have been found to influence relevant goal outcomes. </p>"""
                }
            }
        )

        self.sequence.append("instructions/general_instructions")
        StudyContext.objects.update_or_create(study=self.study, view="general_instructions",
            defaults={
                "context": {
                    "title": "General Instructions",
                    "text": """<p> The study consists of two main tasks. Please allow yourself at least one hour to complete this study. 
                            It is best to complete this study in one uninterrupted session. You will need to concentrate and
                            process what you are writing, so try to complete tasks when you are feeling alert and relatively
                            unrushed. Simply follow the on-screen instructions as you go along. Press the button on the bottom to
                            move on to the next page. </p>
                            
                            <p>For technical reasons, you will not be able to access the forms that have already been sent. It means
                            you will also not be able to use the "Back" button in your browser. So please check your entries every
                            time before you move on to the next page.</p>
                            
                            <p>Please answer the questions honestly and remember that this study does not intend to examine your
                            personal information, but the relationship between research variables of the study.</p>
                            
                            <p>Please try to take as few breaks as possible.</p>"""
                }
            }
        )

        self.sequence.append("consent")
        StudyContext.objects.update_or_create(study=self.study, view="consent",
            defaults={
                "context": {
                    "title": "Informed Consent Procedure",
                    "text": """<p> In order to participate in this research study, it is necessary that you give your informed consent. By
                            agreeing to this form, you are indicating that you understand the nature of the research study and your
                            role in that research and that you agree to participate in the research. Please read over the following
                            consent form carefully. </p>
                    
                            <h2>Purpose of the Study</h2>
                            <p> This study is designed to examine the relationship between task-related experience and academic goal
                            setting. </p>
                            
                            <h2>Procedures</h2>
                            <p>You will be asked to work through a series of web-based writing tasks (Part 1) and questionnaires
                            (Part 2).</p>
                            
                            <p style="margin-left: 55px;">Part 1:<br>
                            You will be asked to (1) <b>answer the open-ended questions about your past task-related
                            experiences</b>. Then you will be asked to (2) <b>set one personal academic goal</b>.
                            The sequence of describing your experiences &#8594; setting a goal will be repeated five times with
                            a different set of questions. After completing five steps, you will have elicited five
                            of your academic goals in total.</p>
                            
                            <p style="margin-left: 55px;">Part 2:<br>
                            You will be asked to complete the goal characteristics questionnaire in which you will rate the
                            characteristics of the five goals you set in the previous process.</p>
                            
                            <h2>Risks and Benefits</h2>
                            <p> There are no known risks to participating in this study. This research has been designed to investigate
                            various means of academic goal setting, and its effects on academic performance could be rather
                            beneficial. </p>
                            
                            <h2>Confidentiality</h2>
                            <p>No names or identifying information, e.g., email or IP address, will be collected, and your responses to
                            this study will be processed for scientific purposes and remain confidential. Information on the screen
                            size of your device will be collected additionally but only used for ensuring your experimental setting
                            with a desktop or laptop.</p>
                            
                            <h2>Participant Statement</h2>
                            <ul>
                                <li>I understand that I am participating in psychological research;</li>
                                <li>I understand that my identity will not be linked with my data, and that all information I
                                provide will remain confidential;</li>
                                <li>I understand that I will be provided with an explanation of the research in which I participated
                                and be given the name and email of an individual to contact if I have questions about the
                                research.</li>
                                <li>I understand that certain facts about the study might be withheld from me, and the researchers
                                might not, initially, tell me the true or full purpose of the study. However, the complete facts
                                and true purpose of the study will be revealed to me at the completion of the study session.</li>
                                <li>I understand that participation in research is not required, is voluntary, and that, after any
                                individual research project has begun, I may refuse to participate further without penalty.</li>
                            </ul>
                            
                            <p>By clicking “I hereby give my consent”, I am stating that I understand the above information and
                            consent to participate in this study being conducted at Osnabrück University.</p>""",
                }
            }
        )

        self.sequence.append("userdata")
        StudyContext.objects.update_or_create(study=self.study, view="userdata",
            defaults={
                "context": {
                    "title": "Registration",
                    "introduction": "",
                    "ask_english_proficiency": True,
                }
            }
        )

        self.sequence.append("instructions/task_instructions_part_1")
        StudyContext.objects.update_or_create(study=self.study, view="task_instructions_part_1",
            defaults={
                "context": {
                    "title": "Part 1: Task-Related Experience and Goal",
                    "text": """<h2>Task Instruction</h2>
                            <p>In the following pages, you will be asked several questions about your thoughts on past experiences
                            and your future goals. We would like you to spend some time thinking about answers to each question.</p>
                            
                            <p>Please type them into the text box provided and consider the minimum or maximum number of words
                            we will ask you to write. It will be shown under the text box with a word count. You can move on
                            to the next task when your text meets the number of words specified.</p>
                            
                            <p>You don’t have to worry about sentence construction, spelling, or grammar.</p>"""
                }
            }
        )

        StudyContext.objects.update_or_create(study=self.study, view="step_1",
            defaults={
                "context": {
                    "title": "",
                    "introduction": "",
                    "questions": [
                        {
                            "type": "text",
                            "text": "Think about a task you did that you <b>enjoyed</b>.                                                                <br>"
                                    "Describe why you think it was an <b>enjoyable</b> experience for you.",
                        },
                        {
                            "type": "text",
                            "text": "Think about a task you did because you found it <b>fun</b>.                                                        <br>"
                                    "Describe why you think it was <b>fun</b> to do.",
                        },
                        {
                            "type": "text",
                            "text": "Think about a task you did that was a <b>pleasure</b> to do.                                                       <br>"
                                    "Describe why you think it was a <b>pleasant</b> experience for you.",
                        },
                        {
                            "type": "text",
                            "text": "Think about a task you did that was <b>interesting</b>.                                                            <br>"
                                    "Describe why you think it was an <b>interesting</b> task for you.",
                        },
                        {
                            "type": "text",
                            "text": "Think about a task you did in which you <b>enjoyed</b> learning new things.                                        <br>"
                                    "Describe why you think it was an <b>enjoyable</b> experience.",
                        },
                        {
                            "type": "text",
                            "text": "Think about a task you did in which you found <b>satisfaction</b> by acquiring new knowledge and skills.           <br>"
                                    "Describe why you think it was a <b>satisfying</b> experience.",
                        },
                        {
                            "type": "text",
                            "text": "Think about a task you did for the <b>pleasure</b> you experienced when you discovered new things never seen before.<br>"
                                    "Describe why you think it was a <b>pleasant</b> experience.",
                        },
                        {
                            "type": "text",
                            "text": "Think about a task you did that allowed you to continue to learn about many things that <b>interested</b> you.     <br>"
                                    "Describe why you think it was <b>interesting</b> to do.",
                        },
                        {
                            "type": "goal",
                            "text": "What goal will you be pursuing during your studies?"
                                    " <b>Try to think of one goal that you will work on throughout the year and possibly beyond.                        </b> "
                                    "Write that goal into the box. <br>"
                                    "<small>Please do not include simple tasks such as “going to the store” or “clean my room.”</small>",
                            "random": False,
                        },
                    ],
                    "random_order": True,
                    "single_view": True,
                    "min_answer_words": 20, # words instead length counts number words
                    "show_min_answer_words": True,
                    "max_goal_words": 10,
                    "show_max_goal_words": True,
                    "required": True,
                }
            }
        )

        StudyContext.objects.update_or_create(study=self.study, view="step_2",
            defaults={
                "context": {
                    "title": "",
                    "introduction": "",
                    "questions": [
                        {
                            "type": "text",
                            "text": "Think about a task you did that you strongly <b>valued</b>.                                                              <br>"
                                    "Describe why you think you <b>valued</b> that task.",
                        },
                        {
                            "type": "text",
                            "text": "Think about a task you did that was <b>personally important</b> to you.                                                  <br>"
                                    "Describe why you think it was a <b>personally important</b> task.",
                        },
                        {
                            "type": "text",
                            "text": "Think about a task you did that was your <b>personal choice</b> to do.                                                   <br>"
                                    "Describe why you think it was your <b>personal choice</b>.",
                        },
                        {
                            "type": "text",
                            "text": "Think about a task you did that was <b>meaningful</b> to you.                                                            <br>"
                                    "Describe why you think it was a <b>meaningful</b> experience.",
                        },
                        {
                            "type": "text",
                            "text": "Think about a task you did because you <b>wanted to learn and acquire an understanding</b> of the task or related topics.<br>"
                                    "Describe why you think you <b>wanted to learn and understand</b> that task or related topics.",
                        },
                        {
                            "type": "text",
                            "text": "Think about a task you did because it was <b>important to you to do well</b> in that task.                                <br>"
                                    "Describe why you think it was <b>important to do well</b> in that task.",
                        },
                        {
                            "type": "text",
                            "text": "Think about a task you did because it would <b>improve your training</b> for <b>your future career</b>.                   <br>"
                                    "Describe why you think it could <b>improve your training</b> for <b>your future career</b>.",
                        },
                        {
                            "type": "text",
                            "text": "Think about a task you did because it allowed you to <b>learn</b> things which you can then <b>apply in other areas of your life</b>.<br>"
                                    "Describe why you think it allowed you to <b>learn</b> things and <b>apply them in other areas of your life</b>.",
                        },
                        {
                            "type": "goal",
                            "text": "What goal will you be pursuing during your studies?"
                                    " <b>Try to think of one goal that you will work on throughout the year and possibly beyond.</b>"
                                    "Write that goal into the box. <br>"
                                    "<small>Please do not include simple tasks such as “going to the store” or “clean my room.”</small>",
                            "random": False,
                        },
                    ],
                    "random_order": True,
                    "single_view": True,
                    "min_answer_words": 10, # words instead length counts number words
                    "show_min_answer_words": True,
                    "max_goal_words": 20,
                    "show_max_goal_words": True,
                    "required": True,
                }
            }
        )

        StudyContext.objects.update_or_create(study=self.study, view="step_3",
            defaults={
                "context": {
                    "title": "",
                    "introduction": "",
                    "questions": [
                        {
                            "type": "text",
                            "text": "Think about a task you did because you would have <b>felt guilty</b> if you hadn’t done it.<br>"
                                    "Describe why you think you could have <b>felt guilty</b> about it.",
                        },
                        {
                            "type": "text",
                            "text": "Think about a task you did because you would have <b>felt ashamed</b> if you hadn’t done it.<br>"
                                    "Describe why you think you could have <b>felt ashamed</b> about it.",
                        },
                        {
                            "type": "text",
                            "text": "Think about a task you did because you would have <b>felt like a failure</b> if you hadn’t done it.<br>"
                                    "Describe why you think you could have <b>felt like a failure</b> that way.",
                        },
                        {
                            "type": "text",
                            "text": "Think about a task you did because you didn’t want to <b>feel bad about yourself</b>.<br>"
                                    "Describe why you think you didn’t want to <b>feel bad about yourself</b> by doing that task.",
                        },
                        {
                            "type": "text",
                            "text": "Think about a task you did because you wanted to <b>feel proud of yourself</b>.<br>"
                                    "Describe why you think you wanted to <b>feel proud of yourself</b> by doing that task.",
                        },
                        {
                            "type": "text",
                            "text": "Think about a task you did because you wanted to <b>prove to yourself</b> that you were <b>capable</b>.<br>"
                                    "Describe why you think you wanted to <b>prove to yourself</b> that you were <b>capable</b> by doing that task.",
                        },
                        {
                            "type": "text",
                            "text": "Think about a task you did that <b>boosted your self-esteem</b>.<br>"
                                    "Describe why you think it <b>boosted your self-esteem</b>.",
                        },
                        {
                            "type": "text",
                            "text": "Think about a task you did because you wanted to <b>feel good about yourself</b>.<br>"
                                    "Describe why you think you wanted to <b>feel good about yourself</b> by doing that task.",
                        },
                        {
                            "type": "goal",
                            "text": "What goal will you be pursuing during your studies?"
                                    " <b>Try to think of one goal that you will work on throughout the year and possibly beyond.</b> "
                                    "Write that goal into the box. <br>"
                                    "<small>Please do not include simple tasks such as “going to the store” or “clean my room.”</small>",
                            "random": False,
                        },
                    ],
                    "random_order": True,
                    "single_view": True,
                    "min_answer_words": 10, # words instead length counts number words
                    "show_min_answer_words": True,
                    "max_goal_words": 20,
                    "show_max_goal_words": True,
                    "required": True,
                }
            }
        )

        StudyContext.objects.update_or_create(study=self.study, view="step_4",
            defaults={
                "context": {
                    "title": "",
                    "introduction": "",
                    "questions": [
                        {
                            "type": "text",
                            "text": "Think about a task you did that made <b>important people</b> (i.e., parents, professors) <b>like you better</b>.<br>"
                                    "Describe why you think it was important to you that <b>those people liked you</b>.",
                        },
                        {
                            "type": "text",
                            "text": "Think about a task you did because <b>others</b> would have become <b>angry</b> if you hadn’t done it.<br>"
                                    "Describe why you think <b>others</b> could have become <b>angry</b>.",
                        },
                        {
                            "type": "text",
                            "text": "Think about a task you did because you would have <b>got in trouble</b> if you hadn’t done it.<br>"
                                    "Describe why you think it could have <b>put you in trouble</b>.",
                        },
                        {
                            "type": "text",
                            "text": "Think about a task that you <b>didn’t have any choice</b> but to do.<br>"
                                    "Describe why you think you <b>didn’t have any choice</b> about it.",
                        },
                        {
                            "type": "text",
                            "text": "Think about a task you did because it was what <b>you were supposed to do</b>.<br>"
                                    "Describe why you think <b>you were supposed to do</b> that task.",
                        },
                        {
                            "type": "text",
                            "text": "Think about a task you did so that <b>your professor or boss</b> did <b>not single you out</b>.<br>"
                                    "Describe why you think <b>your professor or boss</b> could have <b>singled you out</b>.",
                        },
                        {
                            "type": "text",
                            "text": "Think about a task you did because you believed <b>the system required</b> you to do it even though it was not explicitly mandatory.<br>"
                                    "Describe why you think <b>the system required</b> you to do it.",
                        },
                        {
                            "type": "text",
                            "text": "Think about a task you did because you wanted to <b>obtain a more prestigious job</b> later on.<br>"
                                    "Describe why you think you wanted to <b>get a more prestigious job</b>.",
                        },
                        {
                            "type": "goal",
                            "text": "What goal will you be pursuing during your studies?"
                                    " <b>Try to think of one goal that you will work on throughout the year and possibly beyond.</b> "
                                    "Write that goal into the box. <br>"
                                    "<small>Please do not include simple tasks such as “going to the store” or “clean my room.”</small>",
                            "random": False,
                        },
                    ],
                    "random_order": True,
                    "single_view": True,
                    "min_answer_words": 10, # words instead length counts number words
                    "show_min_answer_words": True,
                    "max_goal_words": 20,
                    "show_max_goal_words": True,
                    "required": True,
                }
            }
        )

        StudyContext.objects.update_or_create(study=self.study, view="step_5",
            defaults={
                "context": {
                    "title": "",
                    "introduction": "",
                    "questions": [
                        {
                            "type": "text",
                            "text": "Think about a task that you <b>once had good reasons</b> for doing, but <b>later you didn’t</b>.<br>"
                                    "Describe why you think you <b>lost those reasons</b> later.",
                        },
                        {
                            "type": "text",
                            "text": "Think about a task that you honestly <b>didn’t know why you did</b>.<br>"
                                    "Describe why you think you <b>didn’t know why you did</b> that task.",
                        },
                        {
                            "type": "text",
                            "text": "Think about a task you did, but you were <b>not sure about it and wondered</b> whether you should <b>continue doing it</b>.<br>"
                                    "Describe why you think you were <b>not sure about continuing that task</b>.",
                        },
                        {
                            "type": "text",
                            "text": "Think about a task that you <b>used to know why you did</b>, but later <b>you didn’t anymore</b>.<br>"
                                    "Describe why you think you <b>didn’t know why you did</b> that task <b>anymore</b>.",
                        },
                        {
                            "type": "text",
                            "text": "Think about a task that you <b>didn’t understand why you had to do</b>.<br>"
                                    "Describe why you think you <b>didn’t understand why you had to do</b>.",
                        },
                        {
                            "type": "text",
                            "text": "Think about a task that you actually thought was <b>wasting your time</b>.<br>"
                                    "Describe why you think it was <b>a waste of your time</b>.",
                        },
                        {
                            "type": "text",
                            "text": "Think about a task that you <b>didn’t think you’d got much out of</b>.<br>"
                                    "Describe why you think you <b>didn’t get much out of</b> that task.",
                        },
                        {
                            "type": "text",
                            "text": "Think about a task you did but you <b>couldn't understand exactly what you were doing</b>.<br>"
                                    "Describe why you think you <b>couldn't understand what you were doing</b>.",
                        },
                        {
                            "type": "goal",
                            "text": "What goal will you be pursuing during your studies?"
                                    " <b>Try to think of one goal that you will work on throughout the year and possibly beyond.</b> "
                                    "Write that goal into the box. <br>"
                                    "<small>Please do not include simple tasks such as “going to the store” or “clean my room.”</small>",
                            "random": False,
                        },
                    ],
                    "random_order": True,
                    "single_view": True,
                    "min_answer_words": 20, # words instead length counts number words
                    "show_min_answer_words": True,
                    "max_goal_words": 10,
                    "show_max_goal_words": True,
                    "required": True,
                }
            }
        )

        # show views in random order
        self.sequence.append("random_views")
        StudyContext.objects.update_or_create(study=self.study, view="random_views",
            defaults={
                "context": {
                    "views": [
                        "open_questions/step_1",
                        "open_questions/step_2",
                        "open_questions/step_3",
                        "open_questions/step_4",
                        "open_questions/step_5",
                    ],
                    "sequences": [          # pseudo random sequences picked iteratively
                        [0, 1, 2, 3, 4],    # each value corresponds to view index
                        [1, 2, 3, 4, 0],
                        [2, 3, 4, 0, 1],
                        [3, 4, 0, 1, 2],
                        [4, 0, 1, 2, 3],
                    ]
                }
            }
        )

        self.sequence.append("instructions/task_instructions_part_2")
        StudyContext.objects.update_or_create(study=self.study, view="task_instructions_part_2",
            defaults={
                "context": {
                    "title": "Part 2: Goal Characteristic Questionnaire (GCQ)",
                    "text": """<h2>Task Instruction</h2>
                            <p>In the previous part, you have set five academic goals. Now we would like you to think about certain
                            characteristics of those goals in the following questionnaire.</p>
                            
                            <p>You will be asked to rate the extent to which you agree to statements in the questionnaire, with regard
                            to each of your goals presented on the left side (see the example below). 
                            You can mark it at any point on the scale from 0 (Strongly disagree) to 100 (Strongly agree) that you
                            find appropriate.</p>
                            
                            <p>Please make sure that you rate all of five goals before you move on to the next item.</p>
                            
                            <p>Tip: If you find some goals difficult to rate, try to assess by comparing them with other goals that you
                            already rated on the scale.</p>
                            
                            <img style="width: 75%; display: block; margin-left: auto; margin-right: auto;" src="{image}"></p>""".format(
                                image=static("construction/data/study_data/goal_setting/example_gcq.png")),
                }
            }
        )

        gcq_items = Item.get_gcq_items(file="study_data/goal_setting/gcq.csv", language="en")
        for i in range(len(gcq_items)):
            item = gcq_items[i]
            self.sequence.append("questionnaire/goal_characteristics_questionnaire_item_"+str(i+1))
            StudyContext.objects.update_or_create(study=self.study, view="goal_characteristics_questionnaire_item_"+str(i+1),
                defaults={
                    "context": {
                        "personal_goal_items": True,
                        "item_text": """<p style='font-weight: bold;font-size: x-large;'>{}</p>""".format(item.get("item_text", "")), # overrides the item text of the goal item
                        "code": item.get("code", ""),                                   # overrides the item code of the goal item
                        "latent_variable": item.get("latent_variable", ""),             # overrides the item latent_variable of the goal item
                        "reverse_coded": item.get("reverse_coded", ""),                 # overrides the item reverse_coded
                        "answers": ["Strongly disagree", "Disagree", "Slightly disagree", "Slightly agree", "Agree", "Strongly agree"],
                        "type": "slider",
                        "slider_min": 0,                # minimum slider value
                        "slider_max": 100,              # maximum slider value
                        "slider_step": 1,            # slider step length
                        "show_values": True,
                        # "required": True,
                    }
                }
            )

        self.sequence.append("instructions/debriefing")
        StudyContext.objects.update_or_create(study=self.study, view="debriefing",
            defaults={
                "context": {
                    "title": "Study Debriefing",
                    "text": """<p style="font-weight: bold;">The true purpose of the study</p>
                    
                            <p>For scientific reasons, you were not told the true purpose of the study at the beginning, concerning
                            “priming.” In psychology, priming describes a phenomenon in which exposure to one stimulus affects
                            cognition of a subsequent stimulus without conscious guidance.</p>
                            
                            <p>This study aims to investigate whether and how the priming of different <b>motivations</b> (intrinsic,
                            identified, introjected, extrinsic motivation, and amotivation) influences <b>goals</b> that people would set,
                            especially those that feel internally determined and caused by one’s own interests or beliefs, called
                            <b>“self-concordant goals.”</b><br>
                            Since the study needed to prevent the conscious connection between your “primed” motivation and the
                            process of setting new goals, some questions in the first part of the study had to withhold the purpose
                            of presenting motivational priming stimuli and seem to ask about your experiences. For example,
                            terms such as <i>fun</i>, <i>enjoy</i>, and <i>interesting</i> were priming stimuli describing the characteristics of intrinsic
                            motivation.</p>
                            
                            <p>If you are willing to continue and complete your participation, we thank you for your understanding.
                            For the reasons given above, we ask that you do not discuss this information with the potential
                            participants of the study.</p>
                            
                            <p>If you have any questions or comments, please contact Jueun Lee at 
                            <a href='mailto:julee@uni-osnabrueck.de'>julee@uni-osnabrueck.de</a>.</p>""",
                }
            }
        )

        self.sequence.append("open_questions/feedback_questions")
        StudyContext.objects.update_or_create(study=self.study, view="feedback_questions",
            defaults={
                "context": {
                    "title": """Feedback on the Study""",
                    "introduction": """<p>We would appreciate your feedback on our study. Please answer the questions below.</p>""",
                    "questions": [
                        {
                            "type": "radio",
                            "text": "1. Did you notice the true purpose of the study while doing the tasks?",
                            "answers": ["Yes", "No"],
                            "required": True,
                        },
                        {
                            "type": "text",
                            "text": "1.1. If you answered “Yes”, please give details.",
                            "required": False,
                        },
                        {
                            "type": "radio",
                            "text": "2. Did you feel any difficulty understanding the questions about your task-related experience?",
                            "answers": ["Yes", "No"],
                            "required": True,
                        },
                        {
                            "type": "text",
                            "text": "2.1. If you answered “Yes”, please give details.",
                            "required": False,
                        },
                        {
                            "type": "radio",
                            "text": "3. How would you describe your experience of using graphical rating scale for multiple "
                                    "goals in the goal characteristics questionnaire?",
                            "answers": ["Very Unsatisfied", "Unsatisfied", "Neutral", "Satisfied", "Very Satisfied"],
                            "required": True,
                        },
                        {
                            "type": "text",
                            "text": "3.1. If you were unsatisfied, please give details.",
                            "required": False,
                        },
                        {
                            "type": "text",
                            "text": "4. Please give us feedback on your overall experience of participating in this study.",
                            "required": True,
                        },
                    ],
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
                            <a href='mailto:julee@uni-osnabrueck.de'>julee@uni-osnabrueck.de</a> including your
                            <b>Matrikel-Nr. and major</b> with the subject “<b>VP {timestamp}</b>”</p>
                            
                            <p>If you have any questions about the digital study assistant, contact us at 
                            <a href='mailto:fweber@uni-osnabrueck.de'>fweber@uni-osnabrueck.de</a>.</p>""",
                    "text_bottom": """<p><b>Thank you for participating in our study, and good luck with your goals! You can close the
                                    browser now.</b></p>""",
                }
            }
        )

        self.study.sequence = self.sequence
        self.study.save()
