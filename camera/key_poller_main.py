import keyboard

def on_press_handler(event):
    print(event.name)
    
keyboard.on_press(on_press_handler)

while True:
    pass
