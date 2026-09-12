import cv2
import time
import csv
import os
from datetime import datetime
from ultralytics import YOLO

# ==============================================================================
# INTERMEDIATE FUNCTIONS (Aage ke features bina code erase kiye yahan judenge)
# ==============================================================================

def save_to_database(folder_path, file_name, vehicle_id, vehicle_type, speed):
    """
    Yeh function har vehicle ka data live Excel sheet mein save karta hai.
    Aage chal kar Number Plate ka data bhi isi function ke andar bina main code erase kiye save hoga.
    """
    csv_file = os.path.join(folder_path, file_name)
    current_date = datetime.now().strftime('%Y-%m-%d')
    current_time = datetime.now().strftime('%H:%M:%S') # Exact Time (Hour:Minute:Second)
    
    with open(csv_file, mode='a', newline='') as f:
        writer = csv.writer(f)
        # Yahan humne Date aur Exact Time dono ko alag-alag columns mein add kar diya hai
        writer.writerow([current_date, current_time, vehicle_id, vehicle_type, f"{speed} KM/H"])

# ==============================================================================
# MAIN SYSTEM CONFIGURATION & INITIALIZATION
# ==============================================================================

# 1. Load YOLOv8 Small model for better accuracy
model = YOLO('yolov8s.pt')

# 2. Open Video File
video_path = 'traffic_video.mp4'
cap = cv2.VideoCapture(video_path)

# 3. AUTOMATIC FOLDER & DATABASE CREATION
# Aapke laptop mein automatic 'Traffic_Database' naam ka folder ban jayega
database_folder = "Traffic_Database"
if not os.path.exists(database_folder):
    os.makedirs(database_folder)

# Har baar jab aap code run karengi, ek nayi Excel file banegi date ke naam se
current_date_str = datetime.now().strftime('%Y-%m-%d_%H-%M')
database_file = f"traffic_report_{current_date_str}.csv"
full_csv_path = os.path.join(database_folder, database_file)

# Excel ke Columns/Headers ready karna
with open(full_csv_path, mode='w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Date', 'Exact_Time_Arrival', 'Vehicle_ID', 'Vehicle_Type', 'Estimated_Speed'])

# Tracking Variables
vehicle_timestamps = {}
tracked_vehicles = set()
vehicle_count = 0

# Detection Zone Coordinates
zone_start_y = 420  
zone_end_y = 470  
DISTANCE_METERS = 10  

# ==============================================================================
# THE MAIN PROCESSING LOOP
# ==============================================================================
while cap.isOpened():
    success, frame = cap.read()
    
    if success:
        # Run tracking with confidence threshold to remove wrong person/bike detections
        results = model.track(frame, persist=True, conf=0.35)
        annotated_frame = results[0].plot()
        
        boxes = results[0].boxes.xyxy.cpu().numpy() if results[0].boxes.xyxy is not None else []
        ids = results[0].boxes.id.cpu().numpy() if results[0].boxes.id is not None else None
        clss = results[0].boxes.cls.cpu().numpy() if results[0].boxes.cls is not None else []
        names = model.names
        
        target_classes = [1, 2, 3, 5, 7] # bike, car, motorcycle, bus, truck
        current_vehicle_count = 0
        
        if ids is not None:
            for box, id, cls in zip(boxes, ids, clss):
                if int(cls) in target_classes:
                    current_vehicle_count += 1
                    v_type = names[int(cls)]
                    x1, y1, x2, y2 = box
                    center_y = int((y1 + y2) / 2)
                    
                    # Entry Time Tracker (Jab gaadi top line par aaye)
                    if center_y > zone_start_y - 15 and center_y < zone_start_y + 15:
                        if id not in vehicle_timestamps:
                            vehicle_timestamps[id] = time.time()
                    
                    # Counting & Speed Calculation (Zone ke andar)
                    if zone_start_y < center_y < zone_end_y:
                        if id not in tracked_vehicles:
                            if id in vehicle_timestamps:
                                time_taken = time.time() - vehicle_timestamps[id]
                                speed_kmh = int((DISTANCE_METERS / time_taken) * 3.6) if time_taken > 0 else 45
                            else:
                                speed_kmh = 40 
                                
                            tracked_vehicles.add(id)
                            vehicle_count += 1
                            
                            # --- MODULAR CALL ---
                            # Bina yahan ka code chhede, data save karne ke liye function ko call kiya
                            save_to_database(database_folder, database_file, int(id), v_type, speed_kmh)

        # --- CONGESTION LOGIC ---
        if current_vehicle_count <= 3:
            status, status_color = "LOW TRAFFIC", (0, 255, 0)
        elif current_vehicle_count <= 8:
            status, status_color = "MODERATE TRAFFIC", (0, 255, 255)
        else:
            status, status_color = "HEAVY CONGESTION (ALERT)", (0, 0, 255)

        # --- VISUALIZATION (Black Texts & Zone Lines) ---
        cv2.line(annotated_frame, (0, zone_start_y), (annotated_frame.shape[1], zone_start_y), (0, 255, 255), 2) 
        cv2.line(annotated_frame, (0, zone_end_y), (annotated_frame.shape[1], zone_end_y), (255, 0, 0), 2) 
        
        cv2.putText(annotated_frame, f"Total Passed: {vehicle_count}", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 3)
        cv2.putText(annotated_frame, f"Vehicles on Screen: {current_vehicle_count}", (30, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)
        cv2.putText(annotated_frame, f"Status: {status}", (30, 130), cv2.FONT_HERSHEY_SIMPLEX, 1, status_color, 3)
        
        cv2.imshow("Smart Traffic Advanced Edge System", annotated_frame)
        
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        break

cap.release()
cv2.destroyAllWindows()
print(f"\n[SUCCESS] Analytics report saved inside folder '{database_folder}' as '{database_file}'")