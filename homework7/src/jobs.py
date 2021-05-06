import uuid, os
from hotqueue import HotQueue
from redis import StrictRedis


# Pass IP as an environment variable
redis_ip = os.environ.get('REDIS_IP')
worker_ip = os.environ.get('WORKER_IP')
if not redis_ip:
    raise Exception()


# I'm using the same redis deployment for like 2 assignments. So I'm just assigning db to 10 and 11 just in case.
q = HotQueue("queue", host=redis_ip, port=6379, db=10)   # Jobs q
rd = redis.StrictRedis(host=redis_ip, port=6379, db=11)  # Jobs db


def _generate_jid():
    return str(uuid.uuid4())


def _generate_job_key(jid):
    return 'job.{}'.format(jid)


def _instantiate_job(jid, status, start, end):
    if type(jid) == str:
        return {'id': jid,
                'status': status,
                'start': start,
                'end': end
                }
    return {'id': jid.decode('utf-8'),
            'status': status.decode('utf-8'),
            'start': start.decode('utf-8'),
            'end': end.decode('utf-8')
            }


def _save_job(job_key, job_dict):
    """Save a job object in the Redis database."""
    rd.hmset(job_key, job_dict)


def _queue_job(jid):
    """Add a job to the redis queue."""
    q.put(jid)


def add_job(start, end, status="submitted"):
    """Add a job to the redis queue."""
    jid = _generate_jid()
    job_dict = _instantiate_job(jid, status, start, end)
    _save_job(_generate_job_key(jid), job_dict)
    _queue_job(jid)
    return job_dict


def update_job_status(jid, status):
    """Update the status of job with job id `jid` to status `status`."""
    jid, status, start, end = rd.hmget(_generate_job_key(jid), 'id', 'status', 'start', 'end')
    job = _instantiate_job(jid, status, start, end)
    if job:
        job['IP'] = worker_ip
        job['status'] = status
        _save_job(_generate_job_key(jid), job)
    else:
        raise Exception()
