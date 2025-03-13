# To control three servos using a PCA9685 PWM driver connected via I2C to a Raspberry Pi 4 B, you can use the Adafruit PCA9685 library.

#Step 1: Install Dependencies
#nsure you have the required libraries installed:

#sh
#sudo apt update
#sudo apt install python3-pip
#pip3 install adafruit-circuitpython-servokit
#Step 2: Connect the PCA9685 to Raspberry Pi
#VCC → 3.3V or 5V
#GND → GND
#SCL → GPIO3 (SCL)
#SDA → GPIO2 (SDA)
#V+ (External Power for Servos, e.g., 5V)
#Step 3: Python Code to Control 3 Servos

from adafruit_servokit import ServoKit
import time

# Initialize PCA9685 (16 channels, default I2C address is 0x40)
kit = ServoKit(channels=16)

# Servo channel assignments
SERVO_CHANNELS = [0, 1, 2]  # Channels for the 3 servos

def set_servo_angle(channel, angle):
    """Set the angle of a servo (0-180 degrees)"""
    if 0 <= angle <= 180:
        kit.servo[channel].angle = angle
    else:
        print(f"Invalid angle: {angle}. Must be between 0 and 180.")

try:
    while True:
        for angle in [0, 90, 180]:  # Sweep through angles
            print(f"Moving servos to {angle} degrees")
            for channel in SERVO_CHANNELS:
                set_servo_angle(channel, angle)
            time.sleep(1)

except KeyboardInterrupt:
    print("\nStopping servos")
finally:
    # Set all servos to neutral (90 degrees) or disable them
    for channel in SERVO_CHANNELS:
        kit.servo[channel].angle = None  # Disables the servo
    print("Servos disabled.")


#How It Works
#Initialize the PCA9685 driver using ServoKit(channels=16).
#Set servo angles (0-180 degrees) using kit.servo[channel].angle = angle.
#Loop through angles for all three servos.
#Graceful exit on KeyboardInterrupt and disable servos.
