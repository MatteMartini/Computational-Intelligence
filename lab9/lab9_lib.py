# Copyright © 2023 Giovanni Squillero <giovanni.squillero@polito.it>
# https://github.com/squillero/computational-intelligence
# Free for personal or classroom use; see 'LICENSE.md' for details.

from abc import abstractmethod


class AbstractProblem:
    def __init__(self):
        self._calls = 0 #inizializza il contatore delle chiamate

    @property
    @abstractmethod
    def x(self): #proprietà astratta x che deve essere implementata dalle sottoclassi.
        pass

    @property
    def calls(self):
        return self._calls #ritorna il valore definito con la init, cioe il numero di chiamate della fitness

    @staticmethod
    def onemax(genome):  #calcola la somma degli 1 presenti nel vettore genome (ovvero le bit string in analisi)
        return sum(bool(g) for g in genome)

#La funzione __call__ è un metodo speciale in Python che viene chiamato quando un'istanza di una classe viene invocata come una funzione (come fatto nell'altro file, e li si passa ind(la bit string) che qui diventa il genome
    def __call__(self, genome): #è la funzione di fitness. calcola la fitness per diverse suddivisioni del genoma, penalizza le soluzioni meno performanti e restituisce un valore normalizzato.
        self._calls += 1 #Incrementa il contatore delle chiamate
        #Calcola la fitness della soluzione genome. Per fare ciò, suddivide il genoma in diverse parti (con una dimensione specificata da self.x) e calcola la fitness per ogni parte utilizzando la funzione onemax, che conta il numero di bit a 1 nella parte del genoma e li ordina dal migliore al peggiore.
        fitnesses = sorted((AbstractProblem.onemax(genome[s :: self.x]) for s in range(self.x)), reverse=True) 
#nel caso in cui la dim del problema è 1, calcolerà una sola fitnesses, sara un vettore di un elemento

        #Ordina le fitness calcolate in ordine decrescente e le utilizza per calcolare il valore finale di fitness. In particolare, somma le fitness delle parti che sono uguali alla fitness massima, sottrae una penalità per le fitness inferiori alla massima.
        #con la prima sum si trova il valore della fitness maggiore (se ci sono più di una con quella fitness top le somma!) -> piu ne trovi uguali meglio è!
        #con la seconda sum si somma tutte le penitenze, che sono trovate come descritte nelle successive 2 righe
        #k è la k-esima fitness della lista di fitnesses escluse la/e top, e più la fitness in analisi è scarsa piu è in basso nella lista (e quindi piu l'indice k è grande)
        val = sum(f for f in fitnesses if f == fitnesses[0]) - sum(
            f * (0.1 ** (k + 1)) for k, f in enumerate(f for f in fitnesses if f < fitnesses[0])
        )
        return val / len(genome) #Normalizza il valore di fitness dividendo per la lunghezza totale del genoma. Restituisce il valore normalizzato di fitness.


def make_problem(a): #La funzione make_problem restituisce una sottoclasse di AbstractProblem chiamata Problem con la dimensione a specificata (passata come parametro), e implementa il metodo astratto da completare mettendoci la dimensione del problema, che è il valore passatogli come parametro!.
    class Problem(AbstractProblem):
        @property
        @abstractmethod
        def x(self):
            return a

    return Problem()
