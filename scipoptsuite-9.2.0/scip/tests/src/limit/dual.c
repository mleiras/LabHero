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

/**@file   dual.c
 * @brief  unit tests for dual limit
 * @author Dominik Kamp
 */

#include "scip/scip.h"
#include "scip/scipdefplugins.h"
#include "include/scip_test.h"

/** GLOBAL VARIABLES **/
static SCIP* scip = NULL;

/* TEST SUITE */
static
void setup(void)
{
   /* initialize SCIP */
   SCIP_CALL( SCIPcreate(&scip) );
   SCIP_CALL( SCIPincludeDefaultPlugins(scip) );
}

static
void teardown(void)
{
   /* free SCIP */
   SCIP_CALL( SCIPfree(&scip) );
   /* check for memory leaks */
   cr_assert_eq(BMSgetMemoryUsed(), 0, "There is a memory leak!");
}

TestSuite(dual, .init = setup, .fini = teardown);

Test(dual, duallimit_min, .description = "tests dual limit for minimization")
{
   const SCIP_Real target = 66;
   SCIP_Real duallimit;

   cr_assert_not_null(scip);
   SCIP_CALL( SCIPsetRealParam(scip, "limits/dual", target) );
   /* turn on aggressive separators to get more limit candidates */
   SCIP_CALL( SCIPsetSeparating(scip, SCIP_PARAMSETTING_AGGRESSIVE, TRUE) );
   /* turn off heuristics to oppose optimality before the limit */
   SCIP_CALL( SCIPsetHeuristics(scip, SCIP_PARAMSETTING_OFF, TRUE) );
   SCIP_CALL( SCIPreadProb(scip, "../check/instances/MIP/rgn.mps", NULL) );
   SCIP_CALL( SCIPsolve(scip) );

   cr_assert_eq(SCIPgetStatus(scip), SCIP_STATUS_DUALLIMIT, "SCIP terminated with status %d but should have terminated with status %d", SCIPgetStatus(scip), SCIP_STATUS_DUALLIMIT);
   duallimit = SCIPgetDualbound(scip);
   cr_assert_geq(duallimit, target, "Dual bound is %f but should be at least %f", duallimit, target);
   SCIP_CALL( SCIPgetRealParam(scip, "limits/dual", &duallimit) );
   cr_assert_eq(duallimit, target, "Dual limit is %f but should be %f", duallimit, target);
}

Test(dual, duallimit_max, .description = "tests dual limit for maximization")
{
   const SCIP_Real target = 30;
   SCIP_Real duallimit;

   cr_assert_not_null(scip);
   SCIP_CALL( SCIPsetRealParam(scip, "limits/dual", target) );
   /* turn on aggressive separators to get more limit candidates */
   SCIP_CALL( SCIPsetSeparating(scip, SCIP_PARAMSETTING_AGGRESSIVE, TRUE) );
   /* turn off heuristics to oppose optimality before the limit */
   SCIP_CALL( SCIPsetHeuristics(scip, SCIP_PARAMSETTING_OFF, TRUE) );
   SCIP_CALL( SCIPreadProb(scip, "../check/instances/Symmetry/packorb_1-FullIns_3.cip", NULL) );
   SCIP_CALL( SCIPsolve(scip) );

   cr_assert_eq(SCIPgetStatus(scip), SCIP_STATUS_DUALLIMIT, "SCIP terminated with status %d but should have terminated with status %d", SCIPgetStatus(scip), SCIP_STATUS_DUALLIMIT);
   duallimit = SCIPgetDualbound(scip);
   cr_assert_leq(duallimit, target, "Dual bound is %f but should be at most %f", duallimit, target);
   SCIP_CALL( SCIPgetRealParam(scip, "limits/dual", &duallimit) );
   cr_assert_eq(duallimit, target, "Dual limit is %f but should be %f", duallimit, target);
}
