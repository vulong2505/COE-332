import time
from jobs import q, update_job_status


@q.worker()
def execute_job(jid):
    update_job_status(jid, "In progress...")
    time.sleep(15)
    update_job_status(jid, "Completed")


execute_job()
