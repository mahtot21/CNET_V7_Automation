from Automate import create_dto, create_irepositories, create_irepository_manager, create_irepository_implementation, \
    create_repository_manager, create_iservice_manager, create_iservice, create_service_manager, \
    create_iservice_implementation, create_controllers, configure_mapping

model_path = r"D:\LAB\CNET\CNET_V7\CNET_V7_Entities\DataModels"

create_irepository_root_path = r"C:\Users\mahto\Desktop\test"
create_iservice_root_path = r"C:\Users\mahto\Desktop\test"
created_dto_root_path = r'D:\LAB\Mahtot\test'

irepository_manager_create_path = r'C:\Users\mahto\Desktop\test\IRepositoryManager.cs'
repository_manager_create_path = r'C:\Users\mahto\Desktop\test\RepositoryManager.cs'

iservice_manager_create_path = r'C:\Users\mahto\Desktop\test\IServiceManager.cs'
service_manager_create_path = r'C:\Users\mahto\Desktop\test\ServiceManager.cs'

create_irepository_implementation_root = r'C:\Users\mahto\Desktop\test'
create_iservice_implementation_root = r'C:\Users\mahto\Desktop\test'

controller_root = r'C:\Users\mahto\Desktop\test'
mapping_file_path = r'C:\Users\mahto\Desktop\test\MappingProfile.cs'

# create_irepository_root_path = r"C:\Users\mahto\OneDrive\Documents\MAIN LAB\V7\CNET_V7_Repository.Contracts"

# create_iservice_root_path = r"C:\Users\mahto\OneDrive\Documents\MAIN LAB\V7\CNET_V7_Service.Contracts"

# created_dto_root_path = r'C:\Users\mahto\OneDrive\Documents\MAIN LAB\V7\CNET_V7_Domain\Domain'

# irepository_manager_create_path = r'C:\Users\mahto\OneDrive\Documents\MAIN LAB\V7\CNET_V7_Repository.Contracts\IRepositoryManager.cs'

# repository_manager_create_path = r'C:\Users\mahto\OneDrive\Documents\MAIN LAB\V7\CNET_V7_Repository.Implementation\RepositoryManager.cs'

# iservice_manager_create_path = r'C:\Users\mahto\OneDrive\Documents\MAIN LAB\V7\CNET_V7_Service.Contracts\IServiceManager.cs'

# service_manager_create_path = r'C:\Users\mahto\OneDrive\Documents\MAIN LAB\V7\CNET_V7_Service.Implementation\ServiceManager.cs'

# create_irepository_implementation_root = r'C:\Users\mahto\OneDrive\Documents\MAIN LAB\V7\CNET_V7_Repository.Implementation'

# create_iservice_implementation_root = r'C:\Users\mahto\OneDrive\Documents\MAIN LAB\V7\CNET_V7_Service.Implementation'

# controller_root = r'C:\Users\mahto\OneDrive\Documents\MAIN LAB\V7\CNET_V7_Presentation\BaseControllers'

if __name__ == '__main__':

    create_dto(model_path, created_dto_root_path)

    # create_irepositories(model_path, create_irepository_root_path)

    # create_irepository_implementation(model_path, create_irepository_implementation_root)

    # create_irepository_manager(model_path, irepository_manager_create_path)

    # create_repository_manager(model_path, repository_manager_create_path)

    # create_iservice(model_path, create_iservice_root_path)

    # create_iservice_implementation(model_path, create_iservice_implementation_root)

    # create_iservice_manager(model_path, iservice_manager_create_path)

    # create_service_manager(model_path, service_manager_create_path)

    # create_controllers(model_path, controller_root)

    # configure_mapping(model_path, mapping_file_path)
