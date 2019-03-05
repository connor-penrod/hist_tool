import PySimpleGUI as sg
from compute_stats import get_keywords

#['title', 'ID', 'label1', 'boolean1', 'label2', 'boolean2', True]
#0           1       2           3           4       5           6
def histogram_screen(title = "", id = "", label1 = "", param1 = "", label2 = "", param2 = "", log = False):

    keywds = get_keywords("results_with_data.csv")
    column1 = [[sg.Text('Column 1', background_color='#d3dfda', justification='center', size=(10, 1))],      
               [sg.Spin(values=('Spin Box 1', '2', '3'), initial_value='Spin Box 1')],      
               [sg.Spin(values=('Spin Box 1', '2', '3'), initial_value='Spin Box 2')],      
               [sg.Spin(values=('Spin Box 1', '2', '3'), initial_value='Spin Box 3')]]      
    layout = [      
        [sg.Text('Create Histogram', size=(30, 1), font=("Helvetica", 25))],
        [sg.Text('Title:'), sg.InputText(title)],
        [sg.Text('Select x-axis variable:'), sg.InputCombo(keywds, size=(20, 3), default_value = id)],        
        [sg.Text('Enter boolean statement for sample #1 (in Python syntax):'), sg.Text('Label for sample #1:'), sg.InputText(label1)],      
        [sg.InputText(param1)],   
        [sg.Text('Enter boolean statement for sample #2 (in Python syntax):'), sg.Text('Label for sample #2:'), sg.InputText(label2)],      
        [sg.InputText(param2)],
        [sg.Checkbox('Logarithmic',default=log)],
        [sg.Submit(), sg.Cancel()]
    ]

    window = sg.Window('Histogram Settings', default_element_size=(40, 1)).Layout(layout)
    button, values = window.Read()
    if button is None:
        return None
    
    window.Close()
    return values