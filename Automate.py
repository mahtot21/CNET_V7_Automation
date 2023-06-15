import os
from database import find_schema


def generate_dto_files(model_path_dir: str, dto_root_path: str = None):
    """
    Create DTOs (Data Transfer Objects) for each file in the model path directory.

    Args:
        model_path_dir (str): Directory path where the model files are located.
        dto_root_path (str): Root directory path where the DTOs will be Generated.

    Returns:
        None
    """
    if dto_root_path is None:
        dto_root_path = os.path.join(os.path.dirname(model_path_dir), "Auto", "Dto")

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
                # Construct the path where the DTO file should be Generated
                # by joining 'dto_root_path' and 'schema'

                if not os.path.exists(schema_path):
                    # If the schema path doesn't exist, create the directory
                    os.makedirs(schema_path)

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

    print("DTOS Generated.")


def generate_i_repository_files(model_path_dir: str, i_repository_root_dir: str = None):
    """
    Create IRepository interfaces for each model file in the model path directory.

    Args:
        model_path_dir (str): Directory path where the model files are located.
        i_repository_root_dir (str): Directory path where the IRepository files will be Generated.

    Returns:
        None
    """

    i_repository_sample_code = read_sample_code("IRepository.cs")

    if i_repository_sample_code == -1:
        print("File IRepository.cs inside 'samples' folder not found!.")
    else:
        if i_repository_root_dir is None:
            i_repository_root_dir = os.path.join(os.path.dirname(model_path_dir), "Auto", "IRepository")

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
                    schema_dir = os.path.join(i_repository_root_dir, schema)
                    if not os.path.exists(schema_dir):
                        # If the schema path doesn't exist, create the directory
                        os.makedirs(schema_dir)

                    repo_name = 'I' + name + 'Repository'
                    # Construct the IRepository file name by appending 'I' to the model name and 'Repository' to the end

                    i_repository_file_path = os.path.join(schema_dir, repo_name + '.cs')
                    with open(i_repository_file_path, 'w+') as file:
                        # Open the IRepository file for writing (create if it doesn't exist, truncate if it does)

                        generated_code = i_repository_sample_code.replace('EntityName', name).replace('SchemaName', schema).replace('SafeName', safe_model_name(name))
                        file.write(generated_code)
                        # Replace placeholders in the IRepository sample code with actual names

        print("IRepository Files Are Generated.")


def generate_i_repository_manager(model_path_dir: str, i_repository_manager_file_path: str = None):
    """
    Create IRepositoryManager interface for the model files in the given directory.

    Args:
        model_path_dir (str): Directory path where the model files are located.
        i_repository_manager_file_path (str): File path where the IRepositoryManager file will be Generated.

    Returns:
        None
    """

    implementation_sample = read_sample_code("IRepositoryManager.cs")
    if implementation_sample == -1:
        print("File IRepositoryManager.cs inside 'samples' folder not found!.")
    else:
        # Check if the i_repository_manager_file_path variable is None
        if i_repository_manager_file_path is None:
            # If it is None, construct a new path using the model_path_dir variable
            # os.path.dirname(model_path_dir) returns the parent directory of model_path_dir
            # os.path.join() is used to concatenate the parent directory with additional subdirectories
            i_repository_manager_file_path = os.path.join(os.path.dirname(model_path_dir), "Auto", "IRepository")

            if not os.path.exists(i_repository_manager_file_path):
                os.makedirs(i_repository_manager_file_path)

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
                    the_declaration += f'\n\t\tI{model_name}Repository {model_name} ' + '{ get; }\n'

                    if schema not in using_statements:
                        # Add the schema to the list of using statements if it hasn't been added already
                        using_statements.append(schema)

        # Generate the using statements by joining the schema names
        using_statement = '\n'.join([f'using CNET_V7_Repository.Contracts.{schema}Schema;' for schema in using_statements])

        # Write the generated IRepositoryManager code to the specified file path
        manager_file_name = os.path.join(i_repository_manager_file_path, "IRepositoryManger.cs")
        with open(manager_file_name, 'w+') as manager:
            manager.write(implementation_sample.replace('THE_USING_STATEMENT', using_statement).replace('THE_DECLARATION', the_declaration))

        print(f"IRepositoryManager Generated.")


def generate_repository_implementation_files(model_path_dir: str, repository_implementation_root_path: str = None):
    """
    Create IRepository implementation files for the model files in the given directory.

    Args:
        model_path_dir (str): Directory path where the model files are located.
        repository_implementation_root_path (str): Root directory path where the IRepository implementation files will be Generated.

    Returns:
        None
    """

    implementation_template = read_sample_code("RepositoryImplementation.cs")
    if implementation_template == -1:
        print("File RepositoryImplementation.cs inside 'samples' folder not found!.")
    else:
        # Check if the repository_implementation_root_path variable is None
        if repository_implementation_root_path is None:
            # If it is None, construct a new path using the model_path_dir variable
            # os.path.dirname(model_path_dir) returns the parent directory of model_path_dir
            # os.path.join() is used to concatenate the parent directory with additional subdirectories
            repository_implementation_root_path = os.path.join(os.path.dirname(model_path_dir), "Auto", "Repository")

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
                    schema_directory = os.path.join(repository_implementation_root_path, schema)
                    if not os.path.exists(schema_directory):
                        os.makedirs(schema_directory)

                    # Generate the repository file path
                    repository_filepath = os.path.join(schema_directory, filename + 'Repository.cs')

                    # Open the repository file in write mode
                    with open(repository_filepath, 'w+') as file:
                        # Replace placeholders in the implementation template and write to the file

                        file.write(
                            implementation_template.replace('SAFE_MODEL_NAME', safe_model_name(filename))
                            .replace('MODEL_NAME', filename)
                            .replace("SCHEMA_NAME", schema))

        print("Repository Implementation Files Are Generated")


def generate_repository_manager(model_path_dir: str, repository_manager_file_path: str = None) -> str:
    """
    Generates a repository manager class based on the models found in the specified directory.

    Args:
        model_path_dir (str): The directory path where the models are located.
        repository_manager_file_path (str, optional): The file path for the repository manager class. If not provided,
            a default path will be used. Defaults to None.

    Returns:
        str: The file path of the generated repository manager class.

    Raises:
        FileNotFoundError: If the specified model directory does not exist.
    """

    using_statements = []
    lazy_declarations = ''
    lazy_initializations = ''
    lazy_instantiations = ''

    repository_manager_template = read_sample_code("RepositoryManager.cs")
    if repository_manager_template == -1:
        print("File RepositoryManager.cs inside 'samples' folder not found!.")
    else:
        if repository_manager_file_path is None:
            repository_manager_file_path = os.path.join(os.path.dirname(model_path_dir), "Auto", "Repository")

            if not os.path.exists(repository_manager_file_path):
                os.makedirs(repository_manager_file_path)

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
                    lazy_declarations += f'\n\t\tprivate readonly Lazy<I{model_name}Repository> {lazy_property_name};'
                    lazy_initializations += f'\n\t\t\t{lazy_property_name} = new Lazy<I{model_name}Repository>(() => new {model_name}Repository(repositoryContext));'
                    lazy_instantiations += f'\n\t\tpublic I{model_name}Repository {model_name} => {lazy_property_name}.Value;'

        using_statement_block = '\n'.join(
            [f'using CNET_V7_Repository.Contracts.{schema}Schema;' for schema in using_statements])

        repository_manager_code = repository_manager_template.replace('THE_USING_STATEMENTS', using_statement_block).replace(
            'THE_LAZY_DECLARATIONS', lazy_declarations).replace('THE_LAZY_INITIALIZATIONS', lazy_initializations).replace(
            'THE_LAZY_INSTANTIATIONS', lazy_instantiations)

        manager_file = os.path.join(repository_manager_file_path, 'RepositoryManager.cs')
        with open(manager_file, 'w+') as repository_manager_file:
            repository_manager_file.write(repository_manager_code)

        print("Repository Manager Generated.")


def generate_i_service_manager(model_path_dir: str, i_service_manager_file_path: str = None):
    the_using_statement = ''
    the_declaration = ''
    using_printed_schemas = []

    i_service_manager_init = read_sample_code("IServiceManager.cs")
    if i_service_manager_init == -1:
        print("File IServiceManager.cs inside 'samples' folder not found!.")
    else:
        if i_service_manager_file_path is None:
            i_service_manager_file_path = os.path.join(os.path.dirname(model_path_dir), "Auto", "IService")

        manager_file = os.path.join(i_service_manager_file_path, "IServiceManager.cs")
        with open(manager_file, 'w+') as i_service_manager:
            for root, dirs, files in os.walk(model_path_dir):
                for file in files:
                    model_name = os.path.splitext(file)[0]

                    schema = find_schema(model_name)
                    if schema.lower() != 'view':
                        model_name, file_extension = os.path.splitext(file)
                        if schema not in using_printed_schemas:
                            using_printed_schemas.append(schema)
                            the_using_statement += f'using CNET_V7_Service.Contracts.{schema}Schema;\n'
                        the_declaration += f'\t\tI{model_name}Service {model_name[0].lower() + model_name[1:]}Service ' + \
                                           '{ get; }\n'
            i_service_manager.write(
                i_service_manager_init.replace('THE_USING_STATEMENT', the_using_statement).replace('THE_DECLARATION', the_declaration))

        print("IServiceManager.cs file Generated.")


def generate_i_service_files(model_path_dir: str, i_service_root_dir: str = None):
    i_service_sample = read_sample_code("IService.cs")
    if i_service_sample == -1:
        print("File IService.cs inside 'samples' folder not found!.")
    else:

        if i_service_root_dir is None:
            i_service_root_dir = os.path.join(os.path.dirname(model_path_dir), "Auto", "IService")

        for root, dirs, files in os.walk(model_path_dir):
            filenames = [os.path.splitext(file)[0] for file in files]

            for name in filenames:
                schema = find_schema(name)

                if not os.path.exists(os.path.join(i_service_root_dir, schema)):
                    os.makedirs(os.path.join(i_service_root_dir, schema))

                file_name = 'I' + name + 'Service'
                with open(os.path.join(i_service_root_dir, schema, file_name + '.cs'), 'w+') as file:
                    # let me replace it then
                    file.write(i_service_sample.replace(
                        'SCHEMA', schema).replace('MODEL_NAME', name))
        print("IService Files Are Generated")


def generate_service_manager(model_path_dir: str, service_manager_file_path: str = None):
    the_using_statement = ''
    the_lazy_declaration = ''
    the_lazy_ctor = ''
    the_lazy_instantiation = ''
    using_printed_schemas = []

    service_manager_sample = read_sample_code("ServiceManager.cs")
    if service_manager_sample == -1:
        print("File ServiceManager.cs inside 'samples' folder not found!.")
    else:

        if service_manager_file_path is None:
            service_manager_file_path = os.path.join(os.path.dirname(model_path_dir), "Auto", "Service")

        manager_file = os.path.join(service_manager_file_path, "ServiceManager.cs")
        with open(manager_file, 'w+') as manager:
            for root, dirs, files in os.walk(model_path_dir):
                for file in files:
                    model_name, file_extension = os.path.splitext(file)
                    schema = find_schema(model_name)
                    if schema.lower() != 'view':
                        if schema == -1:
                            print("schema not found: ", model_name)
                            continue

                        if schema not in using_printed_schemas:
                            using_printed_schemas.append(schema)
                            the_using_statement += f'using CNET_V7_Service.Contracts.{schema}Schema;\nusing CNET_V7_Service.Implementation.{schema}Schema;\n'

                        the_lazy_declaration += f'\n\t\tprivate readonly Lazy<I{model_name}Service> _{model_name[0].lower() + model_name[1:]}Service;'

                        the_lazy_ctor += f'\n\t\t\t_{model_name[0].lower() + model_name[1:]}Service = new Lazy<I{model_name}Service>(()=>new {model_name}Service(repositoryManager, logger, mapper));'

                        the_lazy_instantiation += f'\n\t\tpublic I{model_name}Service {model_name[0].lower() + model_name[1:]}Service => _{model_name[0].lower() + model_name[1:]}Service.Value;'
            # so we can write it
            final_design = service_manager_sample.replace('THE_USING_STATEMENT', the_using_statement).replace(
                'THE_LAZY_DECLARATION', the_lazy_declaration).replace('THE_LAZY_CTOR', the_lazy_ctor).replace(
                'THE_LAZY_INSTANTIATION', the_lazy_instantiation)
            manager.write(final_design)

        print(f"Service manager generated.")


def generate_service_implementation_files(model_path_dir: str, service_implementation_root: str = None):
    implementation_sample = read_sample_code("Service.cs")
    if implementation_sample == -1:
        print("File Service.cs inside 'samples' folder not found!.")
    else:

        if service_implementation_root is None:
            service_implementation_root = os.path.join(os.path.dirname(model_path_dir), "Auto", "Service")

        for root, dirs, files in os.walk(model_path_dir):
            filenames = [os.path.splitext(file)[0] for file in files]
            # print(filenames)
            for name in filenames:
                schema = find_schema(name)

                if schema.lower() != "view":
                    # Create the schema directory if it doesn't exist
                    schema_directory = os.path.join(service_implementation_root, schema)
                    if not os.path.exists(schema_directory):
                        os.makedirs(schema_directory)

                    if not os.path.exists(os.path.join(service_implementation_root, schema)):
                        os.makedirs(os.path.join(service_implementation_root, schema))

                    # repo_name = 'I' + name + 'Repository'
                    with open(os.path.join(service_implementation_root, schema, name + 'Service.cs'), 'w+') as file:
                        # let me replace it
                        file.write(implementation_sample.replace('SAFE_MODEL_NAME', safe_model_name(name)).replace('MODEL_NAME', name).replace(
                            'SCHEMA_NAME', schema).replace('LOWER_START_SAFE', safe_model_name(name)[0].lower() + safe_model_name(name)[1:]))

        print("Service Implementation Files Are Generated.")


def generate_controllers(model_path_dir: str, controller_root: str = None):
    # entity_controller_implementation_sample = read_sample_code("EntityController.cs")
    entity_controller_implementation_sample = read_sample_code("AbstractController.cs")

    # view_controller_implementation_sample = read_sample_code("ViewController.cs")
    view_controller_implementation_sample = read_sample_code("ViewBaseController.cs")

    if entity_controller_implementation_sample == -1 or view_controller_implementation_sample == -1:
        print("File ViewController.cs or EntityController.cs inside 'samples' folder not found!.")
    else:

        if controller_root is None:
            controller_root = os.path.join(os.path.dirname(model_path_dir), "Auto", "Controllers")

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
                    os.makedirs(os.path.join(controller_root, schema))
                controller_file = os.path.join(controller_root, schema, model_name + 'Controller.cs')

                with open(controller_file, 'w+') as file:
                    # let me replace it
                    parameter = model_name[0].lower() + model_name[1:]
                    if model_name.lower() == 'delegate':
                        parameter = 'delegateObj'
                    elif model_name.lower() == 'range':
                        parameter = 'rangeObj'
                    if schema.lower() == "view":
                        file.write(
                            view_controller_implementation_sample.replace(
                                'MODEL_NAME_CAMILE', model_name[0].lower() + model_name[1:])
                            .replace('SAFE_MODEL_NAME', safe_model_name(model_name))
                            .replace('MODEL_NAME', model_name)
                            .replace('SCHEMA', schema)
                            .replace('PARAMETER', parameter))
                    else:
                        file.write(
                            entity_controller_implementation_sample.replace(
                                'MODEL_NAME_CAMILE', model_name[0].lower() + model_name[1:])
                            .replace('SAFE_MODEL_NAME', safe_model_name(model_name))
                            .replace('MODEL_NAME', model_name)
                            .replace('SCHEMA', schema)
                            .replace('PARAMETER', parameter))

        print("Controllers  and views are Generated.")


def generate_mapping_configuration(model_path_dir: str, mapping_file_path: str = None):
    """
    Configure AutoMapper mappings based on the models found in the specified directory.

    Args:
        model_path_dir (str): The directory path where the model files are located.
        mapping_file_path (str): The file path to write the mapping configuration.
    """

    using_statements = []
    the_configuration = ''

    mapping_sample_code = read_sample_code("MappingProfile.cs")
    if mapping_sample_code == -1:
        print("File MappingProfile.cs inside 'samples' folder not found!.")
    else:

        if mapping_file_path is None:
            mapping_file_path = os.path.join(os.path.dirname(model_path_dir), "Auto")
            if not os.path.exists(mapping_file_path):
                os.makedirs(mapping_file_path)

        # Generate the using statements and configuration for each model
        for _, _, files in os.walk(model_path_dir):
            for file in files:
                model_name, _ = os.path.splitext(file)
                schema_name = find_schema(model_name)
                if schema_name != "View":
                    if schema_name not in using_statements:
                        using_statements.append(schema_name)

                    the_configuration += f'\t\t\tCreateMap<{safe_model_name(model_name)}, {model_name}DTO>().ReverseMap();\n'

        # Generate the using statements by joining the schema names
        using_statement = '\n'.join([f'using CNET_V7_Domain.Domain.{schema}Schema;' for schema in using_statements])

        profile_name = os.path.join(mapping_file_path, "MappingProfile.cs")
        # Write the mapping configuration to the file
        with open(profile_name, 'w+') as mapping_file:
            mapping_file.write(
                mapping_sample_code.replace('THE_USING_STATEMENT', using_statement)
                .replace('THE_CONFIGURATION', the_configuration)
            )

        print("Mapping.cs file Generated.")


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


def read_sample_code(sample_name: str):
    sample = -1
    with open(f"samples/{sample_name}") as file:
        sample = file.read()

    return sample
