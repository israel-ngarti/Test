# ==============================================================================
"""SUDOKU : algorithm able to solve basic sudoku grid"""
# ==============================================================================
__author__  = "Charpentier Corentin, Fergach Aya"
__version__ = "1.0" # skeleton version
__date__    = "2023-11-17"
# ==============================================================================
import tools
ma_liste = tools.Reader('data/evil_00.txt').lines
print(f"{ma_liste = }") # pour afficher le contenu de ma_liste



class Cell:
    """ Identifie le numero de la case (ligne, colonne) et sa valeur.
        Cell permet de stocker ses informations """

    def __init__(self, id: int, value: int):
        """ initialise les attribut qu'on utilisera pour résoudre le sudoku """      
        self.idnum = id
        self.value = value or 0
        self.domain = set(range(1, 10))
        self.locked = False if value == 0 else True

    def line(self) -> int:
        """ line reçoit un entier entre {0,80}
            line renvoit un entier entre {0,8}
            axiome : line(idnum) == idnum//9"""
        return self.idnum // 9

    
    def column(self) -> int:
        """ column reçoit un entier entre {0,80}
            column renvoit un entier entre {0,9}
            axiome : column(idnum) == idnum%9 """
        return self.idnum % 9

    def square(self) -> int:
        """ square reçoit un entier entre {0,80}
            square renvoit un entier entre {0,8}
            axiome : square(idnum) == line(self.idnum)//3)*3 + (column(self.idnum)//3 """
        return (self.line() // 3) * 3 + (self.column() // 3)


    def remove_value(self, value: int) -> bool:
        """ Reçoit un entier entre {0,8}
            Renvoi un booléen : True si la valeur a été supprimé du domaine
            False si le domaine n'a pas été modifié """
        if value in self.domain and not self.locked:
            self.domain.remove(value)
            return True
        return False

    def update_value(self) -> bool:
        """ Fonction sans paramètre qui renvoie un booléen.
            Si la case n'est pas bloquée et que le domaine est de taille 1,
            met à jour les attributs value et locked et renvoie True.
            Renvoie False sinon """
        if not self.locked and len(self.domain) == 1:
            self.value = self.domain.pop()
            self.locked = True
            return True
        return False

    def update_domain(self, value: list) -> bool:
        """ Reçoit une liste de valeur de 1 à 9
            Renvoie True si le domaine est modifié, False sinon.
            Si le domaine n'est pas verouillé , il est mis à jour en conservant
            uniquement les valeurs présentes à la fois dans le domaine actuel et
            dans la liste de valeurs """
        if self.locked:
            return False
        updated_domain = self.domain.intersection(value)
        if updated_domain != self.domain:
            self.domain = updated_domain
            return True
        return False

    def reduce_domain(self, value: list) -> bool:
        """ Reçoit une liste de valeurs entre {1,9}
            Renvoie un booléen : True or False
            Si la case est verouillé, le domaine est mis à jour avec la
            différence du domaine et de la lkste. Renvoie True si le
            domaine est modifié, False sinon """
        if self.locked:
            return False
        updated_domain = self.domain.difference(value)
        if updated_domain != self.domain:
            self.domain = updated_domain
            return True
        return False


class Sudoku:
    """La classe Sudoku va tenter de résoudre une grille de sudoku"""

    def __init__(self):
        """ initialise les attribut qu'on utilisera pour résoudre le sudoku """  
        self.internal_grid = []

    def reset(self, initial_values=None):
        """ reset ne reçoit rien
            reset ne renvoie rien
            axiome : reset créer une grille avec une liste en mettant à jour les attributs
            des cases """
        self.internal_grid = [Cell(i, 0) for i in range(81)]

    def __str__(self)->list:
        """ __str__ ne reçoit rien
            __str__ renvoie une liste 
            axiome : __str__ va afficher la chaîne de caractère internal_grid sous forme
            de grille de sudoku avec des " = " pour les lignes et des " | " pour
            les colonnes. Si la cellule est vérouillée (self.locked == True),
            sa valeur s'affichera. Sinon un point sera affiché """
        grid_str = "=" * 28 + "\n"
        for i, cell in enumerate(self.internal_grid):
            if i % 9 == 0:
                grid_str += "\n"
                if i % 27 == 0:
                    grid_str += "=" * 28 + "\n"
            if cell.locked:
                grid_str += f" {cell.value} "
            else:
                grid_str += " . "
            if (i + 1) % 3 == 0 and i % 9 != 8:
                grid_str += "|"
        grid_str += "\n" + "=" * 28
        return grid_str

    def line(self, row_index:int)->list:
        """ line reçoit un nombre entre 0 et 8
            line renvoie une liste de 9 valeurs entre 0 et 80
            axiome : line va recevoir un indice de ligne, va parcourir la grille et renvoyer
            une liste de toutes les valeurs présentes sur la ligne donnée """
        return [cell for cell in self.internal_grid if cell.line() == row_index]

    def column(self, col_index:int)->list:
        """ column reçoit un nombre entre 0 et 8
            column renvoie une liste de 9 valeurs entre 0 et 80
            axiome : column va recevoir un indice de ligne, va parcourir la grille et renvoyer
            une liste de toutes les valeurs présentes sur la colonne donnée """
        return [cell for cell in self.internal_grid if cell.column() == col_index]

    def square(self, square_index:int)->list:
        """ column reçoit un nombre entre 0 et 8
            column renvoie une liste de 9 valeurs entre 0 et 80
            axiome : column va recevoir un indice de carré, va parcourir la grille et renvoyer
            une liste de toutes les valeurs présentes dans le carré donné """
        return [cell for cell in self.internal_grid if cell.square() == square_index]

    def neighbors(self, cell:int)->list:
        """ neighbors reçoit un nombre entre 0 et 80
            neighbors renvoie une liste de valeurs entre 0 et 80
            axiome : neighbors va recevoir une case, va parcourir la grille et renvoyer une liste de
            toutes les valeurs présentes sur la colonne, la ligne ou dans le carré
            associé """
        return [other_cell for other_cell in self.internal_grid
                if (other_cell != cell and
                    (other_cell.line() == cell.line() or
                     other_cell.column() == cell.column() or
                     other_cell.square() == cell.square()))]

    def propagate(self, blocked_cell:int)->list:
        """ propagate reçoit un nombre entre 0 et 80
            propagate renvoie une liste de valeurs entre 0 et 80
            axiome : propagate va recevoir une case bloquée, va parcourir la grille et renvoyer une liste de
            toutes les cases non bloquées ayant un domaine avec qu'une seule valeur. Met à jour le
            domaine des cases de la même ligne, colonne ou carré de la case reçue, en enlevant la
            valeur de celle-ci """
        updated_cells = set()

        # Collect neighbors from the same row
        row_neighbors = self.line(blocked_cell.line())
        for cell in row_neighbors:
            if not cell.locked and blocked_cell.value in cell.domain:
                cell.remove_value(blocked_cell.value)
                updated_cells.add(cell)

        # Collect neighbors from the same column
        column_neighbors = self.column(blocked_cell.column())
        for cell in column_neighbors:
            if not cell.locked and blocked_cell.value in cell.domain:
                cell.remove_value(blocked_cell.value)
                updated_cells.add(cell)

        # Collect neighbors from the same square
        square_neighbors = self.square(blocked_cell.square())
        for cell in square_neighbors:
            if not cell.locked and blocked_cell.value in cell.domain:
                cell.remove_value(blocked_cell.value)
                updated_cells.add(cell)

        return updated_cells

    def set_values(self, cells_set:list)->bool:
        """ set_values reçoit une liste
            set_values renvoie un booléen
            axiome : set_values va recevoir un ensemble de case. Pour chaque case, va appliquer la méthode
            update_value et applique la méthode propagate au résultat. Si il y a eu une mise à jour
            par la méthode update_value, set_values renvoie True. False sinon """
        updated = False

        while cells_set:
            cell = cells_set.pop()
            if cell.update_value():
                updated = True
                updated_cells = self.propagate(cell)
                cells_set.update(updated_cells)

        return updated

    def grid_parser(self, initial_values:list):
        """ grid_parser reçoit une liste
            grid_parser ne renvoie rien
            axiome : grid_parser va recevoir toute les cases de la grille. Elle vérifie que le format des cases est bon.
            La méthode va changer l'état bloqué des cases, ce qui va changer le domaine des cases sur la même ligne,
            colonne et carré """
        self.reset()
        todo = set()

        if len(initial_values) == 81 and all(isinstance(value, int) and 0 <= value <= 9 for value in initial_values):
            for i, value in enumerate(initial_values):
                cell = self.internal_grid[i]
                if value > 0:
                    cell.value = value
                    cell.locked = True
                    cell.domain = {value}
                    todo.add(cell)

        elif len(initial_values) == 9 and all(len(row) == 9 and all(isinstance(value, int) and 0 <= value <= 9 for value in row) for row in initial_values):
            for row_index, row in enumerate(initial_values):
                for col_index, value in enumerate(row):
                    cell = self.internal_grid[row_index * 9 + col_index]
                    if value > 0:
                        cell.value = value
                        cell.locked = True
                        cell.domain = {value}
                        todo.add(cell)

        else:
            raise ValueError("Invalid input format.")

        new_todo = set()

        for cell in todo:
            cell.locked = True
            cell.domain = {cell.value}
            new_todo.update(self.propagate(cell))

        todo.update(new_todo)
        self.set_values(todo)

    def find_unique(self, linked_cells:list)->bool:
        """ find_unique reçoit une liste
            find_unique renvoie un booléen
            axiome : find_unique va recevoir un ensemble de cases liées, va vérifier leur domaine et si un des domaine a une valeur
            qui n'apparaît pas dans les autres domaines, vérouille cette case avec la valeur unique et met à jour les autres
            domaines. Renvoye True si il y a des modifications. Flase sinon"""
        dico_val = {v: [] for v in range(1, 10)}
        todo = set()
        rep = False

        for case in linked_cells:
            if case.locked:
                continue
            for v in case.domain:
                dico_val[v].append(case)

        for k, l in dico_val.items():
            if len(l) == 1:
                rep = True
                unique_case = l[0]
                unique_case.value = k
                unique_case.locked = True
                unique_case.domain = {k}
                todo.add(unique_case)
                todo.update(self.propagate(unique_case))

        return self.set_values(todo) or rep

    def find_pairs(self, linked_cells:list)->bool:
        """ find_pairs reçoit une liste
            find_pairs renvoie un booléen
            axiome : find_pairs va recevoir un ensemble de cases liées, va vérifier leur domaine et si deux des domaines ont deux
            valeurs identiques, modifie le domaine des autres cases. Renvoie True si il y a des modifications. False sinon"""
        dico_paires = {}
        success = False

        for case in linked_cells:
            if len(case.domain) != 2:
                continue
            clef = tuple(sorted(case.domain))
            if clef in dico_paires:
                dico_paires[clef].append(case)
            else:
                dico_paires[clef] = [case]

        for k, v in dico_paires.items():
            if len(v) == 2:
                for case in linked_cells:
                    if case not in v:
                        if case.reduce_domain(k):
                            success = True

        return self.set_values(set(linked_cells)) or success

    def solve(self, lvl=1)->list:
        """ solve reçoit un nombre (1 ou 2)
            solve renvoie une liste
            axiome : solve prend comme paramètre 1 ou 2. Si son paramètre est 1, solve utilise la méthode find_unique pour résoudre
            la grille. Si son paramètre est 2, solve utilise la méthode find_pairs. Renvoie la grille quand elle est résolue
            ou s'arrête quand aucun changement n'a eu lieu """
        cpt = 0

        while cpt < 81:
            modified = False

            for i in range(9):
                if lvl == 1:
                    modified_line = self.find_unique(self.line(i))
                    modified_column = self.find_unique(self.column(i))
                    modified_square = self.find_unique(self.square(i))
                elif lvl == 2:
                    modified_line = self.find_unique(self.line(i)) or self.find_pairs(self.line(i))
                    modified_column = self.find_unique(self.column(i)) or self.find_pairs(self.column(i))
                    modified_square = self.find_unique(self.square(i)) or self.find_pairs(self.square(i))

              # Utiliser any pour vérifier s'il y a eu une modification
                modified = any([modified, modified_line, modified_column, modified_square])

            if not modified:
                break

            cpt += 1

      
            return all(cell.locked for cell in self.internal_grid)

#-------------------------------------------------------------------------------------

sudoku = Sudoku()
initial_grid = ma_liste
sudoku.grid_parser(initial_grid)

print( "La grille après chargement:")
print(sudoku)

for lvl in [1, 2]:
    print(f"\nSolving with level {lvl}:")
    if sudoku.solve(lvl):
        print("Solved Sudoku:")
        print(sudoku)
        print("Sudoku is solved:", sudoku.solve())
    else:
        print("No solution found.")
        print(sudoku)
        print("Sudoku is solved:", sudoku.solve())

#-------------------------------------------------------------------------------------
#testcode        
from ezCLI import testcode

code_a_tester = """
a = Cell(56,3)
a.line()
a.column()
a.square()
a.remove_value(7)
a.update_value()
a.update_domain((4,7,8))
a.reduce_domain((2,3,1))
b = a
b = Sudoku()
b.line(3)
b.column(4)
b.square(6)
b.neighbors(5)
b.propagate(4)
b.set_values(54)
b.grid_parser(4)
b.find_unique(6)
b.find_pairs(4)
b.solve(1)
""" ; testcode(code_a_tester)

#testpour line : 
         #for i in range (81)
             #if line(n)!= n//9 : print("Erreur for" i) # test pour line

#test pour column: 
        #for i in range (81)
             #if column(n)!= n%9 : print("Erreur for" i)

#test square : 
        #square = """
#square(0) == 0
#square(1) == 1
#square(81) == 9

#testcode(square)

# test pour remove_value :
            #self.locked = False
            # self.domain ={1,2,3}
            #self.value = 2
            #result = remove_value(self.value)
            #assert rsult == True
            #aassert self.domain == {1,3}
            #test_remove_value ()

#test pour update_value :
        #value = 0
        #domain = {3}
        #locked = False 
        #result, value, locked = update_value_test_case(value, domain, locked)
        #if result :
            #print(f"Mise à jour effectuée. Nouvelle valeur : {value}, Case verouillée : {locked})
        #else:
            #print("Mise à jour non effectuée. La condition n'est pas remplie.")


#test pour update_domain :
        #self.locked = False
        #self.domain = {1,2,3,4,5,}
        #list_value = [2,4,6,8]
        #result = update_domain (list_value)
        #assert result = True
        #assert update_domain == {2,4}
        #test_update_domain()

#test pour reduce_domain :
        #list_value = [2,4,6,8]
        # self.locked = True
        #result = update_domain(list_value)
        #assert result == False, "la fonction devrait renvoyer False si la case


