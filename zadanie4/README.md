# Todo API z autoryzacją JWT

Todo List z systemem kont użytkowników. Każdy użytkownik widzi tylko swoje zadania. Dane zapisywane w pliku `auth_todo.db`.

---

## Jak uruchomić

```powershell
cd zadanie4
py -m uvicorn main:app --reload
```

Następnie otwórz: **http://127.0.0.1:8000/docs**

---

## Kolejność użycia

Żeby korzystać z API musisz najpierw założyć konto, zalogować się i dopiero wtedy możesz dodawać zadania.

### Krok 1 — Zarejestruj konto
```
POST /auth/register
```
```json
{
  "username": "jan",
  "email": "jan@example.com",
  "password": "mojehaslo123"
}
```

---

### Krok 2 — Zaloguj się
```
POST /auth/login
```
W Swaggerze (`/docs`) kliknij ten endpoint, a następnie wpisz `username` i `password` w formularz (nie JSON).

W odpowiedzi dostaniesz token:
```json
{
  "access_token": "eyJhbGci...",
  "token_type": "bearer"
}
```

---

### Krok 3 — Podaj token w Swaggerze

W Swaggerze (`/docs`) kliknij przycisk **Authorize** (kłódka, górny prawy róg), wklej token i kliknij Authorize. Od tej chwili wszystkie zapytania będą wysyłane z Twoim tokenem.

---

### Krok 4 — Używaj endpointów TODO

### Pobierz swoje zadania
```
GET /todos
```
Zwraca tylko zadania zalogowanego użytkownika.

---

### Dodaj zadanie
```
POST /todos
```
```json
{
  "title": "Zrobić zakupy",
  "completed": false
}
```

---

## Uwaga

Token jest ważny przez **30 minut**. Po tym czasie musisz zalogować się ponownie i wkleić nowy token w Swaggerze.
