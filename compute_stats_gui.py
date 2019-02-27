from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.stacklayout import StackLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.checkbox import CheckBox
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from compute_stats_gui_simple import histogram_screen
from compute_stats import hist_model, hist_stats
from collections import defaultdict

#class TextForm(BoxLayout):
#    def __init__(self, **kwargs):
#        super(TextForm, self).__init__(**kwargs)
#        self.orientation = 'horizontal'
#        self.add_widget(Label(text='Restrictions'))
#        self.username = TextInput(multiline=False)
#        self.add_widget(self.username)
#    def build(self):
#        return self.layout
        
all_settings = defaultdict(int)
displayed_settings = defaultdict(bool)

def saveSettings():
    saved_settings = [all_settings[key] for key in all_settings if all_settings[key] != 0]
    print(saved_settings)
    with open('last_settings.hst', 'w') as f:
        for item in saved_settings:
            f.write("%s\n" % item)
                
def loadSettings():
    idx = 0
    with open('last_settings.hst', 'r') as f:
        for line in f:
            all_settings[idx] = (eval(line))
            idx += 1
    return idx
        
class HistDescriptor(BoxLayout):
    def __init__(self, title, parentWidget, id, **kwargs):
        super(HistDescriptor, self).__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint = (1,0.1)
        self.add_widget(Label(text=title,size_hint=(None,0.5)))
        self.add_widget(Button(text="Remove",size_hint=(None,0.5), on_press=self.removeHist))
        self.parentWidget = parentWidget
        self.setting_id = id
    #def build(self):
    #    return self
    def removeHist(self, instance):
        self.parentWidget.remove_widget(self)
        all_settings[self.setting_id] = 0
        displayed_settings[self.setting_id] = False
        saveSettings()

class HistToolApp(App):

    def __init__(self):
        super().__init__()
        self.models = []
        self.histLayout = None
        self.usedIDs = []
        self.currID = loadSettings() + 1

    def build(self):
    
        add_hist_button = Button(text='Add Histogram', font_size=14, on_press=self.addHistogram)
        create_hists_button = Button(text='Create Histograms', font_size=14, on_press=self.createHistograms)
        save_hists_button = Button(text='Save Histograms', font_size=14)
        
        btnLayout = BoxLayout(size_hint=(1, None), height=50)
        btnLayout.add_widget(add_hist_button)
        btnLayout.add_widget(create_hists_button)
        btnLayout.add_widget(save_hists_button)
        
        self.histLayout = StackLayout(orientation='tb-lr')
        #histLayout.add_widget(Label(text="test", size_hint=(None, 0.15)))
        #histLayout.add_widget(Label(text="test", size_hint=(None, 0.15)))
        #self.histLayout.add_widget(HistDescriptor("test"))
        #self.histLayout.add_widget(HistDescriptor("test2"))
        #self.histLayout.add_widget(HistDescriptor("test3"))
        #self.histLayout.add_widget(HistDescriptor("test4"))
    
        self.root = BoxLayout(orientation='vertical')
        self.root.add_widget(self.histLayout)
        self.root.add_widget(btnLayout)
        self.updateHistList()
        return self.root
        
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
        
        if string == "":
            return None
        return (vars,"lambda " + ",".join(varReplacements[:len(vars)]) + " : " + string)
        
    def addHistogram(self, instance):
        settings = histogram_screen()
        print(settings)
        
        eval_params1 = self.parseEvalString(settings[3])
        eval_params2 = self.parseEvalString(settings[5])
        if eval_params1 is None or eval_params2 is None:
            print("No evaluation parameters found. Histogram cancelled.")
            return 
        
        print(eval_params1)
        print(eval_params2)
        
        model = hist_model()
        
        model.addTargetQuantity(settings[1])
        model.addParameter(0, eval_params1[0], eval(eval_params1[1]))
        model.addParameter(1, eval_params2[0], eval(eval_params2[1]))
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
        all_settings[self.currID] = settings
        displayed_settings[self.currID] = False
        self.currID += 1
        self.models.append(model)
        
        self.updateHistList()
   
    def createHistograms(self, instance):
        hstats = hist_stats("results_with_data.csv")
        for model in self.models:
            hstats.addHistObject(model)
        
        hstats.execute()
        
    def updateHistList(self):
        for key in all_settings.keys():
            if all_settings[key] != 0 and displayed_settings[key] == False:
                self.histLayout.add_widget(HistDescriptor(all_settings[key][0], self.histLayout, key, size_hint=(1,0.5)))
                displayed_settings[key] = True
        saveSettings()

if __name__ == '__main__':
    HistToolApp().run()