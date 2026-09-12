# Smart Edge Analytical System

An AI-powered smart traffic management and video analytics system utilizing YOLOv8 object detection to monitor traffic flow, analyze edge data, and store real-time records.

## 🚀 Features
- **Real-Time Traffic Detection:** Uses YOLOv8 (`yolov8n.pt` / `yolov8s.pt`) for vehicle tracking and analysis.
- **Edge Analytics:** Processes video feeds at the edge to optimize analysis speed and latency.
- **Database Logs:** Automatically records detection data into `traffic_analytics_database.csv`.

## 📁 Repository Structure
- `main.py` - Primary Python application script.
- `traffic_video.mp4` - Sample video feed for testing and analysis.
- `yolov8n.pt` / `yolov8s.pt` - Pre-trained YOLOv8 weights.
- `traffic_analytics_database.csv` - Output analytics log file.

## 🛠️ How to Run
1. Clone this repository:
   ```bash
   git clone [https://github.com/maryambashir1455-hub/smart-edge-analytical-system.git](https://github.com/maryambashir1455-hub/smart-edge-analytical-system.git)
   cd smart-edge-analytical-system
   Install dependencies:

Bash
pip install ultralytics opencv-python pandas
Run the application:

Bash
python main.py
### Steps to save it:
1. Click the green **"Add a README"** button on GitHub.
2. Paste the code above into the main editor box.
3. Click the green **"Commit changes..."** button at the top right to save
