-Działający interpreter z możliwością wykonania kodu
-Obsługa zmiennych
-Obsługa operatorów
-Obsługa instrukcji warunkowej
-Obsługa pętli
-Obsługa komentarzy
-Obsługa dodatkowych instrukcji
-Obsługa błędów 

----------------------------------------------------
Uruchomienie programu:

PowerShell script

	.\run.ps1 program.txt

Git Bash

	winpty python interpreter.py program.txt

----------------------------------------------------

Deklaracja zmiennych 

	zmienna x;

Obsługa instrukcji warunkowej

	jezeli (x > y) wtedy {
    wypisz "dziala jezeli";
	}
	inaczej {
		wypisz "dziala inaczej";
	};

Obsługa pętli

	dopoki (abc <= 5) wykonuj {
    wypisz "abc = " + abc;
    abc = abc + 1;
	};

Obsługa komentarzy

	##to komentarz jednoliniowy

	/# 
	to komentarz
	wieloliniowy
	#/

Obsługa dodatkowych instrukcji

	wypisz num;
