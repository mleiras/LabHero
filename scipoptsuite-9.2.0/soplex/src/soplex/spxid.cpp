/* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */
/*                                                                           */
/*                  This file is part of the class library                   */
/*       SoPlex --- the Sequential object-oriented simPlex.                  */
/*                                                                           */
/*  Copyright (c) 1996-2024 Zuse Institute Berlin (ZIB)                      */
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
/*  along with SoPlex; see the file LICENSE. If not email to soplex@zib.de.  */
/*                                                                           */
/* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */

#include <stdlib.h>
#include <assert.h>

#include "soplex/spxid.h"
#include "soplex/exceptions.h"

namespace soplex
{
SPxColId::SPxColId(const DataKey& p_key)
   : DataKey(p_key)
{
   info = SPxId::COL_ID;
}

SPxColId::SPxColId(const SPxId& p_key)
   : DataKey(p_key)
{
   assert(!p_key.isSPxRowId());

   info = SPxId::COL_ID;
}

SPxRowId::SPxRowId(const DataKey& p_key)
   : DataKey(p_key)
{
   info = SPxId::ROW_ID;
}

SPxRowId::SPxRowId(const SPxId& p_key)
   : DataKey(p_key)
{
   assert(!p_key.isSPxColId());

   info = SPxId::ROW_ID;
}

std::ostream& operator<<(std::ostream& os, const SPxId& id)
{
   switch(id.type())
   {
   case SPxId::ROW_ID:
      os << "row ";
      break;

   case SPxId::COL_ID :
      os << "col ";
      break;

   case SPxId::INVALID :
      os << "Invalid ";
      break;

   default :
      throw SPxInternalCodeException("XSPXID01 This should never happen.");
   }

   os << id.idx << " (" << id.info << ")";

   return os;
}

} // namespace soplex
