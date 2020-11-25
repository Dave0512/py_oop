import os

def dateien_in_ordner(pfad,suffix='.zip'):
    """
    Listung von Dateien jeglichen Typs in beliebigem Ordner
    Input:
        Ordner
        Dateityp (Vorbelegt mit zip) "Alle Typen möglich"
    Output:
        Liste der Dateien des gewählten Typs in dem angegebenen Ordner
    """
    fil_lst = [fil for fil in os.listdir(pfad) if fil.endswith(suffix)]
    return fil_lst

