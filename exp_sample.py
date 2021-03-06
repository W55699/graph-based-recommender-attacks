
from gbra.recommender.recommenders import RandomRecommender
from gbra.data.network_loader import TinyTestLoader, ErdosRenyiLoader


# Tiny Test
tiny_network = TinyTestLoader().load()
recommender = RandomRecommender(tiny_network)
recs_for_3 = recommender.recommend(entity_id=3, number_of_items=3)
recs_for_5 = recommender.recommend(entity_id=5, number_of_items=2)

print("Tiny test")
print("Random recommendations for 3: %s" % str(recs_for_3))
print("Random recommendations for 5: %s" % str(recs_for_5))
print("---")

# Erdos-renyi bipartite graph
loader =  ErdosRenyiLoader(num_entities=20, num_items=50, num_edges=60)
er_network = loader.load()
recommender = RandomRecommender(er_network)
recs_for_15 = recommender.recommend(entity_id=15, number_of_items=3)
recs_for_21 = recommender.recommend(entity_id=21, number_of_items=5)

print("Erdos Renyi:")
print("Random recommendations for 15: %s" % str(recs_for_15))
print("Random recommendations for 21: %s" % str(recs_for_21))

assert(er_network.base().GetNodes() == 20 + 50)
assert(er_network.base().GetEdges() == 60)
