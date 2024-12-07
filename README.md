# Disease Network Visualization

This project provides an interactive web-based visualization of disease networks, built with Flask and Pinecone. It allows users to input a disease ID and explore its relationships with symptoms, triggers, and treatments. The visualization is displayed as a dynamic graph using Pyvis and Flask.

## Features

- **Interactive Disease Network**: Visualizes diseases and their associated symptoms, triggers, and treatments.
- **Color-coded Relationships**: Different types of relationships (HAS_SYMPTOM, IS_TRIGGERED_BY, TRIGGERS, IS_TREATED_WITH) are color-coded for easy understanding.
- **User Input**: Users can input a disease ID to view its network and explore connected diseases and symptoms.
- **Graph Display**: A dynamic network graph is generated using Pyvis and displayed in the browser.

## Requirements

- Python 3.6+
- Flask
- Pinecone
- Pyvis
- Python-dotenv

### Install Dependencies

To set up the project locally, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/disease-network-visualization.git
   cd disease-network-visualization

2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
3. Create a .env file in the root directory and add your Pinecone API credentials:
   ```bash
   PINECONE_API_KEY=your-pinecone-api-key
   PINECONE_INDEX_NAME=your-pinecone-index-name

## Usage
1. Run the Flask app:

   ```bash
   python app.py
2.Visit the app in your browser at http://127.0.0.1:5000/.
3.Input a disease ID into the form and submit to view the connected disease network in the graph format.
4.The graph will dynamically update with nodes representing diseases and symptoms, and edges representing relationships between them.

# How It Works
1. Backend (Flask + Pinecone): The Flask backend handles the logic for fetching disease data from Pinecone, building the network graph, and rendering the visualization in HTML format.
2. Graph Visualization (Pyvis): Pyvis is used to create a dynamic network graph that shows the relationships between diseases and symptoms. The relationships are color-coded based on the type:

   Blue: HAS_SYMPTOM
   Green: IS_TRIGGERED_BY
   Red: TRIGGERS
   Orange: IS_TREATED_WITH
   Purple: Causes (from source nodes)

3. Caching: Data from Pinecone is cached for performance improvements to avoid redundant queries.

4. User Input: Users can input a disease ID to dynamically update the visualization.
