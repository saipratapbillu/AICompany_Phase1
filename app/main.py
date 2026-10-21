from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.schemas import RequirementCreate, ProjectCreate, TaskCreate
from app.services.orchestrator import classify_requirement
import uuid, json

app = FastAPI(title="AI Company Control Plane", version="0.1.0")

def uid(): return str(uuid.uuid4())

@app.get("/health")
def health(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {"status":"ok","database":"AICompany","server":"localhost"}

@app.post("/requirements")
def create_requirement(req: RequirementCreate, db: Session = Depends(get_db)):
    rid = uid(); analysis = classify_requirement(req.description)
    db.execute(text("""INSERT INTO Requirement
      (RequirementID,Title,Description,RequestedBy,Priority,RiskLevel,Status,CreatedAtUtc,CreatedBy,ModifiedAtUtc,ModifiedBy)
      VALUES (:id,:t,:d,:rb,:p,:risk,'Assessed',SYSUTCDATETIME(),:rb,SYSUTCDATETIME(),:rb)"""),
      {"id":rid,"t":req.title,"d":req.description,"rb":req.requested_by,"p":req.priority,"risk":analysis["risk_level"]})
    db.commit()
    return {"requirement_id":rid,"ceo_analysis":analysis}

@app.post("/projects")
def create_project(p: ProjectCreate, db: Session = Depends(get_db)):
    pid = uid()
    db.execute(text("""INSERT INTO Project
      (ProjectID,ProjectName,Objective,BusinessOwner,BudgetAmount,Status,CreatedAtUtc,CreatedBy,ModifiedAtUtc,ModifiedBy)
      VALUES (:id,:n,:o,:bo,:b,'Planning',SYSUTCDATETIME(),:bo,SYSUTCDATETIME(),:bo)"""),
      {"id":pid,"n":p.name,"o":p.objective,"bo":p.business_owner,"b":p.budget})
    db.commit(); return {"project_id":pid,"status":"Planning"}

@app.post("/tasks")
def create_task(t: TaskCreate, db: Session = Depends(get_db)):
    tid = uid()
    db.execute(text("""INSERT INTO Task
      (TaskID,ProjectID,Description,Priority,AssignedAgentID,RiskLevel,BudgetLimit,TokenLimit,Status,CreatedAtUtc,CreatedBy,ModifiedAtUtc,ModifiedBy)
      VALUES (:id,:pid,:d,:p,:a,:r,:b,:tok,'Created',SYSUTCDATETIME(),'API',SYSUTCDATETIME(),'API')"""),
      {"id":tid,"pid":t.project_id,"d":t.description,"p":t.priority,"a":t.assigned_agent_id,"r":t.risk_level,"b":t.budget_limit,"tok":t.token_limit})
    db.commit(); return {"task_id":tid,"status":"Created"}

@app.get("/agents")
def agents(db: Session = Depends(get_db)):
    rows=db.execute(text("SELECT AgentID,AgentName,AgentType,Grade,AutonomyLevel,RiskLevel,Status,CurrentWorkload FROM Agent ORDER BY AgentName")).mappings().all()
    return [dict(r) for r in rows]
