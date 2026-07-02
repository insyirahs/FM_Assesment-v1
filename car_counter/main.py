import cv2
from ultralytics import YOLO

model = YOLO("yolov8n.pt")
cap = cv2.VideoCapture("video.mp4")

fps = cap.get(cv2.CAP_PROP_FPS) or 25
w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
out = cv2.VideoWriter("output.mp4", cv2.VideoWriter_fourcc(*"mp4v"), fps, (w, h))

line_x = 960  

VEHICLES = ("car", "bus", "truck", "motorcycle")

counts = {v: 0 for v in VEHICLES}

track_memory = {}   
counted_ids = set()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model.track(frame, persist=True, verbose=False, conf=0.2)[0]

    cv2.line(frame, (line_x, 0), (line_x, frame.shape[0]), (255, 0, 0), 2)

    if results.boxes is not None and results.boxes.id is not None:
        for box in results.boxes:
            cls = int(box.cls[0])
            label = model.names[cls]

            if label not in VEHICLES:
                continue

            track_id = int(box.id[0])
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            cx = (x1 + x2) // 2
            cy = (y1 + y2) // 2

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.circle(frame, (cx, cy), 4, (0, 0, 255), -1)
            cv2.putText(frame, f"{label} {track_id}", (x1, y1 - 8),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

            prev_cx = track_memory.get(track_id, cx)
            crossed = (prev_cx < line_x <= cx) or (prev_cx > line_x >= cx)
            if track_id not in counted_ids and crossed:
                counts[label] += 1
                counted_ids.add(track_id)

            track_memory[track_id] = cx


    total = sum(counts.values())
    y_pos = 40
    cv2.putText(frame, f"Total: {total}", (50, y_pos),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
    for vtype, n in counts.items():
        y_pos += 35
        cv2.putText(frame, f"{vtype}: {n}", (50, y_pos),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

    out.write(frame)               
    cv2.imshow("Car Counter", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
out.release()
cv2.destroyAllWindows()

print("\nFINAL CAR COUNT")
for vtype, n in counts.items():
    print(f"{vtype:12s}: {n}")
print(f"{'TOTAL':12s}: {sum(counts.values())}")
print("Annotated video saved to: output.mp4")
