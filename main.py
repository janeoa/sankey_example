import pandas as pd
import plotly.graph_objects as go

### Example data
# source,applied,Category,status
# LinkedIn,custom,Rust,rejected
# LinkedIn,custom,Embedded,rejected
# LinkedIn,custom,Rust,rejected


data = pd.read_csv("data.csv")

# Convert to DataFrame
df = pd.DataFrame(data)
print(data.head())

# Step 1: Process the data
# Create connections and count occurrences
connections = []
for _, row in df.iterrows():
    connections.append((row["source"], row["applied"]))
    connections.append((row["applied"], row["Category"]))
    if row["status"]:
        for status in row["status"].split():
            connections.append((row["Category"], status))

# Count occurrences of each connection
connection_counts = pd.DataFrame(connections, columns=["source", "target"]).value_counts().reset_index()
connection_counts.columns = ["source", "target", "value"]

# Step 2: Prepare Sankey inputs
# Create a list of unique nodes
nodes = list(set(connection_counts["source"].tolist() + connection_counts["target"].tolist()))
node_indices = {node: i for i, node in enumerate(nodes)}

# Map source and target to indices
connection_counts["source_idx"] = connection_counts["source"].map(node_indices)
connection_counts["target_idx"] = connection_counts["target"].map(node_indices)

# Step 3: Create Sankey diagram
fig = go.Figure(data=[go.Sankey(
    node=dict(
        pad=15,
        thickness=20,
        line=dict(color="black", width=0.5),
        label=nodes
    ),
    link=dict(
        source=connection_counts["source_idx"],
        target=connection_counts["target_idx"],
        value=connection_counts["value"]
    )
)])

fig.update_layout(title_text="Sankey Diagram", font_size=10)
fig.show()