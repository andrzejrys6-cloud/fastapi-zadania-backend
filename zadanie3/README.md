# Blog API

API dla prostego bloga z postami i komentarzami. Dane zapisywane są w pliku `blog.db` (SQLite) — nie znikają po restarcie.

---

## Jak uruchomić

```powershell
cd zadanie3
py -m uvicorn main:app --reload
```

Następnie otwórz: **http://127.0.0.1:8000/docs**

---

## Endpointy — Posty

### Pobierz wszystkie posty
```
GET /posts
```

---

### Dodaj nowy post
```
POST /posts
```
```json
{
  "title": "Mój pierwszy post",
  "content": "Treść posta...",
  "author": "Jan"
}
```

---

### Pobierz post wraz z komentarzami
```
GET /posts/{id}
```
Zwraca post i wszystkie jego komentarze w jednej odpowiedzi.

---

### Zaktualizuj post
```
PUT /posts/{id}
```
Wysyłasz te same pola co przy tworzeniu.

---

### Usuń post
```
DELETE /posts/{id}
```

---

## Endpointy — Komentarze

### Dodaj komentarz do posta
```
POST /posts/{id}/comments
```
```json
{
  "content": "Świetny post!",
  "author": "Anna"
}
```
Jeśli post o podanym ID nie istnieje, zwraca błąd 404.

---

### Pobierz komentarze posta
```
GET /posts/{id}/comments
```

---

## Baza danych

Plik `blog.db` tworzony jest automatycznie przy pierwszym uruchomieniu w folderze `zadanie3/`. Możesz go otworzyć programem [DB Browser for SQLite](https://sqlitebrowser.org/) żeby podejrzeć dane.
