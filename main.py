from xtermgui import Colour, RGBs, console_inputs, read_console


if __name__ == "__main__":
    Colour.configure_default_background(RGBs.DEFAULT_BACKGROUND_WSL.value)

    print("This program showcases the basic capabilities of XtermGUI. Exit with ctrl + c.\t\n")
    with console_inputs():
        while True:
            read = read_console()
            print(read)
