# Intrusion Detection System (IDS)

A Python-based network intrusion detection system that monitors network traffic and identifies potential security threats using both signature-based and anomaly-based detection methods.

## Features

- **Real-time packet capture** using Scapy
- **Signature-based detection** for known attack patterns (SYN flood, port scan)
- **Anomaly detection** using machine learning (Isolation Forest)
- **Traffic flow analysis** with packet and byte rate calculations
- **Alert logging** with configurable severity levels
- **Multi-threaded architecture** for concurrent packet processing

## Components

### Core Modules

- **`main.py`** - Main orchestrator that coordinates all system components
- **`packet_capture.py`** - Handles network packet capture using Scapy
- **`traffic_analyzer.py`** - Analyzes packet flows and extracts network features
- **`detection_engine.py`** - Implements threat detection using signatures and ML
- **`alert_system.py`** - Manages alert generation and logging

### Detection Methods

1. **Signature-based Detection**
   - SYN flood detection (high SYN packet rate)
   - Port scan detection (small packets at high rate)

2. **Anomaly Detection**
   - Uses Isolation Forest algorithm from scikit-learn
   - Detects unusual traffic patterns based on packet size, packet rate, and byte rate
   - Requires training on normal traffic data

## Requirements

```
scapy
scikit-learn
numpy
```

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install scapy scikit-learn numpy
   ```
3. Run with appropriate privileges (packet capture requires root/admin):
   ```bash
   sudo python main.py
   ```

## Usage

### Basic Usage

```python
from main import IntrusionDetectionSystem

# Initialize IDS with default interface (eth0)
ids = IntrusionDetectionSystem()
ids.start()

# Or specify a different interface
ids = IntrusionDetectionSystem(interface="wlan0")
ids.start()
```

### Training the Anomaly Detector

Before using anomaly detection effectively, train the model with normal traffic:

```python
# Collect normal traffic data
normal_data = [[packet_size, packet_rate, byte_rate], ...]

# Train the detector
ids.detection_engine.train_anomaly_detector(normal_data)
```

## Configuration

### Alert Thresholds

Modify detection thresholds in `detection_engine.py`:
- Anomaly score threshold: `-0.5` (lower values = more anomalous)
- High confidence alert threshold: `0.8`

### Signature Rules

Add new signature rules in `DetectionEngine.load_signature_rules()`:

```python
"new_rule": {
    "condition": lambda features: (
        # Your detection logic here
        features["some_feature"] > threshold
    )
}
```

## Output

The system generates alerts in two formats:

1. **Log file** (`ids_alerts.log`) - JSON formatted alerts with timestamps
2. **Console output** - Critical alerts for high-confidence threats

Example alert:
```json
{
  "timestamp": "2024-01-15T10:30:45.123456",
  "threat_type": "signature",
  "source_ip": "192.168.1.100",
  "destination_ip": "10.0.0.1",
  "confidence": 1.0,
  "details": {
    "type": "signature",
    "rule": "syn_flood",
    "confidence": 1.0
  }
}
```

## Limitations

- **Interface dependency**: Requires network interface access
- **Training required**: Anomaly detection needs training on normal traffic
- **Basic signatures**: Limited to simple attack patterns
- **No packet reassembly**: Analyzes individual packets, not reconstructed flows
- **Single-threaded analysis**: Traffic analysis runs in main thread

## Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│  PacketCapture  │───▶│ TrafficAnalyzer  │───▶│ DetectionEngine │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                                         │
                                                         ▼
                                               ┌─────────────────┐
                                               │  AlertSystem    │
                                               └─────────────────┘
```

## Contributing

To extend the system:

1. Add new signature rules in `DetectionEngine`
2. Implement additional feature extraction in `TrafficAnalyzer`
3. Enhance alert handling in `AlertSystem`
4. Add new ML models for anomaly detection

## License

This project is provided as-is for educational and research purposes.
