import wpf

from System.Windows import Application, Window
from System.Windows.Controls import Canvas, Button, TextBox
from datetime import datetime
import calculator

def Walk(tree):
    yield tree
    if hasattr(tree, 'Children'):
        for child in tree.Children:
            for x in Walk(child):
                yield x
    elif hasattr(tree, 'Child'):
        for x in Walk(tree.Child):
            yield x
    elif hasattr(tree, 'Content'):
        for x in Walk(tree.Content):
            yield x

class Calc(Canvas):
    def __init__(self):
        wpf.LoadComponent(self, 'Calc.xaml')

        controls = [ n for n in Walk(self) if isinstance(n, Button) or isinstance(n, TextBox) ]
        for c in controls:
            c.FontSize *=2
        calculator.enliven(self)

class Clock(Canvas):
    def __init__(self):
        wpf.LoadComponent(self, 'Clock.xaml')

        self.start()
    def _fromAngle(self, time, divisor = 5, offset = 0):
        return ((time / (12.0 * divisor)) * 360) + offset + 180
    def _toAngle(self, time):
        return self._fromAngle(time) + 360
    def start(self):
        d = datetime.now()
        from_h = self._fromAngle(d.hour, 1, d.minute/2)
        to_h = from_h + 360.0
        self.hourAnimation.From = from_h
        self.hourAnimation.To = to_h
        self.minuteAnimation.From = self._fromAngle(d.minute)
        self.minuteAnimation.To = self._toAngle(d.minute)
        self.secondAnimation.From = self._fromAngle(d.second)
        self.secondAnimation.To = self._toAngle(d.second)

class Drag(object):
    def __init__(self, obj):
        self.click = None
        self.obj = obj
        self.root = obj.Parent
    def OnMouseLeftButtonDown(self, sender, e):
        self.click = e.GetPosition(self.root)
        self.sx = Canvas.GetLeft(self.obj)
        self.sy = Canvas.GetTop(self.obj)
        if (self.sx.IsNaN(self.sx)): self.sx = 0.0
        if (self.sy.IsNaN(self.sy)): self.sy = 0.0
        self.obj.CaptureMouse()
    def OnMouseLeftButtonUp(self, sender, e):
        if(self.click != None):
            self.obj.ReleaseMouseCapture()
            self.click = None
    def OnMouseMove(self, sender, e):
        if(self.click != None):
            mouse_pos = e.GetPosition(self.root)
            Canvas.SetLeft(self.obj, (self.sx + mouse_pos.X - self.click.X))
            Canvas.SetTop(self.obj, (self.sy + mouse_pos.Y - self.click.Y))
    def enable(self):
         self.obj.MouseLeftButtonDown += self.OnMouseLeftButtonDown
         self.obj.MouseLeftButtonUp += self.OnMouseLeftButtonUp
         self.obj.MouseMove += self.OnMouseMove
    def disable(self):
         self.obj.MouseLeftButtonDown -= self.OnMouseLeftButtonDown
         self.obj.MouseLeftButtonUp -= self.OnMouseLeftButtonUp
         self.obj.MouseMove -= self.OnMouseMove

class MyWindow(Window):
    def __init__(self):
        wpf.LoadComponent(self, 'WpfApplicationClockCalc.xaml')

        self.calc = Calc()
        self.rootCanvas.Children.Add (self.calc)

        self.clock = Clock()
        self.rootCanvas.Children.Add (self.clock)
        Canvas.SetTop(self.clock, 50)
        Canvas.SetLeft(self.clock, 10)

        Canvas.SetTop(self.calc, 50)
        Canvas.SetLeft(self.calc, 350)

        d1 = Drag(self.calc )
        d1.enable()

        d2 = Drag(self.clock)
        d2.enable()

if __name__ == '__main__':
    Application().Run(MyWindow())
