from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.checkbox import CheckBox
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from compute_stats_gui_simple import histogram_screen
from compute_stats import hist_model, hist_stats

#class TextForm(BoxLayout):
#    def __init__(self, **kwargs):
#        super(TextForm, self).__init__(**kwargs)
#        self.orientation = 'horizontal'
#        self.add_widget(Label(text='Restrictions'))
#        self.username = TextInput(multiline=False)
#        self.add_widget(self.username)
#    def build(self):
#        return self.layout
        
class LoginScreen(GridLayout):

    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.cols = 2
        self.height = 20
        self.button = Button(text='Make Histogram', font_size=14, on_press=self.addHistogram)
        self.button.size_hint = (1,0.2)
        self.add_widget(self.button)


class HistToolApp(App):

    def __init__(self):
        super().__init__()
        self.all_settings = []
        self.models = []

    def build(self):
    
        add_hist_button = Button(text='Add Histogram', font_size=14, on_press=self.addHistogram)
        create_hists_button = Button(text='Create Histograms', font_size=14, on_press=self.createHistograms)
        
        btnLayout = BoxLayout(size_hint=(1, None), height=50)
        btnLayout.add_widget(add_hist_button)
        btnLayout.add_widget(create_hists_button)
    
        root = BoxLayout(orientation='vertical')
        root.add_widget(Widget())
        root.add_widget(btnLayout)
        return root
        
    def parseEvalString(self, string):
        varSt = 0
        varEnd = 0
        varReplacements = ['x','y','z','a','b','c','d','e','f','g','h','i','j','k']
        vars = []
        remainingBrackets = True
        while remainingBrackets == True:
            remainingBrackets = False
            for idx,c in enumerate(string):
                if c == "{":
                    remainingBrackets = True
                    varSt = idx
                elif c == "}":
                    varEnd = idx
                    retVar = string[varSt+1:varEnd]
                    
                    if retVar in vars:
                        inserted = varReplacements[vars.index(retVar)]
                    else:
                        vars.append(retVar)
                        inserted = varReplacements[len(vars)-1]
                    
                    string = string[:varSt] + inserted + string[varEnd+1:]
                    break
        return (vars,"lambda " + ",".join(varReplacements[:len(vars)]) + " : " + string)
        
    def addHistogram(self, instance):
        settings = histogram_screen()
        print(settings)
        
        eval_params = self.parseEvalString(settings[3])
        model = hist_model()
        
        model.addTargetQuantity(settings[1])
        model.addParameter(0, eval_params[0], eval(eval_params[1]))
        model.addParameter(1, eval_params[0], eval(eval_params[1]))
        model.changeLog(settings[6])
        model.changeTitle(settings[0])
        model.changeLabels((settings[2],settings[4]))
        
        #['title', 'ID', 'label1', 'boolean1', 'label2', 'boolean2', True]
        #0           1       2           3           4       5           6
#        def addTargetQuantity(self, quantity):
#        self.targetQuantity = quantity
#   def addParameter(self, group, params, condition):
#        c = condition.__code__.co_argcount
#        self.parameters.append((group, params, condition, c))
#    
#    def changeLog(self,b):
#        self.enableLog = b
#    
#    def changeTitle(self,s):
#        self.title = s
#        
#    def changeLabels(self, tup):
#        self.labels = tup
#        
        self.all_settings.append(settings)
        self.models.append(model)
   
    def createHistograms(self, instance):
        hstats = hist_stats("results_with_data.csv")
        for model in self.models:
            hstats.addHistObject(model)
        
        hstats.execute()

if __name__ == '__main__':
    HistToolApp().run()