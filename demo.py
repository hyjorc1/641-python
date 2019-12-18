#%% load dataset and models
import dr
import util
from eva import evaluator

df = util.get_iris()
ds_path = 'models/iris_ds.txt'
dl_path = 'models/iris_dl.txt'
ds_rules = dr.create_rules(ds_path)
dl_rules = dr.create_rules(dl_path)

#%% print ds rules
dr.print_rules(ds_rules)

#%% print dl rules
dr.print_rules(dl_rules)

#%% convert dl to ds
dl_new_rules = dr.convert_to_rules(dl_rules)
dr.print_rules(dl_new_rules)

#%% build a evaluator with lambda vector
e = evaluator(df, [1,1,1,1,1,0,0])

#%% evaluate model 1
print("*---- iris_ds ----*")
id1 = e.add_model(ds_rules)
print("*---- iris_ds function scores ----*")
e.print_scores(id1)
print("*---- iris_ds total score ----*")
e.print_total_score(id1)

#%% evaluate model 2
print("*---- iris_dl ----*")
dl_new_rules = dr.convert_to_rules(dl_rules)
id2 = e.add_model(dl_new_rules)
print("*---- iris_dl function scores ----*")
e.print_scores(id2)
print("*---- iris_dl total score ----*")
e.print_total_score(id2)

# %%
