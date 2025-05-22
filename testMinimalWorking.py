from scapy.all import IP, TCP
import logging
from main import IntrusionDetectionSystem
## minimal working test file
# Setup logging
logging.basicConfig(
    filename="ids_log.txt",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    filemode='w'
)

def test_ids():
    test_packets = [
        IP(src="192.168.1.1", dst="192.168.1.2") / TCP(sport=1234, dport=80, flags="A"),
        IP(src="10.0.0.1", dst="192.168.1.2") / TCP(sport=5678, dport=80, flags="S"),
        IP(src="192.168.1.100", dst="192.168.1.2") / TCP(sport=4321, dport=22, flags="S"),
    ]

    ids = IntrusionDetectionSystem()

    # Train the anomaly detector
    normal_data = [[100, 1, 100], [200, 2, 100], [150, 1.5, 100]]
    ids.detection_engine.train_anomaly_detector(normal_data)

    print("Starting IDS Test...")
    for i, packet in enumerate(test_packets, 1):
        print(f"\nProcessing packet {i}: {packet.summary()}")
        features = ids.traffic_analyzer.analyze_packet(packet)

        if features:
            threats = ids.detection_engine.detect_threats(features)
            if threats:
                print(f"Detected threats: {threats}")
                logging.info(f"Packet {i}: Detected threats: {threats}")
            else:
                print("No threats detected.")
                logging.info(f"Packet {i}: No threats detected.")
        else:
            print("Packet skipped.")
            logging.info(f"Packet {i}: Skipped (not TCP/IP)")

    print("\nIDS Test Completed.")

if __name__ == "__main__":
    test_ids()
