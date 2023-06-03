using CNET_V7_Repository.Contracts;
using Microsoft.Identity.Client;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using CNET_V7_Entities.DataModels;
using CNET_V7_Repository.Contracts.SCHEMA_NAMESchema;
using Microsoft.EntityFrameworkCore;
using CNET_V7_Entities.Data;

namespace CNET_V7_Repository.Implementation.SCHEMA_NAMESchema
{
    public class MODEL_NAMERepository : Repository<SAFE_MODEL_NAME>, IMODEL_NAMERepository
    {
        public MODEL_NAMERepository(CnetV7DbContext context) : base(context)
        {
        }
    }
}