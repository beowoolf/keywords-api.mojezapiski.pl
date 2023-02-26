import sys
import os

# dodanie katalogu zawierającego kod do listy ścieżek wyszukiwania modułów Pythona
sys.path.insert(0, os.path.dirname(__file__))

# zaimportowanie modułu z serwerem
from server import run

# uruchomienie serwera
application = run()
