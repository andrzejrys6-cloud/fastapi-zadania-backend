# Katalog Produktów API

API katalogu produktów z filtrowaniem, wyszukiwaniem, sortowaniem i paginacją. Dane zapisywane w pliku `produkty.db`.

---

## Jak uruchomić

```powershell
cd zadanie5
py -m uvicorn main:app --reload
```

Następnie otwórz: **http://127.0.0.1:8000/docs**

---

## Endpointy

### Dodaj produkt
```
POST /products
```
```json
{
  "name": "Laptop Dell XPS",
  "description": "Wydajny laptop do pracy",
  "price": 4999.99,
  "category": "elektronika",
  "available": true
}
```

---

### Pobierz produkty
```
GET /products
```

Bez żadnych parametrów zwraca pierwsze 10 produktów. Możesz dodać dowolne filtry:

| Parametr     | Opis                              | Przykład                  |
|--------------|-----------------------------------|---------------------------|
| `category`   | Filtruj po kategorii              | `?category=elektronika`   |
| `min_price`  | Minimalna cena                    | `?min_price=1000`         |
| `max_price`  | Maksymalna cena                   | `?max_price=5000`         |
| `available`  | Tylko dostępne (`true`/`false`)   | `?available=true`         |
| `search`     | Szukaj w nazwie i opisie          | `?search=laptop`          |
| `sort`       | Sortowanie (patrz niżej)          | `?sort=price_asc`         |
| `page`       | Numer strony (domyślnie 1)        | `?page=2`                 |
| `per_page`   | Wyników na stronie (domyślnie 10) | `?per_page=5`             |

### Opcje sortowania (`sort`)
- `price_asc` — cena rosnąco
- `price_desc` — cena malejąco
- `name_asc` — nazwa A→Z
- `name_desc` — nazwa Z→A

### Przykład z kilkoma filtrami naraz
```
GET /products?category=elektronika&min_price=1000&max_price=5000&sort=price_asc&page=1&per_page=5&search=laptop
```

### Przykładowa odpowiedź
```json
{
  "total": 3,
  "page": 1,
  "per_page": 5,
  "results": [...]
}
```
`total` — łączna liczba wyników (bez paginacji), przydatne żeby wiedzieć ile jest stron.
