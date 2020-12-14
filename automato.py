from utils import *

class AFD:
  def __init__(self):
    filename = "automato.txt"
    lines = []
    with open(filename) as f:
      lines = f.read().splitlines()
    
    lines[0] = readUntil(lines[0], '=')[1]
    lines[0] = lines[0][lines[0].find('{') + 1:]

    self.alphabet, lines[0] = readUntil(lines[0], '}')
    self.alphabet = self.alphabet.split(',')
    
    lines[0] = lines[0][lines[0].find('{') + 1:]
    self.states, lines[0] = readUntil(lines[0], '}')
    self.states = self.states.split(',')

    lines[0] = lines[0][lines[0].find(',') + 1:]
    self.transitions, lines[0] = readUntil(lines[0])

    self.initialState, lines[0] = readUntil(lines[0])
    
    lines[0] = lines[0][lines[0].find('{') + 1:]
    self.finalStates, lines[0] = readUntil(lines[0],'}')
    self.finalStates = self.finalStates.split(',')
    self.transitions = readTransitions(lines[2:])

  def checkMultiple(self, wordList):
    acc = []
    rej = []
    for word in wordList:
      result = self.checkWord(word)[0]
      if result:
        acc.append(word)
      else:
        rej.append(word)
    
    print("Palavras aceitas: ")
    for w in acc:
      print(w)
    print("Palavras rejeitadas: ")
    for w in rej:
      print(w)


  def checkWord(self, word):
    acctualState = self.initialState
    for letter in word:
      for transition in self.transitions[acctualState]:
        if transition[0] == letter:
          acctualState = transition[1]

    if acctualState in self.finalStates:
      return [True, "Palavra aceita"]
    else:
      return [False, "Palavra não aceita"]

  def notReachables(self):
    reachables = [self.initialState]
    for state in reachables:
        for transition in self.transitions[state]:
          if transition[1] not in reachables:
            reachables.append(transition[1])

    self.notReachables = []
    for state in self.states:
      if state not in reachables:
        self.notReachables.append(state)

  def deadStates(self):
    reachedStates = []
    self.deadStates = []

    for state in self.states:
      for transition in self.transitions[state]:
        if transition[1] not in reachedStates:
          reachedStates.append(transition[1])
          
      for rState in reachedStates:
        for transition in self.transitions[rState]:
          if transition[1] not in reachedStates:
            reachedStates.append(transition[1])

      dead = True
      for finalState in self.finalStates:
        if finalState in reachedStates:
          dead = False
      if dead == True:
        self.deadStates.append(state)
      
      reachedStates = []

  def minimization(self):
    self.notReachables()
    self.deadStates()

    print("Transições antes da minimalização: \n ",self.transitions,"\n")
    for state in self.states:
      for dState in self.deadStates:
        for transition in self.transitions[state]:
          if transition[1] == dState:
            self.transitions[state].remove([transition[0],transition[1]])
            # del self.transitions[state, letter]
      if state in self.notReachables or state in self.deadStates:
          del self.transitions[state]
  
    print("Transições depois da minimalização: \n ",self.transitions,"\n")

    print("Estados não alcançaveis: ",self.notReachables)
    print("Estados mortos: ",self.deadStates)

  def cli(self):
    while(True):
      s = input("# ").strip()
      if s == 'sair':
        break
      else:
        space = s.find(' ')
        command = s[:space]
        args = s[space:].strip().split(' ')
        if len(args) == 1 and command == 'testar':
          print(self.checkWord(readUntil(args[0], '')[0])[1])
        elif len(args) == 1 and command == 'lista':
          wordList = readCSV(args[0])
          self.checkMultiple(wordList)
        elif command == 'mi':
          self.minimization()
        elif command == 'hel': 
          print("Comandos disponiveis: \nMinimizacao:\tmin\nTeste:\t\ttestar < PALAVRA >\nTestar varios:\tlista < CAMINHO_ARQUIVO >\nTerminar:\tsair")
        else:
          print("Comando invalido, digite help para uma lista de comandos")
        
afd = AFD()
afd.cli()