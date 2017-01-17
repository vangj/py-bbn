from pybbn.graph.dag import BbnUtil
from pybbn.graph.jointree import Evidence, EvidenceBuilder, EvidenceType
from pybbn.graph.node import Clique, SepSet
from pybbn.pptc.potentialinitializer import PotentialInitializer
from pybbn.pptc.moralizer import Moralizer
from pybbn.pptc.triangulator import Triangulator
from pybbn.pptc.transformer import Transformer
from pybbn.pptc.initializer import Initializer
from pybbn.pptc.propagator import Propagator
from pybbn.pptc.inferencecontroller import InferenceController

bbn = BbnUtil.get_huang_graph()
PotentialInitializer.init(bbn)

ug = Moralizer.moralize(bbn)
cliques = Triangulator.triangulate(ug)

join_tree = Transformer.transform(cliques)

Initializer.initialize(join_tree)
Propagator.propagate(join_tree)

join_tree.set_listener(InferenceController())

ev = EvidenceBuilder().with_node(join_tree.get_bbn_node_by_name('a')).with_evidence('on', 1.0).build()
join_tree.set_observation(ev)
join_tree.set_observation(ev)

# for k, v in join_tree.potentials.items():
#     clique = join_tree.get_node(k)
#     potential = v
#     print(clique)
#     print(potential)

for node in join_tree.get_bbn_nodes():
    potential = join_tree.get_bbn_potential(node)
    print(node)
    print(potential)
    total = sum([entry.value for entry in potential.entries])
    print('total = {}'.format(total))
