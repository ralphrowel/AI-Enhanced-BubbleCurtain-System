import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# ─────────────────────────────────────────
# 1. DATA SIMULATION
# ─────────────────────────────────────────

def simulate_sensor_data(n=100, freq='T'):
    """
    Simulate bubble curtain sensor readings.
    Returns a DataFrame with timestamp, trash_level, pressure, battery.
    """
    np.random.seed(42)
    data = {
        'timestamp': pd.date_range(start=datetime.now(), periods=n, freq=freq),
        'trash_level': np.random.choice(['LOW', 'MEDIUM', 'HIGH'], n, p=[0.5, 0.3, 0.2]),
        'pressure_value': np.round(np.random.uniform(0.1, 5.0, n), 2),
        'battery_level': np.round(np.random.uniform(20.0, 100.0, n), 1),
        'device_status': np.random.choice(['ONLINE', 'OFFLINE'], n, p=[0.95, 0.05]),
    }
    return pd.DataFrame(data)


# ─────────────────────────────────────────
# 2. PREPROCESSING
# ─────────────────────────────────────────

def encode_trash_level(df):
    """
    Encode trash_level column: LOW=0, MEDIUM=1, HIGH=2
    """
    mapping = {'LOW': 0, 'MEDIUM': 1, 'HIGH': 2}
    df = df.copy()
    df['trash_level_encoded'] = df['trash_level'].map(mapping)
    return df


def normalize_column(df, column):
    """
    Normalize a numeric column to range [0, 1].
    """
    df = df.copy()
    min_val = df[column].min()
    max_val = df[column].max()
    df[column + '_normalized'] = (df[column] - min_val) / (max_val - min_val)
    return df


def handle_missing_values(df):
    """
    Fill missing numeric values with column mean.
    Drop rows where trash_level is missing.
    """
    df = df.copy()
    df['pressure_value'] = df['pressure_value'].fillna(df['pressure_value'].mean())
    df['battery_level'] = df['battery_level'].fillna(df['battery_level'].mean())
    df = df.dropna(subset=['trash_level'])
    return df


# ─────────────────────────────────────────
# 3. VISUALIZATION HELPERS
# ─────────────────────────────────────────

def plot_pressure_over_time(df):
    """
    Line chart of pressure_value over time.
    """
    plt.figure(figsize=(12, 4))
    plt.plot(df['timestamp'], df['pressure_value'], color='steelblue', linewidth=1.5)
    plt.title('Bubble Pressure Over Time')
    plt.xlabel('Timestamp')
    plt.ylabel('Pressure (bar)')
    plt.tight_layout()
    plt.show()


def plot_trash_level_distribution(df):
    """
    Bar chart showing frequency of each trash level.
    """
    counts = df['trash_level'].value_counts().reindex(['LOW', 'MEDIUM', 'HIGH'])
    colors = ['green', 'orange', 'red']
    plt.figure(figsize=(6, 4))
    counts.plot(kind='bar', color=colors, edgecolor='black')
    plt.title('Trash Level Distribution')
    plt.xlabel('Trash Level')
    plt.ylabel('Count')
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.show()


def plot_battery_trend(df):
    """
    Line chart showing battery level over time.
    """
    plt.figure(figsize=(12, 4))
    plt.plot(df['timestamp'], df['battery_level'], color='orange', linewidth=1.5)
    plt.axhline(y=20, color='red', linestyle='--', label='Critical (20%)')
    plt.title('Battery Level Over Time')
    plt.xlabel('Timestamp')
    plt.ylabel('Battery (%)')
    plt.legend()
    plt.tight_layout()
    plt.show()


# ─────────────────────────────────────────
# 4. FILE HELPERS
# ─────────────────────────────────────────

def save_dataframe(df, filename, folder='data'):
    """
    Save a DataFrame as CSV inside a given folder.
    Creates the folder if it doesn't exist.
    """
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, filename)
    df.to_csv(path, index=False)
    print(f"Saved: {path}")


def load_dataframe(filename, folder='data'):
    """
    Load a CSV file from a given folder.
    """
    path = os.path.join(folder, filename)
    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")
    return pd.read_csv(path)