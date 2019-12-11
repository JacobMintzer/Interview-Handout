import mock_db
import uuid
from worker import worker_main
from threading import Timer
from threading import Thread
from datetime import datetime
from datetime import timedelta
import time

initiated=False


def lock_is_free_no_variable(db):
    """
        Version of lock that does not use initiated variable, for if you consider that to be a local lock.
    """
    try:
        db.insert_one({"_id":"Lock","Lock":True})
        return True
    except Exception:
        pass
    lockStatus=db.count({"_id":"Lock","Lock":True})
    if lockStatus==1:
        return False
    else:
        db.update_one({"_id":"Lock","Lock":False},{"_id":"Lock","Lock":True})
        return True

def lock_is_free(db):
    """
    checks if lock is free, if it is, locks and returns true
    else returns false
    Args: 
        db: instance of MockDB
    Returns: Boolean
    """
    global initiated
    lock=db.find_one({"_id":"Lock"})
    
    try:
        if lock is None:
            db.insert_one({"_id":"Lock","Lock":True})
            initiated=True
            return True
    except Exception: 
        return False #if there is a race condition, and this one is second, we can assume that the process hasn't ended yet and the lock isn't free
    if lock["Lock"]:
        return False
    else:
        db.update_one({"_id":"Lock","Lock":False},{"_id":"Lock","Lock":True})
        return True

def unlock(db):
    """after process is done, remove the lock
    Args:
        db: instance of MockDB
     """
    db.update_one({"_id":"Lock","Lock":True},{"_id":"Lock","Lock":False})

def timeout():
    raise Exception("Timeout Exception")

def attempt_run_worker(worker_hash, give_up_after, db, retry_interval):
    """
        Notes start time, then continually checks lock until give_up_after seconds have passed. 
        When lock is free, starts the process, then unlocks the lock.
        

        Args:
            worker_hash: a random string we will use as an id for the running worker
            give_up_after: if the worker has not run after this many seconds, give up
            db: an instance of MockDB
            retry_interval: continually poll the locking system after this many seconds
                            until the lock is free, unless we have been trying for more
                            than give_up_after seconds
    """
    end=datetime.now()+timedelta(seconds=give_up_after)
    while(datetime.now()<end):
        if lock_is_free(db):
            try:
                #print("thread {0} is using the lock now".format(worker_hash))
                worker_main(worker_hash, db)
                #print("thread {0} is done with the lock now".format(worker_hash))
            except Exception as e:
                print(e)
            finally:
                unlock(db)
                return
        else:
            time.sleep(retry_interval)
    print("thread {0} has timed out")

if __name__ == "__main__":
    """
        DO NOT MODIFY

        Main function that runs the worker five times, each on a new thread
        We have provided hard-coded values for how often the worker should retry
        grabbing lock and when it should give up. Use these as you see fit, but
        you should not need to change them
    """

    db = mock_db.DB()
    threads = []
    for _ in range(25):
        t = Thread(target=attempt_run_worker, args=(uuid.uuid1(), 2000, db, 0.1))
        threads.append(t)
    for t in threads:
        t.start()
    for t in threads:
        t.join()
