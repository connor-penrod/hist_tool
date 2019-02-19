import PySimpleGUI as sg
from compute_stats import get_keywords


def histogram_screen():

    keywds = get_keywords("results_with_data.csv")
    column1 = [[sg.Text('Column 1', background_color='#d3dfda', justification='center', size=(10, 1))],      
               [sg.Spin(values=('Spin Box 1', '2', '3'), initial_value='Spin Box 1')],      
               [sg.Spin(values=('Spin Box 1', '2', '3'), initial_value='Spin Box 2')],      
               [sg.Spin(values=('Spin Box 1', '2', '3'), initial_value='Spin Box 3')]]      
    layout = [      
        [sg.Text('Create Histogram', size=(30, 1), font=("Helvetica", 25))],
        [sg.Text('Title:'), sg.InputText('')],
        [sg.Text('Select x-axis variable:'), sg.InputCombo(keywds, size=(20, 3))],        
        [sg.Text('Enter boolean statement for sample #1 (in Python syntax):'), sg.Text('Label for sample #1:'), sg.InputText('')],      
        [sg.InputText('')],   
        [sg.Text('Enter boolean statement for sample #2 (in Python syntax):'), sg.Text('Label for sample #2:'), sg.InputText('')],      
        [sg.InputText('')],
        [sg.Checkbox('Logarithmic',default=False)],
        [sg.Submit(), sg.Cancel()]
    ]

    window = sg.Window('Histogram Settings', default_element_size=(40, 1)).Layout(layout)
    button, values = window.Read()
    window.Close()
    return values