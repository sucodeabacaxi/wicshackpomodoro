import PySimpleGUI as sg
import time

"""
    Highly experimental demo of how the illusion of a window with a background image is possible with PySimpleGUI.

    Requires the latest PySimpleGUI from GitHub.  Your copy of PySimpleGUI should be local to your application so that 
    the global variable _move_all_windows can be changed.  
    
    Copyright 2020 PySimpleGUI.org
"""


sg.Window._move_all_windows = True


def title_bar(title, text_color, background_color):
    """
    Creates a "row" that can be added to a layout. This row looks like a titlebar
    :param title: The "title" to show in the titlebar
    :type title: str
    :param text_color: Text color for titlebar
    :type text_color: str
    :param background_color: Background color for titlebar
    :type background_color: str
    :return: A list of elements (i.e. a "row" for a layout)
    :rtype: List[sg.Element]
    """
    bc = background_color
    tc = text_color
    font = 'Helvetica 12'

    return [sg.Col([[sg.T(title, text_color=tc, background_color=bc, font=font, grab=True)]], pad=(0, 0), background_color=bc),
            sg.Col([[sg.T('_', text_color=tc, background_color=bc, enable_events=True, font=font, key='-MINIMIZE-'), sg.Text('❎', text_color=tc, background_color=bc, font=font, enable_events=True, key='Exit')]], element_justification='r', key='-C-', grab=True,
                   pad=(0, 0), background_color=bc)]

def timer():
    return int(round(time.time() * 100))

def main():

    background_layout = [ title_bar('pomodoro!', "#5dfdab", "#2f1266"),
                        [sg.Image(background_image)]]
    window_background = sg.Window('Background', background_layout, no_titlebar=True, finalize=True, margins=(0, 0), element_padding=(0,0), right_click_menu=[[''], ['Exit']])

    window_background['-C-'].expand(True, False, False)  # expand the titlebar's rightmost column so that it resizes correctly


    # ------ Column Definition ------ #
    columnLeft = [[sg.Text('          ')],
          [sg.Text('', size=(8, 2), font=('helvetica', 20),
                justification='center', key='text')],
          [sg.Button('Run', key='-RUN-PAUSE-', button_color=('white', '#a92aba')),
           sg.Button('Reset', button_color=('white', '#a92aba'), key='-RESET-'),
           sg.Exit(button_color=('white', '#a92aba'), key='Exit1')]]

    columnRight = []

    #layout = [[sg.Column(columnLeft), sg.VSeperator(), sg.Column(columnRight)]]
    layout = [[columnLeft]]

    window = sg.Window('Everything bagel', layout, finalize=True, keep_on_top=True, grab_anywhere=False,  transparent_color=sg.theme_background_color(), no_titlebar=True)

    # window_background.send_to_back()
    # top_window.bring_to_front()

    current_time, paused_time, paused = 0, timer(), True
    start_time = timer()

    while True:
        # --------- Read and update window --------
        if not paused:
            event, values = window.read(timeout=10)
            #window.read(timeout=10)
            #sg.read_all_windows()
            current_time = timer() - start_time
        else:
            window, event, values = sg.read_all_windows()
        # --------- Exit --------
        if event in (sg.WIN_CLOSED, 'Exit', 'Exit1'):
            window.close()
            break
        # --------- Do Button Operations --------
        if event == '-RESET-':
            paused = True
            window['-RUN-PAUSE-'].update('Run')
            paused_time = start_time = timer()
            current_time = 0
        elif event == '-RUN-PAUSE-':
            paused = not paused
            if paused:
                paused_time = timer()
            else:
                start_time = start_time + timer() - paused_time
            # Change button's text
            window['-RUN-PAUSE-'].update('Run' if paused else 'Pause')
        elif event == 'Edit Me':
            sg.execute_editor(__file__)
        # --------- Display timer in window --------
        displayTime = 1500 - (current_time/100)
        #while(displayTime > 0):
        if(displayTime > 0):
            window['text'].update("{:02d}:{:02d}".format(int(displayTime//60),int(displayTime%60)))
        else:
            window['text'].update("00.00")
            
    window.close()
    window_background.close()


if __name__ == '__main__':

    background_image = "pomodoro.png"
    
    main()
