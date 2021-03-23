import json
import tkinter as tk

from tkinter import filedialog

class ListItem(tk.Frame):
    def __init__(self, parent, name, data):
        super().__init__(master=parent)
        self.parent = parent
        self.name = name
        self.data = data
        self.is_leaf = not isinstance(data, dict) and not isinstance(data, list)
        self.list_items = []

        self.create_widgets()

    def create_widgets(self):
        label = tk.Label(self, text=self.name)
        label.bind("<Button-1>", self.expand)
        label.pack()

    def expand(self, evt=None):
        if len(self.list_items) <= 0:
            if isinstance(self.data, dict):
                for key in self.data:
                    self.list_items.append(ListItem(self, key, self.data[key]))
                    self.list_items[-1].pack()
            elif isinstance(self.data, list):
                for i, item in enumerate(self.data):
                    self.list_items.append(ListItem(self, f"Element: {i}", item))
                    self.list_items[-1].pack()
            elif self.is_leaf:
                self.list_items.append(tk.Label(self, text=f"{self.data}"))
                self.list_items[-1].pack()
            else:
                print("NOT IMPLEMENTED")
        else:
            for item in self.list_items:
                item.destroy()
            self.list_items = []

    

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry('800x300')
        self.title('JSON Viewer')
        self.create_widgets()
        self.data = None

    def upload_file(self, e=None):
        print(type(self.data))
        fname = filedialog.askopenfilename()
        new_data = {}
        with open(fname, 'r') as f:
            new_data = json.load(f)
        
        if self.data is not None:
            self.data.destroy()
        self.data = ListItem(self.scrollable_frame, "root", new_data)
        self.data.pack()

    def create_widgets(self):
        frame = tk.Frame(self)
        canvas = tk.Canvas(frame)
        self.scrollable_frame = tk.Frame(canvas)
        scrollbar = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.pack(fill=tk.BOTH)
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor='nw')
        self.scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        button = tk.Button(self.scrollable_frame, text="Select File", command=self.upload_file)
        button.pack(side="top")

        self.data = ListItem(self.scrollable_frame, "root", {
            "item1" : 3,
            "item2" : "Hi",
            "item3" : False,
            "item4" : None,
            "item5" : [
                56,
                4,
                345,
                2854,
                535
            ],
        })

        self.data.pack(fill=tk.BOTH)

        frame.pack(fill=tk.BOTH)


if __name__ == "__main__":
    app = App()
    app.mainloop()