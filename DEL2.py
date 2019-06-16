module = __import__('DEL')
class_ = getattr(module, 'Foo')
test = class_()
print(test)