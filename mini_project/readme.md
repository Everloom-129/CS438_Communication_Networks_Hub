# Communication Networks Wireless Project

## Project Overview
This open-source project presents a Python-based analytical tool designed to conduct a comprehensive wireless network analysis. Developed at Urbana, IL from April 2023 to May 2023, the tool specializes in examining Wi-Fi access points, focusing on the mechanisms of roaming and signal strength distribution across various locations.

## Features
- **Roaming Mechanisms Analysis:** Deep dive into the behavior of Wi-Fi access points and their roaming mechanisms.
- **Signal Strength Heatmap:** Generate heatmaps to visualize the signal strength distribution effectively.
- **Data Pipeline Architecture:** A procedure-oriented pipeline for data handling, from collection to processing and analysis.
- **UIUC Campus Network Analysis:** A focused study on the Thomas M. Siebel Center's network environment at the University of Illinois Urbana-Champaign.

## Usage

### Prerequisites
- Floor plan map of your target building
- Python 3.8 or above
- Necessary Python libraries: `numpy`, `matplotlib`, `scipy`, etc.

### Installation
1. Clone the repository to your local machine:
    ```sh
    git clone https://github.com/Everloom-129/CS438_Communication_Networks_Hub.git
    ```
2. Navigate to the project directory:
    ```sh
    cd communication-networks-wireless-project
    ```
3. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

### Running the Tool
1. To begin data collection, execute:
    ```sh
    python data_collector.py
    ```
2. For data preprocessing, run:
    ```sh
    python data_preprocessor.py
    ```
3. Generate heatmaps using:
    ```sh
    python heatmap_generator.py
    ```
4. Conduct individual AP analysis with:
    ```sh
    python ap_analyzer.py
    ```

## Contributing
We welcome contributions from the community. If you wish to contribute, please fork the repository and submit a pull request.

## Collaboration
This project was conducted in collaboration with the UIUC IT Network team, contributing to a comprehensive report on the real-world network environment of UIUC.

## License
This project is licensed under the MIT License.
