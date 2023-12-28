# Done by Dimanto Polo, Darren Michael. SID: 20895475
# COMP1021 Music System
import turtle # Import the turtle module for drawing
import music  # Import the music module for playing music
import time   # Import the time module for time.sleep()

# Initialize the music data
music_data = []

# Store the current instrument
instrument = 0

# A dictionary containing the menu settings
main_menu = {
    # menu key: (caption, position and size, colour)
    "load" : ("Load Music", (-250, 20, 220, 140), "cyan"),
    "play" : ("Play Music", (0, 20, 220, 140), "yellow"),
    "instrument" : ("Change Instrument", (250, 20, 220, 140), "magenta"),
    "transpose" : ("Transpose Music", (-250, -150, 220, 140), "orange"),
    "speed" : ("Adjust Speed", (0, -150, 220, 140), "red"),
    "crazymusic" : ("Make Crazy Music", (250, -150, 220, 140), "lawn green")
}


# This function draws a coloured box at (x, y) with a size of (w, h)
def drawBox(color, x, y, w, h):
    turtle.fillcolor(color)
    turtle.goto(x - w / 2, y - h / 2)
    turtle.down()
    turtle.begin_fill()
    for _ in range(2):
        turtle.forward(w)
        turtle.left(90)
        turtle.forward(h)
        turtle.left(90)
    turtle.end_fill()
    turtle.up()
    turtle.goto(x, y)

    
# This function creates the menu on the turtle window
def drawMenu():
    turtle.hideturtle()
    turtle.up()
    turtle.width(5)

    turtle.tracer(False)    # Disable any turtle animation
    
    turtle.clear()

    # Write the title
    turtle.goto(0, 200)
    turtle.write("♪ Python Music System ♪", align="center", \
                 font=("Arial", 30, "bold"))

    # Draw the menu boxes
    for menu_info in main_menu.values():
        caption = menu_info[0]
        x, y, w, h = menu_info[1]
        color = menu_info[2]

        drawBox(color, x, y, w, h)

        turtle.goto(x, y - 10)
        turtle.write(caption, align="center", \
                     font=("Arial", 16, "bold"))

    turtle.tracer(True)    # Refresh the turtle window


# This function shows the music summary
def updateMusicSummary():
    text_turtle.up()
    text_turtle.hideturtle()

    text_turtle.clear()
    text_turtle.goto(0, 140)

    if len(music_data) == 0:
        # Music is empty
        summary = "Click on the 'Load Music' area to load a music file"
    else:
        # Number of notes
        summary = "No. of notes = " + str(len(music_data)) + ", "

        # Duration
        duration = 0
        for note in music_data:
            if note[0] + note[2] > duration:
                duration = note[0] + note[2]
        mins = int(duration / 60)
        secs = round(duration % 60, 2)
        summary = summary + "song duration = " + str(mins) + "m " + str(secs) + "s"

        #####
        #
        # TODO:
        # - Update and display the instrument appropriately (DONE)
        #
        #####

        summary = summary + ', instrument = ' +\
            str(music.instrument_list[instrument])
        
    text_turtle.write(summary, align="center", font=("Arial", 14, "normal"))


# This function loads some music into the music data list
def loadMusic():
    global music_data

    # Get the song list from the song folder
    song_list = music.getsonglist()
    song_menu = ""
    for i in range(len(song_list)):
        song_menu = song_menu + str(i) + ": " + song_list[i][0] + "\n"
    if song_menu == "":
        song_menu = "No music files available"
    
    # Ask the user for the music file
    filename = turtle.textinput("Music File", song_menu + \
                   "\nPlease give me a music file number or a file name:")
    if filename == None:
        return

    # Get the song for numeric input
    if filename.isnumeric():
        filename = song_list[int(filename)][1]

    # Open the file for reading
    file = open(filename, "r")

    # Reset the music data
    music_data = []

    # Read the data into the music list
    for line in file:
        # Read each line as a music note
        note = line.rstrip().split("\t")

        # Convert the data to the right data type
        note[0] = float(note[0])  # Time
        note[1] = int(note[1])    # Pitch
        note[2] = float(note[2])  # Duration

        # Add the note at the end of the music
        music_data.append(note)

    # Close the file
    file.close()

    # Update the music summary
    updateMusicSummary()


# This function plays the music
def playMusic():
    global music_data

    # Clear the music data in the music module
    music.clear()

    # Add the music notes
    for i in range(len(music_data)):
        # Show progress every 10 notes
        if i % 10 == 0:
            turtle.tracer(False)
            text_turtle.clear()
            text_turtle.write("Adding note " + str(i) + \
                              " of " + str(len(music_data)), \
                              align="center", font=("Arial", 14, "normal"))
            turtle.tracer(True)

        # Add the note
        note = music_data[i]
        music.addnote(note[0], note[1], note[2])

    # Update the music summary
    updateMusicSummary()

    # Play the music
    music.play()


# This function changes the instrument
def changeInstrument():
    global instrument
    
    #####
    #
    # TODO:
    # - Change the instrument appropriately (DONE)
    # - Show the instrument list in the input box (DONE)
    # - Update the instrument display (DONE)
    #
    #####

    instru_selected = int(0)
    instru = ''
    
    for instrument in [0, 10, 19, 24, 32, 40, 56, 64, 73, 123]:
        instru = instru + str(instrument) + ': ' + music.instrument_list[instrument] + '\n'
        
    display = instru + '\nPlease enter the instrument number (0-127):'
    
    instru_selected = turtle.numinput('Change Instrument', display)

    if instru_selected == None:
        return
    instru_selected = int(instru_selected)
    if instru_selected < 0:
        return
    if instru_selected > 127:
        return

    
    music.setinstrument(instru_selected)
    instrument = instru_selected
    updateMusicSummary()
    
# This function transposes the music pitch
def transpose():
    global music_data
    
    change = turtle.numinput('Transpose', \
                             'Please enter the transposition:')

    if change == None:
        return

    change = int(change)
    
    for note in range(len(music_data)):
        music_data[note][1] = music_data[note][1] + change        
        
        if music_data[note][1] < 0:
            music_data[note][1] = 0    
        elif music_data[note][1] > 127:
            music_data[note][1] = 127 
    
# This function adjusts the speed of the music
def adjustSpeed():
    global music_data

    changespeed = turtle.numinput('Speed Change', \
                             'Please enter the speed change (%):')

    if changespeed == None:
        return

    changespeed = int(changespeed)
    
    changespeed /= 100
    
    for note in range(len(music_data)):
        music_data[note][0] = (music_data[note][0])/changespeed
        music_data[note][2] = (music_data[note][2])/changespeed

    updateMusicSummary()
    

# This function makes a piece of crazy music in the music list
def makeCrazyMusic():
    global music_data

    times = turtle.numinput('Number of Repetitions',\
                            'Please enter the number of repetitions:')
    if times == None:
        return
    
    else:
        duration = turtle.numinput('Sound Duration',\
                               'Please enter the duration of the sound:')
        if duration == None:
            return
        else:
            startpitch = turtle.numinput('Starting Pitch',\
                             'Please enter the starting pitch:')
        if startpitch == None:
            return
        else:
            endpitch = turtle.numinput('Ending Pitch',\
                             'Please enter the ending pitch:')
            if endpitch == None:
                return

    times = int(times)
    duration = float(duration)
    startpitch = int(startpitch)
    endpitch = int(endpitch)

    music_data = []

    num_notes = abs(endpitch - startpitch) + 1
    duration_one = duration/num_notes

    if endpitch > startpitch:
        step = 1
    elif endpitch < startpitch:
        step = -1
        
    starting = 0
    for i in range(times):
        for pitch in range(startpitch, endpitch + step, step):
            music_data.append([starting, pitch, duration_one])
            starting += duration_one

    updateMusicSummary()

# This function handles the screen click and the menu selection
def handleMenu(x, y):
    # Get the menu item that the user has clicked on
    selected_key = None
    for key, menu_info in main_menu.items():
        menux, menuy, menuw, menuh = menu_info[1]
        if x > menux - menuw / 2 and x < menux + menuw / 2 and \
           y > menuy - menuh / 2 and y < menuy + menuh / 2:
            selected_key = key

    # Run the corresponding functions for each menu item
    if selected_key == "load":
        loadMusic()
    elif selected_key == "play":
        playMusic()
    elif selected_key == "instrument":
        changeInstrument()
    elif selected_key == "transpose":
        transpose()
    elif selected_key == "speed":
        adjustSpeed()
    elif selected_key == "crazymusic":
        makeCrazyMusic()
        

# Set up the turtle module
turtle.setup(800, 600)
turtle.speed(0)

# Show the menu
drawMenu()

# Create a new turtle to show music summary
text_turtle = turtle.Turtle()

# Update the music summary
updateMusicSummary()

# Set up the screen click event
turtle.onscreenclick(handleMenu)

turtle.done()

# Kill any currently playing sounds and remove the sound
music.stop(True)
