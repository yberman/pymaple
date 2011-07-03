import maple
for name in dir(maple):
    if not name in dir(__builtins__):
        obj = getattr(maple, name)
        setattr(__builtins__, name, obj)

from wx.py.PyShell import main
main()
