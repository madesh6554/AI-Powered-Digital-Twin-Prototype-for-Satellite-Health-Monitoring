import mysql.connector
import pandas as pd
import joblib
import streamlit as st
import numpy as np
import time
import smtplib
import random
from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from sklearn.preprocessing import MinMaxScaler
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Configuration
DIGITAL_TWIN_VERSION = "4.0"
SYSTEM_ID = "SAT-2025-DT-001"
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "Madesh6554@12",
    "database": "satellite_data",
    "table": "real_time_data_3"
}
MODEL_PATH = "best_health_isolation_forest.pkl"
ALERT_CONFIG = {
    "sender": "mass1441m2@gmail.com",
    "receiver": "madesh6554@gmail.com",
    "password": "vozt twrn pldb vfco"
}

class DatabaseManager:
    def __enter__(self):
        self.conn = mysql.connector.connect(
            host=DB_CONFIG["host"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            database=DB_CONFIG["database"]
        )
        return self.conn.cursor()
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.commit()
        self.conn.close()

class DataGenerator:
    def __init__(self):
        self.last_timestamp = datetime.now() - timedelta(minutes=1)
        self.param_config = {
            "timestamp": None,
            "battery_voltage": (24, 32, 28, 1.5),
            "battery_current": (3, 7, 5, 0.5),
            "state_of_charge": (60, 100, 80, 3),
            "solar_panel_voltage": (90, 110, 100, 5),
            "solar_panel_current": (6, 10, 8, 0.5),
            "solar_panel_efficiency": (15, 28, 22, 2),
            "power_consumption": (120, 180, 150, 10),
            "internal_temp": (15, 35, 25, 3),
            "battery_temp": (25, 35, 30, 2),
            "solar_panel_temp": (30, 50, 40, 5),
            "radiator_temp": (15, 25, 20, 2),
            "radiator_efficiency": (75, 95, 85, 3),
            "thermal_gradient": (3, 7, 5, 1),
            "position": (300, 500, 400, 50),
            "velocity": (7.4, 7.8, 7.6, 0.1),
            "gyroscope": (0.03, 0.07, 0.05, 0.01),
            "magnetometer_rpm": (4800, 5200, 5000, 100),
            "reaction_wheel_rpm": (2900, 3100, 3000, 50),
            "thruster_status": (0, 1, 0.95),
            "signal_strength": (-80, -60, -70, 5),
            "data_rate": (90, 110, 100, 5),
            "packet_loss": (0, 5, 0.5, 0.2),
            "payload_power": (45, 55, 50, 2),
            "sensor_data_rate": (9, 11, 10, 0.5),
            "camera_temp": (10, 20, 15, 2),
            "data_quality": (95, 100, 98, 1),
            "error_flags": (0, 1, 0.97),
            "latency": (100, 300, 200, 50),
            "bit_error_rate": (1e-7, 1e-5, 1e-6, 5e-7),
            "sensor_discrepancies": (0, 1, 0.98),
            "thruster_malfunctions": (0, 1, 0.99),
            "thruster_efficiency": (90, 100, 95, 2),
            "orientation": (-10, 10, 0, 5),
            "throughput": (90, 100, 95, 2),
            "power_anomalies": (0, 1, 0.95),
            "thermal_anomalies": (0, 1, 0.95),
            "aocs_faults": (0, 1, 0.95),
            "payload_failures": (0, 1, 0.95)
        }

    def _generate_value(self, config):
        if len(config) == 4:
            min_val, max_val, mean, std = config
            return np.clip(random.gauss(mean, std), min_val, max_val)
        return 0 if random.random() < config[2] else 1

    def generate_data_point(self):
        self.last_timestamp += timedelta(minutes=1)
        data = {"timestamp": self.last_timestamp}
        for param, config in self.param_config.items():
            if param != "timestamp":
                data[param] = self._generate_value(config)
        if random.random() < 0.07:
            anomaly_type = random.choice(["power", "thermal", "aocs", "payload"])
            if anomaly_type == "power":
                data["battery_voltage"] *= 0.6
                data["power_anomalies"] = 1
            elif anomaly_type == "thermal":
                data["internal_temp"] += 20
                data["thermal_anomalies"] = 1
            elif anomaly_type == "aocs":
                data["gyroscope"] *= 10
                data["aocs_faults"] = 1
            else:
                data["payload_failures"] = 1
                data["data_quality"] = 0
        return data

class AnomalyDetector:
    def __init__(self):
        self.model = joblib.load(MODEL_PATH)
        self.scaler = MinMaxScaler()
        self.features = [
            "battery_voltage", "battery_current", "state_of_charge",
            "solar_panel_voltage", "solar_panel_current", "solar_panel_efficiency",
            "power_consumption", "internal_temp", "battery_temp",
            "solar_panel_temp", "radiator_temp", "radiator_efficiency",
            "thermal_gradient", "position", "velocity", "gyroscope",
            "magnetometer_rpm", "reaction_wheel_rpm", "thruster_status",
            "signal_strength", "data_rate", "packet_loss", "payload_power",
            "sensor_data_rate", "camera_temp", "data_quality", "error_flags",
            "latency", "bit_error_rate", "sensor_discrepancies",
            "thruster_malfunctions", "thruster_efficiency", "orientation",
            "throughput", "power_anomalies", "thermal_anomalies",
            "aocs_faults", "payload_failures"
        ]

    def predict(self, data):
        df = pd.DataFrame([data])
        scaled_data = self.scaler.fit_transform(df[self.features])
        return self.model.predict(scaled_data)[0] == -1

class AlertSystem:
    def send_alert(self, data):
        try:
            msg = MIMEMultipart()
            msg['From'] = ALERT_CONFIG["sender"]
            msg['To'] = ALERT_CONFIG["receiver"]
            msg['Subject'] = f"🚨 {SYSTEM_ID} Anomaly Alert - {data['timestamp']}"
            body = f"""
            CRITICAL ANOMALY DETECTED!
            System: {SYSTEM_ID}
            Timestamp: {data['timestamp']}
            Key Parameters:
            - Battery Voltage: {data['battery_voltage']:.2f} V
            - Internal Temperature: {data['internal_temp']:.1f}°C
            - Gyroscope: {data['gyroscope']:.4f} rad/s
            - Data Quality: {data['data_quality']:.1f}%"""
            msg.attach(MIMEText(body, 'plain'))
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(ALERT_CONFIG["sender"], ALERT_CONFIG["password"])
            server.sendmail(ALERT_CONFIG["sender"], ALERT_CONFIG["receiver"], msg.as_string())
            server.quit()
        except Exception as e:
            st.error(f"Alert failed: {str(e)}")

class SatelliteDashboard:
    def __init__(self, data_generator):
        self.generator = data_generator
        st.set_page_config(page_title=f"{SYSTEM_ID} Monitor", layout="wide")
        st.title(f"🌍 {SYSTEM_ID} Digital Twin Dashboard")
        self.status_container = st.empty()
        self.metrics_container = st.container()
        self.chart_container = st.empty()
        st.sidebar.button("🔄 Manual Refresh", key="refresh")
        if 'history' not in st.session_state:
            self._load_initial_data()

    def _load_initial_data(self):
        with DatabaseManager() as cursor:
            cursor.execute(f"SELECT * FROM {DB_CONFIG['table']} ORDER BY timestamp DESC LIMIT 10")
            st.session_state.history = [dict(zip([col[0] for col in cursor.description], row)) for row in cursor.fetchall()]

    def update_display(self, data, anomaly):
        self._update_status(data, anomaly)
        self._update_metrics(data)
        self._update_charts()

    def _update_status(self, data, anomaly):
        status_color = "#FF4B4B" if anomaly else "#0F9D58"
        self.status_container.markdown(f"""
            <div style="padding:20px; background:{status_color}10; border-radius:10px; margin-bottom:20px;
                        border-left:5px solid {status_color}; box-shadow: 0 2px 4px rgba(0,0,0,0.1)">
                <h2 style="color:{status_color}; margin:0;">
                    {'🚨 CRITICAL ANOMALY DETECTED' if anomaly else '✅ SYSTEM NOMINAL'} 
                    <span style="float:right; font-size:0.8em; color:#666;">{DIGITAL_TWIN_VERSION}</span>
                </h2>
                <p style="margin:5px 0 0 0; color:#666;">
                    Last Update: {data['timestamp'].strftime('%Y-%m-%d %H:%M:%S UTC')}
                </p>
            </div>""", unsafe_allow_html=True)

    def _update_metrics(self, data):
        with self.metrics_container:
            st.subheader("🔑 Key System Metrics")
            cols = st.columns(4)
            metrics = [
                ("⚡ Power Systems", ['battery_voltage', 'solar_panel_voltage', 'power_consumption']),
                ("🌡 Thermal Systems", ['internal_temp', 'battery_temp', 'solar_panel_temp']),
                ("🛰 AOCS", ['gyroscope', 'orientation', 'reaction_wheel_rpm']),
                ("📡 Communications", ['signal_strength', 'data_rate', 'packet_loss'])
            ]
            for col, (title, params) in zip(cols, metrics):
                with col:
                    st.markdown(self._build_metric_card(title, params, data), unsafe_allow_html=True)

    def _build_metric_card(self, title, params, data):
        html = f"""
        <div style="padding:15px; background:#FFFFFF; border-radius:10px; border:1px solid #EEE; 
                    margin-bottom:20px; box-shadow:0 2px 4px rgba(0,0,0,0.05)">
            <h4 style="margin:0 0 15px 0; color:#2C3E50;">{title}</h4>"""
        for param in params:
            value = data[param]
            config = self.generator.param_config[param]
            min_val, max_val = (config[0], config[1]) if len(config) == 4 else (None, None)
            unit = self._get_unit(param)
            
            # Format value safely
            try:
                formatted_value = f"{float(value):.2f}{unit}" if isinstance(value, (int, float)) else f"{value}{unit}"
            except:
                formatted_value = f"{value}{unit}"
            
            alert = "⚠️" if (min_val and max_val and not (min_val <= value <= max_val)) else ""
            
            html += f"""
            <div style="margin-bottom:12px;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <span style="color:#666; font-size:0.9em;">{param.replace('_', ' ').title()}</span>
                    <span style="color:#FF4B4B;">{alert}</span>
                </div>
                <div style="font-size:1.4em; color:#2C3E50;">
                    {formatted_value}
                </div>
                <div style="font-size:0.8em; color:#888;">
                    Range: {min_val:.1f}-{max_val:.1f}{unit}
                </div>
            </div>"""
        return html + "</div>"

    def _update_charts(self):
        with self.chart_container:
            st.subheader("📈 Real-Time Telemetry Trends (Last 10 Readings)")
            df = pd.DataFrame(st.session_state.history[-10:]).set_index('timestamp')
            fig = make_subplots(rows=2, cols=2, subplot_titles=(
                'Battery Voltage (V)', 'Internal Temperature (°C)', 
                'Gyroscope (rad/s)', 'Data Quality (%)'))
            fig.add_trace(go.Scatter(x=df.index, y=df.battery_voltage, name='Battery', line=dict(color='#4285F4')), 1, 1)
            fig.add_trace(go.Scatter(x=df.index, y=df.internal_temp, name='Temp', line=dict(color='#DB4437')), 1, 2)
            fig.add_trace(go.Scatter(x=df.index, y=df.gyroscope, name='Gyro', line=dict(color='#0F9D58')), 2, 1)
            fig.add_trace(go.Scatter(x=df.index, y=df.data_quality, name='Quality', line=dict(color='#F4B400')), 2, 2)
            fig.update_layout(height=600, showlegend=False, margin=dict(l=40, r=40, t=80, b=40),
                            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)

    def _get_unit(self, param):
        units = {
            "voltage": "V", "current": "A", "temp": "°C", "efficiency": "%",
            "consumption": "W", "velocity": "km/s", "rpm": "RPM",
            "rate": "Mbps", "loss": "%", "error": "bps", "orientation": "°"
        }
        return next((v for k, v in units.items() if k in param.lower()), "")

def main():
    generator = DataGenerator()
    detector = AnomalyDetector()
    alert = AlertSystem()
    dashboard = SatelliteDashboard(generator)

    if 'last_update' not in st.session_state:
        st.session_state.update({
            'last_update': datetime.min,
            'history': [],
            'data': None,
            'anomaly': False
        })

    if (datetime.now() - st.session_state.last_update).total_seconds() >= 2:
        try:
            new_data = generator.generate_data_point()
            anomaly = detector.predict(new_data)
            
            # Add anomaly status to data
            new_data['anomaly'] = int(anomaly)

            with DatabaseManager() as cursor:
                # Insert with anomaly column
                columns = list(new_data.keys())
                values = list(new_data.values())
                cursor.execute(
                    f"INSERT INTO {DB_CONFIG['table']} ({', '.join(columns)}) VALUES ({', '.join(['%s']*len(values))})",
                    values
                )

            # Keep only last 10 entries
            st.session_state.history = [new_data] + st.session_state.history[:9]
            
            st.session_state.update({
                'last_update': datetime.now(),
                'data': new_data,
                'anomaly': anomaly
            })
            
            if anomaly:
                alert.send_alert(new_data)

        except Exception as e:
            st.error(f"System Error: {str(e)}")

    if st.session_state.data:
        dashboard.update_display(st.session_state.data, st.session_state.anomaly)

    time.sleep(1)
    st.rerun()

if __name__ == "__main__":
    main()