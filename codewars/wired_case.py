#-*-coding utf-8-*-

def to_weird_case(string):
    import re
    o = []
    if len(re.split('\W',string)) >= 2: 
        for word in (re.split('\W',string)):
            print word
            o.append(updown(word))
    else:
            return updown(string)
    return ' '.join(o)



def updown(s):
  t = ''
  if len(s) == 1:
    return s.upper()
  else:
      for index, l in enumerate(s):
        if index % 2 != 0:
          t+=l.lower()
        else:
          t+=l.upper()
  return t


print to_weird_case('JuSt kIdDiNg')     
      
    
