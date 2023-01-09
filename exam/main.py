"""
This implements the main user interface using PySimpleGUI.
"""
import PySimpleGUI as sg
import exam_thread

PROGRAM_TITLE='Hearing Exam'

def main():
    """Creates the main user interface"""
    sg.theme('dark grey 8')
    window = None
    exam = None

    while True:
        if window:
            event, values = window.read()
        else:
            event = 'program_launch'

        match event:
            case 'program_launch' | 'stop':
                #Stop running exam if it exists
                if window and exam:
                    exam.stop()
                    window.close()
                # Create the initial window layout
                default_layout = [[sg.Button('Start Hearing Exam', key="start")],
                    [sg.Checkbox('Randomize the Exam', default=False, key='randomize')]]
                window = sg.Window(PROGRAM_TITLE, default_layout, grab_anywhere=True, finalize=True)
                window.Refresh()

            case 'start':
                window.close()
                test_layout = [
                            [sg.Text("Which ear do you hear sound from?")],
                            [[sg.Button('Left Ear', key='left'),
                                sg.Button('Right Ear', key='right')]],
                            [sg.Text(size=(40,1), key='output')],
                            [sg.Button('Stop Exam', key='stop')],
                            ]
                window = sg.Window(PROGRAM_TITLE, test_layout, grab_anywhere=True, finalize=True)
                window.Refresh()
                exam = exam_thread.ExamThread()
                exam.daemon = True
                exam.generate_exam_combinations(randomize=(values["randomize"]))
                exam.start()

            case 'right' | 'left':
                if exam.sound_is_heard(event):
                    window['output'].update(f"Sound correctly detected from the {event}",
                                            text_color='green')
                else:
                    window['output'].update(f"Incorrect. Sound is not coming from the {event}",
                                            text_color='red')

            case sg.WINDOW_CLOSED:
                break

if __name__ == '__main__':
    main()
