THE_USING_STATEMENT
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace CNET_V7_Repository.Contracts
{
    public interface IRepositoryManager
    {
        Task<IDbContextTransaction> StartTransaction();
        void Save();
        THE_DECLARATION
    }
}