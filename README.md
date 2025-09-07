# AI Energy Automation
<img width="915" height="394" alt="l1" src="https://github.com/user-attachments/assets/e90476ef-bfaf-4dae-9640-24e21ddad3a3" />
<img width="946" height="395" alt="l2" src="https://github.com/user-attachments/assets/7eff5ec2-9917-4314-9437-1658180c6795" />
<img width="949" height="400" alt="l3" src="https://github.com/user-attachments/assets/05d03f27-da52-4fef-a0c9-ff9d03736295" />
<img width="890" height="384" alt="l4" src="https://github.com/user-attachments/assets/3377ec7a-de38-49a4-95d0-b11bb3b2b08c" />
<img width="920" height="344" alt="l5" src="https://github.com/user-attachments/assets/cb1a9601-a5fc-4804-87cf-b530abadc9ba" />
<img width="949" height="385" alt="l7" src="https://github.com/user-attachments/assets/769ed06b-4619-4eb0-b93c-1eca06017af6" />
<img width="752" height="379" alt="l8" src="https://github.com/user-attachments/assets/9a9b2d13-f7b6-4c45-a2ba-009e970a34d3" />
<img width="754" height="377" alt="l9" src="https://github.com/user-attachments/assets/7728b403-6db5-487c-906d-97c311a78da9" />
<img width="709" height="339" alt="l11" src="https://github.com/user-attachments/assets/f7fd6697-a375-4653-bba2-31fde78f307b" />

AI Energy Automation to aplikacja realizująca automatyzację zarządzania energią przy użyciu sztucznej inteligencji. Projekt wykorzystuje LLM do podejmowania decyzji oraz mechanizm RAG (Retrieval-Augmented Generation) do interaktywnego czatu i analizowania danych, umożliwiając inteligentne sterowanie energią w różnych scenariuszach.

## Funkcjonalności

- Automatyczne podejmowanie decyzji energetycznych na podstawie danych wejściowych.
- Interaktywny czat z wykorzystaniem AI (RAG + LLM).
- Integracja z zewnętrznymi API do sterowania urządzeniami lub systemami.
- Możliwość rozbudowy o dodatkowe źródła danych i funkcje AI.

## Wymagania

Projekt wymaga Pythona 3.10 lub nowszego oraz następujących bibliotek:

- `fastapi`
- `uvicorn`
- `python-jose`
- `requests`
- `python-dotenv`
- `google-generativeai`
- `httpx`
- `streamlit`

## Instalacja

1. Sklonuj repozytorium:

```bash
git clone https://github.com/twoj_uzytkownik/ai-energy-automation.git
cd ai-energy-automation

    Stwórz i aktywuj wirtualne środowisko (opcjonalnie, zalecane):

python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

    Zainstaluj wymagania:

pip install -r requirements.txt

Konfiguracja

    Stwórz plik .env w katalogu głównym projektu i dodaj swoje klucze API oraz konfiguracje, np.:

GOOGLE_API_KEY=twoj_google_api_key
FASTAPI_URL=http://localhost:8000

    Dostosuj parametry w kodzie aplikacji według potrzeb.

#Uruchomienie

Aplikację uruchamiasz za pomocą Streamlit:

streamlit run app.py

Dla środowiska FastAPI (backend):

uvicorn main:app --reload

Użycie

    Otwórz aplikację Streamlit w przeglądarce.

    Wprowadź dane wejściowe lub komendy.

    AI podejmie decyzje energetyczne i może wysyłać zapytania do zintegrowanych API.

    Korzystaj z czatu RAG, aby analizować i interpretować dane w czasie rzeczywistym.

#Wkład

Wszelkie sugestie i pull requesty są mile widziane!
