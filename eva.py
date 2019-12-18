# %%
import os
import numpy as np
import pandas as pd
import dr
import util
from sklearn.datasets import load_iris

class evaluator:
    def __init__(self, df, lambdas):
        self.df = df
        self.lambdas = lambdas
        self.S = 24           # number of input set of itemsets
        self.n = df.shape[0]  # size of input dataset
        self.C = df.iloc[:, -1].nunique()
        self.models = []
        self.scores_dict = dict()

    def add_model(self, rules):
        idx = len(self.models)
        self.models.append(rules)
        self.scores_dict[idx] = [self.f1(rules), self.f2(rules),
                                 self.f3(rules), self.f4(rules),
                                 self.f5(rules), self.f6(rules),
                                 self.f7(rules)]
        return idx

    def f1(self, rules):
        model_size = len(rules)
        return (self.S - model_size) * 1.0 / self.S

    def f2(self, rules):
        max: int = 0
        length: int = 0
        if isinstance(rules[0], dr.rule):
            for r in rules:
                tmp = len(r.predicates)
                if tmp > max:
                    max = tmp
                length = length + tmp
        return (max * self.S - length) * 1.0 / (max * self.S)

    def f3(self, rules):
        def data_cover(r1: dr.rule):
            s = set()
            for index, row in self.df.iterrows():
                if (r1.cover(row)):
                    s.add(index)
            return s
        def data_overlap(idx1, idx2, rule_to_covered_data):
            s1 = rule_to_covered_data[idx1]
            s2 = rule_to_covered_data[idx2]
            return len(s1.intersection(s2))
        size = len(rules)
        n_data_overlap: int = 0
        rule_to_covered_data = {}  # rule idx to data cover set
        for i in range(0, size):
            set1 = data_cover(rules[i])
            rule_to_covered_data[i] = set1
        for i in range(0, size - 1):
            for j in range(i + 1, size):
                n_data_overlap += data_overlap(i, j, rule_to_covered_data)
        return (self.n*pow(self.S, 2) - n_data_overlap) * 1.0 / (self.n*pow(self.S, 2))

    # recall
    def f4(self, rules):
        def exist_true_data_cover(row):
            for r in rules:
                if (r.cover(row) and r.class_label == row['label']):
                    return True
            return False
        true_cover = 0
        for index, row in self.df.iterrows():
            if exist_true_data_cover(row):
                true_cover += 1
        return true_cover * 1.0 / self.n

    # precision
    def f5(self, rules):
        size = len(rules)
        false_data_cover = 0
        for r in rules:
            for index, row in self.df.iterrows():
                if (r.cover(row) and r.class_label != row['label']):
                    false_data_cover += 1
        return (self.n * self.S - false_data_cover) / (self.n * self.S)

    def f6(self, rules):
        unique_classes = set()
        for r in rules:
            unique_classes.add(r.class_label)
        return len(unique_classes) * 1.0 / self.C

    def f7(self, rules):
        classes = set()
        duplicate = 0
        size = len(rules)
        for r in rules:
            if r.class_label in classes:
                duplicate += 1
            else:
                classes.add(r.class_label)
        return (size - duplicate) * 1.0 / size

    def print_scores(self, idx):
        print(*self.scores_dict[idx], sep=", ")

    def print_total_score(self, idx):
        return print(str(util.dot(self.scores_dict[idx], self.lambdas)))



# %%
