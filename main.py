from Automate import (
    generate_dto_files,
    generate_i_repository_files,
    generate_i_repository_manager,
    generate_repository_implementation_files,
    generate_repository_manager,
    generate_i_service_manager,
    generate_i_service_files,
    generate_service_manager,
    generate_service_implementation_files,
    generate_controllers,
    generate_mapping_configuration
)


def main():
    # you should change this file path to your data models root folder!
    model_path = r"C:\Users\Admin\Desktop\test\DataModels\DataModels"

    # Generate DTO files
    generate_dto_files(model_path)

    # # Generate IRepository files
    # generate_i_repository_files(model_path)
    #
    # # Generate IRepository implementation files
    # generate_repository_implementation_files(model_path)
    #
    # # Generate IRepositoryManager file
    # generate_i_repository_manager(model_path)
    #
    # # Generate RepositoryManager file
    # generate_repository_manager(model_path)
    #
    # # Generate IService files
    # generate_i_service_files(model_path)
    #
    # # Generate IService implementation files
    # generate_service_implementation_files(model_path)
    #
    # # Generate IServiceManager file
    # generate_i_service_manager(model_path)
    #
    # # Generate ServiceManager file
    # generate_service_manager(model_path)
    #
    # # Generate Controllers
    # generate_controllers(model_path)
    #
    # # Configure mapping
    # generate_mapping_configuration(model_path)


if __name__ == '__main__':
    main()
