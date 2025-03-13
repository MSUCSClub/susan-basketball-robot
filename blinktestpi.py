import serial
import time

esp = serial.Serial('/dev/ttyUSB0', 115200, timeout = 10)

time.sleep(2)

def send_command():
	command - "Test_Drive_Motors()\n"
	esp.write(command.encode)
	print("send command")
	
	response = esp.readline().decode().strip()
	if response:
		print(f"Response: {response}")


try:
	send_command
except Exception as e:
	print(f"Error: {e}")
finally:
	esp.close()
	print("connection closed")
