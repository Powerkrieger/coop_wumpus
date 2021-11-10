WumpusVision v1.0 - 29.10.2021

Die Idee ist, dass "train.py" eine Liste von Vektoren als .txt ausgibt,
die dann von diesem Tool gelesen wird, um den Spielverlauf anzuzeigen.

Das Programm liest dafür die "board-Vektoren" aus der senf.txt (sollten wir noch
umbenennen :D) und baut daraus im GUI das Feld zusammen. Wie diese Datei strukturiert
sein muss, lässt sich aus "HowToStructTheSenf.txt" entnehmen. Ein kleines Beispiel ist
bereits in der enthaltenen senf.txt vorhanden.

Die Vektoren sind eine wie folgt strukturierte Liste (Zeilentrennung nur zur Übersicht!):

BoardGrößeX, BoardGrößeY, 
AgentPosX, AgentPosY, AngentBlickrichtung (0=UP, 1=RIGHT, 2=DOWN, 3 = LEFT),
WumpusX,WumpusY, WumpusStatus (1=Alive, 0=Dead),
GoldX, GoldY, AHasGold (0=No, 1=Yes),
NumberOfPits, P1_X, P1_Y, ..., Pn_X,Pn_Y


Was jetzt noch fehlt, ist die Funktion in "train.py", um die "senf.txt" zu schreiben.