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

/**@file   tpi_none.c
 * @ingroup TASKINTERFACE
 * @brief  the interface functions for dummy tpi
 * @author Stephen J. Maher
 * @author Leona Gottwald
 * @author Marc Pfetsch
 */

/*---+----1----+----2----+----3----+----4----+----5----+----6----+----7----+----8----+----9----+----0----+----1----+----2*/

#include "tpi/tpi.h"
#include "scip/pub_misc.h"

/* do not define struct SCIP_Lock and struct SCIP_Condition, since they are not used */

/*
 * locks
 */

/** initializes the given lock */
SCIP_RETCODE SCIPtpiInitLock(
   SCIP_LOCK**           lock                /**< the lock */
   )
{
   assert(lock != NULL);
   *lock = NULL;

   return SCIP_OKAY;
}

/** destroys the given lock */
void SCIPtpiDestroyLock(
   SCIP_LOCK**           lock                /**< the lock */
   )
{
   assert(lock != NULL);
   *lock = NULL;
}

/** acquires the given lock */
SCIP_RETCODE SCIPtpiAcquireLock(
   SCIP_LOCK*            lock                /**< the lock */
   )
{  /*lint --e{715}*/
   return SCIP_OKAY;
}

/** releases the given lock */
SCIP_RETCODE SCIPtpiReleaseLock(
   SCIP_LOCK*            lock                /**< the lock */
   )
{  /*lint --e{715}*/
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
   *condition = NULL;

   return SCIP_OKAY;
}

/** destroys the given condition variable */
void SCIPtpiDestroyCondition(
   SCIP_CONDITION**      condition           /**< condition to be destroyed and freed */
   )
{
   assert(condition != NULL);
   *condition = NULL;
}

/** signals one waiting thread */
SCIP_RETCODE SCIPtpiSignalCondition(
   SCIP_CONDITION*       condition           /**< the condition variable to signal */
   )
{  /*lint --e{715}*/
   return SCIP_OKAY;
}

/** signals all waiting threads */
SCIP_RETCODE SCIPtpiBroadcastCondition(
   SCIP_CONDITION*       condition           /**< the condition variable to broadcast */
   )
{  /*lint --e{715}*/
   return SCIP_OKAY;
}

/** waits on a condition variable. The given lock must be held by the caller and will
 *  be held when this function returns.
 */
SCIP_RETCODE SCIPtpiWaitCondition(
   SCIP_CONDITION*       condition,          /**< the condition variable to wait on */
   SCIP_LOCK*            lock                /**< the lock that is held by the caller */
   )
{  /*lint --e{715}*/
   return SCIP_OKAY;
}

/** returns the number of threads */
int SCIPtpiGetNumThreads(
   void
   )
{
   return 1;
}

/** returns the thread number */
int SCIPtpiGetThreadNum(
   void
   )
{
   return 0;
}



/*
 * other functions
 */

/** creates a job for parallel processing */
SCIP_RETCODE SCIPtpiCreateJob(
   SCIP_JOB**            job,                /**< pointer to the job that will be created */
   int                   jobid,              /**< the id for the current job */
   SCIP_RETCODE          (*jobfunc)(void* args),/**< pointer to the job function */
   void*                 jobarg              /**< the job's argument */
   )
{
   SCIP_UNUSED( job );
   SCIP_UNUSED( jobid );
   SCIP_UNUSED( jobfunc );
   SCIP_UNUSED( jobarg );

   return SCIP_ERROR;
}

/** get a new job id for a new set of jobs */
int SCIPtpiGetNewJobID(
   void
   )
{
   return 0;
}

/** submit a job for parallel processing; the return value is a globally defined status */
SCIP_RETCODE SCIPtpiSubmitJob(
   SCIP_JOB*             job,                /**< pointer to the job to be submitted */
   SCIP_SUBMITSTATUS*    status              /**< pointer to store the job's submit status */
   )
{
   SCIP_UNUSED( job );
   SCIP_UNUSED( status );

   return SCIP_ERROR;
}

/** Blocks until all jobs with the given jobid have finished and then returns the smallest SCIP_RETCODE of all the
 *  jobs */
SCIP_RETCODE SCIPtpiCollectJobs(
   int                   jobid               /**< the id of the jobs to collect */
   )
{
   SCIP_UNUSED( jobid );

   return SCIP_ERROR;
}

/** initializes tpi */
SCIP_RETCODE SCIPtpiInit(
   int         nthreads,                     /**< the number of threads to be used */
   int         queuesize,                    /**< the size of the queue */
   SCIP_Bool   blockwhenfull                 /**< should the queue block when full */
   )
{
   SCIP_UNUSED( nthreads );
   SCIP_UNUSED( queuesize );
   SCIP_UNUSED( blockwhenfull );

   return SCIP_ERROR;
}

/** deinitializes the tpi */
SCIP_RETCODE SCIPtpiExit(
   void
   )
{
   return SCIP_ERROR;
}

/** indicate whether a working TPI is available */
SCIP_Bool SCIPtpiIsAvailable(void)
{
   return FALSE;
}

/** get name of library that the TPI interfaces to */
void SCIPtpiGetLibraryName(
   char*                 name,               /**< buffer to store name */
   int                   namesize            /**< length of name buffer */
   )
{
   assert(name != NULL);

   (void) SCIPsnprintf(name, namesize, "none");
}

/** get description of library that the TPI interfaces to */
void SCIPtpiGetLibraryDesc(
   char*                 desc,               /**< buffer to store description */
   int                   descsize            /**< length of description */
   )
{
   assert(desc != NULL);
   assert(descsize >= 1);

   *desc = '\0';
}
