Advanced Keylogger tool.

This project is a Python-based host data collection framework designed to demonstrate how multiple telemetry sources can be integrated into a single, automated pipeline. 
The implementation emphasizes concurrency, modular data acquisition, encryption, and controlled exfiltration.
The system operates using a configuration-driven architecture (config.json) that defines file paths, execution intervals, encryption keys, and delivery parameters. 
At runtime, the application initializes parallel threads to collect static host metadata (OS, hardware, network identifiers) and browser history, 
while a timed execution loop continuously gathers dynamic data including keyboard input, clipboard contents, screenshots, and short audio samples. 
Keyboard events are captured asynchronously using an event listener, with buffered writes to minimize overhead.
Collected artifacts are staged to disk, selectively encrypted using symmetric cryptography (Fernet), and transmitted as email attachments via SMTP. 
The design separates plaintext capture files from encrypted delivery files to simplify processing and reduce coupling between components. 
Threading and ThreadPoolExecutor are used to coordinate concurrent capture, encryption, and transmission tasks while maintaining deterministic execution intervals.
The project also implements basic operational hygiene: centralized logging, exception handling across threads, one-time transmission of static system data, 
periodic transmission of dynamic data, and post-execution cleanup of generated artifacts.
This repository is intended for technical analysis, security research, and defensive tooling education,
offering insight into how coordinated host-level data collection, encryption, and exfiltration workflows are structured in practice.
