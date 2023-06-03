using AutoMapper;
using CNET_V7_Domain.Domain.SCHEMA_NAMESchema;
using CNET_V7_Entities.DataModels;
using CNET_V7_Logger;
using CNET_V7_Repository.Contracts;
using CNET_V7_Service.Contracts.SCHEMA_NAMESchema;
using CNET_V7_Service.Contracts;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Linq.Expressions;
using CNET_V7_Domain.Misc;
using Azure;

namespace CNET_V7_Service.Implementation.SCHEMA_NAMESchema
{
    public class MODEL_NAMEService : IMODEL_NAMEService
    {
        private readonly IRepositoryManager _repository;
        private readonly ILoggerManager _logger;
        private readonly IMapper _mapper;

        public MODEL_NAMEService(IRepositoryManager repository, ILoggerManager logger, IMapper mapper)
        {
            _repository = repository;
            _logger = logger;
            _mapper = mapper;
        }

        public async Task<ResponseModel<MODEL_NAMEDTO>> Create(MODEL_NAMEDTO entity)
        {
            try
            {
                //map dto to entity
                var LOWER_START_SAFE = _mapper.Map<SAFE_MODEL_NAME>(entity);

                //fetch entity obj
                var createdObj = await _repository.MODEL_NAME.Create(LOWER_START_SAFE);

                //map fetched entity to dto
                var returnedObj = _mapper.Map<MODEL_NAMEDTO>(createdObj);

                //return response object

                return new ResponseModel<MODEL_NAMEDTO>() { Success = true, Data = returnedObj }; ;
            }
            catch (Exception e)
            {
                _logger.LogError(e.Message);
                return new ResponseModel<MODEL_NAMEDTO> () { Success = false, Ex = e, Message = e.Message };
            }
        }

        public async Task<ResponseModel<MODEL_NAMEDTO>> Delete(int id)
        {
            try
            {
                var res = await _repository.MODEL_NAME.Delete(id);
                var returnedObj = _mapper.Map<MODEL_NAMEDTO>(res);
                return new ResponseModel<MODEL_NAMEDTO>() { Success = true, Data = returnedObj };
            }
            catch (Exception e)
            {
                _logger.LogError(e.Message);
                return new ResponseModel<MODEL_NAMEDTO>() { Success = false, Ex = e, Message = e.Message };
            }
        }

        public async Task<ResponseModel<IEnumerable<MODEL_NAMEDTO>>> FindAll(bool trackChanges)
        {
            try
            {
                var result = await _repository.MODEL_NAME.FindAll(trackChanges);
                var returnedObj = _mapper.Map<IEnumerable<MODEL_NAMEDTO>>(result);
                return new ResponseModel<IEnumerable<MODEL_NAMEDTO>>() { Success = true, Data = returnedObj };
            }
            catch (Exception e)
            {
                _logger.LogError(e.Message);
                return new ResponseModel<IEnumerable<MODEL_NAMEDTO>>() { Success = false, Ex = e, Message = e.Message };
            }
        }

        public async Task<ResponseModel<MODEL_NAMEDTO>> FindById(int id)
        {
            try
            {
                var result = await _repository.MODEL_NAME.FindById(id);
                var returnedObj = _mapper.Map<MODEL_NAMEDTO>(result);
                return new ResponseModel<MODEL_NAMEDTO>() { Success = true, Data = returnedObj };
            }
            catch (Exception e)
            {
                _logger.LogError(e.Message);
                return new ResponseModel<MODEL_NAMEDTO>() { Success = false, Ex = e, Message = e.Message };
            }
        }

        public async Task<ResponseModel<MODEL_NAMEDTO>> Update(MODEL_NAMEDTO entity)
        {
            try
            {
                var LOWER_START_SAFE = _mapper.Map<SAFE_MODEL_NAME>(entity);
                var updatedObject = await _repository.MODEL_NAME.Update(LOWER_START_SAFE);
                var returnedObj = _mapper.Map<MODEL_NAMEDTO>(updatedObject);
                return new ResponseModel<MODEL_NAMEDTO>() { Success = true, Data = returnedObj }; ;
            }
            catch (Exception e)
            {
                _logger.LogError(e.Message);
                return new ResponseModel<MODEL_NAMEDTO>() { Success = false, Ex = e, Message = e.Message };
            }
        }
    }
}