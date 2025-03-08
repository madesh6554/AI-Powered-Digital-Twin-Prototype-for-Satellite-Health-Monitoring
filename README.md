# AI-Powered Digital Twin Prototype for Satellite Health Monitoring

## Overview
This project develops an **AI-powered digital twin** for **satellite health monitoring**, integrating **real-time data processing, machine learning, and predictive analytics**. The digital twin mirrors satellite behavior using **live telemetry data and historical trends**, improving reliability, reducing risks, and optimizing maintenance. 

## Features
- **Real-Time Monitoring:** Collects and processes telemetry data, including battery voltage, current, state of charge, power consumption, thermal data, and satellite positioning.
- **Anomaly Detection:** Uses AI models to identify deviations from normal behavior across multiple satellite parameters.
- **Predictive Maintenance:** Forecasts potential failures in subsystems such as power, thermal, and propulsion.
- **Digital Twin Simulation:** Creates a virtual representation for operational analysis and failure prediction.
- **Automated Alert System:** Triggers notifications (SMS, email, dashboard) when anomalies or failures are detected.
- **Data Visualization:** Provides interactive dashboards to monitor satellite health and performance.

## Key Parameters for Dataset & Model Development
The following telemetry parameters will be used to generate the dataset, train the anomaly detection model, and build the dashboard & alert system:

- **Power System:** Battery voltage, battery current, state of charge, solar panel voltage, solar panel current, solar panel efficiency, power consumption
- **Thermal System:** Internal temperature, battery temperature, solar panel temperature, radiator temperature, radiator efficiency, thermal gradient
- **Navigation & Control:** Position, velocity, gyroscope readings, magnetometer RPM, reaction wheel RPM, thruster status, orientation
- **Communications & Data Handling:** Signal strength, data rate, packet loss, payload power, sensor data rate, camera temperature, data quality, error flags, latency, bit error rate
- **Fault & Performance Monitoring:** Sensor discrepancies, thruster malfunctions, thruster efficiency, throughput, power anomalies, thermal anomalies, AOCS (Attitude and Orbit Control System) faults, payload failures

## Technologies Used
- **Machine Learning & AI:** TensorFlow, PyTorch, Scikit-learn
- **Data Processing:** Apache Kafka, Spark, Pandas
- **IoT & Telemetry:** MQTT, AWS IoT, Google Cloud
- **Alert System:** Twilio (SMS), AWS SNS (Notifications), Email Automation
- **Visualization Tools:** Tableau, Power BI, Web Dashboards

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/ai-digital-twin.git
   cd ai-digital-twin
   ```
2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   pip install -r requirements.txt
   ```

## Usage
1. **Run the Data Processing Module:**
   ```bash
   python data_processing.py
   ```
2. **Start the AI Model for Anomaly Detection:**
   ```bash
   python anomaly_detection.py
   ```
3. **Launch the Dashboard:**
   ```bash
   streamlit run dashboard.py
   ```

## Expected Outcomes
- Enhanced satellite reliability through real-time monitoring.
- Early anomaly detection to prevent failures.
- Reduced operational costs with predictive maintenance.
- Improved decision-making via AI-driven insights.

## Contributing
Contributions are welcome! Please submit a pull request or open an issue.

## License
This project is licensed under the MIT License.

## .gitignore
```
# Virtual environment
venv/

# Python cache files
__pycache__/
*.py[cod]

# Jupyter Notebook checkpoints
.ipynb_checkpoints/

# Logs and temporary files
logs/
*.log

# Dataset files
data/
*.csv
*.json
*.h5

# Environment variables
.env

# Compiled Python files
*.pyc

# IDE settings
.vscode/
.idea/
