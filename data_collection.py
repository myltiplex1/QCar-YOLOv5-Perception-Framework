import os
import cv2
import time
import numpy as np
import keyboard
from threading import Thread
from datetime import datetime
from pal.products.qcar import QCar, QCarCameras

# ================= Configuration =================
CONTROLLER_UPDATE_RATE = 100
CSI_WIDTH, CSI_HEIGHT = 820, 410
DISPLAY_WIDTH, DISPLAY_HEIGHT = 820, 410
DATA_DIR = "dataset_collection"

# ================= State Management =================
class State:
    def __init__(self):
        self.kill = False
        
        # Physics / Control
        self.throttle = 0.0
        self.steering = 0.0
        
        # Data Collection State
        self.last_capture_img = None
        self.capture_timer = 0.0
        self.capture_msg = ""
        self.image_count = 0

state = State()

# ================= Setup Functions =================
def setup_dirs():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
        print(f">> Created directory: {DATA_DIR}")
    
    # Count existing images to continue numbering if needed
    existing = [f for f in os.listdir(DATA_DIR) if f.endswith('.jpg')]
    state.image_count = len(existing)
    print(f">> Found {state.image_count} existing images.")

# ================= Helper Functions =================
def capture_image(frame):
    """Saves the current frame to disk and triggers the UI feedback."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    filename = f"{DATA_DIR}/img_{timestamp}.jpg"
    
    # Save the original high-res frame (820x410), not the resized display
    cv2.imwrite(filename, frame)
    
    # Update State for UI Feedback
    state.image_count += 1
    state.last_capture_img = cv2.resize(frame, (200, 100)) # Create thumbnail
    state.capture_timer = time.time() # Start 2s timer
    state.capture_msg = f"SAVED: img_{timestamp}.jpg"
    
    print(f">> CAPTURED [{state.image_count}]: {filename}")

def handle_arrow(key):
    # --- DRIVING CONTROLS ---
    t_step = 0.01
    s_step = 0.1
    
    if key == 'up': state.throttle = np.clip(state.throttle + t_step, -0.3, 0.5)
    elif key == 'down': state.throttle = np.clip(state.throttle - t_step, -0.3, 0.5)
    elif key == 'left': state.steering = np.clip(state.steering - s_step, -0.6, 0.6)
    elif key == 'right': state.steering = np.clip(state.steering + s_step, -0.6, 0.6)

# ================= Main Loop =================
def controlLoop():
    # setup
    setup_dirs()
    cv2.namedWindow("Data Collection Mode", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Data Collection Mode", DISPLAY_WIDTH, DISPLAY_HEIGHT)
    
    qcar = QCar(readMode=1, frequency=CONTROLLER_UPDATE_RATE)
    cameras = QCarCameras(frameWidth=CSI_WIDTH, frameHeight=CSI_HEIGHT, frameRate=30, enableFront=True)
    
    with qcar, cameras:
        while not state.kill:
            # 1. Read Inputs
            qcar.read()
            if cameras.csiFront.read():
                raw_frame = cameras.csiFront.imageData.copy()
                
                # Check for Spacebar Trigger inside the loop to sync with frame
                if keyboard.is_pressed('space'):
                    # Debounce: ensure we don't take 30 pics per second holding space
                    # Simple check: if timer is active, don't take another? 
                    # Or just rely on user tapping quickly. 
                    # Let's add a tiny sleep to preventing double-triggering
                    capture_image(raw_frame)
                    time.sleep(0.2) 

                # 2. Draw HUD
                display_img = raw_frame.copy()
                
                # --- Status Text (Bottom) ---
                # Green text for controls
                info_str = f"THR: {state.throttle:.2f}  STR: {state.steering:.2f}  IMGs: {state.image_count}"
                cv2.putText(display_img, info_str, (20, CSI_HEIGHT - 30), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

                # --- Capture Feedback (Top Right) ---
                # If within 2 seconds of last capture, show the thumbnail and message
                if time.time() - state.capture_timer < 2.0 and state.last_capture_img is not None:
                    
                    # 1. Draw "SNAPSHOT SAVED" text in Center
                    cv2.putText(display_img, "SNAPSHOT SAVED", (CSI_WIDTH//2 - 100, CSI_HEIGHT//2), 
                               cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 3)
                    
                    # 2. Picture-in-Picture (Thumbnail) in Top Right
                    # Dimensions of thumb
                    th_h, th_w, _ = state.last_capture_img.shape
                    
                    # Position: Top Right with 10px padding
                    y_offset = 10
                    x_offset = CSI_WIDTH - th_w - 10
                    
                    # Draw white border for visibility
                    cv2.rectangle(display_img, (x_offset-2, y_offset-2), 
                                 (x_offset+th_w+2, y_offset+th_h+2), (255,255,255), -1)
                    
                    # Overlay the thumbnail
                    display_img[y_offset:y_offset+th_h, x_offset:x_offset+th_w] = state.last_capture_img

                # 3. Show Window
                cv2.imshow("Data Collection Mode", display_img)
                cv2.waitKey(1)
            
            # 4. Write Motors
            qcar.write(state.throttle, state.steering)
            
    cv2.destroyAllWindows()

if __name__ == '__main__':
    # Arrow keys
    keyboard.add_hotkey('up', lambda: handle_arrow('up'))
    keyboard.add_hotkey('down', lambda: handle_arrow('down'))
    keyboard.add_hotkey('left', lambda: handle_arrow('left'))
    keyboard.add_hotkey('right', lambda: handle_arrow('right'))
    
    # Quit
    keyboard.add_hotkey('q', lambda: setattr(state, 'kill', True))

    print("=================================================")
    print("   QCAR DATA COLLECTION SCRIPT")
    print("=================================================")
    print(" CONTROLS:")
    print("   [ARROWS] : Drive (Throttle/Steering)")
    print("   [SPACE]  : Capture Image")
    print("   [Q]      : Quit")
    print("=================================================")

    t = Thread(target=controlLoop)
    t.start()
    
    while t.is_alive() and not state.kill:
        time.sleep(1)
    state.kill = True