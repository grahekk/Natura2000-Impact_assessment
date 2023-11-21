# Natura2000-Impact_assessment
This is a repository of a tool for generating reports or assessments of potential impacts of development projects on Natura 2000 ecological network sites.

## overview
This Python tool is designed to assess the impacts of development projects on the Natura 2000 ecological network. The Natura 2000 network is a network of protected areas in the European Union, established to ensure the long-term survival of Europe's most valuable and threatened species and habitats.
Most of the scripts are still standalone while some are chained. Some scripts are used for qgis autimatization, while others are here to provide data for qgis (scraper scripts). 
These scraper scripts are downloading data predominantly in spatial boundaries of Republic of Croatia.
Feel free to explore and download some data using those scripts. Some of those scripts are outdated and buggy and need fixing.

## Natura2000 network
For more info about what this is and general purpose why these scripts were written in the first place, see: https://www.eea.europa.eu/themes/biodiversity/natura-2000

## Features

- **Impact Assessment:** The tool provides functionality to assess the potential impacts of development projects on the Natura 2000 network.
  
- **Data Download:** It automates the process of downloading relevant data for impact assessment from specified sources.

- **Report Generation:** The tool generates reports summarizing the impact assessment results for easy interpretation.

## Installation

To use this tool, follow these steps:

1. Clone the repository to your local machine:

    ```bash
    git clone https://github.com/grahekk/Natura2000-Impact_assessment
    ```

2. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Run the tool:

    ```bash
    python main.py
    ```

## Usage

1. Configure the tool by modifying the configuration files in the `config/` directory. (Which I have not yet created)

2. Run the tool to perform the impact assessment:

    ```bash
    python main.py
    ```

3. View the generated reports in the `reports/` directory.

## Configuration

Adjust the configuration files in the `config/` directory to customize the tool's behavior. Configuration includes input data sources, parameters for impact assessment, and output settings.

## Data Sources

This tool relies on specific data sources to perform impact assessments. Ensure that these sources are accessible and up-to-date. Refer to the configuration files for details on data sources.

## Contributing

If you would like to contribute to the development of this tool, please follow these steps:

1. Fork the repository.

2. Create a new branch for your feature or bug fix:

    ```bash
    git checkout -b feature-name
    ```

3. Make your changes and commit them:

    ```bash
    git commit -m "Description of your changes"
    ```

4. Push the changes to your fork:

    ```bash
    git push origin feature-name
    ```

5. Create a pull request.
