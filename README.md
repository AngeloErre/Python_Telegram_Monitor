# Telegram Work Account Status Monitor

> **Purpose / Scopo:** a small Python + Telethon utility for logging `ONLINE` / `OFFLINE` updates of **Telegram work accounts that you own, control, or are authorized to administer**. It does not bypass Telegram privacy settings and only receives updates Telegram makes available to the authenticated account.

**Italiano:** [vai alla guida italiana](#italiano) · **English:** [jump to English guide](#english)

---

## Italiano

### 1. Cosa fa

Il programma resta collegato a Telegram tramite Telethon e registra nel file `telegram_accessi.csv` le variazioni `ONLINE` e `OFFLINE` degli ID configurati. Usalo esclusivamente per account propri, controllati o per i quali disponi di autorizzazione. Telegram richiede che ogni applicazione utilizzi un proprio `api_id`; l'uso dell'API è inoltre soggetto ai Termini API di Telegram.

### 2. Requisiti

- Python 3.9 o successivo consigliato
- Un account Telegram
- `API ID` e `API Hash` Telegram
- Gli ID Telegram degli account di lavoro da configurare
- macOS, Linux o Windows

### 3. Creare API ID e API Hash

![API Development Tools](docs/images/01-api-tools.png)

1. Apri **https://my.telegram.org**.
2. Accedi con il numero associato al tuo account Telegram.
3. Seleziona **API development tools**.

![Create application](docs/images/02-create-app.png)

4. Crea un'applicazione indicando almeno **App title** e **Short name**.
5. Telegram mostrerà `api_id` e `api_hash`.
6. **Non pubblicare l'API Hash.** Non inserirlo nel repository GitHub.

Documentazione ufficiale: https://core.telegram.org/api/obtaining_api_id

### 4. Installazione

```bash
unzip telegram-work-account-monitor.zip
cd telegram-work-account-monitor
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
```

Su Windows, per attivare l'ambiente virtuale:

```powershell
.venv\Scripts\activate
```

### 5. Configurazione

![Configure env](docs/images/03-env.png)

Crea il file locale `.env` partendo dall'esempio:

```bash
cp .env.example .env
```

Aprilo e configura:

```dotenv
TELEGRAM_API_ID=12345678
TELEGRAM_API_HASH=your_private_api_hash
TELEGRAM_SESSION_NAME=telegram_monitor
TARGET_1_ID=111111111
TARGET_1_NAME=Work account 1
TARGET_2_ID=222222222
TARGET_2_NAME=Work account 2
CSV_FILE=telegram_accessi.csv
```

`.env` è già incluso in `.gitignore`.

### 6. Come trovare gli ID

Dopo aver configurato API ID/Hash, puoi eseguire:

```bash
python3 find_ids.py
```

Al primo utilizzo Telethon può richiedere l'autenticazione. Lo script elenca le chat private visibili alla sessione con i relativi ID. Individua **solo gli account che possiedi/controlli** e copia i loro ID nel `.env`.

### 7. Primo avvio

![First run](docs/images/04-first-run.png)

```bash
python3 telegram_monitor.py
```

Al primo avvio inserisci, quando richiesto da Telethon:

1. numero di telefono dell'account Telegram che esegue il client;
2. codice di accesso ricevuto tramite Telegram;
3. password 2FA, se attiva.

Verrà creato un file `telegram_monitor.session`. **È una credenziale sensibile:** chi ne entra in possesso può utilizzare la sessione autenticata. Non caricarlo mai su GitHub, non inviarlo via chat e non condividerlo.

### 8. Monitoraggio

![Running monitor](docs/images/05-running.png)

Il terminale mostrerà righe simili a:

```text
2026-10-01 08:42:15 +0200 | Work account 1 | ONLINE
2026-10-01 08:47:32 +0200 | Work account 1 | OFFLINE
```

Le stesse variazioni vengono aggiunte a `telegram_accessi.csv`.

### 9. Avvio rapido su macOS

È incluso `run_mac.command`. Una volta estratto il progetto:

```bash
chmod +x run_mac.command
```

Poi puoi avviarlo con doppio clic. Se macOS lo blocca la prima volta, usa **tasto destro → Apri**.

### 10. Pubblicazione su GitHub

Prima di ogni `git push`, controlla:

```bash
git status
```

Non devono comparire `.env`, `*.session`, `*.session-journal` o `telegram_accessi.csv`. Il `.gitignore` fornito li esclude già.

> **Importante:** se una credenziale è stata pubblicata accidentalmente, considerala compromessa. Una sessione Telethon può essere revocata dalle sessioni/dispositivi Telegram. Per le credenziali API consulta la documentazione Telegram corrente.

### 11. Limiti

- Non aggira le impostazioni privacy di Telegram.
- Non garantisce che Telegram invii ogni variazione di presenza.
- Registra soltanto gli aggiornamenti ricevuti mentre il client è collegato.
- Se il computer va in stop o perde Internet, possono mancare eventi.
- Il progetto non è progettato per il monitoraggio di terzi senza autorizzazione.

---

## English

### 1. What it does

This program stays connected to Telegram through Telethon and appends `ONLINE` and `OFFLINE` changes for configured IDs to `telegram_accessi.csv`. Use it only for accounts you own, control, or are authorized to administer. Telegram requires applications to use their own `api_id`, and API usage is subject to Telegram's API Terms.

### 2. Requirements

- Python 3.9+ recommended
- A Telegram account
- Telegram `API ID` and `API Hash`
- Telegram IDs for the work accounts you are configuring
- macOS, Linux, or Windows

### 3. Create an API ID and API Hash

![API Development Tools](docs/images/01-api-tools.png)

1. Open **https://my.telegram.org**.
2. Sign in with the phone number linked to your Telegram account.
3. Choose **API development tools**.

![Create application](docs/images/02-create-app.png)

4. Create an application, providing at least **App title** and **Short name**.
5. Telegram displays your `api_id` and `api_hash`.
6. **Keep the API Hash private.** Never commit it to GitHub.

Official documentation: https://core.telegram.org/api/obtaining_api_id

### 4. Installation

```bash
unzip telegram-work-account-monitor.zip
cd telegram-work-account-monitor
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
```

Windows activation:

```powershell
.venv\Scripts\activate
```

### 5. Configuration

![Configure env](docs/images/03-env.png)

Create your private `.env` file:

```bash
cp .env.example .env
```

Configure it:

```dotenv
TELEGRAM_API_ID=12345678
TELEGRAM_API_HASH=your_private_api_hash
TELEGRAM_SESSION_NAME=telegram_monitor
TARGET_1_ID=111111111
TARGET_1_NAME=Work account 1
TARGET_2_ID=222222222
TARGET_2_NAME=Work account 2
CSV_FILE=telegram_accessi.csv
```

`.env` is already excluded by `.gitignore`.

### 6. Finding the IDs

After setting your API credentials, run:

```bash
python3 find_ids.py
```

Telethon may request authentication on first use. The helper lists private dialogs visible to the session and their IDs. Select **only accounts you own/control**, then put those IDs in `.env`.

### 7. First run

![First authentication](docs/images/04-first-run.png)

```bash
python3 telegram_monitor.py
```

On first run, Telethon may ask for:

1. the phone number of the Telegram account running the client;
2. the Telegram login code;
3. the 2FA password, if enabled.

A `telegram_monitor.session` file will be created. **Treat it as a sensitive login credential.** Never commit it to GitHub or share it.

### 8. Running

![Running monitor](docs/images/05-running.png)

Example terminal output:

```text
2026-10-01 08:42:15 +0200 | Work account 1 | ONLINE
2026-10-01 08:47:32 +0200 | Work account 1 | OFFLINE
```

The same changes are appended to `telegram_accessi.csv`.

### 9. Quick launch on macOS

The repository includes `run_mac.command`:

```bash
chmod +x run_mac.command
```

You can then double-click it. If macOS blocks it on first launch, use **right-click → Open**.

### 10. Publishing to GitHub

Before every push, check:

```bash
git status
```

`.env`, `*.session`, `*.session-journal`, and `telegram_accessi.csv` must never appear in the commit. The included `.gitignore` excludes them.

### 11. Limitations

- It does not bypass Telegram privacy settings.
- Telegram may not deliver every presence transition.
- It logs only updates received while the client is connected.
- Sleep/network outages may cause missed events.
- This project is not intended for unauthorized monitoring of third parties.

---

## Security / Sicurezza

Telethon documentation warns that session files/string sessions contain authorization material and must be kept secret. Telegram also requires developers to obtain their own API ID and comply with its API Terms.

Official resources:

- Telegram API ID: https://core.telegram.org/api/obtaining_api_id
- Telegram API Terms: https://core.telegram.org/api/terms
- Telethon sign-in: https://docs.telethon.dev/en/stable/basic/signing-in.html
- Telethon sessions: https://docs.telethon.dev/en/stable/concepts/sessions.html

## License

MIT. Telegram and Telethon are third-party projects; this repository is not affiliated with Telegram.
