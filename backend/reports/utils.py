import json
import os
from datetime import datetime
from typing import List, Dict, Any, Optional
from pathlib import Path

REPORTS_FILE = Path("backend/data/reports.json")
PENALTIES_FILE = Path("backend/data/penalties.json")

def load_reports() -> List[Dict[str, Any]]:
    if not REPORTS_FILE.exists():
        return []
    
    with open(REPORTS_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_reports(reports: List[Dict[str, Any]]) -> None:
    REPORTS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(REPORTS_FILE, "w") as f:
        json.dump(reports, f, indent=4)

def load_penalties() -> List[Dict[str, Any]]:
    if not PENALTIES_FILE.exists():
        return []
    
    with open(PENALTIES_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_penalties(penalties: List[Dict[str, Any]]) -> None:
    PENALTIES_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(PENALTIES_FILE, "w") as f:
        json.dump(penalties, f, indent=4)

def create_report(reporter_id: str, movie_id: str, reason: str, description: str = None) -> Dict[str, Any]:
    reports = load_reports()
    
    new_report = {
        "report_id": f"report_{len(reports) + 1}",
        "reporter_id": reporter_id,
        "movie_id": movie_id,
        "reason": reason,
        "description": description,
        "status": "pending",
        "created_at": datetime.utcnow().isoformat(),
        "assigned_moderator": None,
        "resolution": None,
        "resolved_at": None,
        "moderator_notes": None
    }
    
    reports.append(new_report)
    save_reports(reports)
    return new_report

def get_reports_for_moderator() -> List[Dict[str, Any]]:
    return [r for r in load_reports() if r["status"] == "pending"]

def get_report_by_id(report_id: str) -> Optional[Dict[str, Any]]:
    reports = load_reports()
    return next((r for r in reports if r["report_id"] == report_id), None)

def update_report_status(report_id: str, status: str, moderator_id: str, notes: str = None) -> bool:
    reports = load_reports()
    for report in reports:
        if report["report_id"] == report_id:
            report["status"] = status
            report["assigned_moderator"] = moderator_id
            report["resolved_at"] = datetime.utcnow().isoformat()
            if notes:
                report["moderator_notes"] = notes
            save_reports(reports)
            return True
    return False

def apply_penalty_to_user(user_id: str, reason: str, severity: str, duration_days: int, report_id: str = None) -> Dict[str, Any]:
    penalties = load_penalties()
    
    new_penalty = {
        "penalty_id": f"penalty_{len(penalties) + 1}",
        "user_id": user_id,
        "reason": reason,
        "severity": severity,
        "duration_days": duration_days,
        "report_id": report_id,
        "created_at": datetime.utcnow().isoformat(),
        "active": True
    }
    
    penalties.append(new_penalty)
    save_penalties(penalties)
    
    # Also add penalty to user's record
    from backend.authentication import utils as auth_utils
    users = auth_utils.load_users()
    for user in users:
        if user["user_id"] == user_id:
            if "penalties" not in user:
                user["penalties"] = []
            user["penalties"].append(new_penalty["penalty_id"])
            auth_utils.save_users(users)
            break
    
    return new_penalty

def get_user_penalties(user_id: str) -> List[Dict[str, Any]]:
    penalties = load_penalties()
    return [p for p in penalties if p["user_id"] == user_id and p["active"]]

def dismiss_report(report_id: str, moderator_id: str, notes: str = None) -> bool:
    return update_report_status(report_id, "dismissed", moderator_id, notes)