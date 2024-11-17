/* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */
/*                                                                           */
/*                  This file is part of the program and library             */
/*         SCIP --- Solving Constraint Integer Programs                      */
/*                                                                           */
/*  Copyright (c) 2002-2024 Zuse Institute Berlin (ZIB)                      */
/*                                                                           */
/*  Licensed under the Apache License, Version 2.0 (the "License");          */
/*  you may not use this file except in compliance with the License.         */
/*  You may obtain a copy of the License at                                  */
/*                                                                           */
/*      http://www.apache.org/licenses/LICENSE-2.0                           */
/*                                                                           */
/*  Unless required by applicable law or agreed to in writing, software      */
/*  distributed under the License is distributed on an "AS IS" BASIS,        */
/*  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. */
/*  See the License for the specific language governing permissions and      */
/*  limitations under the License.                                           */
/*                                                                           */
/*  You should have received a copy of the Apache-2.0 license                */
/*  along with SCIP; see the file LICENSE. If not visit scipopt.org.         */
/*                                                                           */
/* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */

/**@file   tpi_openmp.c
 * @ingroup TASKINTERFACE
 * @brief  the interface functions for openmp
 * @author Stephen J. Maher
 * @author Leona Gottwald
 * @author Marc Pfetsch
 */

/*---+----1----+----2----+----3----+----4----+----5----+----6----+----7----+----8----+----9----+----0----+----1----+----2*/

#include "tpi/tpi.h"
#include "blockmemshell/memory.h"
#include "scip/pub_message.h"
#include "scip/pub_misc.h"
#include <omp.h>

/* macros for direct access */

/* lock */
#define SCIPompInitLock(lock)     (omp_init_lock(lock), SCIP_OKAY)
#define SCIPompDestroyLock(lock)  (omp_destroy_lock(lock))
#define SCIPompAcquireLock(lock)  (omp_set_lock(lock), SCIP_OKAY)
#define SCIPompReleaseLock(lock)  (omp_unset_lock(lock), SCIP_OKAY)

/* condition */
#define SCIPompInitCondition(condition)    ( omp_init_lock(&(condition)->_lock), \
                                             (condition)->_waiters = 0, (condition)->_waitnum = 0, (condition)->_signals = 0, SCIP_OKAY )
#define SCIPompDestroyCondition(condition) do { assert((condition)->_waiters == 0); assert((condition)->_waitnum == 0); assert((condition)->_signals == 0); omp_destroy_lock(&(condition)->_lock); } while(0)


/** struct containing lock */
struct SCIP_Lock
{
   omp_lock_t            lock;
};

/** struct for condition */
struct SCIP_Condition
{
   omp_lock_t            _lock;
   int                   _waiters;
   int                   _waitnum;
   int                   _signals;
};


/** A job added to the queue */
struct SCIP_Job
{
   int                   jobid;              /**< id to identify jobs from a common process */
   struct                SCIP_Job* nextjob;  /**< pointer to the next job in the queue */
   SCIP_RETCODE          (*jobfunc)(void* args);/**< pointer to the job function */
   void*                 args;               /**< pointer to the function arguments */
   SCIP_RETCODE          retcode;            /**< return code of the job */
};

/** the thread pool job queue */
struct SCIP_JobQueue
{
   SCIP_JOB*             firstjob;           /**< pointer to the first job in the queue */
   SCIP_JOB*             lastjob;            /**< pointer to the last job in the queue */
   int                   njobs;              /**< number of jobs in the queue */
};
typedef struct SCIP_JobQueue SCIP_JOBQUEUE;

struct SCIP_JobQueues
{
   SCIP_JOBQUEUE         jobqueue;           /**< queue of unprocessed jobs */
   SCIP_JOB**            currentjobs;        /**< array with slot for each thread to store the currently running job */
   int                   ncurrentjobs;       /**< number of currently running jobs */
   int                   nthreads;           /**< number of threads */
   SCIP_JOBQUEUE         finishedjobs;       /**< jobqueue containing the finished jobs */
   omp_lock_t            lock;               /**< lock to protect this stucture from concurrent access */
   SCIP_CONDITION        jobfinished;        /**< condition to signal if a job was finished */
};
typedef struct SCIP_JobQueues SCIP_JOBQUEUES;

static SCIP_JOBQUEUES* _jobqueues = NULL;


/** create job queue */
static
SCIP_RETCODE createJobQueue(
   int                   nthreads,           /**< the number of threads */
   int                   qsize,              /**< the queue size */
   SCIP_Bool             blockwhenfull       /**< should the queue be blocked from new jobs when full */
   )
{
   int i;

   assert(nthreads >= 0);
   assert(qsize >= 0);
   SCIP_UNUSED( blockwhenfull );

   /* allocting memory for the job queue */
   SCIP_ALLOC( BMSallocMemory(&_jobqueues) );
   _jobqueues->jobqueue.firstjob = NULL;
   _jobqueues->jobqueue.lastjob = NULL;
   _jobqueues->jobqueue.njobs = 0;
   _jobqueues->finishedjobs.firstjob = NULL;
   _jobqueues->finishedjobs.lastjob = NULL;
   _jobqueues->finishedjobs.njobs = 0;
   _jobqueues->ncurrentjobs = 0;

   _jobqueues->nthreads = nthreads;
   SCIP_ALLOC( BMSallocMemoryArray(&_jobqueues->currentjobs, nthreads) );

   for( i = 0; i < nthreads; ++i )
      _jobqueues->currentjobs[i] = NULL;

   SCIP_CALL( SCIPompInitLock(&_jobqueues->lock) );
   SCIP_CALL( SCIPompInitCondition(&_jobqueues->jobfinished) );

   return SCIP_OKAY;
}


/** free job queue */
static
SCIP_RETCODE freeJobQueue(
   void
   )
{
   assert(_jobqueues != NULL);

   SCIPompDestroyLock(&_jobqueues->lock);
   SCIPompDestroyCondition(&_jobqueues->jobfinished);
   BMSfreeMemoryArray(&_jobqueues->currentjobs);

   BMSfreeMemory(&_jobqueues);

   return SCIP_OKAY;
}


/** execute job */
static
void executeJob(
   SCIP_JOB*             job                 /**< the job to be executed in parallel */
   )
{
   int threadnum;

   threadnum = SCIPtpiGetThreadNum();

   SCIP_CALL_ABORT( SCIPompAcquireLock(&_jobqueues->lock) );
   _jobqueues->currentjobs[threadnum] = job;
   SCIP_CALL_ABORT( SCIPompReleaseLock(&_jobqueues->lock) );

   job->retcode = (*(job->jobfunc))(job->args);

   SCIP_CALL_ABORT( SCIPompAcquireLock(&_jobqueues->lock) );
   _jobqueues->ncurrentjobs--;
   _jobqueues->currentjobs[threadnum] = NULL;

   /* insert job into finished jobs */
   if( _jobqueues->finishedjobs.njobs == 0 )
   {
      _jobqueues->finishedjobs.firstjob = job;
      _jobqueues->finishedjobs.lastjob = job;
   }
   else
   {
      _jobqueues->finishedjobs.lastjob->nextjob = job;
      _jobqueues->finishedjobs.lastjob = job;
   }

   ++_jobqueues->finishedjobs.njobs;

   SCIP_CALL_ABORT( SCIPtpiBroadcastCondition(&_jobqueues->jobfinished) );

   SCIP_CALL_ABORT( SCIPompReleaseLock(&_jobqueues->lock) );
}

/** wait for a condition */
SCIP_RETCODE SCIPtpiWaitCondition(
   SCIP_CONDITION*       condition,          /**< condition to wait for */
   SCIP_LOCK*            lock                /**< corresponding lock */
   )
{
   int waitnum;

   SCIP_CALL( SCIPtpiReleaseLock(lock) );

   SCIP_CALL( SCIPompAcquireLock(&condition->_lock) );
   waitnum = ++condition->_waitnum;

   ++condition->_waiters;

   do
   {
      SCIP_CALL( SCIPompReleaseLock(&condition->_lock) );
      #pragma omp taskyield
      SCIP_CALL( SCIPompAcquireLock(&condition->_lock) );
   }
   while( condition->_signals < waitnum );

   --condition->_waiters;

   if( condition->_waiters == 0 )
   {
      condition->_signals = 0;
      condition->_waitnum = 0;
   }

   SCIP_CALL( SCIPompReleaseLock(&condition->_lock) );

   SCIP_CALL( SCIPtpiAcquireLock(lock) );

   return SCIP_OKAY;
}

/** wait for a condition (direct access to lock) */
static
SCIP_RETCODE SCIPompWaitCondition(
   SCIP_CONDITION*       condition,          /**< condition to wait for */
   omp_lock_t*           lock                /**< corresponding lock */
   )
{
   int waitnum;

   SCIP_CALL( SCIPompReleaseLock(lock) );

   SCIP_CALL( SCIPompAcquireLock(&condition->_lock) );
   waitnum = ++condition->_waitnum;

   ++condition->_waiters;

   do
   {
      SCIP_CALL( SCIPompReleaseLock(&condition->_lock) );
      #pragma omp taskyield
      SCIP_CALL( SCIPompAcquireLock(&condition->_lock) );
   }
   while( condition->_signals < waitnum );

   --condition->_waiters;

   if( condition->_waiters == 0 )
   {
      condition->_signals = 0;
      condition->_waitnum = 0;
   }

   SCIP_CALL( SCIPompReleaseLock(&condition->_lock) );

   SCIP_CALL( SCIPompAcquireLock(lock) );

   return SCIP_OKAY;
}


/** process jobs from job queue
 *
 * The job will only be added when the number of active jobs is equal to the number of threads.
 * As such, there will always be number of threads + 1 tasks available for the scheduler to run.
 */
static
void jobQueueProcessJob(
   void
   )
{
   SCIP_JOB* job;

   SCIP_CALL_ABORT( SCIPompAcquireLock(&_jobqueues->lock) );

   while( _jobqueues->ncurrentjobs == SCIPtpiGetNumThreads() )
   {
      SCIP_CALL_ABORT( SCIPompWaitCondition(&_jobqueues->jobfinished, &_jobqueues->lock) );
   }

   if( _jobqueues->jobqueue.njobs == 1 )
   {
      job = _jobqueues->jobqueue.firstjob;
      _jobqueues->jobqueue.firstjob = NULL;
      _jobqueues->jobqueue.lastjob = NULL;
      --(_jobqueues->jobqueue.njobs);
   }
   else if( _jobqueues->jobqueue.njobs > 1 )
   {
      job = _jobqueues->jobqueue.firstjob;
      _jobqueues->jobqueue.firstjob = job->nextjob;
      --_jobqueues->jobqueue.njobs;
   }
   else
   {
      job = NULL;
   }

   ++(_jobqueues->ncurrentjobs);
   SCIP_CALL_ABORT( SCIPompReleaseLock(&_jobqueues->lock) );

   if( job )
   {
      executeJob(job);
   }
}


/** adding a job to the job queue
 *
 * This gives some more flexibility in the handling of new jobs.
 * IMPORTANT: This function MUST be called from within a mutex.
 */
static
SCIP_RETCODE jobQueueAddJob(
   SCIP_JOB*             newjob
   )
{
   /* @todo we want to work out what to do with a full job queue. Is there a problem if the limit is hit? */
   /* @note it is important to have a queuesize. This will stop the code submitting infinitely many jobs. */
   assert(newjob != NULL);

   newjob->nextjob = NULL;

   /* This function queries the current job list. This could change by other threads writing to the list. So a lock is
    * required to ensure that the current joblist remains static. */
   SCIP_CALL( SCIPompAcquireLock(&_jobqueues->lock) );

   /* checking the status of the job queue */
   if( _jobqueues->ncurrentjobs == SCIPtpiGetNumThreads() )
   {
      if( _jobqueues->jobqueue.njobs == 0 )
      {
         _jobqueues->jobqueue.firstjob = newjob;
         _jobqueues->jobqueue.lastjob = newjob;
      }
      else /* it is assumed that the jobqueue is not full */
      {
         _jobqueues->jobqueue.lastjob->nextjob = newjob;
         _jobqueues->jobqueue.lastjob = newjob;
      }

      _jobqueues->jobqueue.njobs++;

      SCIP_CALL( SCIPompReleaseLock(&_jobqueues->lock) );

      #pragma omp task
      jobQueueProcessJob();
   }
   else
   {
      assert(_jobqueues->ncurrentjobs < SCIPtpiGetNumThreads());

      _jobqueues->ncurrentjobs++;

      SCIP_CALL( SCIPompReleaseLock(&_jobqueues->lock) );
      /* running the new job */
      #pragma omp task firstprivate(newjob)
      executeJob(newjob);
   }

   return SCIP_OKAY;
}


/** signal a condition */
SCIP_RETCODE SCIPtpiSignalCondition(
   SCIP_CONDITION*       condition           /**< condition to signal */
   )
{
   assert( condition != NULL );

   SCIP_CALL( SCIPompAcquireLock(&condition->_lock) );

   if( condition->_waitnum > condition->_signals )
      ++condition->_signals;

   SCIP_CALL( SCIPompReleaseLock(&condition->_lock) );

   return SCIP_OKAY;
}


/** broadcase a condition */
SCIP_RETCODE SCIPtpiBroadcastCondition(
   SCIP_CONDITION*       condition           /**< broadcast a condition */
   )
{
   assert( condition != NULL );

   SCIP_CALL( SCIPompAcquireLock(&condition->_lock) );
   condition->_signals = condition->_waitnum;
   SCIP_CALL( SCIPompReleaseLock(&condition->_lock) );

   return SCIP_OKAY;
}



/** returns the number of threads */
int SCIPtpiGetNumThreads(
   )
{
   return omp_get_num_threads();
}

/** returns the thread number */
int SCIPtpiGetThreadNum(
   )
{
   return omp_get_thread_num();
}

/** creates a job for parallel processing */
SCIP_RETCODE SCIPtpiCreateJob(
   SCIP_JOB**            job,                /**< pointer to the job that will be created */
   int                   jobid,              /**< the id for the current job */
   SCIP_RETCODE          (*jobfunc)(void* args),/**< pointer to the job function */
   void*                 jobarg              /**< the job's argument */
   )
{
   SCIP_ALLOC( BMSallocMemory(job) );

   (*job)->jobid = jobid;
   (*job)->jobfunc = jobfunc;
   (*job)->args = jobarg;
   (*job)->nextjob = NULL;

   return SCIP_OKAY;
}

/** get a new job id for the new set of submitted jobs */
int SCIPtpiGetNewJobID(
   void
   )
{
   static int currentjobid = 0;
   int jobid;

   #pragma omp atomic capture
   jobid = ++currentjobid;

   return jobid;
}

/** submit a job for parallel processing; the return value is a globally defined status */
SCIP_RETCODE SCIPtpiSubmitJob(
   SCIP_JOB*             job,                /**< pointer to the job to be submitted */
   SCIP_SUBMITSTATUS*    status              /**< pointer to store the submit status */
   )
{
   assert(_jobqueues != NULL);

   *status = SCIP_SUBMIT_SUCCESS;
   SCIP_CALL( jobQueueAddJob(job) );

   return SCIP_OKAY;
}


/** check whether a job is running */
static
SCIP_Bool isJobRunning(
   int                   jobid               /**< job id to check */
   )
{
   int i;

   if( _jobqueues->ncurrentjobs > 0 )
   {
      for( i = 0; i < _jobqueues->nthreads; ++i )
      {
         if( _jobqueues->currentjobs[i] != NULL && _jobqueues->currentjobs[i]->jobid == jobid )
            return TRUE;
      }
   }

   return FALSE;
}


/** check whether a job is waiting */
static
SCIP_Bool isJobWaiting(
   int                   jobid               /**< job id to check */
   )
{
   if( _jobqueues->jobqueue.njobs > 0 )
   {
      SCIP_JOB* currjob;
      currjob = _jobqueues->jobqueue.firstjob;

      do
      {
         if( currjob->jobid == jobid )
            return TRUE;

         if( currjob == _jobqueues->jobqueue.lastjob )
            break;

         currjob = currjob->nextjob;
      }
      while( TRUE ); /*lint !e506*/
   }

   return FALSE;
}


/** blocks until all jobs of the given jobid have finished
 *  and then returns the smallest SCIP_RETCODE of all the jobs */
SCIP_RETCODE SCIPtpiCollectJobs(
   int                   jobid               /**< the jobid of the jobs to wait for */
   )
{
   SCIP_RETCODE retcode;

   retcode = SCIP_OKAY;
   SCIP_CALL( SCIPompAcquireLock(&_jobqueues->lock) );

   while( isJobRunning(jobid) || isJobWaiting(jobid) )
   {
      SCIP_CALL( SCIPompWaitCondition(&_jobqueues->jobfinished, &_jobqueues->lock) );
   }

   if( _jobqueues->finishedjobs.njobs > 0 )
   {
      SCIP_JOB* currjob = _jobqueues->finishedjobs.firstjob;
      SCIP_JOB* prevjob = NULL;

      /* finding the location of the processed job in the currentjobs queue */
      do
      {
         if( currjob->jobid == jobid )
         {
            SCIP_JOB* nextjob;

            /* if the job has the right jobid collect its retcode, remove it from the finished job list, and free it */
            retcode = MIN(retcode, currjob->retcode);

            /* removing the finished job from finished jobs list */
            if( currjob == _jobqueues->finishedjobs.firstjob )
               _jobqueues->finishedjobs.firstjob = currjob->nextjob;
            else
            {
               if( prevjob != NULL )
                  prevjob->nextjob = currjob->nextjob; /*lint !e613*/
            }

            if( currjob == _jobqueues->finishedjobs.lastjob )
               _jobqueues->finishedjobs.lastjob = prevjob;

            _jobqueues->finishedjobs.njobs--;

            /* update currjob and free finished job; prevjob stays the same */
            nextjob = currjob->nextjob;
            BMSfreeMemory(&currjob);
            currjob = nextjob;
         }
         else
         {
            prevjob = currjob;
            currjob = prevjob->nextjob;
         }
      }
      while( prevjob != _jobqueues->finishedjobs.lastjob );
   }
   else
   {
      /* given jobid was not submitted */
      printf("err1");
      retcode = SCIP_ERROR;
   }

   SCIP_CALL_ABORT( SCIPompReleaseLock(&_jobqueues->lock) );

   return retcode;
}

/** initializes tpi */
SCIP_RETCODE SCIPtpiInit(
   int                   nthreads,           /**< the number of threads to be used */
   int                   queuesize,          /**< the size of the queue */
   SCIP_Bool             blockwhenfull       /**< should the queue block when full */
   )
{
   omp_set_num_threads(nthreads);
   assert(_jobqueues == NULL);

   SCIP_CALL( createJobQueue(nthreads, queuesize, blockwhenfull) );

   return SCIP_OKAY;
}

/** deinitializes tpi */
SCIP_RETCODE SCIPtpiExit(
   void
   )
{
   assert(_jobqueues != NULL);
   assert(_jobqueues->finishedjobs.njobs == 0);
   assert(_jobqueues->jobqueue.njobs == 0);
   assert(_jobqueues->ncurrentjobs == 0);

   SCIP_CALL( freeJobQueue() );

   return SCIP_OKAY;
}


/*
 * locks
 */

/** initializes the given lock */
SCIP_RETCODE SCIPtpiInitLock(
   SCIP_LOCK**           lock                /**< the lock */
   )
{
   assert(lock != NULL);

   SCIP_ALLOC( BMSallocMemory(lock) );
   omp_init_lock(&(*lock)->lock);
   return SCIP_OKAY;
}

/** destroys the given lock */
void SCIPtpiDestroyLock(
   SCIP_LOCK**           lock                /**< the lock */
   )
{
   assert(lock != NULL);

   omp_destroy_lock(&(*lock)->lock);
   BMSfreeMemory(lock);
}

/** acquires the given lock */
SCIP_RETCODE SCIPtpiAcquireLock(
   SCIP_LOCK*            lock                /**< the lock */
   )
{
   omp_set_lock(&lock->lock);
   return SCIP_OKAY;
}

/** releases the given lock */
SCIP_RETCODE SCIPtpiReleaseLock(
   SCIP_LOCK*            lock                /**< the lock */
   )
{
   omp_unset_lock(&lock->lock);
   return SCIP_OKAY;
}


/*
 * conditions
 */

/** initializes the given condition variable */
SCIP_RETCODE SCIPtpiInitCondition(
   SCIP_CONDITION**      condition           /**< condition to be created and initialized */
   )
{
   assert(condition != NULL);

   SCIP_ALLOC( BMSallocMemory(condition) );

   omp_init_lock(&(*condition)->_lock);
   (*condition)->_waiters = 0;
   (*condition)->_waitnum = 0;
   (*condition)->_signals = 0;

   return SCIP_OKAY;
}

/** destroys the given condition variable */
void SCIPtpiDestroyCondition(
   SCIP_CONDITION**      condition           /**< condition to be destroyed and freed */
   )
{
   assert((*condition)->_waiters == 0);
   assert((*condition)->_waitnum == 0);
   assert((*condition)->_signals == 0);

   omp_destroy_lock(&(*condition)->_lock);

   BMSfreeMemory(condition);
}

/** indicate whether a working TPI is available */
SCIP_Bool SCIPtpiIsAvailable(void)
{
   return TRUE;
}

/** get name of library that the TPI interfaces to */
void SCIPtpiGetLibraryName(
   char*                 name,               /**< buffer to store name */
   int                   namesize            /**< length of name buffer */
   )
{
   assert(name != NULL);

   (void) SCIPsnprintf(name, namesize, "OpenMP %d", _OPENMP);  /*lint !e40*/
}

/** get description of library that the TPI interfaces to */
void SCIPtpiGetLibraryDesc(
   char*                 desc,               /**< buffer to store description */
   int                   descsize            /**< length of description */
   )
{
   assert(desc != NULL);

   (void) SCIPsnprintf(desc, descsize, "shared-memory multiprocessing library (openmp.org)");
}
