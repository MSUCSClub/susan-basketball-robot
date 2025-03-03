import time
import DriverMotors


class robot:
    def __init__(self):
        # Sensor Variables
        self.LBack = False
        self.RBack = False
        self.FColorSensor = False
        self.BColorSensor = False
        self.right_side = False
        self.left_side = False
        self.ball_left = False
        self.ball_right = False
        self.ball_center = False
        self.leftRampUp = False     # not sure we need the ramp variables but I don't remember why they are here so leaving for now.
        self.rightRampUp = False
        self.StartButton = StartButton
        # State Variables
        self.shooting = False
        self.in_middle = False
        self.pickup = False
        self.moveLeft = False
        self.moveRight = False
        # Motors
        self.leftDrive = leftDrive
        self.rightDrive = rightDrive
        self.shooterRelay = relayPin

while robot.StartButton:
    if not robot.ball_center:
        robot.pickup = True
        while robot.pickup and not robot.right_side:
            # Move right
            robot.RightRamp = True
            robot.moveRight = True

            if robot.right_side:
                # Stop left
                robot.moveLeft = True
                time.sleep(0.5)  # pause
                robot.RightRamp = False  # Close right ramp

                if robot.ball_center:
                    robot.moveLeft = True
                    while robot.FColorSensor and robot.BColorSensor:
                        robot.in_middle = True
                        robot.shooting = True  # Activate shooters

                else:
                    robot.LeftRamp = True
                    robot.moveLeft = True
                    while not robot.left_side:
                        # Move left
                        robot.moveLeft = True

                    if robot.left_side:
                        # Stop right
                        robot.moveRight = True
                        time.sleep(0.5)  # pause
                        robot.LeftRamp = False  # Close left ramp

                        if robot.ball_center:
                            robot.moveRight = True
                            while robot.FColorSensor and robot.BColorSensor:
                                robot.in_middle = True
                                robot.shooting = True  # Activate shooters

                        else:
                            robot.RightRamp = True
                            robot.moveRight = True
                            while not robot.right_side:
                                # Move right
                                robot.moveRight = True



    def move_to_center_and_shoot(self):
        ##Moves robot to center and shoot
        self.moveLeft = True
        while self.FColorSensor and self.BColorSensor:
            self.in_middle = True
            self.shooting = True
    def pickup_sequence(self):
        ##Ball pickip
        if not self.ball_center:
            self.pickup = True
            while self.pickup:
                self.moveRight = True  # Move right
                self.RightRamp = True

                while not self.right_side:
                    # Bot moves right until it reaches the right edge
                    self.moveRight = True

                if self.right_side:
                    # Bot is on the right edge
                    self.ball_left = True
                    print("Ball detected on left side")

                    # Move left
                    self.moveLeft = True
                    time.sleep(0.5)
                    self.RightRamp = False  # Close right ramp

                    if self.FColorSensor and self.BColorSensor:
                        # If the center ball sensor is triggered
                        self.move_to_center_and_shoot()
                    else:
                        # Move to the left edge
                        self.LeftRamp = True
                        self.moveLeft = True
                        while not self.left_side:
                            self.moveLeft = True

                        if self.left_side:
                            # Bot reached the left edge
                            self.moveRight = True
                            time.sleep(0.5)
                            self.LeftRamp = False  # Close left ramp

                            if self.FColorSensor and self.BColorSensor:
                                self.move_to_center_and_shoot()
                            else:
                                # Move to left edge again
                                self.moveLeft = True
    def activate_push_ramp(self):
        # If no ball is detected, don't try shooting
        if not (self.ball_center or self.ball_left or self.ball_right):
            self.shooting = False

robot = robot()
if robot.StartButton:
    robot.pickup_sequence()
    robot.activate_push_ramp()

    def move_back(self):
        print("Moving Back from Wall...")
        time.sleep(1)

    def move_left(self, distance=0.5):
        print(f"Moving Left {distance} inch...")
        time.sleep(1)

    def move_right(self, distance=0.5):
        print(f"Moving Right {distance} inch...")
        time.sleep(1)

    def activate_shooter(self):
        if self.in_middle:
            print("Activating Shooter Motors...")
            self.shooting = True
            time.sleep(2)
        else:
            print("Not in middle, cannot shoot!")

    def activate_ramp(self, side):
        if side == "left":
            print("Activating Left Ramp Servo...")
        elif side == "right":
            print("Activating Right Ramp Servo...")
        elif side == "center":
            print("Activating Center Ramp Servo...")
        time.sleep(1)

    def check_edges(self):
        if self.right_side:
            print("Bot is on the right edge.")
            if self.ball_center:
                print("Moving to center and shooting.")
                self.activate_shooter()
            else:
                print("Moving to left edge.")
                self.move_left()
        elif self.left_side:
            print("Bot is on the left edge.")
            if self.ball_center:
                print("Moving to center and shooting.")
                self.activate_shooter()
            else:
                print("Moving to right edge.")
                self.move_right()

    def handle_ball_sensors(self):
        if self.ball_left:
            self.activate_ramp("left")
        if self.ball_right:
            self.activate_ramp("right")
        if self.ball_center:
            self.activate_ramp("center")
        if not (self.ball_center or self.ball_left or self.ball_right):
            print("No balls detected, stopping shooting.")
            self.shooting = False

    def robot_logic(self):
        self.move_back()
        self.check_edges()
        self.handle_ball_sensors()

        if self.in_middle:
            print("Activating pushRamp servo...")
            self.activate_ramp("center")

        if not self.ball_center:
            self.pickup = True
            print("Pickup activated.")

        while self.pickup:
            print("Picking up balls...")
            time.sleep(2)
            self.pickup = False  # Stop after picking up

# Run Simulation
robot = Robot()
robot.robot_logic()
