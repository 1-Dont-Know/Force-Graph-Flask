import os
from dotenv import load_dotenv
import pinecone
from pyvis.network import Network
from flask import Flask, render_template, request

# Load environment variables from .env file for Pinecone credentials
load_dotenv()

# Retrieve the Pinecone API key and index name from environment variables
api_key = os.getenv("PINECONE_API_KEY")
index_name = os.getenv("PINECONE_INDEX_NAME")

# Initialize Flask app for web server
app = Flask(__name__)

# Initialize Pinecone client using the API key 
pc = pinecone.Pinecone(api_key=api_key)

# Initialize the Pinecone index with the provided index name
pinecone_index = pc.Index(index_name)

# Set a default disease ID, can be modified by user input
preset_disease_id = "Fever"  # Example preset disease ID

# Cache dictionary to store node data for performance improvement
cache = {}

# Function to initialize and return a Pyvis network object
def create_network():
    """Initialize and return a Pyvis network object for visualizing the graph."""
    return Network(height="800px", width="100%", notebook=True)

# Function to fetch data from cache if available
def fetch_from_cache(node_id):
    """Retrieve data from the cache based on the node ID."""
    return cache.get(node_id)

# Function to store data in cache
def store_in_cache(node_id, data):
    """Store the fetched data in the cache for future use."""
    cache[node_id] = data

# Recursive function to fetch all connected nodes and build the graph
def fetch_all_data(node_id, visited, net):
    """Recursively fetch connected nodes (diseases, symptoms, etc.) and build the graph."""
    
    # Prevent processing empty or already visited nodes
    if not node_id or node_id in visited:
        return

    visited.add(node_id)

    # Check if the node data is already cached
    cached_data = fetch_from_cache(node_id)
    if cached_data:
        node_data = cached_data
    else:
        # Fetch data for the current node (disease or symptom) from Pinecone
        try:
            query = pinecone_index.fetch(ids=[node_id], namespace="test")
            node_data = query.get("vectors", {}).get(node_id, {})
            store_in_cache(node_id, node_data)  # Cache the fetched data
        except Exception as e:
            print(f"Error fetching data for node_id: {node_id}. Error: {e}")
            return

    if node_data:
        # Extract metadata from node data
        metadata = node_data.get("metadata", {})
        details = metadata.get("details", "")
        target_symptoms = metadata.get("target", [])
        relationships = metadata.get("relationship", [])
        sources = metadata.get("source", [])

        # Add the current node to the network if it’s not already added
        if node_id not in net.get_nodes():
            net.add_node(node_id, title=details)

        # Process target nodes (symptoms, causes, etc.)
        for i, target_id in enumerate(target_symptoms):
            if target_id:
                # Fetch target node details from Pinecone or cache
                target_data = fetch_from_cache(target_id)
                if not target_data:
                    try:
                        target_query = pinecone_index.fetch(ids=[target_id], namespace="test")
                        target_data = target_query.get("vectors", {}).get(target_id, {})
                        store_in_cache(target_id, target_data)  # Cache the fetched data
                    except Exception as e:
                        print(f"Error fetching target_id: {target_id}. Error: {e}")
                        continue

                target_details = target_data.get("metadata", {}).get("details", "")
                if target_id not in net.get_nodes() and target_details:
                    net.add_node(target_id, title=target_details)

                # Define relationship and edge colors based on the relationship type
                relationship = relationships[i] if i < len(relationships) else "UNKNOWN"
                edge_label = relationship.replace("_", " ").title()  # Format the relationship label
                edge_color = "gray"  # Default edge color

                # Assign specific colors based on the relationship type
                if relationship == "HAS_SYMPTOM":
                    edge_color = "blue"
                elif relationship == "IS_TRIGGERED_BY":
                    edge_color = "green"
                elif relationship == "TRIGGERS":
                    edge_color = "red"
                elif relationship == "IS_TREATED_WITH":
                    edge_color = "orange"

                # Add edge between current node and target node with the appropriate color and label
                if node_id in net.get_nodes() and target_id in net.get_nodes():
                    net.add_edge(node_id, target_id, title=edge_label, color=edge_color)

                # Recursively fetch data for the target node
                fetch_all_data(target_id, visited, net)

        # Process source nodes (e.g., causes, triggers, etc.)
        for source_id in sources:
            if source_id:
                # Fetch source node details from Pinecone or cache
                source_data = fetch_from_cache(source_id)
                if not source_data:
                    try:
                        source_query = pinecone_index.fetch(ids=[source_id], namespace="test")
                        source_data = source_query.get("vectors", {}).get(source_id, {})
                        store_in_cache(source_id, source_data)  # Cache the fetched data
                    except Exception as e:
                        print(f"Error fetching source_id: {source_id}. Error: {e}")
                        continue

                source_details = source_data.get("metadata", {}).get("details", "")
                if source_id not in net.get_nodes() and source_details:
                    net.add_node(source_id, title=source_details)

                # Add edge for the source node with label "Causes" and purple color
                if source_id in net.get_nodes() and node_id in net.get_nodes():
                    net.add_edge(source_id, node_id, title="Causes", color="purple")

                # Recursively fetch data for the source node
                fetch_all_data(source_id, visited, net)

# Function to initialize the network and start the recursive data fetching process
def fetch_connected_data(disease_id):
    """Initialize the network and start the recursive data fetching process from the disease ID."""
    visited = set()  # To keep track of visited nodes and prevent cycles
    net = create_network()  # Create a new network object
    fetch_all_data(disease_id, visited, net)  # Recursively fetch data starting from the disease ID
    return net

# Route to render the Flask app with user input for disease ID
@app.route('/', methods=['GET', 'POST'])
def index():
    """Handle user input and display the graph visualization of connected diseases and symptoms."""
    global preset_disease_id  # Use the preset disease ID for the initial view
    if request.method == 'POST':
        # Update the preset disease ID from user input
        disease_id = request.form['disease_id']
        preset_disease_id = disease_id

        # Fetch connected data and generate the graph
        net = fetch_connected_data(disease_id)
        net.show("graph.html")  # Generate HTML file for the graph

        # Read the generated HTML file and send it to the front-end
        with open("graph.html", "r") as file:
            graph_html = file.read()
        return render_template('index.html', graph_html=graph_html)

    # Fetch connected data for the preset disease ID and render the graph
    net = fetch_connected_data(preset_disease_id)
    net.show("graph.html")

    with open("graph.html", "r") as file:
        graph_html = file.read()

    return render_template('index.html', graph_html=graph_html)

# Run Flask app in debug mode
if __name__ == '__main__':
    app.run(debug=True)
