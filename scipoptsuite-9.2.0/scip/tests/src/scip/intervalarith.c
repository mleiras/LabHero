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

/**@file   intervalarith.c
 * @brief  unit tests to check that bug1861 doesn't appear
 * @author Stefan Vigerske
 */

#include "scip/intervalarith.h"
#include "include/scip_test.h"
#include <stdio.h>

Test(intervalarith, issue1861)
{
   SCIP_Real             infinity;
   SCIP_INTERVAL         resultant;
   SCIP_Real             ax;
   SCIP_Real             ay;
   SCIP_Real             axy;
   SCIP_Real             bx;
   SCIP_Real             by;
   SCIP_INTERVAL         rhs;
   SCIP_INTERVAL         xbnds;
   SCIP_INTERVAL         ybnds;

   infinity = 1e43;
   ax = 12;
   ay = 27;
   axy = -36;
   bx = -32;
   by = 48;
   SCIPintervalSetBounds(&rhs, -21.333333336466665741681936197, -21.3333333341333322152877371991);
   SCIPintervalSetBounds(&xbnds, -10.0382009139778674011722614523, 0.0);
   SCIPintervalSetBounds(&ybnds, -7.93110393120117596055251851794, -0.537524704319278456843278490851);

   // the quadratic equation
   // ax*x^2 + ay*y^2 + axy*x*y + bx*x + by*y \in rhs
   // does not have a solution for x \in xbnds and y \in ybnds
   // however, relaxing rhs very slightly gives a solution
   // SCIPintervalSolveBivariateQuadExpressionAllScalar() is expected to either
   // - figure out that there is no solution, or
   // - return compute some bounds because it decided to relax the bounds a bit
   // However, it is not supposed to throw an assert (#1861).

   SCIPintervalSolveBivariateQuadExpressionAllScalar(
      infinity,           /**< value for infinity in interval arithmetics */
      &resultant,          /**< buffer where to store result of operation */
      ax,                 /**< square coefficient of x */
      ay,                 /**< square coefficient of y */
      axy,                /**< bilinear coefficients */
      bx,                 /**< linear coefficient of x */
      by,                 /**< linear coefficient of y */
      rhs,                /**< right-hand-side of equation */
      xbnds,              /**< bounds on x */
      ybnds               /**< bounds on y */
      );
 }

/** some tests for SCIPintervalSolveUnivariateQuadExpression */
Test(intervalarith, solveuniquad)
{
   SCIP_INTERVAL resultant;
   SCIP_INTERVAL expect;
   SCIP_INTERVAL sqrcoef;
   SCIP_INTERVAL lincoef;
   SCIP_INTERVAL rhs;
   SCIP_INTERVAL xbnds;

   SCIPintervalSetEntire(SCIP_DEFAULT_INFINITY, &xbnds);

   // test with lincoef = 0
   SCIPintervalSet(&lincoef, 0.0);
   for( sqrcoef.inf = -2.0; sqrcoef.inf <= 2.0; ++sqrcoef.inf )
   {
      sqrcoef.sup = sqrcoef.inf;

      for( rhs.inf = -2.0; rhs.inf <= 2.0; rhs.inf += 2.0 )
      {
         for( rhs.sup = rhs.inf + 1.0; rhs.sup <= 3.0; rhs.sup += 1.0 )
         {
            /* sqrcoef * x^2 = rhs -> x^2 = rhs/sqrcoef */
            SCIPintervalSolveUnivariateQuadExpression(SCIP_DEFAULT_INFINITY, &resultant, sqrcoef, lincoef, rhs, xbnds);
            /* printf("%g x^2 in [%g,%g] -> [%g,%g]\n", sqrcoef.inf, rhs.inf, rhs.sup, resultant.inf, resultant.sup); */

            if( sqrcoef.inf != 0.0 )
            {
               SCIPintervalDivScalar(SCIP_DEFAULT_INFINITY, &expect, rhs, sqrcoef.inf);
               SCIPintervalSquareRoot(SCIP_DEFAULT_INFINITY, &expect, expect);
               if( !SCIPintervalIsEmpty(SCIP_DEFAULT_INFINITY, expect) )
                  expect.inf = -expect.sup;
            }
            else if( rhs.inf <= 0.0 && rhs.sup >= 0.0 )
            {
               SCIPintervalSetEntire(SCIP_DEFAULT_INFINITY, &expect);
            }
            else
               SCIPintervalSetEmpty(&expect);
            /* printf("%g*x^2 = [%g,%g]; expect [%g,%g], got [%g,%g]\n", sqrcoef.inf, rhs.inf, rhs.sup, expect.inf, expect.sup, resultant.inf, resultant.sup); */

            cr_assert(SCIPintervalIsEmpty(SCIP_DEFAULT_INFINITY, resultant) == SCIPintervalIsEmpty(SCIP_DEFAULT_INFINITY, expect));
            cr_assert(SCIPintervalIsEntire(SCIP_DEFAULT_INFINITY, resultant) == SCIPintervalIsEntire(SCIP_DEFAULT_INFINITY, expect));
            if( !SCIPintervalIsEmpty(SCIP_DEFAULT_INFINITY, expect) && !SCIPintervalIsEntire(SCIP_DEFAULT_INFINITY, expect) )
            {
               cr_assert_float_eq(resultant.inf, expect.inf, 1e-12, "unexpected x.inf %g for %g*x^2=[%g,%g], expected %g", resultant.inf, sqrcoef.inf, rhs.inf, rhs.sup, expect.inf);
               cr_assert_float_eq(resultant.sup, expect.sup, 1e-12, "unexpected x.sup %g for %g*x^2=[%g,%g], expected %g", resultant.sup, sqrcoef.inf, rhs.inf, rhs.sup, expect.sup);
            }
         }
      }
   }

   // test with lincoef != 0
   for( lincoef.inf = -6.0; lincoef.inf <= 6.0; lincoef.inf += 3.0 )
   {
      lincoef.sup = lincoef.inf;

      for( rhs.sup = -2.0; rhs.sup <= 2.0; rhs.sup += 2.0 )
      {
         rhs.inf = rhs.sup-1.0;
         SCIPintervalSet(&sqrcoef, 0.5);
         /* 0.5*x^2 + lincoef * x = rhs -> x = -lincoef +- sqrt(2*rhs + lincoef^2)
          * thus: empty for 2*rhs+lincoef^2 < 0
          */

         SCIPintervalSolveUnivariateQuadExpression(SCIP_DEFAULT_INFINITY, &resultant, sqrcoef, lincoef, rhs, xbnds);

         if( 2.0*rhs.sup + lincoef.inf * lincoef.inf < 0.0 )
            cr_assert(SCIPintervalIsEmpty(SCIP_DEFAULT_INFINITY, resultant));
         else
         {
            expect.inf = -lincoef.inf - sqrt(2.0*rhs.sup + lincoef.inf*lincoef.inf);
            expect.sup = -lincoef.inf + sqrt(2.0*rhs.sup + lincoef.inf*lincoef.inf);
            cr_assert_float_eq(resultant.inf, expect.inf, 1e-12, "unexpected x.inf %g for 0.5*x^2%+g*x=[%g,%g], expected %g", resultant.inf, lincoef.inf, rhs.inf, rhs.sup, expect.inf);
            cr_assert_float_eq(resultant.sup, expect.sup, 1e-12, "unexpected x.sup %g for 0.5*x^2%+g*x=[%g,%g], expected %g", resultant.sup, lincoef.inf, rhs.inf, rhs.sup, expect.sup);
         }

         SCIPintervalSet(&sqrcoef, -0.5);
         /* -0.5*x^2 + lincoef * x = rhs -> x = lincoef +- sqrt(-2*rhs + lincoef^2)
          * thus: empty for -2*rhs+lincoef^2 < 0
          */

         SCIPintervalSolveUnivariateQuadExpression(SCIP_DEFAULT_INFINITY, &resultant, sqrcoef, lincoef, rhs, xbnds);

         if( -2.0*rhs.inf + lincoef.inf * lincoef.inf < 0.0 )
            cr_assert(SCIPintervalIsEmpty(SCIP_DEFAULT_INFINITY, resultant));
         else
         {
            expect.inf = lincoef.inf - sqrt(-2.0*rhs.inf + lincoef.inf*lincoef.inf);
            expect.sup = lincoef.inf + sqrt(-2.0*rhs.inf + lincoef.inf*lincoef.inf);
            cr_assert_float_eq(resultant.inf, expect.inf, 1e-12, "unexpected x.inf %g for -0.5*x^2%+g*x=[%g,%g], expected %g", resultant.inf, lincoef.inf, rhs.inf, rhs.sup, expect.inf);
            cr_assert_float_eq(resultant.sup, expect.sup, 1e-12, "unexpected x.sup %g for -0.5*x^2%+g*x=[%g,%g], expected %g", resultant.sup, lincoef.inf, rhs.inf, rhs.sup, expect.sup);
         }
      }
   }

   /* 0.5x^2-x has a minimum at x=1 (value -0.5) and maxima at the bounds of x
    * further, {x : 0.5x^2-x >= 0} = [-infty,0] v [2,infty]
    * further, {x : 0.5x^2-x in [0,1.5]} = [-1,0] v [2,3]
    * further, {x : 0.5x^2-x >= 1.5} = [-infty,-1] v [3,infty]
    */
   SCIPintervalSet(&sqrcoef, 0.5);
   SCIPintervalSet(&lincoef, -1.0);
   SCIPintervalSetBounds(&rhs, 0.0, SCIP_DEFAULT_INFINITY);
   SCIPintervalSolveUnivariateQuadExpression(SCIP_DEFAULT_INFINITY, &resultant, sqrcoef, lincoef, rhs, xbnds);
   cr_assert_eq(resultant.inf, -SCIP_DEFAULT_INFINITY);
   cr_assert_eq(resultant.sup, +SCIP_DEFAULT_INFINITY);

   SCIPintervalSetBounds(&rhs, 0.0, 1.5);
   SCIPintervalSolveUnivariateQuadExpression(SCIP_DEFAULT_INFINITY, &resultant, sqrcoef, lincoef, rhs, xbnds);
   cr_assert_float_eq(resultant.inf, -1.0, 1e-12);
   cr_assert_float_eq(resultant.sup,  3.0, 1e-12);

   SCIPintervalSetBounds(&rhs, 1.5, SCIP_DEFAULT_INFINITY);
   SCIPintervalSolveUnivariateQuadExpression(SCIP_DEFAULT_INFINITY, &resultant, sqrcoef, lincoef, rhs, xbnds);
   cr_assert_eq(resultant.inf, -SCIP_DEFAULT_INFINITY);
   cr_assert_eq(resultant.sup, +SCIP_DEFAULT_INFINITY);

   /* now, let's look only for solutions x >= 0:
    * {x >= 0 : 0.5x^2-x >= 0} = [0,0] v [2,infty]
    * {x >= 0 : 0.5x^2-x in [0,1.5]} = [0,0] v [2,3]
    * {x >= 0 : 0.5x^2-x >= 1.5} = [3,infty]
    */
   SCIPintervalSetBounds(&xbnds, 0.0, SCIP_DEFAULT_INFINITY);

   SCIPintervalSetBounds(&rhs, 0.0, SCIP_DEFAULT_INFINITY);
   SCIPintervalSolveUnivariateQuadExpression(SCIP_DEFAULT_INFINITY, &resultant, sqrcoef, lincoef, rhs, xbnds);
   cr_assert_float_eq(resultant.inf, 0.0, 1e-12);
   cr_assert_eq(resultant.sup, +SCIP_DEFAULT_INFINITY);

   SCIPintervalSetBounds(&rhs, 0.0, 1.5);
   SCIPintervalSolveUnivariateQuadExpression(SCIP_DEFAULT_INFINITY, &resultant, sqrcoef, lincoef, rhs, xbnds);
   cr_assert_float_eq(resultant.inf, 0.0, 1e-12);
   cr_assert_float_eq(resultant.sup, 3.0, 1e-12);

   SCIPintervalSetBounds(&rhs, 1.5, SCIP_DEFAULT_INFINITY);
   SCIPintervalSolveUnivariateQuadExpression(SCIP_DEFAULT_INFINITY, &resultant, sqrcoef, lincoef, rhs, xbnds);
   cr_assert_float_eq(resultant.inf, 3.0, 1e-12);
   cr_assert_eq(resultant.sup, +SCIP_DEFAULT_INFINITY);


   /* now, let's look only for solutions x >= 1:
    * {x >= 1 : 0.5x^2-x >= 0} = [2,infty]
    * {x >= 1 : 0.5x^2-x in [0,1.5]} = [2,3]
    * {x >= 1 : 0.5x^2-x >= 1.5} = [3,infty]
    */
   SCIPintervalSetBounds(&xbnds, 1.0, SCIP_DEFAULT_INFINITY);

   SCIPintervalSetBounds(&rhs, 0.0, SCIP_DEFAULT_INFINITY);
   SCIPintervalSolveUnivariateQuadExpression(SCIP_DEFAULT_INFINITY, &resultant, sqrcoef, lincoef, rhs, xbnds);
   cr_assert_float_eq(resultant.inf, 2.0, 1e-12);
   cr_assert_eq(resultant.sup, +SCIP_DEFAULT_INFINITY);

   SCIPintervalSetBounds(&rhs, 0.0, 1.5);
   SCIPintervalSolveUnivariateQuadExpression(SCIP_DEFAULT_INFINITY, &resultant, sqrcoef, lincoef, rhs, xbnds);
   cr_assert_float_eq(resultant.inf, 2.0, 1e-12);
   cr_assert_float_eq(resultant.sup, 3.0, 1e-12);

   SCIPintervalSetBounds(&rhs, 1.5, SCIP_DEFAULT_INFINITY);
   SCIPintervalSolveUnivariateQuadExpression(SCIP_DEFAULT_INFINITY, &resultant, sqrcoef, lincoef, rhs, xbnds);
   cr_assert_float_eq(resultant.inf, 3.0, 1e-12);
   cr_assert_eq(resultant.sup, +SCIP_DEFAULT_INFINITY);


  /* similarly, we can look only for solutions x <= -1:
   * {x <= -1 : 0.5x^2-x >= 0} = [-infty,-1]
   * {x <= -1 : 0.5x^2-x in [0,1.5]} = [-1,-1]
   * {x <= -1 : 0.5x^2-x >= 1.5} = [-infty,-1]
   */
  SCIPintervalSetBounds(&xbnds, -SCIP_DEFAULT_INFINITY, -1.0);

  SCIPintervalSetBounds(&rhs, 0.0, SCIP_DEFAULT_INFINITY);
  SCIPintervalSolveUnivariateQuadExpression(SCIP_DEFAULT_INFINITY, &resultant, sqrcoef, lincoef, rhs, xbnds);
  cr_assert_eq(resultant.inf, -SCIP_DEFAULT_INFINITY);
  cr_assert_float_eq(resultant.sup, -1.0, 1e-12);

  SCIPintervalSetBounds(&rhs, 0.0, 1.5);
  SCIPintervalSolveUnivariateQuadExpression(SCIP_DEFAULT_INFINITY, &resultant, sqrcoef, lincoef, rhs, xbnds);
  cr_assert_float_eq(resultant.inf, -1.0, 1e-12);
  cr_assert_float_eq(resultant.sup, -1.0, 1e-12);

  SCIPintervalSetBounds(&rhs, 1.5, SCIP_DEFAULT_INFINITY);
  SCIPintervalSolveUnivariateQuadExpression(SCIP_DEFAULT_INFINITY, &resultant, sqrcoef, lincoef, rhs, xbnds);
  cr_assert_eq(resultant.inf, -SCIP_DEFAULT_INFINITY);
  cr_assert_float_eq(resultant.sup, -1.0, 1e-12);


  /* a linear equation with interval coefficients should be solved well:
   * {x : [-1,1]*x >= 1.0} = [-infty,-1] v [1,infty]
   * {x : [-1,1]*x <= 1.0} = [-infty,infty]
   * {x : [-1,1]*x <=-1.0} = [-infty,-1] v [1,infty]
   * {x : [-1,1]*x >=-1.0} = [-infty,infty]
   *
   * {x : [0,1]*x >= 1.0} = [1,infty]
   * {x : [-1,0]*x >= 1.0} = [-infty,-1]
   * {x : [0,1]*x >= 0.0} = [-infty,infty]
   */
  SCIPintervalSetEntire(SCIP_DEFAULT_INFINITY, &xbnds);
  SCIPintervalSet(&sqrcoef, 0.0);
  SCIPintervalSetBounds(&lincoef, -1.0, 1.0);
  SCIPintervalSetBounds(&rhs, 1.0, SCIP_DEFAULT_INFINITY);
  SCIPintervalSolveUnivariateQuadExpression(SCIP_DEFAULT_INFINITY, &resultant, sqrcoef, lincoef, rhs, xbnds);
  cr_assert_eq(resultant.inf, -SCIP_DEFAULT_INFINITY);
  cr_assert_eq(resultant.sup,  SCIP_DEFAULT_INFINITY);

  SCIPintervalSetBounds(&rhs, -SCIP_DEFAULT_INFINITY, 1.0);
  SCIPintervalSolveUnivariateQuadExpression(SCIP_DEFAULT_INFINITY, &resultant, sqrcoef, lincoef, rhs, xbnds);
  cr_assert_eq(resultant.inf, -SCIP_DEFAULT_INFINITY);
  cr_assert_eq(resultant.sup,  SCIP_DEFAULT_INFINITY);

  SCIPintervalSetBounds(&rhs, -SCIP_DEFAULT_INFINITY, -1.0);
  SCIPintervalSolveUnivariateQuadExpression(SCIP_DEFAULT_INFINITY, &resultant, sqrcoef, lincoef, rhs, xbnds);
  cr_assert_eq(resultant.inf, -SCIP_DEFAULT_INFINITY);
  cr_assert_eq(resultant.sup,  SCIP_DEFAULT_INFINITY);

  SCIPintervalSetBounds(&rhs, -1.0, SCIP_DEFAULT_INFINITY);
  SCIPintervalSolveUnivariateQuadExpression(SCIP_DEFAULT_INFINITY, &resultant, sqrcoef, lincoef, rhs, xbnds);
  cr_assert_eq(resultant.inf, -SCIP_DEFAULT_INFINITY);
  cr_assert_eq(resultant.sup,  SCIP_DEFAULT_INFINITY);

  SCIPintervalSetBounds(&lincoef, 0.0, 1.0);
  SCIPintervalSetBounds(&rhs, 1.0, SCIP_DEFAULT_INFINITY);
  SCIPintervalSolveUnivariateQuadExpression(SCIP_DEFAULT_INFINITY, &resultant, sqrcoef, lincoef, rhs, xbnds);
  cr_assert_float_eq(resultant.inf, 1.0, 1e-12);
  cr_assert_eq(resultant.sup, SCIP_DEFAULT_INFINITY);

  SCIPintervalSetBounds(&lincoef, -1.0, 0.0);
  SCIPintervalSetBounds(&rhs, 1.0, SCIP_DEFAULT_INFINITY);
  SCIPintervalSolveUnivariateQuadExpression(SCIP_DEFAULT_INFINITY, &resultant, sqrcoef, lincoef, rhs, xbnds);
  cr_assert_eq(resultant.inf, -SCIP_DEFAULT_INFINITY);
  cr_assert_float_eq(resultant.sup, -1.0, 1e-12);

  SCIPintervalSetBounds(&lincoef, 0.0, 1.0);
  SCIPintervalSetBounds(&rhs, 0.0, SCIP_DEFAULT_INFINITY);
  SCIPintervalSolveUnivariateQuadExpression(SCIP_DEFAULT_INFINITY, &resultant, sqrcoef, lincoef, rhs, xbnds);
  cr_assert(SCIPintervalIsEntire(SCIP_DEFAULT_INFINITY, resultant));

  /* providing bounds on x should result in better results:
   * {x in [-infty,0]: [-1,1]*x >= 1.0} = [-infty,-1]
   * {x in [0,+infty]: [-1,1]*x >= 1.0} = [1,infty]
   * {x in [-infty,0]: [-1,1]*x <=-1.0} = [-infty,-1]
   * {x in [0,+infty]: [-1,1]*x <=-1.0} = [1,infty]
   */

  SCIPintervalSetBounds(&lincoef, -1.0, 1.0);
  SCIPintervalSetBounds(&rhs, 1.0, SCIP_DEFAULT_INFINITY);
  SCIPintervalSetBounds(&xbnds, -SCIP_DEFAULT_INFINITY, 0.0);
  SCIPintervalSolveUnivariateQuadExpression(SCIP_DEFAULT_INFINITY, &resultant, sqrcoef, lincoef, rhs, xbnds);
  cr_assert_eq(resultant.inf, -SCIP_DEFAULT_INFINITY);
  cr_assert_float_eq(resultant.sup, -1.0, 1e-12);

  SCIPintervalSetBounds(&xbnds, 0.0, SCIP_DEFAULT_INFINITY);
  SCIPintervalSolveUnivariateQuadExpression(SCIP_DEFAULT_INFINITY, &resultant, sqrcoef, lincoef, rhs, xbnds);
  cr_assert_float_eq(resultant.inf, 1.0, 1e-12);
  cr_assert_eq(resultant.sup, SCIP_DEFAULT_INFINITY);

  SCIPintervalSetBounds(&rhs, -SCIP_DEFAULT_INFINITY, -1.0);
  SCIPintervalSetBounds(&xbnds, -SCIP_DEFAULT_INFINITY, 0.0);
  SCIPintervalSolveUnivariateQuadExpression(SCIP_DEFAULT_INFINITY, &resultant, sqrcoef, lincoef, rhs, xbnds);
  cr_assert_eq(resultant.inf, -SCIP_DEFAULT_INFINITY);
  cr_assert_float_eq(resultant.sup, -1.0, 1e-12);

  SCIPintervalSetBounds(&xbnds, 0.0, SCIP_DEFAULT_INFINITY);
  SCIPintervalSolveUnivariateQuadExpression(SCIP_DEFAULT_INFINITY, &resultant, sqrcoef, lincoef, rhs, xbnds);
  cr_assert_float_eq(resultant.inf, 1.0, 1e-12);
  cr_assert_eq(resultant.sup, SCIP_DEFAULT_INFINITY);

  /* some more tests with lincoef=0 */
  /* [0,1]*x^2 = 1 -> x^2 = [1,infty] -> x = [-infty,-1] v [1,infty]*/
  SCIPintervalSetBounds(&sqrcoef, 0.0, 1.0);
  SCIPintervalSet(&lincoef, 0.0);
  SCIPintervalSetBounds(&rhs, 1.0, 1.0);
  SCIPintervalSetEntire(SCIP_DEFAULT_INFINITY, &xbnds);
  SCIPintervalSolveUnivariateQuadExpression(SCIP_DEFAULT_INFINITY, &resultant, sqrcoef, lincoef, rhs, xbnds);
  cr_assert(SCIPintervalIsEntire(SCIP_DEFAULT_INFINITY, resultant));

  /* [0,1]*x^2 = 1, x >= 0 -> x >= 1 */
  SCIPintervalSetBounds(&sqrcoef, 0.0, 1.0);
  SCIPintervalSet(&lincoef, 0.0);
  SCIPintervalSetBounds(&rhs, 1.0, 1.0);
  SCIPintervalSetBounds(&xbnds, 0.0, SCIP_DEFAULT_INFINITY);
  SCIPintervalSolveUnivariateQuadExpression(SCIP_DEFAULT_INFINITY, &resultant, sqrcoef, lincoef, rhs, xbnds);
  cr_assert_float_eq(resultant.inf, 1.0, 1e-12);
  cr_assert_eq(resultant.sup, SCIP_DEFAULT_INFINITY);

  /* [0,1]*x^2 = 1, x <= 0 -> x <= -1 */
  SCIPintervalSetBounds(&sqrcoef, 0.0, 1.0);
  SCIPintervalSet(&lincoef, 0.0);
  SCIPintervalSetBounds(&rhs, 1.0, 1.0);
  SCIPintervalSetBounds(&xbnds, -SCIP_DEFAULT_INFINITY, -1.0);
  SCIPintervalSolveUnivariateQuadExpression(SCIP_DEFAULT_INFINITY, &resultant, sqrcoef, lincoef, rhs, xbnds);
  cr_assert_eq(resultant.inf, -SCIP_DEFAULT_INFINITY);
  cr_assert_float_eq(resultant.sup, -1.0, 1e-12);
}

/** some tests for x*y in rhs */
Test(intervalarith, xy)
{
   SCIP_INTERVAL xbnds;
   SCIP_INTERVAL ybnds;
   SCIP_INTERVAL rhs;
   SCIP_INTERVAL resultant;
   SCIP_INTERVAL sqrcoef;

   /* x*y == 1.0 for x,y in [-1,1] -> x = [-1,-1] v [1,1] */
   SCIPintervalSetBounds(&xbnds, -1.0, 1.0);
   SCIPintervalSetBounds(&ybnds, -1.0, 1.0);
   SCIPintervalSetBounds(&rhs, 1.0, 1.0);
   SCIPintervalSolveBivariateQuadExpressionAllScalar(SCIP_DEFAULT_INFINITY, &resultant, 0.0, 0.0, 1.0, 0.0, 0.0, rhs, xbnds, ybnds);
   cr_assert_eq(resultant.inf, -1.0);
   cr_assert_eq(resultant.sup,  1.0);

   /* with x in [-1,0], this should then give x = [-1,-1] */
   SCIPintervalSetBounds(&xbnds, -1.0, 0.0);
   SCIPintervalSolveBivariateQuadExpressionAllScalar(SCIP_DEFAULT_INFINITY, &resultant, 0.0, 0.0, 1.0, 0.0, 0.0, rhs, xbnds, ybnds);
   cr_assert_eq(resultant.inf, -1.0);
   cr_assert_float_eq(resultant.sup, -1.0, 1e-12);

   /* and with x in [0,1], this should then give x = [1,1] */
   SCIPintervalSetBounds(&xbnds, 0.0, 1.0);
   SCIPintervalSolveBivariateQuadExpressionAllScalar(SCIP_DEFAULT_INFINITY, &resultant, 0.0, 0.0, 1.0, 0.0, 0.0, rhs, xbnds, ybnds);
   cr_assert_float_eq(resultant.inf, 1.0, 1e-12);
   cr_assert_eq(resultant.sup, 1.0);

   /* x*y >= 1.0 for x,y in [-1,1] -> x = [-1,-1] */
   SCIPintervalSetBounds(&xbnds, -1.0, 1.0);
   SCIPintervalSetBounds(&ybnds, -1.0, 1.0);
   SCIPintervalSetBounds(&rhs, 1.0, SCIP_DEFAULT_INFINITY);
   SCIPintervalSolveBivariateQuadExpressionAllScalar(SCIP_DEFAULT_INFINITY, &resultant, 0.0, 0.0, 1.0, 0.0, 0.0, rhs, xbnds, ybnds);
   cr_assert_eq(resultant.inf, -1.0);
   cr_assert_float_eq(resultant.sup,  1.0, 1e-12);

   /* x*y >= 1.0 for x in [-1,1], y in [-1,0] -> x = [-1,-1] */
   SCIPintervalSetBounds(&ybnds, -1.0, -0.0);
   SCIPintervalSolveBivariateQuadExpressionAllScalar(SCIP_DEFAULT_INFINITY, &resultant, 0.0, 0.0, 1.0, 0.0, 0.0, rhs, xbnds, ybnds);
   cr_assert_eq(resultant.inf, -1.0);
   /* currently still gives 1 as upper bound, so cr_assert_float_eq(resultant.sup, -1.0, 1e-12); fails
    * however, SCIPintervalSolveUnivariateQuadExpression handles this better:
    */
   SCIPintervalSet(&sqrcoef, 0.0);
   SCIPintervalSolveUnivariateQuadExpression(SCIP_DEFAULT_INFINITY, &resultant, sqrcoef, ybnds, rhs, xbnds);
   cr_assert_eq(resultant.inf, -1.0);
   cr_assert_float_eq(resultant.sup, -1.0, 1e-12);

   /* similar for x*y >= 1.0 for x in [-1,1], y in [0,1] -> x = [1,1] */
   SCIPintervalSetBounds(&ybnds, 0, 1.0);
   SCIPintervalSolveBivariateQuadExpressionAllScalar(SCIP_DEFAULT_INFINITY, &resultant, 0.0, 0.0, 1.0, 0.0, 0.0, rhs, xbnds, ybnds);
   cr_assert_eq(resultant.sup, 1.0);
   /* currently still gives -1 as lower bound, so cr_assert_float_eq(resultant.inf, 1.0, 1e-12); fails
    * however, SCIPintervalSolveUnivariateQuadExpression handles this better:
    */
   SCIPintervalSet(&sqrcoef, 0.0);
   SCIPintervalSolveUnivariateQuadExpression(SCIP_DEFAULT_INFINITY, &resultant, sqrcoef, ybnds, rhs, xbnds);
   cr_assert_float_eq(resultant.inf, 1.0, 1e-12);
   cr_assert_eq(resultant.sup, 1.0);
}

Test(intervalarith, issue2250)
{
   SCIP_Real             infinity;
   SCIP_INTERVAL         resultant;
   SCIP_Real             ax;
   SCIP_Real             ay;
   SCIP_Real             axy;
   SCIP_Real             bx;
   SCIP_Real             by;
   SCIP_INTERVAL         rhs;
   SCIP_INTERVAL         xbnds;
   SCIP_INTERVAL         ybnds;

   infinity = 1e43;
   ax = 1;
   ay = 0;
   axy = 1;
   bx = -2;
   by = -6;
   SCIPintervalSetBounds(&rhs, -infinity, 0.0);
   SCIPintervalSetBounds(&xbnds, 0.0, infinity);
   SCIPintervalSetBounds(&ybnds, 0.0, infinity);

   /* x=y=4 is feasible for this equation, so x=4 should be part of the solution of this equation */
   cr_assert(ax*4*4 + bx*4 + ay*4*4 + by*4 + axy*4*4 <= 1e-12);

   SCIPintervalSolveBivariateQuadExpressionAllScalar(
      infinity,           /**< value for infinity in interval arithmetics */
      &resultant,         /**< buffer where to store result of operation */
      ax,                 /**< square coefficient of x */
      ay,                 /**< square coefficient of y */
      axy,                /**< bilinear coefficients */
      bx,                 /**< linear coefficient of x */
      by,                 /**< linear coefficient of y */
      rhs,                /**< right-hand-side of equation */
      xbnds,              /**< bounds on x */
      ybnds               /**< bounds on y */
      );

   cr_assert(resultant.inf <= 4.0);
   cr_assert(resultant.sup >= 4.0);
}

/* The fail in #2650 was caused by GCC reorganizing operations in SCIPintervalReciprocal so that divisions
 * were not evaluated with the correct rounding mode.
 * Unfortunately, I was not able to reproduce this with a single test like this
 * (build SCIP with OPT=dbg SHARED=true USRCFLAGS="-O3 -DNDEBUG -fomit-frame-pointer").
 */
Test(intervalarith, issue2650)
{
   SCIP_Real             infinity = 1.0e300;
   SCIP_INTERVAL         resultant;
   SCIP_INTERVAL         operand;
   SCIP_INTERVAL         base;
   SCIP_INTERVAL         image;

   SCIPintervalSetBounds(&base, 0.0, infinity);
   SCIPintervalSetBounds(&image, 9.0, 81.0);
   SCIPintervalPowerScalarInverse(infinity, &resultant, base, 0.2, image);
   printf("x^0.2 = [%.15g,%.15g] -> x = [%.15g,%.15g]\n", image.inf, image.sup, resultant.inf, resultant.sup);

   cr_assert(resultant.inf <= 3486784401.0);
   cr_assert(resultant.sup >= 3486784401.0);

   /* the code above failed because the 1/0.2 wasn't computed correctly: */
   SCIPintervalSetBounds(&operand, 0.2, 0.2);
   SCIPintervalReciprocal(infinity, &resultant, operand);
   printf("1/[0.2,0.2] = [%.15g,%.15g]\n", resultant.inf, resultant.sup);

   cr_assert(resultant.inf <= 5.0);
   cr_assert(resultant.sup >= 5.0);
}

#define EXPECTEQ(a,b) cr_expect_eq(a, b, "%s = %.20g != %g", #a, a, b)
#define EXPECTFEQ(a,b) cr_expect_float_eq(a, b, 1e-12, "%s = %g != %g", #a, a, b)

Test(intervalarith, sincos)
{
   SCIP_INTERVAL arg;
   SCIP_INTERVAL res;

   /* as M_PI, M_PI/2, etc are (obviously) not the exact values for pi, pi/2, etc,
    * we cannot expect to obtain sin(pi)=0, cos(pi/2)=0, etc, so these tests with tolerances
    *   even more this holds for tests against 1/sqrt(2)
    * only at 0, we can expect an exact result, i.e., sin(0)=0, cos(0)=1
    */

   /* arg.inf = 0, arg.sup = 0, pi/4, pi/2, ... 2*pi, 3*pi */
   arg.inf = 0.0;
   arg.sup = M_PI_4;
   SCIPintervalSin(SCIP_INTERVAL_INFINITY, &res, arg);
   EXPECTEQ(res.inf, 0.0);
   EXPECTFEQ(res.sup, M_SQRT1_2);

   SCIPintervalCos(SCIP_INTERVAL_INFINITY, &res, arg);
   EXPECTFEQ(res.inf, M_SQRT1_2);
   EXPECTEQ(res.sup, 1.0);


   arg.inf = 0.0;
   arg.sup = M_PI_2;
   SCIPintervalSin(SCIP_INTERVAL_INFINITY, &res, arg);
   EXPECTEQ(res.inf, 0.0);
   EXPECTEQ(res.sup, 1.0);

   SCIPintervalCos(SCIP_INTERVAL_INFINITY, &res, arg);
   EXPECTFEQ(res.inf, 0.0);
   EXPECTEQ(res.sup, 1.0);


   arg.inf = 0.0;
   arg.sup = M_PI_2 + M_PI_4;
   SCIPintervalSin(SCIP_INTERVAL_INFINITY, &res, arg);
   EXPECTEQ(res.inf, 0.0);
   EXPECTEQ(res.sup, 1.0);

   SCIPintervalCos(SCIP_INTERVAL_INFINITY, &res, arg);
   EXPECTFEQ(res.inf, -M_SQRT1_2);
   EXPECTEQ(res.sup, 1.0);


   arg.inf = 0.0;
   arg.sup = M_PI;
   SCIPintervalSin(SCIP_INTERVAL_INFINITY, &res, arg);
   EXPECTFEQ(res.inf, 0.0);
   EXPECTEQ(res.sup, 1.0);

   SCIPintervalCos(SCIP_INTERVAL_INFINITY, &res, arg);
   EXPECTEQ(res.inf, -1.0);
   EXPECTEQ(res.sup, 1.0);


   arg.inf = 0.0;
   arg.sup = M_PI + M_PI_4;
   SCIPintervalSin(SCIP_INTERVAL_INFINITY, &res, arg);
   EXPECTFEQ(res.inf, -M_SQRT1_2);
   EXPECTEQ(res.sup, 1.0);

   SCIPintervalCos(SCIP_INTERVAL_INFINITY, &res, arg);
   EXPECTEQ(res.inf, -1.0);
   EXPECTEQ(res.sup, 1.0);


   arg.inf = 0.0;
   arg.sup = M_PI + M_PI_2;
   SCIPintervalSin(SCIP_INTERVAL_INFINITY, &res, arg);
   EXPECTEQ(res.inf, -1.0);
   EXPECTEQ(res.sup, 1.0);

   SCIPintervalCos(SCIP_INTERVAL_INFINITY, &res, arg);
   EXPECTEQ(res.inf, -1.0);
   EXPECTEQ(res.sup, 1.0);


   arg.inf = 0.0;
   arg.sup = M_PI + M_PI_2 + M_PI_4;
   SCIPintervalSin(SCIP_INTERVAL_INFINITY, &res, arg);
   EXPECTEQ(res.inf, -1.0);
   EXPECTEQ(res.sup, 1.0);

   SCIPintervalCos(SCIP_INTERVAL_INFINITY, &res, arg);
   EXPECTEQ(res.inf, -1.0);
   EXPECTEQ(res.sup, 1.0);


   arg.inf = 0.0;
   arg.sup = 2*M_PI;
   SCIPintervalSin(SCIP_INTERVAL_INFINITY, &res, arg);
   EXPECTEQ(res.inf, -1.0);
   EXPECTEQ(res.sup, 1.0);

   SCIPintervalCos(SCIP_INTERVAL_INFINITY, &res, arg);
   EXPECTEQ(res.inf, -1.0);
   EXPECTEQ(res.sup, 1.0);


   arg.inf = 0.0;
   arg.sup = 3*M_PI;
   SCIPintervalSin(SCIP_INTERVAL_INFINITY, &res, arg);
   EXPECTEQ(res.inf, -1.0);
   EXPECTEQ(res.sup, 1.0);

   SCIPintervalCos(SCIP_INTERVAL_INFINITY, &res, arg);
   EXPECTEQ(res.inf, -1.0);
   EXPECTEQ(res.sup, 1.0);




   /* arg.inf = pi/4, arg.sup = pi/2, ... 2*pi, 2*pi+pi/4, 3*pi */
   arg.inf = M_PI_4;
   arg.sup = M_PI_2;
   SCIPintervalSin(SCIP_INTERVAL_INFINITY, &res, arg);
   EXPECTFEQ(res.inf, M_SQRT1_2);
   EXPECTEQ(res.sup, 1.0);

   SCIPintervalCos(SCIP_INTERVAL_INFINITY, &res, arg);
   EXPECTFEQ(res.inf, 0.0);
   EXPECTFEQ(res.sup, M_SQRT1_2);


   arg.inf = M_PI_4;
   arg.sup = M_PI_2 + M_PI_4;
   SCIPintervalSin(SCIP_INTERVAL_INFINITY, &res, arg);
   EXPECTFEQ(res.inf, M_SQRT1_2);
   EXPECTEQ(res.sup, 1.0);

   SCIPintervalCos(SCIP_INTERVAL_INFINITY, &res, arg);
   EXPECTFEQ(res.inf, -M_SQRT1_2);
   EXPECTFEQ(res.sup, M_SQRT1_2);


   arg.inf = M_PI_4;
   arg.sup = M_PI;
   SCIPintervalSin(SCIP_INTERVAL_INFINITY, &res, arg);
   EXPECTFEQ(res.inf, 0.0);
   EXPECTEQ(res.sup, 1.0);

   SCIPintervalCos(SCIP_INTERVAL_INFINITY, &res, arg);
   EXPECTEQ(res.inf, -1.0);
   EXPECTFEQ(res.sup, M_SQRT1_2);


   arg.inf = M_PI_4;
   arg.sup = M_PI + M_PI_4;
   SCIPintervalSin(SCIP_INTERVAL_INFINITY, &res, arg);
   EXPECTFEQ(res.inf, -M_SQRT1_2);
   EXPECTEQ(res.sup, 1.0);

   SCIPintervalCos(SCIP_INTERVAL_INFINITY, &res, arg);
   EXPECTEQ(res.inf, -1.0);
   EXPECTFEQ(res.sup, M_SQRT1_2);


   arg.inf = M_PI_4;
   arg.sup = M_PI + M_PI_2;
   SCIPintervalSin(SCIP_INTERVAL_INFINITY, &res, arg);
   EXPECTEQ(res.inf, -1.0);
   EXPECTEQ(res.sup, 1.0);

   SCIPintervalCos(SCIP_INTERVAL_INFINITY, &res, arg);
   EXPECTEQ(res.inf, -1.0);
   EXPECTFEQ(res.sup, M_SQRT1_2);


   arg.inf = M_PI_4;
   arg.sup = M_PI + M_PI_2 + M_PI_4;
   SCIPintervalSin(SCIP_INTERVAL_INFINITY, &res, arg);
   EXPECTEQ(res.inf, -1.0);
   EXPECTEQ(res.sup, 1.0);

   SCIPintervalCos(SCIP_INTERVAL_INFINITY, &res, arg);
   EXPECTEQ(res.inf, -1.0);
   EXPECTFEQ(res.sup, M_SQRT1_2);


   arg.inf = M_PI_4;
   arg.sup = 2*M_PI;
   SCIPintervalSin(SCIP_INTERVAL_INFINITY, &res, arg);
   EXPECTEQ(res.inf, -1.0);
   EXPECTEQ(res.sup, 1.0);

   SCIPintervalCos(SCIP_INTERVAL_INFINITY, &res, arg);
   EXPECTEQ(res.inf, -1.0);
   EXPECTEQ(res.sup, 1.0);


   arg.inf = M_PI_4;
   arg.sup = 2*M_PI + M_PI_4;
   SCIPintervalSin(SCIP_INTERVAL_INFINITY, &res, arg);
   EXPECTEQ(res.inf, -1.0);
   EXPECTEQ(res.sup, 1.0);

   SCIPintervalCos(SCIP_INTERVAL_INFINITY, &res, arg);
   EXPECTEQ(res.inf, -1.0);
   EXPECTEQ(res.sup, 1.0);


   arg.inf = M_PI_4;
   arg.sup = 3*M_PI;
   SCIPintervalSin(SCIP_INTERVAL_INFINITY, &res, arg);
   EXPECTEQ(res.inf, -1.0);
   EXPECTEQ(res.sup, 1.0);

   SCIPintervalCos(SCIP_INTERVAL_INFINITY, &res, arg);
   EXPECTEQ(res.inf, -1.0);
   EXPECTEQ(res.sup, 1.0);




   /* arg.inf = pi/2, arg.sup = pi/2+pi/4, pi/2, ... 2*pi+pi/2, 3*pi */
   arg.inf = M_PI_2;
   arg.sup = M_PI_2 + M_PI_4;
   SCIPintervalSin(SCIP_INTERVAL_INFINITY, &res, arg);
   EXPECTFEQ(res.inf, M_SQRT1_2);
   EXPECTEQ(res.sup, 1.0);

   SCIPintervalCos(SCIP_INTERVAL_INFINITY, &res, arg);
   EXPECTFEQ(res.inf, -M_SQRT1_2);
   EXPECTFEQ(res.sup, 0.0);


   arg.inf = M_PI_2;
   arg.sup = M_PI;
   SCIPintervalSin(SCIP_INTERVAL_INFINITY, &res, arg);
   EXPECTFEQ(res.inf, 0.0);
   EXPECTEQ(res.sup, 1.0);

   SCIPintervalCos(SCIP_INTERVAL_INFINITY, &res, arg);
   EXPECTEQ(res.inf, -1.0);
   EXPECTFEQ(res.sup, 0.0);


   arg.inf = M_PI_2;
   arg.sup = M_PI + M_PI_4;
   SCIPintervalSin(SCIP_INTERVAL_INFINITY, &res, arg);
   EXPECTFEQ(res.inf, -M_SQRT1_2);
   EXPECTEQ(res.sup, 1.0);

   SCIPintervalCos(SCIP_INTERVAL_INFINITY, &res, arg);
   EXPECTEQ(res.inf, -1.0);
   EXPECTFEQ(res.sup, 0.0);


   arg.inf = M_PI_2;
   arg.sup = M_PI + M_PI_2;
   SCIPintervalSin(SCIP_INTERVAL_INFINITY, &res, arg);
   EXPECTEQ(res.inf, -1.0);
   EXPECTEQ(res.sup, 1.0);

   SCIPintervalCos(SCIP_INTERVAL_INFINITY, &res, arg);
   EXPECTEQ(res.inf, -1.0);
   EXPECTFEQ(res.sup, 0.0);


   arg.inf = M_PI_2;
   arg.sup = M_PI + M_PI_2 + M_PI_4;
   SCIPintervalSin(SCIP_INTERVAL_INFINITY, &res, arg);
   EXPECTEQ(res.inf, -1.0);
   EXPECTEQ(res.sup, 1.0);

   SCIPintervalCos(SCIP_INTERVAL_INFINITY, &res, arg);
   EXPECTEQ(res.inf, -1.0);
   EXPECTFEQ(res.sup, M_SQRT1_2);


   arg.inf = M_PI_2;
   arg.sup = 2*M_PI;
   SCIPintervalSin(SCIP_INTERVAL_INFINITY, &res, arg);
   EXPECTEQ(res.inf, -1.0);
   EXPECTEQ(res.sup, 1.0);

   SCIPintervalCos(SCIP_INTERVAL_INFINITY, &res, arg);
   EXPECTEQ(res.inf, -1.0);
   EXPECTEQ(res.sup, 1.0);


   arg.inf = M_PI_4;
   arg.sup = 2*M_PI + M_PI_4;
   SCIPintervalSin(SCIP_INTERVAL_INFINITY, &res, arg);
   EXPECTEQ(res.inf, -1.0);
   EXPECTEQ(res.sup, 1.0);

   SCIPintervalCos(SCIP_INTERVAL_INFINITY, &res, arg);
   EXPECTEQ(res.inf, -1.0);
   EXPECTEQ(res.sup, 1.0);


   arg.inf = M_PI_4;
   arg.sup = 2*M_PI + M_PI_2;
   SCIPintervalSin(SCIP_INTERVAL_INFINITY, &res, arg);
   EXPECTEQ(res.inf, -1.0);
   EXPECTEQ(res.sup, 1.0);

   SCIPintervalCos(SCIP_INTERVAL_INFINITY, &res, arg);
   EXPECTEQ(res.inf, -1.0);
   EXPECTEQ(res.sup, 1.0);


   arg.inf = M_PI_4;
   arg.sup = 3*M_PI;
   SCIPintervalSin(SCIP_INTERVAL_INFINITY, &res, arg);
   EXPECTEQ(res.inf, -1.0);
   EXPECTEQ(res.sup, 1.0);

   SCIPintervalCos(SCIP_INTERVAL_INFINITY, &res, arg);
   EXPECTEQ(res.inf, -1.0);
   EXPECTEQ(res.sup, 1.0);


   /* arg.inf = -pi/4, arg.sup = 0, pi/4, pi/2, pi, 2*pi */
   arg.inf = -M_PI_4;
   arg.sup = 0.0;
   SCIPintervalSin(SCIP_INTERVAL_INFINITY, &res, arg);
   EXPECTFEQ(res.inf, -M_SQRT1_2);
   EXPECTFEQ(res.sup, 0.0);

   SCIPintervalCos(SCIP_INTERVAL_INFINITY, &res, arg);
   EXPECTFEQ(res.inf, M_SQRT1_2);
   EXPECTEQ(res.sup, 1.0);


   arg.inf = -M_PI_4;
   arg.sup = M_PI_4;
   SCIPintervalSin(SCIP_INTERVAL_INFINITY, &res, arg);
   EXPECTFEQ(res.inf, -M_SQRT1_2);
   EXPECTFEQ(res.sup, M_SQRT1_2);

   SCIPintervalCos(SCIP_INTERVAL_INFINITY, &res, arg);
   EXPECTFEQ(res.inf, M_SQRT1_2);
   EXPECTEQ(res.sup, 1.0);


   arg.inf = -M_PI_4;
   arg.sup = M_PI_2;
   SCIPintervalSin(SCIP_INTERVAL_INFINITY, &res, arg);
   EXPECTFEQ(res.inf, -M_SQRT1_2);
   EXPECTEQ(res.sup, 1.0);

   SCIPintervalCos(SCIP_INTERVAL_INFINITY, &res, arg);
   EXPECTFEQ(res.inf, 0.0);
   EXPECTEQ(res.sup, 1.0);


   arg.inf = -M_PI_4;
   arg.sup = M_PI;
   SCIPintervalSin(SCIP_INTERVAL_INFINITY, &res, arg);
   EXPECTFEQ(res.inf, -M_SQRT1_2);
   EXPECTEQ(res.sup, 1.0);

   SCIPintervalCos(SCIP_INTERVAL_INFINITY, &res, arg);
   EXPECTEQ(res.inf, -1.0);
   EXPECTEQ(res.sup, 1.0);


   arg.inf = -M_PI_4;
   arg.sup = 2*M_PI;
   SCIPintervalSin(SCIP_INTERVAL_INFINITY, &res, arg);
   EXPECTEQ(res.inf, -1.0);
   EXPECTEQ(res.sup, 1.0);

   SCIPintervalCos(SCIP_INTERVAL_INFINITY, &res, arg);
   EXPECTEQ(res.inf, -1.0);
   EXPECTEQ(res.sup, 1.0);
}
