# AI Company Local MVP

Implementation-ready control-plane starter for a governed AI Company. It uses SQL Server on `localhost` and a FastAPI API.

## Prerequisites
- Windows with local SQL Server / SQL Server Developer Edition
- SQL Server Management Studio
- Python 3.11+
- Microsoft ODBC Driver 18 for SQL Server

## 1. Create database
Open SSMS against `localhost` with Windows authentication and run:
1. `sql/01_create_database.sql`
2. `sql/02_seed.sql`

## 2. Configure
Copy `.env.example` to `.env`. Defaults already use `localhost`, database `AICompany`, Windows integrated authentication, and local non-encrypted SQL connectivity.

## 3. Run API
From the project directory on Windows:
`run_local.bat`

Then open:
- API: http://127.0.0.1:8000
- Swagger: http://127.0.0.1:8000/docs
- Health: http://127.0.0.1:8000/health

## MVP endpoints
- `POST /requirements`: creates and classifies a requirement
- `POST /projects`: creates a project
- `POST /tasks`: creates a controlled task
- `GET /agents`: lists registered AI employees

## Example requirement
POST `/requirements`
```json
{
  "title": "Supplier Compliance Platform",
  "description": "Build a supplier compliance system using SharePoint, SQL Server and Power BI",
  "requested_by": "HumanOwner",
  "priority": "High"
}
```

## Important
This is a local MVP/control-plane foundation, not production. Agent execution/model-provider calls are intentionally left unconfigured. Production requires Entra workload identities, secret management, API/MCP policy enforcement, approval services, message bus, immutable audit/evidence storage, evaluation gates, and environment separation.
