from xtermgui import Colour, RGBs, terminal, read_event

if __name__ == "__main__":
    Colour.configure_default_background(RGBs.DEFAULT_BACKGROUND_WSL.value)

    print("This program showcases the basic capabilities of XtermGUI. Exit with ctrl + c.\t\n")
    with terminal.setup_inputs():
        while True:
            read = read_event()
            print(read)
