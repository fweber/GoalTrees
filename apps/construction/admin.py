from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

# Register your models here.
from .models import Goal, Participant, Item, Question, Study, PersonalGoal, UserInteraction

# für import-export app
@admin.register(Goal)
@admin.register(Participant)
@admin.register(Item)
@admin.register(Question)
@admin.register(Study)
@admin.register(PersonalGoal)
@admin.register(UserInteraction)
# ohne import-export app
# admin.site.register(Goal)
# admin.site.register(Participant)
# admin.site.register(Item)
# admin.site.register(Question)
# admin.site.register(Study)
# admin.site.register(PersonalGoal)
# admin.site.register(UserInteraction)

class ViewAdmin(ImportExportModelAdmin):
    pass