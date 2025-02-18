import pygame

def init():
    pygame.init()
    pygame.display.set_mode((400, 400))  # Create a small window to capture events

def getKey(keyName):
    pygame.event.pump()  # Ensures pygame processes events
    keyInput = pygame.key.get_pressed()
    myKey = getattr(pygame, f'K_{keyName.lower()}')  # Case insensitive key mapping
    return keyInput[myKey]

if __name__ == "__main__":
    init()
    while True:
        if getKey("left"):
            print("Left key pressed")
        if getKey("right"):
            print("Right key pressed")
        if getKey("up"):
            print("Up key pressed")
        if getKey("down"):
            print("Down key pressed")
        if getKey("w"):
            print("W key (ascend) pressed")
        if getKey("s"):
            print("S key (descend) pressed")
        if getKey("a"):
            print("A key (rotate left) pressed")
        if getKey("d"):
            print("D key (rotate right) pressed")
        if getKey("q"):
            print("Q key (land) pressed")
        if getKey("e"):
            print("E key (takeoff) pressed")

        pygame.time.delay(100)  # Prevent high CPU usage
