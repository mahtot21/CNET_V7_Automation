using AutoMapper;
using CNET_V7_Logger;
using CNET_V7_Repository.Contracts;
using CNET_V7_Service.Contracts;
THE_USING_STATEMENT
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace CNET_V7_Service.Implementation
{
    public class ServiceManager : IServiceManager
    {
        THE_LAZY_DECLARATION
        public ServiceManager(IRepositoryManager repositoryManager, ILoggerManager logger, IMapper mapper)
        {
            THE_LAZY_CTOR
        }

        THE_LAZY_INSTANTIATION
    }
}