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
