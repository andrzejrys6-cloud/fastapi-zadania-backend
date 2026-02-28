# Todo List API

API do zarządzania listą zadań (TODO). Dane przechowywane są w pamięci — znikają po restarcie serwera.

---

## Jak uruchomić

```powershell
cd zadanie2
py -m uvicorn main:app --reload
```

Następnie otwórz: **http://127.0.0.1:8000/docs**

---

## Endpointy

### Pobierz wszystkie zadania
```
GET /todos
```
Zwraca listę wszystkich zadań.

---

### Pobierz jedno zadanie
```
GET /todos/{id}
```
Przykład: `GET /todos/1` — zwraca zadanie o ID 1.  
Jeśli nie istnieje, zwraca błąd 404.

---

### Dodaj nowe zadanie
```
POST /todos
```
Wysyłasz JSON:
```json
{
  "title": "Kupić mleko",
  "description": "2 litry",
  "completed": false
}
```
- `title` — wymagane, od 1 do 200 znaków
- `description` — opcjonalne
- `completed` — opcjonalne, domyślnie `false`

Zwraca kod **201** i utworzone zadanie z nadanym ID.

---

### Zaktualizuj zadanie
```
PUT /todos/{id}
```
Wysyłasz te same pola co przy tworzeniu. Nadpisuje całe zadanie.

Przykład — oznacz zadanie jako wykonane:
```json
{
  "title": "Kupić mleko",
  "description": "2 litry",
  "completed": true
}
```

---

### Usuń zadanie
```
DELETE /todos/{id}
```
Usuwa zadanie o podanym ID. Zwraca kod **204** (brak treści odpowiedzi).

---

## Uwaga

Dane znikają po restarcie serwera — to celowe, bo to zadanie nie używa bazy danych.
