import pyray as pyr


def main():

    pyr.init_window(800, 450, "Hello")  
    while not pyr.window_should_close():
        pyr.begin_drawing()



        pyr.end_drawing()
    pyr.close_window()

if __name__ == "__main__":
    main()
