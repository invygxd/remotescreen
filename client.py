import socket
import cv2
import numpy as np
import zlib
import pygame
from pygame.locals import *

HOST = 'SERVER_IP'  
PORT = 5000
WINDOW_SIZE = (1280, 720)  

def receive_frame(sock):

    size_bytes = sock.recv(4)
    if not size_bytes:
        return None
    size = int.from_bytes(size_bytes, 'big')
    
    data = b''
    while len(data) < size:
        packet = sock.recv(size - len(data))
        if not packet:
            return None
        data += packet
    
    decompressed = zlib.decompress(data)
    frame = cv2.imdecode(np.frombuffer(decompressed, dtype=np.uint8), 1)
    return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

def main():

    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("Remote Screen Viewer")
    clock = pygame.time.Clock()
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    print("Connected to server")
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
        
        frame = receive_frame(sock)
        if frame is None:
            break
        
        frame = cv2.resize(frame, WINDOW_SIZE)
        frame = np.rot90(frame)
        frame = pygame.surfarray.make_surface(frame)
        
        screen.blit(frame, (0, 0))
        pygame.display.flip()
        clock.tick(30) 
    
    sock.close()
    pygame.quit()

if __name__ == "__main__":
    main()
