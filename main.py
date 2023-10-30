# Import Libraries
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Line
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image as img
import pytesseract
import PIL.Image
from PIL import Image
import sys
from docx import Document
import os
os.environ["KIVY_NO_CONSOLELOG"] = "1"

#path = input("Path of the folder: ")
#path = "C:/Users/fmb9/Documents/handwriting_to_text_new/"
path = "C:/Users/faiza/Desktop/Python_Projects/textify/"
#path = "C:/Users/amc0/Desktop/text/"

# Making an file which copies the error in a text file
sys.stderr = open(path + 'sources/err.txt', 'w')
print('This is an error message: ', file=sys.stderr)

# Class which contains the main drawing method
class DrawingWidget(Widget):
    def __init__(self, **kwargs):
        super(DrawingWidget, self).__init__(**kwargs)
        self.touch_start_pos = None
        self.line = None

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.touch_start_pos = touch.pos
            with self.canvas:
                touch.ud["line"] = Line(points=(touch.x, touch.y), width=2)
                self.line = touch.ud["line"]

    def on_touch_move(self, touch):
        if self.touch_start_pos and self.line:
            self.line.points += [touch.x, touch.y]

    def on_touch_up(self, touch):
        self.touch_start_pos = None

    def save_image(self):
        self.export_to_png(path + 'sources/drawing.png')

# Class for UI like buttons and Logo image
class DrawingApp(App):
    def build(self):
        root = BoxLayout(orientation='vertical')

        self.title = "Textify"
        self.drawing_widget = DrawingWidget()
        clear_button = Button(text='Clear', size_hint_y=None, height=200, font_size=32, background_color='red')
        clear_button.bind(on_release=self.clear_canvas)
        save_button = Button( text='Save as .docx', size_hint_y=None, height=200, font_size=32, background_color='red')
        save_button.bind(on_release=self.save_image)
        test = Button( text='', size_hint_y=None, height=200, font_size=32, background_normal = path + 'sources/textify_logo2.png', background_down = path + 'sources/textify_logo2.png')

        root.add_widget(self.drawing_widget)
        button_layout = BoxLayout(orientation='horizontal')
        button_layout.add_widget(test)
        button_layout.add_widget(clear_button)
        button_layout.add_widget(save_button)
        root.add_widget(button_layout)

        return root
 

    def clear_canvas(self, instance):
        self.drawing_widget.canvas.clear()

# drawing a black background for the initial transparent image
    def save_image(self, instance):
        self.drawing_widget.save_image()
        image = Image.open(path + "sources/drawing.png")
        background_color = (0, 0, 0)
        output_image = Image.new("RGBA", image.size, background_color)
        output_image.paste(image, (0, 0), image)
        output_image.save(path + "sources/output.png")

        # Extracting text from image
        def extractTextFromImg(img):
            text = pytesseract.image_to_string(img, lang='eng')         
            text = text.encode("gbk", 'ignore').decode("gbk", "ignore")        
            return text
    
        myconfig = r"--psm 11 --oem 3"
        #text = pytesseract.image_to_string(PIL.Image.open("C:/Users/faiza/Desktop/Python_Projects/handwriting_to_text_new/output.png"), config=myconfig)
        text = extractTextFromImg(PIL.Image.open(path + "sources/output.png"))

        #print(text)

        # Writing the extracted text in a .txt file
        with open(path + "data.txt", "w") as f: 
            f.write(str(text))

        # Writing the extracted text in a .docx file
        document = Document()
        myfile = open(path + "data.txt").read()
        p = document.add_paragraph(myfile)
        document.save(path + 'data.docx')

if __name__ == '__main__':
    DrawingApp().run()
