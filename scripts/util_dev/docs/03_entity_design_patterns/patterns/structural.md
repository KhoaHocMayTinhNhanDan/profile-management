## 2. STRUCTURAL PATTERNS

### 2.1 Adapter
- **Modular Layout:**
  - `[domain]_adapter_pattern/target/[domain]_target_interface.py`
  - `[domain]_adapter_pattern/adaptee/[domain]_adaptee.py`
  - `[domain]_adapter_pattern/adapter/[variant]_adapter.py`

### 2.2 Bridge
- **Modular Layout:**
  - `[domain]_bridge_pattern/abstraction/[domain]_abstraction.py`
  - `[domain]_bridge_pattern/abstraction/[variant]_refined_abstraction.py`
  - `[domain]_bridge_pattern/implementation/[domain]_implementation_interface.py`
  - `[domain]_bridge_pattern/implementation/[variant]_implementation.py`

### 2.3 Composite
- **Modular Layout:**
  - `[domain]_composite_pattern/component/[domain]_component.py`
  - `[domain]_composite_pattern/leaf/[domain]_leaf.py`
  - `[domain]_composite_pattern/composite/[domain]_composite.py`

### 2.4 Decorator
- **Modular Layout:**
  - `[domain]_decorator_pattern/component/[domain]_component_interface.py`
  - `[domain]_decorator_pattern/concrete_component/[variant]_component.py`
  - `[domain]_decorator_pattern/decorator/[domain]_base_decorator.py`
  - `[domain]_decorator_pattern/concrete_decorator/[variant]_decorator.py`

### 2.5 Facade
- **Modular Layout:**
  - `[domain]_facade_pattern/facade/__init__.py`
  - `[domain]_facade_pattern/facade/[domain]_facade.py`
  - `[domain]_facade_pattern/subsystem/__init__.py`
  - `[domain]_facade_pattern/subsystem/[subsystem_name].py`

### 2.6 Flyweight
- **Modular Layout:**
  - `[domain]_flyweight_pattern/context/[domain]_context.py`
  - `[domain]_flyweight_pattern/factory/[domain]_flyweight_factory.py`
  - `[domain]_flyweight_pattern/flyweight/[domain]_flyweight_interface.py`
  - `[domain]_flyweight_pattern/flyweight/[variant]_flyweight.py`

### 2.7 Proxy
- **Modular Layout:**
  - `[domain]_proxy_pattern/subject/[domain]_subject.py`
  - `[domain]_proxy_pattern/real_subject/[domain]_real_subject.py`
  - `[domain]_proxy_pattern/proxy/[variant]_proxy.py`
