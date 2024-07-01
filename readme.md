# Zambia Energy Dashboard

![Application](images\\dash.png) <!-- Update with the path to your logo image -->

## Overview

The Zambia Energy Dashboard is a comprehensive tool designed to monitor and analyze power supply and demand in Zambia. This dashboard focuses on various aspects of the energy sector, including electricity generation, consumption, and the state of Lake Kariba water levels. It aims to provide insights and data-driven analysis to help address the challenges of power outages and load shedding.

## Features

- **Real-time Data Visualization**: Interactive charts and graphs to visualize electricity data.
- **Predictive Analytics**: Advanced models to predict future water levels and electricity trends.
- **Comprehensive Insights**: Detailed analysis of power generation, consumption, and the impact of water levels on energy production.

## Data Sources

The dashboard uses the following datasets:
- `table_1.csv`: Contains data on electricity generation from various sources, electricity imports and exports, and national electricity consumption by economic sector.
- `lake.csv`: Contains data on Lake Kariba water levels measured by height variation and days.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/zambia-energy-dashboard.git
    ```
2. Change to the project directory:
    ```bash
    cd zambia-energy-dashboard
    ```
3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Prepare your data files:
    - Ensure you have `table_1.csv` and `lake.csv` in the `data` directory.

2. Run the Streamlit app:
    ```bash
    streamlit run main.py
    ```

3. Open your web browser and navigate to `http://localhost:8501` to view the dashboard.

## Project Structure

- `main.py`: Main script to run the Streamlit app.
- `model_utils.py`: Contains utility functions for training and predicting with ensemble models.
- `data/`: Directory to store the CSV data files.
- `images/`: Directory to store image files used in the dashboard.
- `README.md`: Project documentation.
- `requirements.txt`: List of required Python packages.

## Example Visualizations

### Lake Kariba Water Levels Over Time
![Lake Kariba Water Levels](path_to_your_lake_kariba_image) <!-- Update with the path to your image -->

### Predicted Lake Kariba Water Levels Over Next Year
![Predicted Water Levels](path_to_your_predicted_levels_image) <!-- Update with the path to your image -->

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

Developed by [Kampamba Shula](mailto:kampambashula@gmail.com)

- [GitHub](https://github.com/kshula)
- [LinkedIn](https://www.linkedin.com/in/yourprofile)

---

![Energy Image](images\\one.jpg) <!-- Update with the path to your energy-related image -->
