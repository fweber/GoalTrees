from django.core.management.base import BaseCommand

import seaborn as sns
import pandas as pd
import numpy as np
import random

import os

EXPORT_PATH = "{}/data/hgs_data".format(os.getcwd())
PLOTS_PATH = "{}/plots".format(EXPORT_PATH)

class Command(BaseCommand):
    help = 'Exports relations of construction app as csv files'

    def handle(self, *args, **kwargs):


        x_values = []
        y_values = []

        for i in range(1000):
            x_values.append(random.randint(50, 1000))
            y_values.append(random.randint(100, 800))


        sns_plot = sns.violinplot(
                                  x=x_values,
                                  #y=y_values,
                                  )

        fig = sns_plot.get_figure()

        fig.savefig("{}/AA_violinplot.png".format(PLOTS_PATH), bbox_inches="tight")

        fig.clf()
