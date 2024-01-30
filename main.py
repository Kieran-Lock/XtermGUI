from xtermgui import TextColour, Colours, terminal, read_event

if __name__ == "__main__":
    TextColour.configure_default_background(Colours.DEFAULT_BACKGROUND_WSL)

    print("This program showcases the basic capabilities of XtermGUI. Exit with ctrl + c.\t\n")
    with terminal.setup_inputs():
        while True:
            read = read_event()
            print(read)
