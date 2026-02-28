# Hello World API

Proste API z trzema endpointami. Służy do nauki podstaw FastAPI.

---

## Jak uruchomić

### 1. Zainstaluj wymagane paczki (tylko raz)

Otwórz terminal w głównym folderze projektu (tam gdzie jest `requirements.txt`) i wpisz:

```bash
pip install -r requirements.txt
```

### 2. Uruchom serwer

Wejdź do folderu `zadanie1/` i wpisz:

```bash
uvicorn main:app --reload
```

Powinieneś zobaczyć coś takiego:

```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

### 3. Zatrzymanie serwera

Wciśnij `CTRL + C` w terminalu.

---

## Jak używać API

### Opcja A — przez przeglądarkę (najłatwiej)

Otwórz: **http://127.0.0.1:8000/docs**

Zobaczysz interaktywną dokumentację — możesz klikać każdy endpoint i od razu go testować bez żadnych dodatkowych narzędzi.

### Opcja B — wpisując adresy w przeglądarce

| Adres                                  | Co robi                        | Przykładowy wynik                          |
|----------------------------------------|--------------------------------|--------------------------------------------|
| http://127.0.0.1:8000/                 | Zwraca "Hello World"           | `{"message": "Hello World"}`               |
| http://127.0.0.1:8000/hello/Anna       | Wita podaną osobę              | `{"message": "Hello Anna"}`                |
| http://127.0.0.1:8000/info             | Informacje o aplikacji         | `{"nazwa": "...", "wersja": "...", ...}`    |

Zamiast `Anna` możesz wpisać dowolne imię lub słowo.

---

## Struktura projektu

```
zadanie1/
└── main.py     ← cały kod aplikacji, tutaj są zdefiniowane endpointy
```
