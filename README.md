
Gebruik:
In Algorithms.py kun je verschillende heuristieken vinden oplossingen voor de case te vinden. Individuele heuristieken gebruiken verschillende combinaties van algorithms om de huizen te verdelen in de batterijen en om kabels aan te leggen om deze aan te sluiten. De verschillende oplossingen voor onze case worden aangeslagen in main.py

Structuur:

Het Optimum prime project heeft sorten mappen: algorithms en classes. The algorithms map heeft een verzameling van alle algoritmes die wij toepassen op het project. De classes organiseert de data types die wij gebruiken. Hieronder een korte beschrijving van de content van elke file:

algorithms/cable_algorithm.py:
Cable:
- Neemt configuration class in
- cable_listbatteries: loopt door een lijst met batterijen heen en roept connect_batty_houses. - Input - lijst met batterijen en booling (True kabels delen, False niet kables delen)
- connect_battery_houses: roept het juste algoritme opbasis van de kabels delen constraint. - Input - 1 batterij en booling (True kabels delen, False niet kables delen)
- connect_points_Astar: sluit twee punten met elkaar met het begruik van een kabel - Input - een start punt en een eind punt (objecten met position_x en position_y) -- Output - een type Cable_line() gevult met een lijst aan Cable_instance()'s.
- calculate_distance: Rekent de afstand uit tussen twee punten - Input - een start punt en een eind punt (objecten met position_x en position_y) -- Output - een int met de directe afstand.
- connecting_cables: Neemt het eerste huis in de lijst en kijkt welke huizen er in een aangegeven radius om dat huis heen zijn. Rekent het midden punt uit van deze groep huizen en legt dan een kabel van dat punt naar de batterij en vervogens legt hij een kabel van alle huizen naar dat punt en sluit deze kabels aan de gedeelde kabel naar de batterij. - Input - een lijst met huizen, een batterij, en de radius -- Output - Een lijst met alle nieuwe kabels van type Cable_line() gevult met een lijst aan Cable_instance()'s.

greedy_algorithm.py
Greedy()::
- Neemt een 



De hierop volgende lijst beschrijft de belangrijkste mappen en files in het project, en waar je ze kan vinden:

/assignment1: bevat alle code van dit project
/assignment1/algorithms: verzameling van de code voor algoritmes
/assignment1/classes: verzameling van de vier benodigde classes voor deze case en de informatie voor de kaarten

