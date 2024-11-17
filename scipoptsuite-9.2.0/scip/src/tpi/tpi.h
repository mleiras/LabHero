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

/**@file   tpi.h
 * @ingroup TASKINTERFACE
 * @brief  the type definitions for the SCIP parallel interface
 * @author Leona Gottwald
 * @author Stephen J. Maher
 * @author Marc Pfetsch
 */

/*---+----1----+----2----+----3----+----4----+----5----+----6----+----7----+----8----+----9----+----0----+----1----+----2*/

#ifndef __TPI_H__
#define __TPI_H__

#include "scip/def.h"
#include "scip/type_retcode.h"
#include "tpi/type_tpi.h"

/** creates and initializes the given lock */
SCIP_EXPORT
SCIP_RETCODE SCIPtpiInitLock(
   SCIP_LOCK**           lock                /**< the lock */
   );

/** destroys and frees the given lock */
SCIP_EXPORT
void SCIPtpiDestroyLock(
   SCIP_LOCK**           lock                /**< the lock */
   );

/** acquires the given lock */
SCIP_EXPORT
SCIP_RETCODE SCIPtpiAcquireLock(
   SCIP_LOCK*            lock                /**< the lock */
   );

/** releases the given lock */
SCIP_EXPORT
SCIP_RETCODE SCIPtpiReleaseLock(
   SCIP_LOCK*            lock                /**< the lock */
   );

/** initializes the given condition variable */
SCIP_EXPORT
SCIP_RETCODE SCIPtpiInitCondition(
   SCIP_CONDITION**      condition           /**< condition to be created and initialized */
   );

/** destroys the given condition variable */
SCIP_EXPORT
void SCIPtpiDestroyCondition(
   SCIP_CONDITION**      condition           /**< condition to be destroyed and freed */
   );

/** signals one waiting thread */
SCIP_EXPORT
SCIP_RETCODE SCIPtpiSignalCondition(
   SCIP_CONDITION*       condition           /**< the condition variable to signal */
   );

/** signals all waiting threads */
SCIP_EXPORT
SCIP_RETCODE SCIPtpiBroadcastCondition(
   SCIP_CONDITION*       condition           /**< the condition variable to broadcast */
   );

/** waits on a condition variable. The given lock must be held by the caller and will
 *  be held when this function returns.
 */
SCIP_EXPORT
SCIP_RETCODE SCIPtpiWaitCondition(
   SCIP_CONDITION*       condition,          /**< the condition variable to wait on */
   SCIP_LOCK*            lock                /**< the lock that is held by the caller */
   );

/** returns the number of threads */
SCIP_EXPORT
int SCIPtpiGetNumThreads(
   void
   );

/** returns the thread number */
SCIP_EXPORT
int SCIPtpiGetThreadNum(
   void
   );

/** creates a job for parallel processing */
SCIP_EXPORT
SCIP_RETCODE SCIPtpiCreateJob(
   SCIP_JOB**            job,                /**< pointer to the job that will be created */
   int                   jobid,              /**< the id for the current job */
   SCIP_RETCODE          (*jobfunc)(void* args),/**< pointer to the job function */
   void*                 jobarg              /**< the job's argument */
   );

/** get a new job id for a new set of jobs */
SCIP_EXPORT
int SCIPtpiGetNewJobID(
   void
   );

/** submit a job for parallel processing; the return value is a globally defined status */
SCIP_EXPORT
SCIP_RETCODE SCIPtpiSubmitJob(
   SCIP_JOB*             job,                /**< pointer to the job to be submitted */
   SCIP_SUBMITSTATUS*    status              /**< pointer to store the job's submit status */
   );

/** blocks until all jobs of the given jobid have finished
 *  and then returns the smallest SCIP_RETCODE of all the jobs
 */
SCIP_EXPORT
SCIP_RETCODE SCIPtpiCollectJobs(
   int                   jobid               /**< the jobid of the jobs to wait for */
   );

/** initializes tpi */
SCIP_EXPORT
SCIP_RETCODE SCIPtpiInit(
   int                   nthreads,           /**< the number of threads to be used */
   int                   queuesize,          /**< the size of the queue */
   /*TODO: specify and implement behaviour of blockwhenfull flag*/
   SCIP_Bool             blockwhenfull       /**< should the queue block when full */
   );

/** deinitializes the tpi */
SCIP_EXPORT
SCIP_RETCODE SCIPtpiExit(
   void
   );

/** indicate whether a working TPI is available */
SCIP_EXPORT
SCIP_Bool SCIPtpiIsAvailable(void);

/** get name of library that the TPI interfaces to */
SCIP_EXPORT
void SCIPtpiGetLibraryName(
   char*                 name,               /**< buffer to store name */
   int                   namesize            /**< length of name buffer */
   );

/** get description of library that the TPI interfaces to */
SCIP_EXPORT
void SCIPtpiGetLibraryDesc(
   char*                 desc,               /**< buffer to store description */
   int                   descsize            /**< length of description */
   );

#endif
