import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import constants as c

# Load weights
sensorToHiddenWeights = np.load("data/weights/sensorToHiddenWeights_B.npy")
hiddenToMotorWeights = np.load("data/weights/hiddenToMotorWeights_B.npy")
recurrentWeights = np.load("data/weights/recurrentWeights_B.npy")

G = nx.DiGraph()

# Node names
sensorNames = ["FrontLowerLeg", "BackLowerLeg", "LeftLowerLeg", "RightLowerLeg"]
motorNames = ["Torso_BackLeg", "Torso_FrontLeg", "Torso_LeftLeg", "Torso_RightLeg", 
              "FrontLeg_FrontLowerLeg", "BackLeg_BackLowerLeg", "LeftLeg_LeftLowerLeg", "RightLeg_RightLowerLeg"]

# Add nodes
for i in range(c.numSensorNeurons):
    G.add_node(sensorNames[i], pos=(0, -i))

for i in range(c.numHiddenNeurons):
    G.add_node(f"Hidden {i}", pos=(1, -i))

for i in range(c.numMotorNeurons):
    G.add_node(motorNames[i], pos=(2, -i))

# Add edges: Sensor → Hidden
for i in range(c.numSensorNeurons):
    for j in range(c.numHiddenNeurons):
        weight = sensorToHiddenWeights[i, j]
        if weight != 0:
            G.add_edge(sensorNames[i], f"Hidden {j}", weight=weight)

# Add edges: Hidden → Motor
for i in range(c.numHiddenNeurons):
    for j in range(c.numMotorNeurons):
        weight = hiddenToMotorWeights[i, j]
        if weight != 0:
            G.add_edge(f"Hidden {i}", motorNames[j], weight=weight)

# Add recurrent edges: Hidden → Hidden
for i in range(c.numHiddenNeurons):
    for j in range(c.numHiddenNeurons):
        weight = recurrentWeights[i, j]
        if weight != 0:
            G.add_edge(f"Hidden {i}", f"Hidden {j}", weight=weight)

# Node positions
pos = nx.get_node_attributes(G, 'pos')

# Edge colors and widths
edges = G.edges(data=True)
edge_colors = []
edge_widths = []

for u, v, d in edges:
    color = 'blue' if d['weight'] > 0 else 'red'
    edge_colors.append(color)
    edge_widths.append(1 + abs(d['weight']) * 3)  # base width + scaled

# Node colors by type
node_colors = []
for node in G.nodes():
    if node in sensorNames:
        node_colors.append('#A1D99B')  # greenish for sensors
    elif node in motorNames:
        node_colors.append('#9ECAE1')  # bluish for motors
    else:
        node_colors.append('#FDD0A2')  # orangish for hidden

# Draw
plt.figure(figsize=(14, 8))

nx.draw_networkx_nodes(G, pos, node_size=5000, node_color=node_colors, edgecolors='black')
nx.draw_networkx_labels(G, pos, font_size=5, font_weight='bold')
nx.draw_networkx_edges(G, pos, edge_color=edge_colors, width=edge_widths, arrows=True, 
                       connectionstyle='arc3,rad=0.1')

plt.title("Neural Network Visualization", fontsize=18, weight='bold')
plt.axis('off')
plt.tight_layout()
plt.show()
