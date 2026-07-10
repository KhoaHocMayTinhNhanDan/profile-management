class CleanArchitecturePaths:
    """
    Subsystem component định nghĩa cấu hình cấu trúc thư mục của Clean Architecture.
    Đóng vai trò là Single Source of Truth cho các công cụ Scaffold (sinh mã nguồn) và Bootstrap.
    """
    # Core directories names
    SRC = "src"
    TESTS = "tests"
    
    # Layer directories names
    LAYER_01 = "layer_01_entities"
    LAYER_02 = "layer_02_usecases"
    LAYER_03 = "layer_03_interface_adapters"
    LAYER_04 = "layer_04_infrastructure"
    LAYER_05 = "layer_05_bootstrap"

    # Layer 2 Subdirectories
    USECASES = "usecases"
    GATEWAYS_INTERFACE = "gateways_interface"

    # Layer 3 Subdirectories
    CONTROLLERS = "controllers"
    PRESENTERS = "presenters"
    GATEWAYS = "gateways"
    GATEWAYS_INBOUND = "inbound"
    GATEWAYS_OUTBOUND = "outbound"

    # Layer 4 Subdirectories
    DATABASES = "databases"
    DEVICES = "devices"
    WEB_DRIVERS = "web_drivers"
    EXTERNAL_SERVICES = "external_services"
    UI = "ui"
