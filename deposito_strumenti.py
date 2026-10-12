import csv
from operator import attrgetter   #poichè si chiede di ordinare la lista: uso attregetter
                                  #per specificare l'attributo da usare nell'ordinamento

class Strumento:
    def __init__(self, id_strumento, tipo, marca, anno_acquisto, valore):
        self.id_strumento=id_strumento
        self.tipo=tipo
        self.marca=marca
        self.anno_acquisto=int(anno_acquisto)
        self.valore=float(valore)

    def __str__(self):
        return f"{self.id_strumento}, {self.tipo}, {self.marca}, {self.anno_acquisto}, {self.valore}"

class Prestito:
    def __init__(self, id_prestito, data, id_strumento, cognome_allievo):
        self.id_prestito=id_prestito
        self.data=data
        self.id_strumento=id_strumento
        self.cognome_allievo=cognome_allievo

    def __str__(self):
        return f"{self.id_prestito} {self.data} {self.id_strumento} {self.cognome_allievo}"

class DepositoStrumenti:
    def __init__(self, nome, responsabile):
        """Inizializza gli attributi e le strutture dati"""
        self.nome=nome
        self.responsabile=responsabile
        self.strumenti={}                              # Dizionario: ID strumento -> Oggetto Strumento
        self.prestiti={}                               # Dizionario: ID prestito -> Oggetto Prestito
        self.strumenti_in_prestito=set()               # Insieme degli ID strumenti attualmente impegnati

    def carica_file_strumenti(self, file_path):
        """Carica gli strumenti dal file"""
        try:
            with open (file_path, "r", encoding="utf-8") as f:
                reader=csv.reader(f)
                for riga in reader:
                    if not riga:
                        continue
                    id_strumento = riga[0].strip()
                    tipo = riga[1].strip()
                    marca = riga[2].strip()
                    anno_acquisto = int(riga[3].strip())
                    valore = float(riga[4].strip())

                    #creo l'oggetto e lo memorizzo nel dizionario
                    strumento=Strumento(id_strumento, tipo, marca, anno_acquisto,valore)
                    self.strumenti[id_strumento]=strumento
        except FileNotFoundError:
            raise FileNotFoundError("Errore: Il file specificato non è stato trovato.")

    def aggiungi_strumento(self, tipo, marca, anno_acquisto, valore):
        """Aggiunge uno strumento nel deposito: aggiunge solo nel sistema e non aggiorna il file"""
        # Calcola il numero successivo basandosi sugli ID esistenti che iniziano con 'S'
        if self.strumenti:
            # Calcola il numero successivo basandosi sugli ID esistenti che iniziano con 'S'
            numeri = [int(k[1:]) for k in self.strumenti.keys() if k.startswith('S') and k[1:].isdigit()]
            next_num = max(numeri) + 1 if numeri else len(self.strumenti) + 1
        else:
            next_num = 1

        id_strumento = f"S{next_num}"
        strumento = Strumento(id_strumento, tipo, marca, anno_acquisto, valore)
        self.strumenti[id_strumento] = strumento
        return strumento

    def strumenti_ordinati_per_marca(self):
        """Ordina gli strumenti per marca in ordine alfabetico"""
        return sorted(self.strumenti.values(), key=attrgetter('marca'))

    def nuovo_prestito(self, data, id_strumento, cognome_allievo):
        """Crea un nuovo prestito"""
        if id_strumento not in self.strumenti:
            raise Exception("Errore: Lo strumento richiesto non esiste nel sistema.")
        if id_strumento in self.strumenti_in_prestito:
            raise Exception("Errore: Lo strumento è attualmente già in prestito.")

        # Genera un ID progressivo per il prestito (es. P1, P2...)
        numeri = [int(k[1:]) for k in self.prestiti.keys() if k.startswith('P') and k[1:].isdigit()]
        next_num = max(numeri) + 1 if numeri else 1
        id_prestito = f"P{next_num}"

        prestito = Prestito(id_prestito, data, id_strumento, cognome_allievo)
        self.prestiti[id_prestito] = prestito
        self.strumenti_in_prestito.add(id_strumento)
        return prestito

    def termina_prestito(self, id_prestito):
        """Termina un prestito in atto rimuovendolo dal sistema"""
        if id_prestito not in self.prestiti:
            raise Exception("Errore: Il codice prestito inserito non esiste.")

        prestito = self.prestiti[id_prestito]
        self.strumenti_in_prestito.remove(prestito.id_strumento)
        del self.prestiti[id_prestito]
