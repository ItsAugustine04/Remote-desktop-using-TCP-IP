# server.py
import socket
import threading
from mss import mss
from PIL import Image
import io
from pynput.mouse import Controller as MouseController
from pynput.keyboard import Controller as KeyboardController

mouse = MouseController()
keyboard = KeyboardController()

CLIENT_IP = '192.168.1.10'  # Change this to client's IP
UDP_PORT = 9999
RAW_PORT = 8888

def capture_and_send_screen():
    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    with mss() as sct:
        while True:
            screenshot = sct.grab(sct.monitors[1])
            img = Image.frombytes('RGB', (screenshot.width, screenshot.height), screenshot.rgb)
            buffer = io.BytesIO()
            img.save(buffer, format='JPEG', quality=30)
            screen_data = buffer.getvalue()
            udp_sock.sendto(screen_data, (CLIENT_IP, UDP_PORT))

def handle_raw_commands():
    raw_sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
    while True:
        packet, _ = raw_sock.recvfrom(65535)
        # We're assuming the payload starts after 40 bytes (IP + TCP header)
        payload = packet[40:]
        if payload[:1] == b'M':
            x = int.from_bytes(payload[1:3], 'big')
            y = int.from_bytes(payload[3:5], 'big')
            mouse.position = (x, y)
        elif payload[:1] == b'K':
            key = payload[1:2].decode()
            keyboard.press(key)
            keyboard.release(key)

if __name__ == '__main__':
    t1 = threading.Thread(target=capture_and_send_screen)
    t2 = threading.Thread(target=handle_raw_commands)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
