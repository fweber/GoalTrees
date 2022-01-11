from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.urls import path, include

from . import api_views
from . import views
urlpatterns = [

                  # ADMINISTRATION
                  path('login', auth_views.LoginView.as_view(template_name="construction/login.html"), name='login'),
                  path('logout', auth_views.LogoutView.as_view(), name='logout'),
                  path('accounts/', include('django.contrib.auth.urls')),

                  # VIEWS
                  path('', views.welcome, name='welcome'),
                  path('welcome', views.welcome, name='welcome'),
                  path('consent', views.consent, name='consent'),
                  path('userdata', views.userdata, name='userdata'),
                  path('instructions', views.instructions, name='instructions'),
                  path('instructions/<str:view>', views.instructions, name='instructions'),
                  path('example_tree', views.example_tree, name='example_tree'),
                  path('goal_definition', views.goal_definition, name='goal_definition'),
                  path('tree_construction', views.tree_construction, name='tree_construction'),
                  path('tree_construction/<int:condition>', views.tree_construction, name='tree_construction'),
                  path('tree_construction/<int:condition>/<str:view>', views.tree_construction, name='tree_construction'),
                  path('nasa_tlx', views.nasa_tlx, name='nasa_tlx'),
                  path('gcq', views.gcq, name='gcq'),
                  path('explore_gcq', views.explore_gcq, name='explore_gcq'),
                  path('explore_gcq/<int:tree_id>', views.explore_gcq, name='explore_gcq'),
                  path('open_questions', views.open_questions, name='open_questions'),
                  path('open_questions/<str:open_questions>', views.open_questions, name='open_questions'),
                  path('questionnaire', views.questionnaire, name='questionnaire'),
                  path('questionnaire/<str:questionnaire>', views.questionnaire, name='questionnaire'),
                  path('thankyou', views.thankyou, name='thankyou'),
                  path('personal_goals', views.personal_goals, name='personal_goals'),
                  path('personal_goal_selection', views.personal_goal_selection, name='personal_goal_selection'),

                  # STUDY ENTRY POINT
                  path('study/<str:study_name>', views.study, name='study'),
                  # STUDY ENTRY POINT FOR EXTERNAL SIDDATA USER
                  path('study/<str:study_name>/<str:userid>', views.study, name='study_userid'),

                  # API VIEWS
                  path('next_view', api_views.next_view, name='next_view'),
                  path('previous_view', api_views.previous_view, name='previous_view'),
                  path('previous_view/<int:offset>', api_views.previous_view, name='previous_view'),
                  path('register_participant', api_views.register_participant, name='register_participant'),
                  path('answer_questionnaire', api_views.answer_questionnaire, name='answer_questionnaire'),
                  path('answer_nasa_tlx', api_views.answer_nasa_tlx, name='answer_nasa_tlx'),
                  path('write_goal', api_views.write_goal, name='write_goal'),
                  path('edit_goal', api_views.edit_goal, name='edit_goal'),
                  path('discard_goal', api_views.discard_goal, name='discard_goal'),
                  path('mark_goal', api_views.mark_goal, name='mark_goal'),
                  path('change_condition', api_views.change_condition, name='change_condition'),
                  path('new_tree', api_views.new_tree, name='new_tree'),
                  path('new_tree/<str:title>', api_views.new_tree, name='new_tree'),
                  path('new_tree/<str:title>/<int:replicated_tree_id>', api_views.new_tree, name='new_tree'),
                  path('answer_open_questions', api_views.answer_open_questions, name='answer_open_questions'),
                  path('write_comment', api_views.write_comment, name='write_comment'),
                  path('write_personal_goal', api_views.write_personal_goal, name='write_personal_goal'),
                  path('delete_personal_goal', api_views.delete_personal_goal, name='delete_personal_goal'),
                  path('process_personal_goals', api_views.process_personal_goals, name='process_personal_goals'),
                  path('random_views', api_views.random_views, name='random_views'),

                  # OLD
                  path('index', views.index, name='index'),

                  # Data views
                  path('<int:tree_id>/explore_trees', views.explore_trees, name='explore_trees'),
                  path('<int:study_id>/explore_studies', views.explore_studies, name='explore_studies'),
                  path('<str:study_id>/export_csv', views.export_csv, name='export_csv'),
                  path('<str:study_id>/export_csv/<str:export_name>', views.export_csv, name='export_csv'),

                  # path('cse_pre',views.cse_pre, name='cse_pre'),
                  # path('cse_post', views.cse_post, name='cse_post'),
                  # path('nasa_tlx', views.nasa_tlx, name='nasa_tlx'),

                  # path('condition1', views.condition1, name='condition1'),
                  # path('condition2', views.condition2, name='condition2'),
                  # path('condition3', views.condition3, name='condition3'),
                  # path('condition4', views.condition4, name='condition4'),
                  # path('condition5', views.condition5, name='condition5'),
                  # path('condition6', views.condition6, name='condition6'),
                  # path('<int:tree_id>/explore_trees', views.explore_trees, name='explore_trees'),
                  #
                  # path('answer_questionnaire', api_views.answer_questionnaire, name='answer_questionnaire'),
                  #
                  # path('write_feedback', api_views.write_feedback, name='write_feedback'),
                  # path('write_root', api_views.write_root, name='write_root'),
                  # path('write_goal', api_views.write_goal, name='write_goal'),

              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
