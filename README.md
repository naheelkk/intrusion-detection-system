# Intrusion Detection System (IDS)

A Python-based network intrusion detection system prototype that monitors network traffic and identifies potential security threats using both signature-based and anomaly-based detection methods.

## ⚠️ Important Disclaimers

This is a **proof-of-concept implementation** with significant limitations. It is intended for educational purposes and should not be used in production environments without substantial improvements.

## Features (Current Implementation)

- **Basic packet capture** using Scapy (TCP packets only)
- **Simple signature-based detection** for basic attack patterns
- **Experimental anomaly detection** using Isolation Forest
- **Basic traffic flow analysis** with packet and byte rate calculations
- **Alert logging** to file and console
- **Single-threaded architecture** with basic packet processing

## Known Limitations

### Critical Issues
- **Threading bug**: The packet capture threading implementation has a bug that may cause the capture thread to not start properly
- **Interface dependency**: Hardcoded to "Wi-Fi" interface, may not work on all systems
- **Error handling**: Minimal error handling for network issues or permission problems
- **Single-threaded processing**: Despite claims of multi-threading, packet analysis runs in the main thread
- **No packet reassembly**: Analyzes individual packets without considering connection state

### Detection Limitations
- **Basic signatures**: Only detects simple SYN flood and port scan patterns
- **High false positives**: Anomaly detection threshold may trigger on normal traffic variations
- **Training required**: Anomaly detection needs manual training data collection
- **Limited protocol support**: Only handles TCP packets, ignores UDP and other protocols
- **No rate limiting**: Signature detection may trigger on single packets rather than sustained attacks

### Performance Issues
- **Memory usage**: Flow statistics accumulate indefinitely without cleanup
- **Blocking operations**: Uses blocking queue operations that may cause delays
- **No optimization**: No performance optimizations for high-traffic environments

## Requirements

```
scapy>=2.4.0
scikit-learn>=1.0.0
numpy>=1.20.0
```

**System Requirements:**
- Root/administrator privileges for packet capture
- Compatible network interface (may need to change from "Wi-Fi" to your interface name)
- Python 3.7+ recommended

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install scapy scikit-learn numpy
   ```
3. **Important**: Modify `main.py` to use your correct network interface name
4. Run with appropriate privileges:
   ```bash
   sudo python main.py
   ```

## Usage

### Basic Usage (With Caveats)

```python
from main import IntrusionDetectionSystem

# Note: Default interface is "Wi-Fi" - change this in main.py
ids = IntrusionDetectionSystem()
ids.start()  # May have threading issues
```

### Training the Anomaly Detector

The anomaly detector requires training before meaningful detection:

```python
# Collect normal traffic data manually
normal_data = [
    [packet_size, packet_rate, byte_rate],
    [100, 10, 1000],  # Example values
    [150, 5, 750],
    # ... more normal traffic samples needed
]

# Train the detector
ids.detection_engine.train_anomaly_detector(normal_data)
```

## Configuration

### Detection Thresholds (May Need Tuning)

Current thresholds in `detection_engine.py`:
- Anomaly score threshold: `-0.5` (very sensitive, may cause false positives)
- High confidence alert threshold: `0.8`
- SYN flood threshold: `>100 packets/second` (may be too low)
- Port scan threshold: `<100 byte packets at >50/second`

### Adding Signature Rules

Basic example of adding rules in `DetectionEngine.load_signature_rules()`:

```python
"custom_rule": {
    "condition": lambda features: (
        features["packet_size"] > 1500  # Large packet detection
        and features["packet_rate"] > 10
    )
}
```

## Output

The system generates alerts in two formats:

1. **Log file** (`ids_alerts.log`) - JSON formatted alerts
2. **Console output** - High-confidence alerts only

Example alert structure:
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

## Testing

A basic test script is provided (`test.py`) that simulates packet processing:

```bash
python test.py
```

This runs offline tests with simulated packets rather than live traffic capture.

## Current Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│  PacketCapture  │───▶│ TrafficAnalyzer  │───▶│ DetectionEngine │
│   (TCP only)    │    │  (Basic stats)   │    │ (Simple rules)  │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                                         │
                                                         ▼
                                               ┌─────────────────┐
                                               │  AlertSystem    │
                                               │ (File logging)  │
                                               └─────────────────┘
```

## Recommendations for Improvement

To make this system production-ready, consider:

1. **Fix threading issues** in packet capture
2. **Add proper error handling** for network operations
3. **Implement connection state tracking** for better analysis
4. **Add support for more protocols** (UDP, ICMP, etc.)
5. **Improve signature rules** with more sophisticated detection logic
6. **Add configuration file** for easy threshold adjustment
7. **Implement proper flow cleanup** to prevent memory leaks
8. **Add rate limiting** and traffic normalization
9. **Include more comprehensive testing** with real attack scenarios
10. **Add performance monitoring** and optimization

## Educational Value

This implementation demonstrates:
- Basic network packet analysis concepts
- Simple machine learning application to security
- Event-driven architecture patterns
- Python networking and threading (with caveats)

## Contributing

If you'd like to improve this system:

1. **Priority fixes**: Address the threading and error handling issues
2. **Add features**: Implement missing protocol support
3. **Improve detection**: Add more sophisticated signature rules
4. **Performance**: Optimize for higher traffic volumes
5. **Testing**: Add comprehensive unit and integration tests

## License

This project is provided as-is for educational and research purposes. Use at your own risk and do not deploy in production environments without significant modifications and testing.
