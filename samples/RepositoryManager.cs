using CNET_V7_Entities.Data;
using CNET_V7_Repository.Contracts;
THE_USING_STATEMENTS
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace CNET_V7_Repository.Implementation
{
    public class RepositoryManager : IRepositoryManager
    {
        private readonly CnetV7DbContext _repositoryContext;
        THE_LAZY_DECLARATIONS

        public RepositoryManager(CnetV7DbContext repositoryContext)
        {
            _repositoryContext = repositoryContext;
            THE_LAZY_INITIALIZATIONS
        }

        // we are not longer using it so
        //public async Task EndTransaction()
        //{
        //    await _repositoryContext.Database.CommitTransactionAsync();
        //}

        public void Save() => _repositoryContext.SaveChanges();
        THE_LAZY_INSTANTIATIONS
    }
}