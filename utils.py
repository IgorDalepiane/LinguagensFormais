def readUntil(line, separator = ','):
  separatorFound = False
  string = ""
  i = 0
  while(not separatorFound and i < len(line)):
    symbol = line[i]
    if(line[i] == separator):
      separatorFound = True
    else:
      string += symbol
    i += 1
  return string.strip(), line[i:]

def readTransitions(lines):
  transitions = {}
  for line in lines: 
    line = line[line.find('(') + 1:]
    lst, line = readUntil(line,')')  
    line = line[line.find('=') + 1:]
    
    lst = lst.split(',')
    lst.append(line)
    if not transitions.get(lst[0]):
      transitions[lst[0]] = []
    transitions[lst[0]].append([lst[1],lst[2]])
  return transitions

def readCSV(filename):
  wordList = []
  try:
    with open(filename) as file:
      wordList = file.read()
      return wordList.split(",")
  except:
      print("Couldn't open file")
