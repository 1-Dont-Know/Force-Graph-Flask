import os
from dotenv import load_dotenv
import pinecone
from pyvis.network import Network
from flask import Flask, render_template

# Load environment variables from .env file
load_dotenv()

# Retrieve the Pinecone API key and index name from the environment
api_key = os.getenv("PINECONE_API_KEY")
index_name = os.getenv("PINECONE_INDEX_NAME")

# Initialize Flask app
app = Flask(__name__)

# Initialize Pinecone and connect to your index using the API key
pc = pinecone.Pinecone(api_key=api_key)
index = pc.Index(index_name)

# Step 2: Retrieve the data from Pinecone (example IDs)
disease_ids = ["Epilepsy", "Thyroid", "Crohn ' s Disease", "Bipolar", "Multiple Sclerosis", "Lupus", "Parkinson s Disease", "Lyme Disease", "Chronic Fatigue Syndrome"]
query = index.fetch(ids=disease_ids, namespace="case-study")

# Extract diseases and their conditions
disease_nodes = {}
disease_symptoms = {}

for disease_id, data in query['vectors'].items():
    metadata = data.get("metadata", {})
    conditions_str = metadata.get("associated conditions", "")
    conditions = [condition.strip() for condition in conditions_str.split(',') if condition.strip()]
    
    if conditions:
        disease_nodes[disease_id] = conditions
        disease_symptoms[disease_id] = set(conditions)

# Step 3: Create a Pyvis Network object and add nodes and edges
net = Network(height="800px", width="100%", notebook=True)

# Add disease nodes
for disease in disease_nodes:
    net.add_node(disease, label=disease, color='skyblue', size=20)  # Disease nodes in skyblue

# Add edges for shared symptoms between diseases
for disease1, symptoms1 in disease_symptoms.items():
    for disease2, symptoms2 in disease_symptoms.items():
        if disease1 != disease2:
            common_symptoms = symptoms1.intersection(symptoms2)
            # If there are common symptoms and both disease1 and disease2 are ID nodes
            if common_symptoms:
                # Only add edges between ID nodes if there are more than 2 relationships
                if disease1 in disease_nodes and disease2 in disease_nodes and len(common_symptoms) > 2:
                    common_symptoms_str = ", ".join(common_symptoms)
                    net.add_edge(disease1, disease2, title=f"Shared Symptoms: {common_symptoms_str}", color="red")

# Add edges between diseases and their individual symptoms
for disease, conditions in disease_nodes.items():
    for condition in conditions:
        # Only add the edge if it's not a self-reference (disease -> disease through symptoms)
        if condition != disease:  # Avoid disease node pointing to itself
            net.add_node(condition, label=condition, color='lightgreen', size=15)  # Symptom nodes in lightgreen
            # Add edge with a label to show relationship
            net.add_edge(disease, condition, title=f"Associated with: {condition}")

# Step 4: Enable physics layout for the dynamic, interactive graph
net.force_atlas_2based()  # This layout allows nodes to repel and stay spread out

# Step 5: Create and render the Flask app with the Pyvis network
@app.route('/')
def index():
    # Save the network as an HTML file
    net.show("graph.html")
    # Render the graph in HTML inside the Flask template
    with open("graph.html", "r") as file:
        graph_html = file.read()
    return render_template('index.html', graph_html=graph_html)

# Run Flask app
if __name__ == '__main__':
    app.run(debug=True)

