# iteration17b.md — PRD: Refactor “Java/JSP/GWT/JS → PRD” Pipeline (Ollama + Weaviate, .env-driven)

**Owner:** Thomas Neusser
**Date:** 2025-10-08
**Status:** Draft for implementation in Cursor
**Goal:** Extend the local, offline reverse-engineering pipeline to reliably turn a **Java/JSP + iBATIS + GWT + JavaScript** codebase into a **PRD auto-draft** using **Ollama** (LLM + embeddings) and **Weaviate** (vector DB), fully configured via **.env**. Support multi-project runs by scanning `JAVA_SOURCE_DIR` and deriving the project name deterministically.

---

## 0) Executive Summary

We evolve the iteration17 plan to also parse and understand **GWT client code** (Activities/Places, EntryPoints, UiBinder, RPC/RequestFactory) and **plain JavaScript** (forms, validation, XHR/fetch endpoints, SPA routes).
We keep the stack **Python-first** (no Java tooling), use **Ollama** locally for LLM + embeddings, and **Weaviate** (vectorizer:none) for storage and retrieval. Outputs: **PRD drafts** with FR/AC/NFR and **traceability** across backend (iBATIS/DAO/JSP/DB) and frontend (GWT/JS views, routes, validations).

---

## 1) Scope

### In scope

* Existing (iteration17) backend parsing and PRD generation.
* **GWT artifacts**:

  * `*.gwt.xml` module descriptors
  * Client packages (`client/`, `shared/`) including **EntryPoint**, **Activity/Place**, **UiBinder** (`*.ui.xml`), **ClientBundle/CssResource**, **i18n** (`Constants`, `Messages`, `*.properties`)
  * **RPC** (`RemoteService` / `RemoteServiceServlet` / `ServiceAsync`) and **RequestFactory** (`RequestContext`, `ValueProxy`) wiring and endpoints (e.g., `/gwt.rpc`, `/gwtRequest`)
* **Plain JavaScript**:

  * `*.js` in webapp, inline `<script>` in JSP, module loaders, SPA routers, `fetch`/XHR calls, client-side validation (HTML5 attrs, RegExp), DOM-form bindings.
* **Frontend routes & navigation**:

  * GWT **History tokens** and PlaceMappings
  * JS routers (hash/history) and URL patterns

### Out of scope (iteration17b)

* Actual compilation/execution of GWT; dynamic runtime tracing.
* Deep transpiler/closure advanced optimizations reversing (we read sources, not compiled JS).

---

## 2) Environment & Configuration (.env)

Additions compared to iteration17:

```ini
# Source discovery
JS_INCLUDE_GLOBS=**/*.js
GWT_INCLUDE_GLOBS=**/*.gwt.xml,**/*.ui.xml,**/*EntryPoint*.java,**/*Activity*.java,**/*Place*.java,**/*Service*.java,**/*RequestFactory*.java
JSP_INCLUDE_GLOBS=**/*.jsp,**/*.jspf

# Heuristics
GWT_RPC_DEFAULT_PATH=/gwt.rpc          # fallback if not found in web.xml
GWT_RF_DEFAULT_PATH=/gwtRequest
JS_ROUTE_HINTS=#/,#/.*,/,/app/.*
JS_HTTP_METHOD_HINTS=GET,POST,PUT,DELETE,PATCH
```

(Keep all iteration17 variables: `JAVA_SOURCE_DIR`, `OLLAMA_MODEL_NAME`, `OLLAMA_EMBED_MODEL_NAME`, `WEAVIATE_URL`, etc.)

---

## 3) Architecture (updated)

```
src/
  config/
  discover/
  extract/
    ibatis_xml.py
    java_calls.py          # also parses GWT client java
    jsp_forms.py
    db_schema.py
    gwt_modules.py         # NEW: *.gwt.xml & module graph
    gwt_client.py          # NEW: EntryPoint/Activity/Place/RPC/RequestFactory
    gwt_uibinder.py        # NEW: *.ui.xml -> widgets/fields/events
    js_static.py           # NEW: .js + inline <script> (forms/xhr/routes)
  chunk/
    build_chunks.py        # extended to GWT/JS artifacts
  embed/
  store/
  retrieve/
  synth/
    prompts.py             # extended with frontend-aware prompts
    prd_markdown.py        # merges frontend + backend views
  cli.py
```

---

## 4) Weaviate Schema (extended; vectorizer: "none")

**Common props** (all classes):
`project, path, lineStart, lineEnd, text, meta(json), createdAt(date)`

### Backend classes (unchanged from iteration17)

* `IbatisStatement`, `DaoCall`, `JspForm`, `DbTable`, `Flow`, `Requirement`

### **New frontend classes**

1. `GwtModule`

   * `moduleName` (string) — from `*.gwt.xml` `<module rename-to="...">` or package
   * `inherits` (string[]) — inherited modules
   * `entryPoints` (string[]) — FQCNs discovered
   * `rawXml` (text)

2. `GwtUiBinder`

   * `uiXmlPath` (string)
   * `ownerType` (string) — bound Java class
   * `widgetsJson` (text) — ids, types
   * `eventsJson` (text) — handlers (onClick, selection, etc.)
   * `i18nKeys` (string[])

3. `GwtActivityPlace`

   * `placeClass` (string), `activityClass` (string)
   * `placeToken` (string) — History token pattern if derivable
   * `views` (string[]) — view classes/widgets
   * `navigatesTo` (string[]) — next places
   * `callsServices` (string[]) — linked RPC/RequestFactory services (by name)

4. `GwtEndpoint`

   * `style` (string: RPC|RequestFactory)
   * `serviceInterface` (string) — `FooService` / `FooRequestContext`
   * `asyncInterface` (string, optional)
   * `path` (string) — `/gwt.rpc` or mapped servlet path
   * `methodsJson` (text) — method names & param shapes
   * `serverImpl` (string) — servlet or handler FQCN (if found)

5. `JsArtifact`

   * `scriptPath` (string)
   * `routesJson` (text) — hash/history routes and handlers
   * `xhrJson` (text) — list of HTTP calls with method/url/payload shape
   * `validationsJson` (text) — client-side field rules
   * `globals` (string[]) — exported names

6. `FrontendRoute`

   * `kind` (string: GWT_PLACE|JS_ROUTER)
   * `pattern` (string) — token or path pattern
   * `view` (string) — component/view id/class
   * `handlerRef` (string)
   * `navigatesTo` (string[])

---

## 5) Extraction (additions)

### 5.1 GWT modules (`gwt_modules.py`)

* Parse `*.gwt.xml` with `lxml`.
* Collect `<inherits>`, `<entry-point class="...">`, `<source path="...">`, `<set-configuration-property>` (i18n/locales).
* Emit `GwtModule` objects.

### 5.2 GWT client Java (`gwt_client.py`)

* Use **`javalang`** like backend, but target **client** packages:

  * Locate classes implementing `EntryPoint` → `onModuleLoad()`
  * Identify **Place** classes (often extend `Place` or carry `Tokenizer`)
  * Identify **Activity** classes (implement `Activity`)
  * Map **Place ↔ Tokenizer** (find `getToken`/`getPlace`)
  * Extract **RPC**: interfaces extending `RemoteService` + paired `ServiceAsync` and the server impl extending `RemoteServiceServlet` (from server package, mapped in `web.xml`)
  * Extract **RequestFactory**: `RequestFactory` implementations, `RequestContext` methods, `ValueProxy` types, and default endpoint (typically `/gwtRequest` or from servlet mapping)
* Output:

  * `GwtActivityPlace` records (place, token, activity, views*)
  * `GwtEndpoint` (style, path, methods)
  * *Views are inferred by matching Activity constructor fields, UiBinder owners, or referenced classes.

### 5.3 GWT UiBinder (`gwt_uibinder.py`)

* Parse `*.ui.xml` with `lxml`:

  * widgets (tags), `ui:field` ids, `ui:with`, event handlers (attributes like `onClick="{owner.method}"`).
  * collect i18n resources (e.g., `ui:with field='msgs' type='com.app.client.Messages'`) and used keys.
* Emit `GwtUiBinder` objects.

### 5.4 JavaScript (`js_static.py`)

* Parse **standalone `.js`** files and **inline `<script>` in JSP**:

  * Prefer **tree-sitter-javascript** (if available) or fallback to regex/`esprima-python` equivalents.
  * Extract:

    * **Routes** (e.g., `router.on('/orders/:id', ...)`, `window.onhashchange`, `history.pushState`)
    * **XHR/fetch** calls (`fetch('/api/...',{method:'POST', body:...})`, `$.ajax({...})`)
    * **Validations** (regex, custom functions bound to forms)
    * **Global exports** (namespacing patterns)
* Emit `JsArtifact` and `FrontendRoute` (kind=JS_ROUTER).

> All extractors write JSON snapshots to `data/build/*.json` besides pushing to Weaviate via `index`.

---

## 6) Chunking & Embedding (frontend-aware)

Extend `chunk/build_chunks.py` to produce human-readable **chunk headers**:

* **GwtModule**

  ```
  [GWT Module] com.app.App (entryPoints=AppEntryPoint)
  inherits: com.google.gwt.user.User
  sources: client/, shared/
  ```
* **GwtActivityPlace**

  ```
  [GWT Place/Activity] OrdersPlace ↔ OrdersActivity
  token: orders/{id}
  navigatesTo: OrderListPlace
  callsServices: OrderService
  ```
* **GwtUiBinder**

  ```
  [UiBinder] OrderView.ui.xml (owner=com.app.client.ui.OrderView)
  widgets: orderForm:FormPanel, saveButton:Button
  events: saveButton.onClick -> onSaveClicked()
  i18n: msgs.orderSaved
  ```
* **GwtEndpoint**

  ```
  [GWT RPC] OrderService @ /gwt.rpc
  methods: getById(id), save(order), list(q, status)
  serverImpl: OrderServiceImpl (RemoteServiceServlet)
  ```
* **JsArtifact**

  ```
  [JS] /webapp/js/orders.js
  routes: /orders/:id -> showOrder
  xhr: GET /api/orders/{id}, POST /api/orders
  validations: qty > 0, email regex
  ```

Embed with `OLLAMA_EMBED_MODEL_NAME`, store vectors explicitly.

---

## 7) Retrieval & Synthesis (frontend + backend fusion)

### Retrieval strategy

* Mixed semantic retrieval across **backend & frontend classes**, filtered by `project`.
* For a **feature candidate** (e.g., “Order Create”), query with:

  * statement verbs (INSERT/UPDATE),
  * related route patterns (`/order/create`),
  * GWT tokens (`orders/new`),
  * JS functions (`saveOrder`),
  * JSP forms (`action="/order/create"`).

### Synthesis prompts (additions)

**Flow (frontend-aware)**

```
You are a senior product analyst. Given these artifacts (GWT Places/Activities, UiBinder views, GWT endpoints, JS routes/XHR, JSP forms, iBATIS statements + DAO calls),
produce ONE coherent user-facing flow that spans UI → API → DB.

Return JSON:
{
 "title": "...",
 "summary": "...",
 "actors": ["Buyer","Admin"],
 "entryPoints": [{"kind":"GWT_PLACE|JS_ROUTE|JSP","value":"orders/new"}],
 "ui": {"views": ["OrderView"], "fields":[{"name":"qty","type":"number","required":true,"validation":"qty>0"}]},
 "api": {"style":"RPC|RequestFactory|REST","endpoint":"/gwt.rpc|/api/orders","methods":["save(order)"], "payloadSchema":"..."},
 "steps": ["..."], 
 "reads": ["table.column", ...], 
 "writes": ["table.column", ...],
 "navigation": {"onSuccess":"orders/{id}","onError":"error dialog"},
 "trace": {"statements":["Order.insert"],"files":["OrderService.java:45-102","order.xml:120-164","OrderView.ui.xml:1-120","orders.js:10-84"],"routes":["orders/new","/order/create"]}
}
Artifacts:
<<<CONTEXT>>>
```

**Requirements writer (merge UI validations)**

* Convert **UiBinder field rules** and **JS validations** into FRs & ACs:

  * AC example: *GIVEN qty ≤ 0 WHEN saving order THEN client prevents submit and server returns 400 without DB write.*

**NFRs (frontend hints)**

* If many **Place** transitions or JS routes → add **loading feedback** requirement.
* If UiBinder shows **tables/lists** → add **pagination** and **sort** NFRs.
* If RPC path shared across services → add **rate-limit** or **payload size** NFRs.

---

## 8) PRD Composition (changes)

Add a **Frontend section per feature**:

```
### Frontend View & Navigation
- Entry Points: GWT Place `orders/new`, JS Route `/orders/new`
- Views (UiBinder): OrderView (saveButton, orderForm)
- Client-side Validations: qty > 0, email regex
- Navigation: On success → Place `orders/{id}`, On cancel → `orders/list`
```

Traceability now lists **frontend artifacts** too (UiBinder, Place/Activity, JS route function).

---

## 9) CLI Additions

```
reveng extract --project <name> --include-frontend   # runs gwt_* and js_static
reveng index   --project <name>
reveng search  --q "orders new save" --project <name> --frontend
reveng prd     --project <name> --frontend
```

Flags:

* `--include-frontend` turns on `gwt_modules.py`, `gwt_client.py`, `gwt_uibinder.py`, `js_static.py`.

---

## 10) Milestones & Acceptance (delta to iteration17)

### M2F — Frontend Extractors (2–4 dev-days)

* `gwt_modules.py`: modules & entry points discovered.
* `gwt_client.py`: Places/Activities mapped to tokens; RPC/RequestFactory endpoints and methods; server implementations.
* `gwt_uibinder.py`: widgets/fields/events/i18n enumerated.
* `js_static.py`: routes, XHR/fetch targets, validations parsed.

**Acceptance**

* For a sample GWT app: at least 1 module, 2 places/activities, 1 RPC endpoint, and 1 UiBinder view extracted.
* For a sample JS SPA: at least 2 routes and 2 XHR calls identified.

### M4F — Frontend-aware Synthesis (1–2 dev-days)

* Flow synthesis includes **entry points (Place/Route)**, **views/fields**, **endpoint style**.
* Requirements integrate **client validations** and **navigation**.

**Acceptance**

* One feature shows a cohesive **UI → API → DB** path with ACs referencing **client + server** behaviors.

---

## 11) Data Contracts (examples)

### `GwtActivityPlace`

```json
{
  "project":"shop-core",
  "placeClass":"com.app.client.place.OrdersPlace",
  "activityClass":"com.app.client.activity.OrdersActivity",
  "placeToken":"orders/{id}",
  "views":["OrderView"],
  "navigatesTo":["OrderListPlace"],
  "callsServices":["OrderService"],
  "path":"src/client/place/OrdersPlace.java",
  "text":"[GWT Place/Activity]..."
}
```

### `JsArtifact`

```json
{
  "project":"shop-core",
  "scriptPath":"webapp/js/orders.js",
  "routesJson":"[{\"pattern\":\"/orders/:id\",\"handler\":\"showOrder\"}]",
  "xhrJson":"[{\"method\":\"GET\",\"url\":\"/api/orders/{id}\"},{\"method\":\"POST\",\"url\":\"/api/orders\"}]",
  "validationsJson":"[{\"field\":\"qty\",\"rule\":\">0\"}]",
  "text":"[JS] /webapp/js/orders.js ..."
}
```

---

## 12) Test Plan (frontend)

* **Fixtures**:

  * Minimal GWT module with 1 EntryPoint, 1 Place/Activity, 1 UiBinder view, 1 RPC method.
  * Minimal JS app with 2 routes and 2 fetch calls.
* **Unit tests**:

  * Place tokenization; Activity mapping; RPC path detection.
  * UiBinder field and event extraction.
  * JS route/XHR detection; validation capture.
* **Smoke**:

  * `make all -- include-frontend` produces PRD where at least one feature documents **entry route, view fields, server endpoint, DB writes** and has **client+server ACs**.

---

## 13) Risks & Mitigations

* **Non-standard routers / minified JS** → limited static recovery.
  *Mitigation:* favor source folders; fall back to searching `fetch(`/`$.ajax(` patterns; allow manual hints via config.
* **GWT token inference** varies by app framework.
  *Mitigation:* look for `Tokenizer` implementations; fall back to common naming patterns and EntryPoint wiring.
* **Mixed RPC and REST** side-by-side.
  *Mitigation:* classify per artifact (`style=RPC|RequestFactory|REST`) and merge during synthesis.

---

## 14) Work Breakdown (for Cursor)

* **New**: `extract/gwt_modules.py`, `extract/gwt_client.py`, `extract/gwt_uibinder.py`, `extract/js_static.py`
* Extend: `chunk/build_chunks.py`, `store/weaviate_client.py` (new classes), `synth/prompts.py`, `synth/prd_markdown.py`
* Update CLI to add `--include-frontend`

---

## 15) Definition of Done (iteration17b)

* Weaviate schema includes **frontend classes**; `reveng schema --ensure` succeeds.
* `reveng extract --include-frontend` emits non-empty frontend JSONs.
* `reveng index` stores frontend artifacts with vectors; `reveng search --frontend` finds them.
* `reveng prd --frontend` generates a PRD that **explicitly** documents at least one **UI → API → DB** flow with **client and server acceptance criteria** and **traceability** (UiBinder, Place, JS route, RPC/REST endpoint, iBATIS statement, DB tables).

---

**End of iteration17b.md**
