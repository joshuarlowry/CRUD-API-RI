# CRUD-API-RI
CRUD API reference implementation

## Running the FastAPI CRM Service

1. **Launch the Dev Container**
   * Open this project in VS Code and select **"Reopen in Container"** when prompted.

2. **Start the server**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

3. **Explore the API**
   * Visit http://localhost:8000/docs for the interactive Swagger UI.
   * CRUD endpoints are available under the **/contacts** path.

4. **Database**
   * SQLite file `crm.db` will be generated at the project root on first run.

### Example Requests

Create:
```bash
curl -X POST http://localhost:8000/contacts \
     -H "Content-Type: application/json" \
     -d '{"first_name":"Ada","last_name":"Lovelace","email":"ada@example.com"}'
```

Retrieve:
```bash
curl http://localhost:8000/contacts/1
```

Update:
```bash
curl -X PUT http://localhost:8000/contacts/1 \
     -H "Content-Type: application/json" \
     -d '{"phone":"555-1234"}'
```

Delete:
```bash
curl -X DELETE http://localhost:8000/contacts/1 -i
```

The API returns appropriate HTTP status codes (e.g., **404** for missing contacts, **409** on duplicate email).

## Web-based CRUD Test UI

Want to play with the API without crafting curl commands? After the server is running, open:

```
http://localhost:8000/ui
```

That page is a lightweight HTML/JS harness (see `frontend/index.html`) that exposes several one-click tests:

* **List contacts** – `GET /contacts`
* **Create contact** – `POST /contacts` with a unique email each click
* **Get contact 1** – `GET /contacts/1` (will return *404* if no such record)
* **Delete missing contact** – `DELETE /contacts/9999` expects *404*

Each action streams the full request and response—including status code—into a console pane so you can watch what happens in real-time.

Feel free to duplicate any block in `tests` inside the page to add more scenarios.
