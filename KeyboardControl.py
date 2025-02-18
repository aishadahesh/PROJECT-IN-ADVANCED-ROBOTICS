from djitellopy import tello
import KeyPressModule as kp
import time
import cv2

# Initialize keyboard control
kp.init()

# Create Tello object
me = tello.Tello()

# Step 1: Establish connection with delay to avoid packet loss
print("[INFO] Connecting to Tello drone...")
time.sleep(2)  # Allow system to stabilize

try:
    me.connect()
    time.sleep(2)  # Give time for state packets to arrive
    print(f"[INFO] Connection successful! Battery Level: {me.get_battery()}%")
except Exception as e:
    print(f"[ERROR] Connection failed: {e}")
    exit(1)  # Exit the program if unable to connect

# Step 2: Function to get keyboard inputs for drone movement
def getKeyboardInput():
    lr, fb, ud, yv = 0, 0, 0, 0
    speed = 30

    if kp.getKey("left"): 
        lr = -speed
        print("[DEBUG] Left key pressed")
    elif kp.getKey("right"): 
        lr = speed
        print("[DEBUG] Right key pressed")

    if kp.getKey("up"): 
        fb = speed
        print("[DEBUG] Up key pressed")
    elif kp.getKey("down"): 
        fb = -speed
        print("[DEBUG] Down key pressed")

    if kp.getKey("w"): 
        ud = speed
        print("[DEBUG] W key (ascend) pressed")
    elif kp.getKey("s"): 
        ud = -speed
        print("[DEBUG] S key (descend) pressed")

    if kp.getKey("a"): 
        yv = -speed
        print("[DEBUG] A key (rotate left) pressed")
    elif kp.getKey("d"): 
        yv = speed
        print("[DEBUG] D key (rotate right) pressed")

    if kp.getKey("q"): 
        print("[INFO] Landing drone...")
        me.land()
        time.sleep(3)

    if kp.getKey("e"): 
        print("[INFO] Taking off...")
        me.takeoff()
        time.sleep(3)

    return [lr, fb, ud, yv]

# Step 3: Takeoff confirmation
try:
    me.takeoff()
    print("[INFO] Drone has taken off.")
except Exception as e:
    print(f"[ERROR] Takeoff failed: {e}")
    exit(1)

# Step 4: Control loop
while True:
    try:
        vals = getKeyboardInput()
        me.send_rc_control(vals[0], vals[1], vals[2], vals[3])
        time.sleep(0.05)  # Small delay to prevent packet overload

    except Exception as e:
        print(f"[ERROR] Issue in movement control: {e}")
        me.land()  # Ensure the drone lands safely if an error occurs
        break

# Step 5: Land the drone safely when script stops
me.land()
print("[INFO] Drone has landed safely.")


