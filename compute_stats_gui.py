from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.stacklayout import StackLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.checkbox import CheckBox
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget
from compute_stats_gui_simple import histogram_screen
from compute_stats import hist_model, hist_stats
from collections import defaultdict
from kivy.core.window import Window

#class TextForm(BoxLayout):
#    def __init__(self, **kwargs):
#        super(TextForm, self).__init__(**kwargs)
#        self.orientation = 'horizontal'
#        self.add_widget(Label(text='Restrictions'))
#        self.username = TextInput(multiline=False)
#        self.add_widget(self.username)
#    def build(self):
#        return self.layout
        
#displayed_settings = defaultdict(bool)
        
class HistDescriptor(BoxLayout):
    def __init__(self, title, mainTool, id, **kwargs):
        super(HistDescriptor, self).__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint = (1,None)
        self.setting_id = id
        self.add_widget(Label(text=str(self.setting_id),size_hint=(0.1,0.5)))
        self.add_widget(Label(text=title,size_hint=(0.5,0.5)))
        self.add_widget(Button(text="Duplicate", size_hint=(0.1,0.5), on_press=self.duplicateHist))
        self.add_widget(Button(text="Edit",size_hint=(0.1,0.5), on_press=self.editHist))
        self.add_widget(Button(text="Remove",size_hint=(0.1,0.5), on_press=self.removeHist))
        self.parentWidget = mainTool.histLayout
        self.mainTool = mainTool
        #self.mainTool.histLayout.height += self.height
    #def build(self):
    #    return self
    def removeHist(self, instance):
        self.parentWidget.remove_widget(self)
        self.mainTool.all_settings[self.setting_id] = 0
        #displayed_settings[self.setting_id] = False
        self.mainTool.saveSettings()
    
    def editHist(self, instance):
        self.mainTool.editHist(self.setting_id)
        
    def duplicateHist(self, instance):
        print("Duplicate setting ID: " + str(self.setting_id))
        self.mainTool.duplicateHist(self.setting_id)

class HistToolApp(App):

    def __init__(self):
        super().__init__()
        self.models = []
        self.histLayout = None
        self.scrollView = None
        self.usedIDs = []
        self.all_settings = defaultdict(int)
        self.currID = self.loadSettings()
        self.initLayoutHeight = 0
        
    def saveSettings(self):
        saved_settings = [self.all_settings[key] for key in self.all_settings if self.all_settings[key] != 0]
        #print(saved_settings)
        with open('last_settings.hst', 'w') as f:
            for item in saved_settings:
                f.write("%s\n" % item)
                
    def loadSettings(self):
        idx = 0
        with open('last_settings.hst', 'r') as f:
            for line in f:
                self.all_settings[idx] = (eval(line))
                idx += 1
        return idx

    def build(self):
    
        add_hist_button = Button(text='Add Histogram', font_size=14, on_press=self.addHistogram)
        create_hists_button = Button(text='Create Histograms', font_size=14, on_press=self.createHistograms)
        save_hists_button = Button(text='Save Histograms', font_size=14)
        
        btnLayout = BoxLayout(size_hint=(1, None), height=50)
        btnLayout.add_widget(add_hist_button)
        btnLayout.add_widget(create_hists_button)
        btnLayout.add_widget(save_hists_button)
        
        self.scrollView = ScrollView(size_hint=(1, 1))
        self.scrollView.do_scroll_x = False
        self.histLayout = StackLayout(orientation='tb-lr')
        self.histLayout.size_hint = (1,None)
        self.histLayout.height = 0#Window.height - btnLayout.height
        self.initLayoutHeight = self.histLayout.height
        self.histLayout.bind(minimum_height=self.histLayout.setter('height'))
        self.scrollView.add_widget(self.histLayout)
    
        self.root = BoxLayout(orientation='vertical')
        self.root.add_widget(self.scrollView)
        self.root.add_widget(btnLayout)
        self.updateHistList()
        return self.root
        
    def updateModels(self):
        self.models = []
        for key in self.all_settings:
            if self.all_settings[key] != 0:
                model = self.createModel(self.all_settings[key])
                self.models.append(model)
       
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
        
    def createModel(self, settings):
        eval_params1 = self.parseEvalString(settings[3])
        eval_params2 = self.parseEvalString(settings[5])
        if eval_params1 is None or eval_params2 is None:
            print("No evaluation parameters found. Histogram cancelled.")
            return 
        
        #print(eval_params1)
        #print(eval_params2)
        
        model = hist_model()
        
        model.addTargetQuantity(settings[1])
        model.addParameter(0, eval_params1[0], eval(eval_params1[1]))
        model.addParameter(1, eval_params2[0], eval(eval_params2[1]))
        model.changeLog(settings[6])
        model.changeTitle(settings[0])
        model.changeLabels((settings[2],settings[4]))
        return model
        
    def addHistogram(self, instance):
        settings = histogram_screen()
        
        #['title', 'ID', 'label1', 'boolean1', 'label2', 'boolean2', True]
        #0           1       2           3           4       5           6
        
        self.all_settings[self.currID] = settings
        #displayed_settings[self.currID] = False
        self.currID += 1
        
        self.updateHistList()
   
    def createHistograms(self, instance):
        self.updateModels()
        hstats = hist_stats("results_with_data.csv")
        for model in self.models:
            hstats.addHistObject(model)
        
        hstats.execute()
        
    def editHist(self, key):
        setting = self.all_settings[key]
        self.all_settings[key] = histogram_screen(*setting)
        #displayed_settings[key] = False
        self.updateHistList()
        
    def duplicateHist(self, key):
        print("CurrID: " + str(self.currID))
        self.all_settings[self.currID] = self.all_settings[key]
        self.currID += 1
        self.updateHistList()
        
    def updateHistList(self):
        #for widget in self.histLayout.children:
         #   print(widget.setting_id)
            #self.histLayout.remove_widget(widget)
        self.histLayout.clear_widgets()
    
        for key in range(self.currID+1):
            if key in self.all_settings and self.all_settings[key] != 0:
                self.histLayout.add_widget(HistDescriptor(self.all_settings[key][0], self, key, size_hint=(None,None)))
        
        self.histLayout.height = self.initLayoutHeight
        for child in self.histLayout.children:
            self.histLayout.height += child.height
            
        self.histLayout.bind(minimum_height=self.histLayout.setter('height'))
        
        self.saveSettings()
        print("HistLayout height: " + str(self.histLayout.height))

if __name__ == '__main__':
    HistToolApp().run()