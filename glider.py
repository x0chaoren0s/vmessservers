import subprocess, platform
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput


class MyApp(App):
    def build(self):
        self.plat = platform.system().lower()
        self.external_process = None
        self.log_file = 'glider_log.txt'
        layout = BoxLayout(orientation='vertical')
        buttons_layout = GridLayout(cols=2, size_hint=(1, 0.1))
        button_a = Button(text='start glider')
        button_a.bind(on_press=self.start_external_process)
        button_b = Button(text='stop glider')
        button_b.bind(on_press=self.stop_external_process)
        buttons_layout.add_widget(button_a)
        buttons_layout.add_widget(button_b)
        layout.add_widget(buttons_layout)
        self.log_text = TextInput(multiline=True, readonly=True)
        layout.add_widget(self.log_text)
        return layout

    def start_external_process(self, *args):
        if self.external_process is None:
            with open(self.log_file, 'w', encoding='utf8') as f:
                if self.plat=='windows':
                    self.external_process = subprocess.Popen(['cmd', '/c', 
                                                            r'D:\Users\60490\kivy_learning\glider.exe', '-config',
                                                            r'D:\Users\60490\kivy_learning\glider_3060.conf'],
                                                            stdout=f,
                                                            stderr=f)
                elif self.plat=='linux':
                    self.external_process = subprocess.Popen(['glider', '-config', '/home/u3060/glider_3060.conf'],
                                                            stdout=f,
                                                            stderr=f)
            self.log_text.text = ''
            Clock.schedule_interval(self.update_log_text, 0.1)

    def stop_external_process(self, *args):
        if self.external_process is not None:
            if self.plat=='windows':
                subprocess.run("TASKKILL /F /PID {pid} /T".format(pid=self.external_process.pid))
            elif self.plat=='linux':
                self.external_process.terminate()
            self.external_process = None
            Clock.unschedule(self.update_log_text)

    def update_log_text(self, *args):
        with open(self.log_file, 'r') as f:
            new_output = f.readlines()
            if new_output:
                self.log_text.text = ''.join(new_output[-50:])


if __name__ == '__main__':
    MyApp().run()