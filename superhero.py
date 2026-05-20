"""
You want to build a base class for superheroes.

Superheroes have certain attributes, all have:

a superhero name
if they belong to a team.  If they don't belong to a team, that attribute is None
Superheroes have certain methods, all have:

a power
most have a catch phrase, for example "It's clobberin' time", "Shazam!" or "Hulk smash!"
1) Create a superhero base class with one extra attribute and one extra method (your choice)

2) Build a subclass that inherits from superhero but is more specific for example, energy projector or alien

3) Build a superhero object from the subclass you made.
"""

class Superhero:
   def __init__(self, name, team, power, catchphrase):
       self.name = name
       self.team = team
       self.power = power
       self.catchphrase = catchphrase
   def say_catchphrase(self):
       print(self.catchphrase)
     
class Hulk(Superhero):
   def __init__(self, name, team, power, catchphrase, color):
       super().__init__(name, team, power, catchphrase)
       self.color = color
    
class CaptainAmerica(Superhero):
   def __init__(self, name, team, power, catchphrase, shield):
       super().__init__(name, team, power, catchphrase)
       self.shield = shield

class Thor(Superhero):
  def __init__(self, name, team, power, catchphrase, hammer):
    super().__init__(name, team, power, catchphrase)
    self.hammer = hammer