from Automate import (
    create_dto,
    create_irepositories,
    create_irepository_manager,
    create_irepository_implementation,
    create_repository_manager,
    create_iservice_manager,
    create_iservice,
    create_service_manager,
    create_iservice_implementation,
    create_controllers,
    configure_mapping
)


def main():
    model_path = r"C:\Users\Admin\Desktop\test\DataModels\DataModels"
    create_irepository_root_path = r"C:\Users\Admin\Desktop\test\Auto\IRepository"
    create_iservice_root_path = r"C:\Users\mahto\Desktop\test"
    created_dto_root_path = r'C:\Users\Admin\Desktop\test\Auto\Dto'
    irepository_manager_create_path = r'C:\Users\Admin\Desktop\test\Auto\IRepository\IRepositoryManager.cs'
    repository_manager_create_path = r'C:\Users\Admin\Desktop\test\Auto\Repository\RepositoryManager.cs'
    iservice_manager_create_path = r'C:\Users\mahto\Desktop\test\IServiceManager.cs'
    service_manager_create_path = r'C:\Users\mahto\Desktop\test\ServiceManager.cs'
    create_irepository_implementation_root = r'C:\Users\Admin\Desktop\test\Auto\Repository'
    create_iservice_implementation_root = r'C:\Users\mahto\Desktop\test'
    controller_root = r'C:\Users\Admin\Desktop\test\Auto\Controller'
    mapping_file_path = r'C:\Users\Admin\Desktop\test\Auto\MappingProfile.cs'

    create_dto(model_path, created_dto_root_path)
    create_irepositories(model_path, create_irepository_root_path)
    create_irepository_implementation(model_path, create_irepository_implementation_root)
    create_irepository_manager(model_path, irepository_manager_create_path)
    create_repository_manager(model_path, repository_manager_create_path)
    create_iservice(model_path, create_iservice_root_path)
    create_iservice_implementation(model_path, create_iservice_implementation_root)
    create_iservice_manager(model_path, iservice_manager_create_path)
    create_service_manager(model_path, service_manager_create_path)
    create_controllers(model_path, controller_root)
    configure_mapping(model_path, mapping_file_path)


if __name__ == '__main__':
    main()
