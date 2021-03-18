# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    from time import sleep
    from ctypes import windll

    print_hi('PyCharm')

    x = 100 #max is 1280
    y = 100 #max is 720

    while(y <= 600):
        windll.user32.SetCursorPos(x, y)
        print("Moved mouse to (%d,%d)",x,y)
        x = x + 100
        y = y + 100
        sleep(1)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
