import cv2
import numpy as np
import time
import os
import handtrackingmodule as htm
from collections import deque

# --- Constants and Setup ---
BRUSH_THICKNESS_DEFAULT = 15
ERASER_THICKNESS_DEFAULT = 100
IMAGE_FOLDER = "Header"
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720

# For smoothing the cursor movement
prev_points = deque(maxlen=10)

# --- Function to load overlay images ---
def load_overlay_images(folder_path):
    """Loads all images from a folder into a list."""
    image_list = []
    if not os.path.exists(folder_path):
        print(f"Error: Folder '{folder_path}' not found.")
        return image_list
    
    files = sorted(os.listdir(folder_path)) # Sort to ensure consistent order
    print(f"Loading images: {files}")
    for file_name in files:
        path = os.path.join(folder_path, file_name)
        image = cv2.imread(path)
        if image is not None:
            image_list.append(image)
    print(f"Loaded {len(image_list)} images.")
    return image_list

# --- Main Application Logic ---
def main():
    # --- Initialization ---
    brush_thickness = BRUSH_THICKNESS_DEFAULT
    eraser_thickness = ERASER_THICKNESS_DEFAULT
    
    overlay_list = load_overlay_images(IMAGE_FOLDER)
    if not overlay_list:
        return # Exit if no images were loaded
        
    header = overlay_list[0]
    draw_color = (255, 0, 255)  # Default color (Pink)

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return
        
    cap.set(3, WINDOW_WIDTH)
    cap.set(4, WINDOW_HEIGHT)

    detector = htm.handDetector(detectionCon=0.85, maxHands=1)
    xp, yp = 0, 0
    img_canvas = np.zeros((WINDOW_HEIGHT, WINDOW_WIDTH, 3), np.uint8)

    while True:
        # 1. Import and flip image
        success, img = cap.read()
        if not success:
            print("Warning: Could not read frame from camera!")
            break
        img = cv2.flip(img, 1)

        # 2. Find Hand Landmarks
        img = detector.findhands(img)
        lm_list = detector.findPosition(img, draw=False)

        if lm_list:
            # Tip of index and middle fingers
            x1, y1 = lm_list[8][1:]
            x2, y2 = lm_list[12][1:]
            
            # Add current point to deque for smoothing
            prev_points.appendleft((x1, y1))
            # Calculate smoothed coordinates
            sx = int(np.mean([p[0] for p in prev_points]))
            sy = int(np.mean([p[1] for p in prev_points]))

            # 3. Check which fingers are up
            fingers = detector.fingerup()

            # 4. Selection Mode - Two fingers are up
            if fingers[1] and fingers[2]:
                xp, yp = 0, 0  # Reset previous position when switching modes
                print("Selection Mode")
                
                # Visual feedback for selection
                cv2.rectangle(img, (sx, sy - 25), (x2, y2 + 25), draw_color, cv2.FILLED)

                # Check for click on header
                if sy < 125:
                    if 250 < sx < 450: # Pink
                        header = overlay_list[0]
                        draw_color = (255, 0, 255)
                    elif 550 < sx < 750: # Blue
                        header = overlay_list[1]
                        draw_color = (255, 100, 0)
                    elif 800 < sx < 950: # Green
                        header = overlay_list[2]
                        draw_color = (0, 255, 0)
                    elif 1050 < sx < 1200: # Eraser
                        header = overlay_list[3]
                        draw_color = (0, 0, 0)
                
            # 5. Drawing Mode - Index finger is up
            elif fingers[1] and not fingers[2]:
                print("Drawing Mode")
                
                # Dynamic brush/eraser size adjustment (pinch gesture)
                thumb_tip = lm_list[4][1:]
                length = np.hypot(thumb_tip[0] - sx, thumb_tip[1] - sy)
                
                if draw_color == (0, 0, 0): # Eraser
                    eraser_thickness = int(np.interp(length, [30, 200], [10, 150]))
                    cv2.circle(img, (sx, sy), eraser_thickness // 2, (255, 255, 255), 2)
                else: # Brush
                    brush_thickness = int(np.interp(length, [30, 200], [5, 50]))
                    cv2.circle(img, (sx, sy), brush_thickness // 2, draw_color, cv2.FILLED)

                if xp == 0 and yp == 0:
                    xp, yp = sx, sy

                # Draw line from previous point to current smoothed point
                thickness = eraser_thickness if draw_color == (0, 0, 0) else brush_thickness
                cv2.line(img_canvas, (xp, yp), (sx, sy), draw_color, thickness)
                
                xp, yp = sx, sy
            else:
                # Reset previous point if no drawing/selection gesture is detected
                xp, yp = 0, 0
                prev_points.clear()

        # --- Image Merging and Display ---
        # Create an inverted mask of the canvas
        img_gray = cv2.cvtColor(img_canvas, cv2.COLOR_BGR2GRAY)
        _, img_inv = cv2.threshold(img_gray, 50, 255, cv2.THRESH_BINARY_INV)
        img_inv = cv2.cvtColor(img_inv, cv2.COLOR_GRAY2BGR)
        
        # Black out the drawing area on the main image and add the canvas drawing
        img = cv2.bitwise_and(img, img_inv)
        img = cv2.bitwise_or(img, img_canvas)

        # Set the header image
        # FIX: Resize the header to match the target slice shape before assigning
        resized_header = cv2.resize(header, (WINDOW_WIDTH, 125))
        img[0:125, 0:WINDOW_WIDTH] = resized_header
        
        cv2.imshow("AI Virtual Painter", img)
        # cv2.imshow("Canvas", img_canvas) # Optional: show canvas separately

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # --- Cleanup ---
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

