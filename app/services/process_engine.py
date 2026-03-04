from app.models.process import Process
from app.extensions import db

def update_process_status(process_id, new_status):
    process = Process.query.get(process_id)
    if not process:
        return None

    process.status = new_status
    db.session.commit()
    return process