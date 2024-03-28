import tkinter as tk
from tkinter import Canvas, Menu
from abc import abstractmethod, ABC
from enum import Enum


class DwgObj:
    color = "#000000"

    @abstractmethod
    def shape_draw(self):
        pass


class DwgLine(DwgObj):
    def __init__(self, spt, ept):
        self.spt = spt
        self.ept = ept

    def shape_draw(self, canvas):
        canvas.create_line(self.spt, self.ept)

#model

class Model:
    mainlist = []

    def appendObj(self,graphobj):
        self.mainlist.append(graphobj)

    def getDwgObjs(self):
        return self.mainlist

class View:
    def __init__(self,root,model):
        self.root = root
        self.model = model
        self.canvas = Canvas(root,width=640,height=480)
        self.canvas.pack()
        self.draw_shapes()

    def draw_shapes(self):
        for i in self.model.getDwgObjs():
            i.shape_draw(self.canvas)

    def update_view(self):
        self.canvas.delete("all")
        self.draw_shapes()

class DrawType(Enum):
    DNone = 1
    DLine = 2
    DCircle = 3

class Controller:
    def __init__(self,root,model,view):
        self.root = root
        self.model = model
        self.view = view
        self.curDrawType = DrawType.DNone
        self.root.bind("<Button-1>",self.on_mouseClick)
        self.isFirst = True
        self.x1 = 0
        self.y1 = 0

    def on_mouseClick(self,event):
        if self.curDrawType == DrawType.DLine : #当前正在画线
            if self.isFirst:
                self.x1,self.y1 = event.x,event.y
                self.isFirst = False
            else:
                x2,y2 = event.x,event.y
                line = DwgLine((self.x1,self.y1),(x2,y2))
                self.model.appendObj(line)
                self.isFirst = True
        self.view.update_view()
    def on_drawline(self):
        self.curDrawType = DrawType.DLine


def main():
    root = tk.Tk()
    model = Model()
    view = View(root,model)
    controller = Controller(root,model,view)

    menu_bar = Menu(root)
    draw_menu = Menu(menu_bar,tearoff=0)
    draw_menu.add_command(label="Line",command=controller.on_drawline)
    menu_bar.add_cascade(label="Draw",menu=draw_menu)
    root.config(menu = menu_bar)

    root.mainloop()


if __name__ == "__main__" :
    main()