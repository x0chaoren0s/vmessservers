import subprocess, os
from threading import Thread
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.core.clipboard import Clipboard

from spider.server.server_parser_vpnjantit import SP_VPNJANTIT



class MyApp(App):
    def build(self):
        self.spiders = [SP_VPNJANTIT]
        self.is_parsing = False
        self.log_file = 'parsing_log.txt'
        layout = BoxLayout(orientation='vertical')
        buttons_layout = GridLayout(cols=3, size_hint=(1, 0.1))
        button_a = Button(text='start parsing')
        button_a.bind(on_press=self.start_parsing)
        button_b = Button(text='show configs')
        button_b.bind(on_press=self.show_configs)
        button_c = Button(text='copy configs')
        button_c.bind(on_press=self.copy_configs)
        buttons_layout.add_widget(button_a)
        buttons_layout.add_widget(button_b)
        buttons_layout.add_widget(button_c)
        layout.add_widget(buttons_layout)
        self.log_text = TextInput(multiline=True, readonly=True, size_hint=(1, 0.45))
        layout.add_widget(self.log_text)
        self.configs = TextInput(multiline=True, readonly=True, size_hint=(1, 0.45))
        layout.add_widget(self.configs)
        return layout

    def start_parsing(self, *args):
        if self.is_parsing is False:
            # with open(self.log_file, 'w', encoding='utf8') as f:
            #     parsing_process = subprocess.Popen(['python', 'run.py'], stdout=f, stderr=f)
            threads = [Thread(target=spider.parse) for spider in self.spiders]
            for t in threads:
                t.daemon = True
                t.start()
            self.is_parsing = True
            self.log_text.text = ''
            Clock.schedule_interval(self.update_log_text, 0.1)
            

    def show_configs(self, *args):
        config_files = [file for file in os.listdir('results') if file.endswith('conf')]
        self.configs.text = ''
        for config_file in config_files:
            with open('results/'+config_file, 'r') as fin:
                new_output = fin.readlines()
                if new_output:
                    self.configs.text += ''.join(new_output)

    def copy_configs(self, *args):
        Clipboard.copy(self.configs.text)

    def update_log_text(self, *args):
        with open(self.log_file, 'r', encoding='ISO-8859-1') as f:
            new_output = f.readlines()
            if new_output:
                # for line in new_output:
                #     self.log_text.text += line
                self.log_text.text = ''.join(new_output[-50:])



if __name__ == '__main__':
    MyApp().run()