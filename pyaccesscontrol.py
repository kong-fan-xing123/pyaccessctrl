from functools import wraps
"""
Class decorator with Private and Public attribute declarations.
Controls access to attributes stored on an instance, or inherited
by it from its classes. Private declares attribute names that
cannot be fetched or assigned outside the decorated class, and
Public declares all the names that can. Caveat: this works in
3.x for normally named attributes only: __X__ operator overloading
methods implicitly run for built-in operations do not trigger
either __getattr__ or __getattribute__ in new-style classes.
Add __X__ methods here to intercept and delegate built-ins.
"""

traceMe = (not __debug__)
def trace(*args):
    if traceMe: print('[' + ' '.join(map(str,args)) + ']')
def accessControl(failIf):
    def deco(aClass):
        @wraps(aClass)
        class onInstance:
            def __init__(self,*args,**kargs):
                self.__wrapped = aClass(*args,**kargs)
            def __getattr__(self,attr):
                trace('get:',attr)
                if failIf:
                    raise TypeError("can't fetch private attr: " + attr)
                else:
                    return object.__getattribute__(self.__wrapped,attr)
            def __setattr__(self,attr,value):
                trace('set:',attr,value)
                if attr == '_onInstance__wrapped':
                    self.__dict__[attr] = value
                elif failIf(attr):
                    raise TypeError("can't set private attr: " + attr)
                else:
                    setattr(self.__wrapped, attr, value)
        return onInstance
    return deco

def Private(*attributes):
    return accessControl(failIf=(lambda attr: attr in attributes))
def Public(*attributes):
    return accessControl(failIf=(lambda attr: attr not in attributes))