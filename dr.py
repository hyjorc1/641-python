# %%
import re
import copy

if_p = re.compile('If (.*?) then (.*)')
elseif_p = re.compile('Else If (.*?) then (.*)')
else_p = re.compile('Else (.*)')
relational_operaters = [">=", "<=", "==", ">", "<"]
opposite_dict = {
    ">=": "<",
    "<=": ">",
    "==": "!=",
    ">": "<=",
    "<": ">="
}

class predicate:
    def __init__(self, feature, relational_operater, value):
        self.feature = feature
        self.relational_operater = relational_operater
        self.value = value

    def cover(self, row):
        a = row[self.feature]
        b = float(self.value)
        switcher = {
            ">=": (a >= b),
            "<=": (a <= b),
            "==": (a == b),
            "==": (a != b),
            ">": (a > b),
            "<": (a < b)
        }
        return switcher.get(self.relational_operater)
    
    def get_opposite_predicate(self):
        return predicate(self.feature, opposite_dict.get(self.relational_operater), self.value)

    def __str__(self):
        return self.feature + ' ' + self.relational_operater + ' ' + self.value

class rule:
    def __init__(self, predicates, class_label):
        self.predicates = predicates
        self.class_label = class_label

    def cover(self, row):
        for pred in self.predicates:
            if (not pred.cover(row)):
                return False
        return True
    
    def get_opposite_predicates(self):
        op = []
        if (len(self.predicates) == 0):
            return op
        for pred in self.predicates:
            op.append(pred.get_opposite_predicate())
        return op
    
    def convert_to_rule(self, predicates):
        predicates = copy.deepcopy(predicates)
        if len(self.predicates) == 0:
            return rule(predicates, self.class_label)
        else:
            predicates.extend(self.predicates)
            return rule(predicates, self.class_label)

    def __str__(self):
        s = "If "
        for pred in self.predicates:
            s += str(pred) + " and "
        s = s[:-5] + " then " + self.class_label
        return s

class else_if_rule(rule):
    def __init__(self, predicates, class_label):
        super().__init__(predicates, class_label)

    def __str__(self):
        return "Else " + super().__str__()

class else_rule(rule):
    def __init__(self, predicates, class_label):
        super().__init__(predicates, class_label)

    def __str__(self):
        return "Else " + self.class_label

def create_rule(line):
    if line.startswith('If '):
        return create_else_if_rule(if_p.match(line), rule)
    if line.startswith('Else If '):
        return create_else_if_rule(elseif_p.match(line), else_if_rule)
    if line.startswith('Else '):
        return create_else_rule(else_p.match(line))

def create_else_if_rule(m, rule):
    predicates = []
    for s in m.group(1).strip().split(" and "):
        for operater in relational_operaters:
            if operater in s:
                arr = s.split(operater)
                predicates.append(
                    predicate(arr[0].strip(), operater, arr[1].strip()))
                break
    return rule(predicates, m.group(2).strip())

def create_else_rule(m):
    return else_rule([], m.group(1).strip())

def create_rules(filepath):
    rules = []
    with open(filepath) as fp:
        for cnt, line in enumerate(fp):
            rules.append(create_rule(line))
    return rules

def print_rules(rules):
    for r in rules:
        print(r)

def convert_to_rules(rules):
    new_rules = []
    size = len(rules)
    prev_predicates = []
    for i in range(0, size):
        if i == 0:
            new_rules.append(rules[i])
            prev_predicates.extend(rules[i].get_opposite_predicates())
            continue
        new_rules.append(rules[i].convert_to_rule(prev_predicates))
        prev_predicates.extend(rules[i].get_opposite_predicates())
    return new_rules
    
# %%
