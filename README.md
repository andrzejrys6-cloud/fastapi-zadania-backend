# Zadania FastAPI

Pięć zadań z FastAPI od podstaw do zaawansowanych.

---

## Wymagania

- Python 3.10 lub nowszy — pobierz z https://python.org/downloads  
  Podczas instalacji zaznacz **"Add Python to PATH"**

---

## Instalacja (tylko raz)

Otwórz terminal w folderze `fastapi_zadania/` i wpisz:

```powershell
py -m pip install -r requirements.txt
```

Poczekaj aż wszystko się pobierze i zainstaluje.

---

## Uruchamianie zadań

Każde zadanie uruchamiasz osobno. Wejdź do jego folderu i wpisz:

```powershell
cd zadanie1
py -m uvicorn main:app --reload
```

Powinieneś zobaczyć:
```
INFO: Uvicorn running on http://127.0.0.1:8000
```

Następnie otwórz w przeglądarce: **http://127.0.0.1:8000/docs**

Tam znajdziesz interaktywną dokumentację — możesz klikać każdy endpoint i testować go bez żadnych dodatkowych narzędzi.

Zatrzymanie serwera: **CTRL+C**

---

## Opis zadań

| Folder     | Zadanie                                      | Poziom              |
|------------|----------------------------------------------|---------------------|
| zadanie1/  | Hello World — 3 podstawowe endpointy         | Podstawowy          |
| zadanie2/  | Todo List — CRUD, walidacja, bez bazy danych | Podstawowy          |
| zadanie3/  | Blog — posty i komentarze, baza SQLite       | Średni              |
| zadanie4/  | Todo z kontami — rejestracja i logowanie JWT | Średni/Zaawansowany |
| zadanie5/  | Katalog produktów — filtry, sortowanie, paginacja | Zaawansowany   |

Każdy folder ma swój własny README z dokładnym opisem jak używać danego zadania.

---

## Uwaga do zadania 3

Zadanie 3 używa Alembic do migracji bazy danych. Przed pierwszym uruchomieniem serwera wykonaj w folderze `zadanie3/`:

```powershell
py -m alembic revision --autogenerate -m "pierwsze tabele"
py -m alembic upgrade head
```

Dopiero potem uruchom serwer normalnie.
