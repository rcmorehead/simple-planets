from simpleabc import simple_abc
import simple_model
import numpy as np
import pickle
from scipy import stats
import time
import sys

name = sys.argv[1]
steps = int(sys.argv[2])
start_step = int(sys.argv[3])
min_part = int(sys.argv[4])
n_procs = int(sys.argv[5])
known = sys.argv[6]


#print known, type(known)

if known == "True":
    known = True
else:
    known = False
#print known, type(known)

stars = pickle.load(file('stars.pkl'))

model = simple_model.MyModel(stars)

if known:
    obs = pickle.load(file('RUNS/{0}/KNOWN/obs_data.pkl'.format(name), 'r'))


else:
    obs = pickle.load(file('RUNS/{0}/SCIENCE/obs_data.pkl'.format(name), 'r'))

model.set_prior([stats.uniform(0, 90.0),
                 stats.uniform(0, 1),
                 stats.uniform(0, 20)])

model.set_data(obs)

start = time.time()
if known:
    OT = pickle.load(file(
                'RUNS/{0}/KNOWN/{0}_{1}samples_{2}.pkl'.format(name, min_part, 
                start_step), 'r'))
else:
    OT = pickle.load(file(
                'RUNS/{0}/SCIENCE/{0}_{1}samples_{2}.pkl'.format(name, min_part, 
                start_step),'r'))

for i in range(start_step + 1, start_step + 1 + steps):
    PT = OT
    OT = simple_abc.pmc_abc(model, obs, epsilon_0=1, min_samples=min_part,
                        resume=PT, steps=1, parallel=True, n_procs=n_procs)
    if known:
        out_pickle = file(
            'RUNS/{0}/KNOWN/{0}_{1}samples_{2}.pkl'.format(name, min_part, i),
            'w')
    else:
        out_pickle = file(
            'RUNS/{0}/SCIENCE/{0}_{1}samples_{2}.pkl'.format(name, min_part, i),
            'w')

    pickle.dump(OT, out_pickle)
    out_pickle.close()

end = time.time()
print 'This run took {}s'.format(end - start)
