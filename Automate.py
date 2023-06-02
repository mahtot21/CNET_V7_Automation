import os
from database import find_schema


def create_dto(model_path_dir: str, dto_root_path: str):
    """
    Create DTOs (Data Transfer Objects) for each file in the model path directory.

    Args:
        model_path_dir (str): Directory path where the model files are located.
        dto_root_path (str): Root directory path where the DTOs will be created.

    Returns:
        None
    """
    for root, _, files in os.walk(model_path_dir):
        # Walk through the directory tree starting from 'model_path_dir'
        # 'root' represents the current directory being traversed
        # '_' is used to ignore the subdirectories since they are not used in this code
        # 'files' contains a list of file names in the current directory
        for file in files:
            # Iterate through each file in the current directory
            file_path = os.path.join(root, file)
            # Construct the absolute file path by joining 'root' and 'file'

            with open(file_path) as domain_file:
                # Open the file for reading
                filename, file_extension = os.path.splitext(file)
                # Split the file name and extension
                # 'filename' stores the name of the file without the extension
                # 'file_extension' stores the extension of the file

                dto_name = filename + 'DTO' + file_extension
                # Generate the name for the DTO by appending 'DTO' to the original file name

                schema = find_schema(filename)
                # Call the 'find_schema' function to get the schema associated with the file
                # The 'filename' is passed as an argument to the function

                if schema == -1:
                    # If the schema is not found (indicated by -1),
                    # print a message and skip the current file
                    print(f"Skipping file: {filename}. No schema found.")
                    continue

                schema_path = os.path.join(dto_root_path, schema)
                # Construct the path where the DTO file should be created
                # by joining 'dto_root_path' and 'schema'

                if not os.path.exists(schema_path):
                    # If the schema path doesn't exist, create the directory
                    os.mkdir(schema_path)

                dto_file_path = os.path.join(schema_path, dto_name)
                # Construct the path for the DTO file by joining 'schema_path' and 'dto_name'

                with open(dto_file_path, 'w+') as dto_file:
                    # Open the DTO file for writing (create if it doesn't exist, truncate if it does)
                    for line in domain_file:
                        # Iterate through each line in the original file
                        if "namespace" in line:
                            # If the line contains "namespace",
                            # modify the line to include the schema in the namespace declaration
                            line = f"namespace CNET_V7_Domain.Domain.{schema}Schema;\n"
                        elif "class" in line:
                            # If the line contains "class",
                            # modify the line to change the class name by appending 'DTO' to it
                            line = line.split('\n')[:-1][0] + 'DTO'
                        elif "virtual" in line or line.isspace():
                            # If the line contains "virtual" or is empty (whitespace),
                            # skip the line and continue to the next iteration
                            continue
                        dto_file.write(line)
                        # Write the modified or unmodified line to the DTO file

    print("All DTOS created.")


def create_irepositories(model_path_dir: str, irepository_path_dir: str):
    """
    Create IRepository interfaces for each model file in the model path directory.

    Args:
        model_path_dir (str): Directory path where the model files are located.
        irepository_path_dir (str): Directory path where the IRepository files will be created.

    Returns:
        None
    """

    IREPOSITORY_SAMPLE = '''using CNET_V7_Entities.DataModels;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
s
namespace CNET_V7_Repository.Contracts.SchemaNameSchema
{
    public interface IEntityNameRepository : IRepository<SafeName>
    {

    }
}
'''

    for root, dirs, files in os.walk(model_path_dir):
        # Walk through the directory tree starting from 'model_path_dir'
        filenames = [os.path.splitext(file)[0] for file in files]
        # Extract the file names without extensions using list comprehension

        for name in filenames:
            # Iterate through each file name
            schema = find_schema(name)
            # Call the 'find_schema' function to get the schema associated with the file

            if schema == -1:
                # If the schema is not found (indicated by -1),
                # print a message and skip the current file
                print(f"Skipping file: {name}. No schema found.")
                continue

            if schema.lower() != "view":
                # Skip processing if the schema is "view" (case-insensitive)
                schema_dir = os.path.join(irepository_path_dir, schema)
                if not os.path.exists(schema_dir):
                    # If the schema path doesn't exist, create the directory
                    os.mkdir(schema_dir)

                repo_name = 'I' + name + 'Repository'
                # Construct the IRepository file name by appending 'I' to the model name and 'Repository' to the end

                irepository_file_path = os.path.join(schema_dir, repo_name + '.cs')
                with open(irepository_file_path, 'w+') as file:
                    # Open the IRepository file for writing (create if it doesn't exist, truncate if it does)
                    safe_model_name = safe_model_name(name)

                    irepository_content = IREPOSITORY_SAMPLE.replace('EntityName', name).replace('SchemaName', schema).replace('SafeName', safe_model_name)
                    file.write(irepository_content)
                    # Replace placeholders in the IRepository sample code with actual names

    print("All IRepository Files Are Created.")


def create_irepository_manager(model_path_dir: str, irepository_manager_file_path: str):
    """
    Create IRepositoryManager interface for the model files in the given directory.

    Args:
        model_path_dir (str): Directory path where the model files are located.
        irepository_manager_file_path (str): File path where the IRepositoryManager file will be created.

    Returns:
        None
    """
    # Define the sample code for IRepositoryManager interface
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

    # Initialize lists to store using statements and the IRepository declarations
    using_statements = []
    the_declaration = ''

    # Iterate through the files in the specified directory
    for root, dirs, files in os.walk(model_path_dir):
        for file in files:
            # Extract the model name and file extension
            model_name, file_extension = os.path.splitext(file)
            # Find the schema associated with the model
            schema = find_schema(model_name)

            if schema == -1:
                # If the schema is not found (indicated by -1),
                # print a message and skip the current file
                print(f"Skipping file: {model_name}. No schema found.")
                continue

            if schema.lower() != 'view':
                # Generate the IRepository declaration for the model
                the_declaration += f'\n\t\tI{model_name}Repository {model_name} ' + '{{ get; }}\n'

                if schema not in using_statements:
                    # Add the schema to the list of using statements if it hasn't been added already
                    using_statements.append(schema)

    # Generate the using statements by joining the schema names
    using_statement = '\n'.join([f'using CNET_V7_Repository.Contracts.{schema}Schema;' for schema in using_statements])

    # Write the IRepositoryManager code to the specified file path
    with open(irepository_manager_file_path, 'w+') as manager:
        manager.write(
            implementation_sample.replace('THE_USING_STATEMENT', using_statement).replace('THE_DECLARATION',
                                                                                          the_declaration))

    print(f"IRepositoryManager created.")


def create_irepository_implementation(model_path_dir: str, irepository_implementation_root: str):
    """
    Create IRepository implementation files for the model files in the given directory.

    Args:
        model_path_dir (str): Directory path where the model files are located.
        irepository_implementation_root (str): Root directory path where the IRepository implementation files will be created.

    Returns:
        None
    """
    implementation_template = '''using CNET_V7_Repository.Contracts;
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

    # Walk through the directory tree starting from the model path directory
    for root, dirs, files in os.walk(model_path_dir):
        # Get the filenames without extension
        filenames = [os.path.splitext(file)[0] for file in files]

        # Process each filename
        for filename in filenames:
            # Find the schema for the current filename
            schema = find_schema(filename)

            if schema == -1:
                # If the schema is not found (indicated by -1),
                # print a message and skip the current file
                print(f"Skipping file: {filename}. No schema found.")
                continue

            if schema.lower() != "view":
                # Create the schema directory if it doesn't exist
                schema_directory = os.path.join(irepository_implementation_root, schema)
                if not os.path.exists(schema_directory):
                    os.makedirs(schema_directory)

                # Generate the repository file path
                repository_filepath = os.path.join(schema_directory, filename + 'Repository.cs')

                # Open the repository file in write mode
                with open(repository_filepath, 'w+') as file:
                    # Replace placeholders in the implementation template and write to the file
                    safe_model_name = safe_model_name(filename)

                    file.write(
                        implementation_template.replace('SAFE_MODEL_NAME', safe_model_name)
                        .replace('MODEL_NAME', filename)
                        .replace("SCHEMA_NAME", schema))

    print("All Repository Implementation Files Are Created")


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

    using_statements = []
    the_lazy_declaration = ''
    the_lazy_ctor = ''
    the_lazy_instantiation = ''

    with open(repository_manager_file_path, 'w+') as repository_manager:
        for root, dirs, files in os.walk(model_path_dir):
            for file in files:
                model_name, file_extension = os.path.splitext(file)
                schema = find_schema(model_name)

                if schema == -1:
                    print(f"Skipping file: {file}. No schema found.")
                    continue

                if schema.lower() != 'view':
                    if schema not in using_statements:
                        using_statements.append(schema)

                    lazy_property_name = f'_{model_name[0].lower() + model_name[1:]}Repository'
                    the_lazy_declaration += f'\n\t\tprivate readonly Lazy<I{model_name}Repository> {lazy_property_name};'
                    the_lazy_ctor += f'\n\t\t\t{lazy_property_name} = new Lazy<I{model_name}Repository>(() => new {model_name}Repository(repositoryContext));'
                    the_lazy_instantiation += f'\n\t\tpublic I{model_name}Repository {model_name} => {lazy_property_name}.Value;'

        # Generate the using statements by joining the schema names
        using_statement = '\n'.join(
            [f'using CNET_V7_Repository.Contracts.{schema}Schema;' for schema in using_statements])

        final_design = repository_manager_design.replace('THE_USING_STATEMENT', using_statement).replace(
            'THE_LAZY_DECLARATION', the_lazy_declaration).replace('THE_LAZY_CTOR', the_lazy_ctor).replace(
            'THE_LAZY_INSTANTIATION', the_lazy_instantiation)

        repository_manager.write(final_design)

    print("Repository manager created")


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

            if schema == -1:
                # If the schema is not found (indicated by -1),
                # print a message and skip the current file
                print(f"Skipping file: {model_name}. No schema found.")
                continue

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
    """
    Configure AutoMapper mappings based on the models found in the specified directory.

    Args:
        model_path_dir (str): The directory path where the model files are located.
        mapping_file_path (str): The file path to write the mapping configuration.
    """
    mapping_init = '''using AutoMapper;
THE_USING_STATEMENT
using CNET_V7_Entities.DataModels;

namespace CNET_V7_API.MappingProfile
{
    public class MappingProfile : Profile
    {
        public MappingProfile() {
            THE_CONFIGURATION
        } 
    }
}
'''

    using_statements = []
    the_configuration = ''

    # Generate the using statements and configuration for each model
    for _, _, files in os.walk(model_path_dir):
        for file in files:
            model_name, _ = os.path.splitext(file)
            schema_name = find_schema(model_name)

            if schema_name not in using_statements:
                using_statements.append(schema_name)

            the_configuration += f'\t\t\tCreateMap<{safe_model_name(model_name)}, {model_name}DTO>().ReverseMap();\n'

    # Generate the using statements by joining the schema names
    using_statement = '\n'.join([f'using CNET_V7_Repository.Contracts.{schema}Schema;' for schema in using_statements])

    # Write the mapping configuration to the file
    with open(mapping_file_path, 'w+') as mapping_file:
        mapping_file.write(
            mapping_init.replace('THE_USING_STATEMENT', using_statement)
            .replace('THE_CONFIGURATION', the_configuration)
        )

    print("Mapping.cs file created.")


def safe_model_name(model_name: str) -> str:
    """
    Modifies the given model name to ensure it is a safe choice.

    Args:
        model_name (str): The name of the model to be modified.

    Returns:
        str: The modified model name.

    """
    if model_name.lower() in ['delegate', 'range', 'route']:
        # If the model_name is one of the restricted keywords,
        # prepend it with 'CNET_V7_Entities.DataModels.'
        return f'CNET_V7_Entities.DataModels.{model_name}'

    # If the model_name is not a restricted keyword,
    # return it as is.
    return model_name

