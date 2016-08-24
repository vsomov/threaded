from random import randint

import threading
import Queue
import time
import json

# import time
# from threading import Thread
#
# def myfunc(i):
#     print "sleeping 5 sec from thread %d" % i
#     time.sleep(5)
#     print "finished sleeping from thread %d" % i
#
# for i in range(50):
#     t = Thread(target=myfunc, args=(i,))
#     t.start()

class Character:
  def __init__(self):
    self.name = ""
    self.health = 1
    self.health_max = 1
  def do_damage(self, enemy):
    damage = min(
        max(randint(0, self.health) - randint(0, enemy.health), 0),
        enemy.health)
    enemy.health = enemy.health - damage
    if damage == 0: print "%s evades %s's attack." % (enemy.name, self.name)
    else: print "%s hurts %s!" % (self.name, enemy.name)
    return enemy.health <= 0

class Player(Character):
  def __init__(self):
    Character.__init__(self)
    self.state = 'normal'
    self.health = 10
    self.health_max = 10
  def quit(self):
    print "%s can't find the way back home, and dies of starvation.\nR.I.P." % self.name
    self.health = 0
  def help(self): print Commands.keys()
  def status(self): print "%s's health: %d/%d" % (self.name, self.health, self.health_max)
  def tired(self):
    print "%s feels tired." % self.name
    self.health = max(1, self.health - 1)
  def rest(self):
    if self.state != 'normal': print "%s can't rest now!" % self.name; self.enemy_attacks()
    else:
      print "%s rests." % self.name
      if randint(0, 1):
        self.enemy = Enemy(self)
        print "%s is rudely awakened by %s!" % (self.name, self.enemy.name)
        self.state = 'fight'
        self.enemy_attacks()
      else:
        if self.health < self.health_max:
          self.health = self.health + 1
        else: print "%s slept too much." % self.name; self.health = self.health - 1
  def explore(self):
    if self.state != 'normal':
      print "%s is too busy right now!" % self.name
      self.enemy_attacks()
    else:
      print "%s explores a twisty passage." % self.name
      if randint(0, 1):
        self.enemy = Enemy(self)
        print "%s encounters %s!" % (self.name, self.enemy.name)
        self.state = 'fight'
      else:
        if randint(0, 1): self.tired()
  def flee(self):
    if self.state != 'fight': print "%s runs in circles for a while." % self.name; self.tired()
    else:
      if randint(1, self.health + 5) > randint(1, self.enemy.health):
        print "%s flees from %s." % (self.name, self.enemy.name)
        self.enemy = None
        self.state = 'normal'
      else: print "%s couldn't escape from %s!" % (self.name, self.enemy.name); self.enemy_attacks()
  def attack(self):
    if self.state != 'fight': print "%s swats the air, without notable results." % self.name; self.tired()
    else:
      if self.do_damage(self.enemy):
        print "%s executes %s!" % (self.name, self.enemy.name)
        self.enemy = None
        self.state = 'normal'
        if randint(0, self.health) < 10:
          self.health = self.health + 1
          self.health_max = self.health_max + 1
          print "%s feels stronger!" % self.name
      else: self.enemy_attacks()
  def enemy_attacks(self):
    if self.enemy.do_damage(self): print "%s was slaughtered by %s!!!\nR.I.P." %(self.name, self.enemy.name)

Commands = {
  'quit': Player.quit,
  'help': Player.help,
  'status': Player.status,
  'rest': Player.rest,
  'explore': Player.explore,
  'flee': Player.flee,
  'attack': Player.attack,
  }

items = json.load(open('items.json'))

def show_gold(gold):
    print ( "You've got " + str(items["items"]["Gold"]["quantity"]) + "g of gold!" )
    # print("You've got {}g of gold!".format(gold))
    # print("You've got 'items["items"]["Gold"]["quantity"]'g of gold!")

def worker():

    print threading.currentThread().getName(), 'Starting '
    print "sleeping 2 sec from thread %s" %threading.currentThread().getName()
    time.sleep(2)
    print threading.currentThread().getName(), 'Exiting'

def menu_service():

    print threading.currentThread().getName(), 'Starting '
    print "sleeping 3 sec from thread %s" %threading.currentThread().getName()
    time.sleep(3)
    print threading.currentThread().getName(), 'Exiting'




def main():

    show_gold(items)
    # print(items)

    while 1:
        print "main loop is working..."
        time.sleep(10)

        m = threading.Thread(name='menu_service', target=menu_service)
        w0 = threading.Thread(name='battle', target=worker)
        # w1 = threading.Thread(name='travel', target=worker)

        m.start()
        w0.start()
        # w1.start()

main()




# def console(q, lock):
#     while 1:
#         input()   # Afther pressing Enter you'll be in "input mode"
#         with lock:
#             cmd = input('> ')
#
#         q.put(cmd)
#         if cmd == 'quit':
#             break
#
# def action_foo(lock):
#     with lock:
#         print('--> action foo')
#     # other actions
#
# def action_bar(lock):
#     with lock:
#         print('--> action bar')
#
# def invalid_input(lock):
#     with lock:
#         print('--> Unknown command')
#
# def main():
#     cmd_actions = {'foo': action_foo, 'bar': action_bar}
#     cmd_queue = Queue.Queue()
#     stdout_lock = threading.Lock()
#
#     dj = threading.Thread(target=console, args=(cmd_queue, stdout_lock))
#     dj.start()
#
#     while 1:
#         cmd = cmd_queue.get()
#         if cmd == 'quit':
#             break
#         action = cmd_actions.get(cmd, invalid_input)
#         action(stdout_lock)
#
# main()