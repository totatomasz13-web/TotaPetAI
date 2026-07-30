# TotaPetAI

TotaPetAI to windowsowy pupil na pulpit z osobowością opartą na sztucznej
inteligencji. Działa jako mały, stale widoczny towarzysz zamiast tradycyjnego
okna aplikacji. Całość jest napisana w Pythonie.

## Planowane funkcje

- Przesuwanie pupila w wybrane miejsce na ekranie
- Zapamiętywanie pozycji między uruchomieniami aplikacji
- Proste animacje i reakcje
- Rozmowy oraz osobowość wspierane przez API LLM
- Lekka aplikacja przeznaczona dla systemu Windows
- Polski interfejs i komunikaty
- Obsługa bota Telegram przez long polling
- Agent z pamięcią rozmowy i lokalnymi komendami
- Osobna aplikacja do konfiguracji wszystkich ustawień

TotaPetAI jest towarzyszem na pulpit i nie zastępuje profesjonalnej porady
weterynaryjnej.

## Status

Pierwsza wersja aplikacji Python/Tkinter jest gotowa. Pupil może być przeciągany
po ekranie, a jego pozycja jest zapisywana lokalnie.

## Uruchomienie

Wymagany jest Python 3.10 lub nowszy dla systemu Windows. Projekt korzysta
wyłącznie ze standardowej biblioteki Pythona.

```powershell
python main.py
```

Przeciągaj pupila lewym przyciskiem myszy. Menu kontekstowe otwiera się prawym
przyciskiem i pozwala otworzyć ustawienia, przywrócić pozycję domyślną albo
zamknąć aplikację.

## Ustawienia

Uruchom aplikację konfiguracji poleceniem:

```powershell
python main.py --ustawienia
```

W ustawieniach można podać adres API LLM, model, klucz API, token Telegrama,
dozwolony identyfikator użytkownika oraz instrukcję systemową agenta. Domyślnie
obsługiwany jest format zgodny z API OpenAI, ale można wskazać dowolny zgodny
endpoint.

Jeżeli ustawisz `TELEGRAM_ALLOWED_USER`, bot odpowie wyłącznie temu
identyfikatorowi. Bez tej wartości odpowie każdemu użytkownikowi, który napisze
do bota, dlatego zalecane jest jej ustawienie.

## Licencja

Projekt jest dostępny na licencji MIT. Szczegóły znajdują się w pliku
[LICENSE](LICENSE).
