from .app_context_base import AppContextBase
from src.layer_02_usecases.usecases.create_profile_template.create_profile_template_interactor import CreateProfileTemplateInteractor
from src.layer_02_usecases.gateways_interface.i_create_profile_template_repository import ICreateProfileTemplateRepository
from src.layer_03_interface_adapters.gateways.outbound.i_create_profile_template_data_source import ICreateProfileTemplateDataSource
from src.layer_03_interface_adapters.gateways.inbound.create_profile_template_repository import CreateProfileTemplateRepository
from src.layer_03_interface_adapters.controllers.web.create_profile_template import CreateProfileTemplateController
from src.layer_04_infrastructure.databases.sqlite.create_profile_template_data_source import SqliteCreateProfileTemplateDataSource
from src.layer_02_usecases.usecases.create_profile.create_profile_interactor import CreateProfileInteractor
from src.layer_02_usecases.gateways_interface.i_create_profile_repository import ICreateProfileRepository
from src.layer_03_interface_adapters.gateways.outbound.i_create_profile_data_source import ICreateProfileDataSource
from src.layer_03_interface_adapters.gateways.inbound.create_profile_repository import CreateProfileRepository
from src.layer_03_interface_adapters.controllers.web.create_profile import CreateProfileController
from src.layer_04_infrastructure.databases.sqlite.create_profile_data_source import SqliteCreateProfileDataSource
from src.layer_02_usecases.usecases.update_profile.update_profile_interactor import UpdateProfileInteractor
from src.layer_02_usecases.gateways_interface.i_update_profile_repository import IUpdateProfileRepository
from src.layer_03_interface_adapters.gateways.outbound.i_update_profile_data_source import IUpdateProfileDataSource
from src.layer_03_interface_adapters.gateways.inbound.update_profile_repository import UpdateProfileRepository
from src.layer_03_interface_adapters.controllers.web.update_profile import UpdateProfileController
from src.layer_04_infrastructure.databases.sqlite.update_profile_data_source import SqliteUpdateProfileDataSource
from src.layer_02_usecases.usecases.checkout_document.checkout_document_interactor import CheckoutDocumentInteractor
from src.layer_02_usecases.gateways_interface.i_checkout_document_repository import ICheckoutDocumentRepository
from src.layer_03_interface_adapters.gateways.outbound.i_checkout_document_data_source import ICheckoutDocumentDataSource
from src.layer_03_interface_adapters.gateways.inbound.checkout_document_repository import CheckoutDocumentRepository
from src.layer_03_interface_adapters.controllers.web.checkout_document import CheckoutDocumentController
from src.layer_04_infrastructure.databases.sqlite.checkout_document_data_source import SqliteCheckoutDocumentDataSource
from src.layer_02_usecases.usecases.checkin_document.checkin_document_interactor import CheckinDocumentInteractor
from src.layer_02_usecases.gateways_interface.i_checkin_document_repository import ICheckinDocumentRepository
from src.layer_03_interface_adapters.gateways.outbound.i_checkin_document_data_source import ICheckinDocumentDataSource
from src.layer_03_interface_adapters.gateways.inbound.checkin_document_repository import CheckinDocumentRepository
from src.layer_03_interface_adapters.controllers.web.checkin_document import CheckinDocumentController
from src.layer_04_infrastructure.databases.sqlite.checkin_document_data_source import SqliteCheckinDocumentDataSource
from src.layer_02_usecases.usecases.generate_document_from_template.generate_document_from_template_interactor import GenerateDocumentFromTemplateInteractor
from src.layer_02_usecases.gateways_interface.i_generate_document_from_template_repository import IGenerateDocumentFromTemplateRepository
from src.layer_03_interface_adapters.gateways.outbound.i_generate_document_from_template_data_source import IGenerateDocumentFromTemplateDataSource
from src.layer_03_interface_adapters.gateways.inbound.generate_document_from_template_repository import GenerateDocumentFromTemplateRepository
from src.layer_03_interface_adapters.controllers.web.generate_document_from_template import GenerateDocumentFromTemplateController
from src.layer_04_infrastructure.databases.sqlite.generate_document_from_template_data_source import SqliteGenerateDocumentFromTemplateDataSource

class AppContextWeb(AppContextBase):
    def __init__(self):
        super().__init__()

    def _register_infrastructure(self):
        super()._register_infrastructure()
        
        # CreateProfileTemplate Bindings (DB: sqlite)
        self.container.register(ICreateProfileTemplateDataSource, SqliteCreateProfileTemplateDataSource())
        self.container.register(ICreateProfileTemplateRepository, CreateProfileTemplateRepository(self.container.resolve(ICreateProfileTemplateDataSource)))
        self.container.register(CreateProfileTemplateInteractor, CreateProfileTemplateInteractor(self.container.resolve(ICreateProfileTemplateRepository)))
        self.container.register(CreateProfileTemplateController, CreateProfileTemplateController(self.container.resolve(CreateProfileTemplateInteractor)))
        
        # CreateProfile Bindings (DB: sqlite)
        self.container.register(ICreateProfileDataSource, SqliteCreateProfileDataSource())
        self.container.register(ICreateProfileRepository, CreateProfileRepository(self.container.resolve(ICreateProfileDataSource)))
        self.container.register(CreateProfileInteractor, CreateProfileInteractor(self.container.resolve(ICreateProfileRepository)))
        self.container.register(CreateProfileController, CreateProfileController(self.container.resolve(CreateProfileInteractor)))
        
        # UpdateProfile Bindings (DB: sqlite)
        self.container.register(IUpdateProfileDataSource, SqliteUpdateProfileDataSource())
        self.container.register(IUpdateProfileRepository, UpdateProfileRepository(self.container.resolve(IUpdateProfileDataSource)))
        self.container.register(UpdateProfileInteractor, UpdateProfileInteractor(self.container.resolve(IUpdateProfileRepository)))
        self.container.register(UpdateProfileController, UpdateProfileController(self.container.resolve(UpdateProfileInteractor)))
        
        # CheckoutDocument Bindings (DB: sqlite)
        self.container.register(ICheckoutDocumentDataSource, SqliteCheckoutDocumentDataSource())
        self.container.register(ICheckoutDocumentRepository, CheckoutDocumentRepository(self.container.resolve(ICheckoutDocumentDataSource)))
        self.container.register(CheckoutDocumentInteractor, CheckoutDocumentInteractor(self.container.resolve(ICheckoutDocumentRepository)))
        self.container.register(CheckoutDocumentController, CheckoutDocumentController(self.container.resolve(CheckoutDocumentInteractor)))
        
        # CheckinDocument Bindings (DB: sqlite)
        self.container.register(ICheckinDocumentDataSource, SqliteCheckinDocumentDataSource())
        self.container.register(ICheckinDocumentRepository, CheckinDocumentRepository(self.container.resolve(ICheckinDocumentDataSource)))
        self.container.register(CheckinDocumentInteractor, CheckinDocumentInteractor(self.container.resolve(ICheckinDocumentRepository)))
        self.container.register(CheckinDocumentController, CheckinDocumentController(self.container.resolve(CheckinDocumentInteractor)))
        
        # GenerateDocumentFromTemplate Bindings (DB: sqlite)
        self.container.register(IGenerateDocumentFromTemplateDataSource, SqliteGenerateDocumentFromTemplateDataSource())
        self.container.register(IGenerateDocumentFromTemplateRepository, GenerateDocumentFromTemplateRepository(self.container.resolve(IGenerateDocumentFromTemplateDataSource)))
        self.container.register(GenerateDocumentFromTemplateInteractor, GenerateDocumentFromTemplateInteractor(self.container.resolve(IGenerateDocumentFromTemplateRepository)))
        self.container.register(GenerateDocumentFromTemplateController, GenerateDocumentFromTemplateController(self.container.resolve(GenerateDocumentFromTemplateInteractor)))
        # <-- BIND_REPOSITORY_HERE -->
