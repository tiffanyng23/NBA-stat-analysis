import pandas as pd
import statistics
from collections import Counter
import itertools

class SortPerformers:
    """sorts and filters stats of interest in descending order """

    def __init__(self, dataset, stat):
        """sorts data in descending order based on a stat of interest"""
        self.dataset = dataset
        self.stat = stat
        self.sorted_stat = dataset.sort_values(stat, ascending = False)

    def __str__(self):
        return "sorts data in descending order based on a stat of interest, can also filter and find top performers"
        
    def filter_data(self, *args):
        """filter sorted data for stat of interest, indicate other columns you want to include as an argument"""  
        filtered = self.sorted_stat[[*args, self.stat]]
        return filtered

    def top_percent(self, percent=10):
        """uses sorted data to find the top percentage (10% by default) of performers in a stat category"""
        num = int(len(self.sorted_stat)*(percent*0.01))
        top_stat = self.sorted_stat.head(num)
        return top_stat

class TopPerformers:
    """Identify top teams across multiple stat categories"""
    def __init__(self, num_categories, *data_lists):
        """concatenates an arbitrary number of lists to a single list"""
        self.data_lists = list(itertools.chain(*data_lists))
        self.num_categories = num_categories

    def top_performers(self):
        """Counts the players who are the top performers across a chosen number of categories"""
        top_overall = set()
        for x in self.data_lists:
            counts = self.data_lists.count(x)
            if counts >= self.num_categories:
                top_overall.add(x)
            else:
                continue
        return top_overall

