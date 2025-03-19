import socket
import cv2
import pyautogui
import numpy as np
import zlib
import threading

HOST = '0.0.0.0'  
PORT = 5000
QUALITY = 50      

def send_screens(conn):
    try:
        while True:
            img = pyautogui.screenshot()
            frame = np.array(img)
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            
            _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, QUALITY])
            compressed = zlib.compress(buffer)
            
            size = len(compressed)
            conn.sendall(size.to_bytes(4, 'big') + compressed)
    except:
        conn.close()

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print("Waiting for connection...")
        conn, addr = s.accept()
        print("Connected to:", addr)
        send_screens(conn)

if __name__ == "__main__":
    main()
