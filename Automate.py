import os
from database import find_schema


def create_dto(model_path_dir: str, dto_root_path: str):
    for root, dirs, files in os.walk(model_path_dir):
        # print(f"length of files: {len(files)}")
        for file in files:

            with open(os.path.join(root, file)) as domain_file:
                filename, file_extension = os.path.splitext(file)
                dto_name = filename + 'DTO' + file_extension

                schema = find_schema(filename)
                if schema == -1:
                    print('file name: ', filename, ', schema: ', schema)
                    continue

                if not os.path.exists(os.path.join(dto_root_path, schema)):
                    os.mkdir(os.path.join(dto_root_path, schema))

                with open(os.path.join(dto_root_path, schema, dto_name), 'w+') as dto_file:
                    for line in domain_file:
                        if "namespace" in line:
                            line = f"namespace CNET_V7_Domain.Domain.{schema}Schema;\n"
                        if "class" in line:
                            line = line.split('\n')[:-1][0] + 'DTO'
                        if "virtual" in line:
                            continue
                        if line.isspace():
                            continue
                        dto_file.write(line)
    print(f"All DTOS Created")


def create_irepositories(model_path_dir: str, irepository_path_dir):
    irepository_sample = '''using CNET_V7_Entities.DataModels;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace CNET_V7_Repository.Contracts.SchemaNameSchema
{
    public interface IEntityNameRepository : IRepository<SafeName>
    {

    }
}
    '''
    schema = 'NotFound'

    for root, dirs, files in os.walk(model_path_dir):
        filenames = [os.path.splitext(file)[0] for file in files]
        # print(filenames)
        for name in filenames:
            schema = find_schema(name)
            if(schema.lower() != "view"):
                if not os.path.exists(os.path.join(irepository_path_dir, schema)):
                    os.mkdir(os.path.join(irepository_path_dir, schema))

                repo_name = 'I' + name + 'Repository'
                with open(os.path.join(irepository_path_dir, schema, repo_name + '.cs'), 'w+') as file:
                    # let me replace it
                    safe_model_name = name
                    if name.lower() in ['delegate', 'range', 'route']:
                        safe_model_name = f'CNET_V7_Entities.DataModels.{name}'

                    file.write(irepository_sample.replace('EntityName', name).replace('SchemaName', schema).replace(
                    'SafeName', safe_model_name))
    print(" All Irepository Files Are Created")


def create_irepository_manager(model_path_dir: str, irepository_manger_file_path: str):
    implementation_sample = '''THE_USING_STATEMENT
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
    '''
    using_statement = ''
    the_declaration = ''
    using_printed_schemas = []
    with open(irepository_manger_file_path, 'w+') as manager:
        for root, dirs, files in os.walk(model_path_dir):
            
            for file in files:
                model_name, file_extension = os.path.splitext(file)
                if(find_schema(model_name).lower() != 'view'):
                    the_declaration += f'\n\t\tI{model_name}Repository {model_name} ' + '{ get; }\n'

                    if find_schema(model_name) not in using_printed_schemas:
                        using_printed_schemas.append(find_schema(model_name))
                        using_statement += f'using CNET_V7_Repository.Contracts.{find_schema(model_name)}Schema;\n'

            manager.write(
                implementation_sample.replace('THE_USING_STATEMENT', using_statement).replace('THE_DECLARATION',
                                                                                              the_declaration))

    print(f"Irepository manager created")


def create_irepository_implementation(model_path_dir: str, irepository_implementation_root: str):
    implementation_sample = '''using CNET_V7_Repository.Contracts;
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

        '''

    for root, dirs, files in os.walk(model_path_dir):
        filenames = [os.path.splitext(file)[0] for file in files]
        # print(filenames)
        for name in filenames:
            schema = find_schema(name)
            if(schema.lower() != "view"):
                if not os.path.exists(os.path.join(irepository_implementation_root, schema)):
                    os.mkdir(os.path.join(irepository_implementation_root, schema))

                # repo_name = 'I' + name + 'Repository'
                with open(os.path.join(irepository_implementation_root, schema, name + 'Repository.cs'), 'w+') as file:
                    # let me replace it
                    safe_model_name = name
                    if name.lower() in ['delegate', 'range', 'route']:
                        safe_model_name = f'CNET_V7_Entities.DataModels.{name}'

                    file.write(
                        implementation_sample.replace('SAFE_MODEL_NAME', safe_model_name).replace('MODEL_NAME',
                                                                                                name).replace(
                            "SCHEMA_NAME", schema))
    print(" All Repository Implementation Files Are Created")


def create_repository_manager(model_path_dir: str, repository_manager_file_path: str):
    repository_manager_design = '''using CNET_V7_Entities.Data;
using CNET_V7_Repository.Contracts;
THE_USING_STATEMENT
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

        THE_LAZY_DECLARATION

        public RepositoryManager(CnetV7DbContext repositoryContext)
        {
            _repositoryContext = repositoryContext;
            THE_LAZY_CTOR
        }

        public async Task EndTransaction()
        {
            await _repositoryContext.Database.CommitTransactionAsync();
        }

        public void Save() => _repositoryContext.SaveChanges();
        THE_LAZY_INSTANTIATION
    }
}
    '''
    the_using_statement = ''
    the_lazy_declaration = ''
    the_lazy_ctor = ''
    the_lazy_instantiation = ''

    using_printed_schemas = []
    with open(repository_manager_file_path, 'w+') as repository_manager:
        for root, dirs, files in os.walk(model_path_dir):
            for file in files:
                model_name, file_extension = os.path.splitext(file)
                schema = find_schema(model_name)
                if(schema.lower() != 'view'):
                    if schema not in using_printed_schemas:
                        using_printed_schemas.append(schema)
                        the_using_statement += f'using CNET_V7_Repository.Contracts.{schema}Schema;\nusing CNET_V7_Repository.Implementation.{schema}Schema;\n'
                    if schema == -1:
                        print("schema not found: ", model_name)

                    the_lazy_declaration += f'\n\t\tprivate readonly Lazy<I{model_name}Repository> _{model_name[0].lower() + model_name[1:]}Repository;'
                    the_lazy_ctor += f'\n\t\t\t_{model_name[0].lower() + model_name[1:]}Repository = new Lazy<I{model_name}Repository>(()=>new {model_name}Repository(repositoryContext));'
                    the_lazy_instantiation += f'\n\t\tpublic I{model_name}Repository {model_name} => _{model_name[0].lower() + model_name[1:]}Repository.Value;'
        final_design = repository_manager_design.replace('THE_USING_STATEMENT', the_using_statement).replace(
            'THE_LAZY_DECLARATION', the_lazy_declaration).replace('THE_LAZY_CTOR', the_lazy_ctor).replace(
            'THE_LAZY_INSTANTIATION', the_lazy_instantiation)
        repository_manager.write(final_design)
    print(f"Repository manager created")


def create_iservice_manager(model_path_dir: str, iservice_manager_file_path: str):
    iservice_manager_init = '''THE_USING_STATEMENT
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace CNET_V7_Service.Contracts
{
    public interface IServiceManager
    {
THE_DECLARATION
    }
}

    '''
    the_using_statement = ''
    the_declaration = ''
    using_printed_schemas = []
    with open(iservice_manager_file_path, 'w+') as iservice_manager:
        for root, dirs, files in os.walk(model_path_dir):
            for file in files:
                model_name, file_extension = os.path.splitext(file)
                if find_schema(model_name) not in using_printed_schemas:
                    using_printed_schemas.append(find_schema(model_name))
                    the_using_statement += f'using CNET_V7_Service.Contracts.{find_schema(model_name)}Schema;\n'
                the_declaration += f'\t\tI{model_name}Service {model_name[0].lower() + model_name[1:]}Service ' + \
                    '{ get; }\n'
        iservice_manager.write(
            iservice_manager_init.replace('THE_USING_STATEMENT', the_using_statement).replace('THE_DECLARATION',
                                                                                              the_declaration))
    print("IServiceManager.cs file created.")


def create_iservice(model_path_dir: str, iservice_root_dir: str):
    iservice_sample = '''using CNET_V7_Domain.DataModels.SCHEMASchema;
using CNET_V7_Entities.DataModels;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace CNET_V7_Service.Contracts.SCHEMASchema
{
    public interface IMODEL_NAMEService : IService<MODEL_NAMEDTO>
    {

    }
}'''

    for root, dirs, files in os.walk(model_path_dir):
        filenames = [os.path.splitext(file)[0] for file in files]
        name = 'mahtot'
        # print(filenames)
        for name in filenames:
            schema = find_schema(name)

            if not os.path.exists(os.path.join(iservice_root_dir, schema)):
                os.mkdir(os.path.join(iservice_root_dir, schema))

            file_name = 'I' + name + 'Service'
            with open(os.path.join(iservice_root_dir, schema, file_name + '.cs'), 'w+') as file:
                # let me replace it
                file.write(iservice_sample.replace(
                    'SCHEMA', schema).replace('MODEL_NAME', name))
    print(" All IService Files Are Created")


def create_service_manager(model_path_dir: str, service_manager_file_path: str):
    repository_manager_design = '''using AutoMapper;
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

    '''
    the_using_statement = ''
    the_lazy_declaration = ''
    the_lazy_ctor = ''
    the_lazy_instantiation = ''

    using_printed_schemas = []
    with open(service_manager_file_path, 'w+') as repository_manager:
        for root, dirs, files in os.walk(model_path_dir):
            for file in files:
                model_name, file_extension = os.path.splitext(file)
                schema = find_schema(model_name)
                if schema not in using_printed_schemas:
                    using_printed_schemas.append(schema)
                    the_using_statement += f'using CNET_V7_Service.Contracts.{schema}Schema;\nusing CNET_V7_Service.Implementation.{schema}Schema;\n'
                if schema == -1:
                    print("schema not found: ", model_name)

                the_lazy_declaration += f'\n\t\tprivate readonly Lazy<I{model_name}Service> _{model_name[0].lower() + model_name[1:]}Service;'

                the_lazy_ctor += f'\n\t\t\t_{model_name[0].lower() + model_name[1:]}Service = new Lazy<I{model_name}Service>(()=>new {model_name}Service(repositoryManager, logger, mapper));'

                the_lazy_instantiation += f'\n\t\tpublic I{model_name}Service {model_name[0].lower() + model_name[1:]}Service => _{model_name[0].lower() + model_name[1:]}Service.Value;'
        # so we can write it
        final_design = repository_manager_design.replace('THE_USING_STATEMENT', the_using_statement).replace(
            'THE_LAZY_DECLARATION', the_lazy_declaration).replace('THE_LAZY_CTOR', the_lazy_ctor).replace(
            'THE_LAZY_INSTANTIATION', the_lazy_instantiation)
        repository_manager.write(final_design)
    print(f"Service manager created")


def create_iservice_implementation(model_path_dir: str, iservice_implementation_root: str):
    implementation_sample = '''using AutoMapper;
using CNET_V7_Domain.DataModels.SCHEMA_NAMESchema;
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
            '''

    for root, dirs, files in os.walk(model_path_dir):
        filenames = [os.path.splitext(file)[0] for file in files]
        # print(filenames)
        for name in filenames:
            schema = find_schema(name)

            if not os.path.exists(os.path.join(iservice_implementation_root, schema)):
                os.mkdir(os.path.join(iservice_implementation_root, schema))

            # repo_name = 'I' + name + 'Repository'
            with open(os.path.join(iservice_implementation_root, schema, name + 'Service.cs'), 'w+') as file:
                # let me replace it
                file.write(implementation_sample.replace('SAFE_MODEL_NAME', safe_model_name(name)).replace('MODEL_NAME',
                                                                                                           name).replace(
                    'SCHEMA_NAME', schema).replace('LOWER_START_SAFE',
                                                   safe_model_name(name)[0].lower() + safe_model_name(name)[1:]))
    print(" All Service Implementation Files Are Created")

# todo: unwanted endpoints in the view controllers like transaction_view!


def create_controllers(model_path_dir: str, controller_root: str):
    implementation_sample = '''using CNET_V7_Domain.Domain.SCHEMASchema;
using CNET_V7_Entities.DataModels;
using CNET_V7_Service.Contracts;
using Microsoft.AspNetCore.Mvc;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace CNET_V7_Presentation.BaseControllers.SCHEMASchema;

[Route("api/[controller]")]
[ApiController]
public class MODEL_NAMEController : ControllerBase
{
    private readonly IService<SAFE_MODEL_NAME, MODEL_NAMEDTO> _commonService;

    public MODEL_NAMEController(IService<SAFE_MODEL_NAME, MODEL_NAMEDTO> commonService)
    {
        _commonService = commonService;
    }

    [HttpGet("{id}")]
    public async Task<IActionResult> GetMODEL_NAMEById(int id)
    {
        var response = await _commonService.FindById(id);
        if (response.Success) return Ok(response.Data);
        return BadRequest(response.Ex.ToString());
    }

    [HttpGet]
    public async Task<IActionResult> GetAllMODEL_NAMEs()
    {
        var response = await _commonService.FindAll(trackChanges: false);
        if(response.Success)
            return Ok(response.Data);
        return BadRequest(response.Message);
    }

    [HttpPost]
    public async Task<IActionResult> CreateMODEL_NAME([FromBody] MODEL_NAMEDTO PARAMETER)
    {
        if (PARAMETER is null)
            return BadRequest("MODEL_NAME_CAMILE is null");
        var response = await _commonService.Create(PARAMETER);
        if (response.Success)
            return Ok(response.Data);
        return BadRequest(response.Ex.ToString());
    }

    [HttpPut]
    public async Task<IActionResult> UpdateMODEL_NAME([FromBody] MODEL_NAMEDTO PARAMETER)
    {
        if (PARAMETER is null) return BadRequest("MODEL_NAME_CAMILE is null");
        var response = await _commonService.Update(PARAMETER);
        if(response.Success) return Ok(response.Data);
        return BadRequest(response.Ex.ToString());
    }

    [HttpDelete("{id}")]
    public async Task<IActionResult> DeleteMODEL_NAME(int id)
    {
        var response = await _commonService.Delete(id);
        if (response.Success)
            return NoContent();
        return BadRequest(response.Ex.ToString());
    }

    [HttpGet("filter")]
    public async Task<IActionResult> GetMODEL_NAMEByCondition([FromQuery] Dictionary<string, string> queryParameters)
    {
        var response = await _commonService.FindByCondition(queryParameters, trackChanges: false);
        if (response.Success)
            return Ok(response.Data);
        return BadRequest(response.Message);
    }
}
'''

    view_implementation_sample = '''using CNET_V7_Domain.Domain.SCHEMASchema;
using CNET_V7_Entities.DataModels;
using CNET_V7_Service.Contracts;
using Microsoft.AspNetCore.Mvc;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace CNET_V7_Presentation.BaseControllers.SCHEMASchema;

[Route("api/[controller]")]
[ApiController]
public class MODEL_NAMEController : ControllerBase
{
    private readonly IService<SAFE_MODEL_NAME, MODEL_NAMEDTO> _commonService;

    public MODEL_NAMEController(IService<SAFE_MODEL_NAME, MODEL_NAMEDTO> commonService)
    {
        _commonService = commonService;
    }

    [HttpGet("{id}")]
    public async Task<IActionResult> GetMODEL_NAMEById(int id)
    {
        var response = await _commonService.FindById(id);
        if (response.Success) return Ok(response.Data);
        return BadRequest(response.Ex.ToString());
    }

    [HttpGet]
    public async Task<IActionResult> GetAllMODEL_NAMEs()
    {
        var response = await _commonService.FindAll(trackChanges: false);
        if(response.Success)
            return Ok(response.Data);
        return BadRequest(response.Message);
    }

    [HttpGet("filter")]
    public async Task<IActionResult> GetMODEL_NAMEByCondition([FromQuery] Dictionary<string, string> queryParameters)
    {
        var response = await _commonService.FindByCondition(queryParameters, trackChanges: false);
        if (response.Success)
            return Ok(response.Data);
        return BadRequest(response.Message);
    }
}
'''

    for root, dirs, files in os.walk(model_path_dir):
        filenames = [os.path.splitext(file)[0] for file in files]
        # print(filenames)
        for model_name in filenames:
            schema = find_schema(model_name)

            if not os.path.exists(os.path.join(controller_root, schema)):
                os.mkdir(os.path.join(controller_root, schema))

            # repo_name = 'I' + name + 'Repository'
            with open(os.path.join(controller_root, schema, model_name + 'Controller.cs'), 'w+') as file:
                # let me replace it
                parameter = model_name[0].lower() + model_name[1:]
                if model_name.lower() == 'delegate':
                    parameter = 'delegateObj'
                elif model_name.lower() == 'range':
                    parameter = 'rangeObj'
                if(schema.lower() == "view"):
                    file.write(
                        view_implementation_sample.replace(
                            'MODEL_NAME_CAMILE', model_name[0].lower() + model_name[1:])
                        .replace('SAFE_MODEL_NAME', safe_model_name(model_name))
                        .replace('MODEL_NAME', (model_name))
                        .replace('SCHEMA', schema)
                        .replace('PARAMETER', parameter))
                else:
                    file.write(
                        implementation_sample.replace(
                            'MODEL_NAME_CAMILE', model_name[0].lower() + model_name[1:])
                        .replace('SAFE_MODEL_NAME', safe_model_name(model_name))
                        .replace('MODEL_NAME', (model_name))
                        .replace('SCHEMA', schema)
                        .replace('PARAMETER', parameter))

    print(" All Controller Implementation Files Are Created")


def configure_mapping(model_path_dir: str, mapping_file_path: str):
    mapping_init = '''using AutoMapper;
THE_USING_STATEMENT
using CNET_V7_Entities.DataModels;

namespace CNET_V7_API.MappingProfile
{
    public class MappingProfile : Profile
    {
        public MappingProfile() {
            CreateMap<Account, AccountDTO>().ReverseMap();
THE_CONFIGURATION
        } 
    }
}

        '''
    the_using_statement = ''
    the_configuration = ''
    using_printed_schemas = []
    with open(mapping_file_path, 'w+') as mapping_file:
        for _, _, files in os.walk(model_path_dir):
            for file in files:
                model_name, _ = os.path.splitext(file)
                if find_schema(model_name) not in using_printed_schemas:
                    using_printed_schemas.append(find_schema(model_name))
                    the_using_statement += f'using CNET_V7_Domain.Domain.{find_schema(model_name)}Schema;\n'
                the_configuration += f'\t\t\tCreateMap<{safe_model_name(model_name)}, {model_name}DTO>().ReverseMap();\n'

        mapping_file.write(
            mapping_init.replace('THE_USING_STATEMENT', the_using_statement).replace('THE_CONFIGURATION',
                                                                                     the_configuration))
    print("Mapping.cs file created.")


def safe_model_name(model_name: str):
    if model_name.lower() in ['delegate', 'range', 'route']:
        return f'CNET_V7_Entities.DataModels.{model_name}'
    return model_name
