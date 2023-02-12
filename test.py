import msvcrt

print("Enter text:")

user_input = ""
while True:
    if msvcrt.kbhit():
        key = msvcrt.getche().decode()
        if key == "\r":
            print("\nYou: " + user_input)
            user_input = ""
        else:
            user_input += key