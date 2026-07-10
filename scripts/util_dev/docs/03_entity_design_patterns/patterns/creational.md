## 1. CREATIONAL PATTERNS

### 1.1 Abstract Factory
- **Modular Layout:**
  - `[domain]_abstract_factory_pattern/factory/[domain]_abstract_factory.py`
  - `[domain]_abstract_factory_pattern/factory/[domain]_factory.py`
  - `[domain]_abstract_factory_pattern/products/abstract/[domain]_abstract_product.py`
  - `[domain]_abstract_factory_pattern/products/[variant]/[variant]_[domain].py`

### 1.2 Builder
- **Modular Layout:**
  - `[domain]_builder_pattern/builder/[domain]_builder_interface.py`
  - `[domain]_builder_pattern/builder/[variant]_builder.py`
  - `[domain]_builder_pattern/director/[domain]_director.py`
  - `[domain]_builder_pattern/product/[domain]_product.py`

### 1.3 Factory Method (inc. Simple Factory)
- **Factory Method Modular Layout:**
  - `[domain]_factory_method_pattern/creator/[domain]_creator_interface.py`
  - `[domain]_factory_method_pattern/creator/[variant]_[domain]_creator.py`
  - `[domain]_factory_method_pattern/product/[domain]_product_interface.py`
  - `[domain]_factory_method_pattern/product/[variant]_[domain]_product.py`
- Every concrete creator MUST be named using the pattern [variant]_[domain]_creator.py.
- Every concrete product MUST be named using the pattern [variant]_[domain]_product.py.

- **Simple Factory Modular Layout:**
  - `[domain]_simple_factory_pattern/creator/[domain]_simple_factory.py`
  - `[domain]_simple_factory_pattern/product/[domain]_product_interface.py`
  - `[domain]_simple_factory_pattern/product/[domain]_product.py`

### 1.4 Prototype
- **Modular Layout:**
  - `[domain]_prototype_pattern/prototype/[domain]_prototype_interface.py`
  - `[domain]_prototype_pattern/prototype/[variant]_prototype.py`

### 1.5 Singleton
- **Modular Layout:**
  - `[domain]_singleton_pattern/[domain]_singleton.py`
