# GoF Design Patterns Structural Specification (Token-Optimized)

> [!IMPORTANT]
> **AI STRICT RULES:**
> 1. **NO CODE SHORTCUTS:** Never combine multiple files into a single file. You MUST split code logically into separate files as specified in the layouts.
> 2. **STRICT DIRECTORY STRUCTURE:** You MUST create the exact directories, `__init__.py` files, and module structures defined below.
> 3. **CLEAN CODE:** Do not omit boilerplate, imports, or helper methods.
> 4. **NAMING CONVENTION (REAL-WORLD ADAPTATION):**
>    - **Role-Suffixed Patterns:** For patterns representing interchangeable behaviors, algorithms, commands, adapters, factories, decorators, handlers, visitors, observers, or similar extensible roles (e.g., Strategy, State, Command, Abstract Factory, Factory Method, Observer, Visitor, Adapter, Proxy, Decorator, Chain of Responsibility/Handler), implementation files MUST be named using the format `[domain]_[pattern_role].py`.
>      - *Example (Strategy):* `paypal_strategy.py`, `stripe_strategy.py`
>      - *Example (Abstract Factory):* `postgres_factory.py`, `sqlite_factory.py`
>      - *Example (Command):* `save_user_command.py`
>      - *Example (Chain of Responsibility):* `validation_handler.py`, `logging_handler.py`
>    - **Domain-Based Patterns:** For patterns whose primary purpose is to model domain structures or subsystem composition (e.g., Composite, Facade, Flyweight, Memento), component and subsystem files MUST use natural domain names (e.g., `folder.py`, `file.py`), while the public entry-point, abstraction, or manager class MUST retain the GoF pattern role as a suffix (e.g., `media_facade.py`, `history_caretaker.py`).
> 5. **STRICT FOLDER STRUCTURE GUARANTEE:** Even if a component package or layout directory contains only a single file (e.g., a single `facade_class.py` inside `facade/`), you **MUST** create the target subfolder and place the file inside it. **NEVER** pull files out of their designated subfolders to the parent directory.
> 6. **NO PATTERN DEGRADATION & PURITY:** Never substitute the requested GoF pattern with another pattern or a simplified implementation. **Every mandatory GoF participant MUST be represented as a separate class.** When the GoF pattern defines interchangeable concrete participants (e.g., Strategy, State, Command, Observer, Visitor, Decorator, Abstract Factory, Factory Method, Chain of Responsibility), **generate at least two concrete implementations** unless explicitly instructed otherwise. Do not generate unnecessary concrete implementations for patterns that do not require them.
> 7. **ROLE MAPPING DOCUMENTATION:** Every generated class MUST clearly correspond to an official GoF participant role. The class docstring MUST explicitly state the corresponding official GoF participant role (e.g., "GoF Role: ConcreteObserver").
> 8. **NO PATTERN MIXING:** Do not mix patterns (e.g., adding Singleton/Service Locator to a Factory, or State with Mediator) unless explicitly requested. Keep the design pattern implementation pure.
> 9. **SOLID COMPLIANCE:** All generated code MUST strictly comply with SOLID principles. High-level modules MUST depend only on abstractions.
> 10. **DEPENDENCY & IMPORT DIRECTION:** Dependencies MUST always point toward abstractions. Concrete implementations MUST NEVER import sibling concrete implementations, depend directly on contexts, or create circular/bidirectional dependencies. **State classes must NOT instantiate Context objects**; they should receive the context dynamically via parameter passing.
> 11. **NO STATIC DISPATCH & ANTI-PATTERNS:** For behavioral patterns, select behaviors exclusively via dynamic dispatch/polymorphism. **ALL forms of static behavior dispatching are STRICTLY FORBIDDEN**, including: `if/elif`, `switch/case`, `match/case`, `isinstance()`, `type()`, dictionary-based dispatch, string-matching reflection, or service locators.
> 12. **PYTHON INTERFACE UNIFICATION:** All abstract interface classes in Python MUST inherit from `abc.ABC` and define abstract methods using `@abc.abstractmethod`. Do not use plain classes, `NotImplementedError`-only methods, or `typing.Protocol` unless explicitly requested.
> 13. **INSTANTIATION CONTROL:** For patterns using Factories, Builders, or Creators, concrete product classes MUST NOT be instantiated directly outside the factory/builder namespace.
> 14. **LAYOUT INTEGRITY & SELF-VALIDATION:** All layouts below define the minimum required structure. Additional files are allowed only when they improve separation of responsibilities. Before completing any design pattern task, you MUST validate that: (a) all GoF roles are represented, (b) no static dispatch exists, (c) no circular imports occur, (d) exact folder structure is met.
> 15. **PATTERN ENCAPSULATION & COMPOSITION:** When one GoF Design Pattern is implemented as an internal part of another GoF Design Pattern, the embedded pattern MUST remain a complete, self-contained module. It MUST preserve its own canonical directory structure, mandatory GoF participants, abstractions, supporting files, public API, and implementation rules exactly as if it were implemented independently.
> Never split, relocate, merge, or omit the mandatory participants of an embedded pattern across unrelated directories or into the parent pattern's implementation.
> The composing pattern MUST treat the embedded pattern as an independent module (i.e., as a client of that module). It MUST interact only through the embedded pattern's exported public abstraction or designated public entry point, and MUST NOT directly access, instantiate, import, or depend upon the embedded pattern's internal participants or implementation details.
> This rule applies only to nested (embedded) pattern composition. Independent GoF patterns collaborating at the same architectural level MUST remain as separate, self-contained modules.
> 16. PUBLIC PACKAGE API:
> Every pattern package MUST expose a stable public API through its package root (`__init__.py`).
> External modules MUST import only from the package root unless explicitly documented otherwise.
> Internal implementation modules are considered private.
> 17. PACKAGE EXPORTS:
> Every package and subpackage MUST contain an `__init__.py`.
> Each `__init__.py` MUST explicitly re-export the intended public classes through imports and `__all__`.

---

## Scope

This specification defines **only the internal implementation structure of GoF Design Patterns**. Application entry points, demonstration clients, test code, integration code, and project-specific bootstrapping are intentionally excluded unless explicitly requested.

> [!NOTE]
> Every GoF Design Pattern MUST be implemented as a self-contained package named using the format `[domain]_<pattern_name>_pattern/`. This package represents the implementation boundary of the pattern. All mandatory GoF participants, abstractions, concrete implementations, helper modules, and internal subpackages belonging to the pattern MUST reside inside this package.

---

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

---

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

---

## 3. BEHAVIORAL PATTERNS

### 3.1 Chain of Responsibility
- **Modular Layout:**
  - `[domain]_chain_of_responsibility_pattern/handler/[domain]_handler_interface.py`
  - `[domain]_chain_of_responsibility_pattern/handler/[domain]_abstract_handler.py`
  - `[domain]_chain_of_responsibility_pattern/concrete_handler/[action]_handler.py`


### 3.2 Command
- **Modular Layout:**
  - `[domain]_command_pattern/command/[domain]_command_interface.py`
  - `[domain]_command_pattern/command/[action]_command.py`
  - `[domain]_command_pattern/invoker/[domain]_invoker.py`
  - `[domain]_command_pattern/receiver/[domain]_receiver.py`

### 3.3 Iterator
- **Modular Layout:**
  - `[domain]_iterator_pattern/collection/[domain]_collection_interface.py`
  - `[domain]_iterator_pattern/collection/[domain]_concrete_collection.py`
  - `[domain]_iterator_pattern/iterator/[domain]_iterator_interface.py`
  - `[domain]_iterator_pattern/iterator/[variant]_iterator.py`

### 3.4 Mediator
- **Modular Layout:**
  - `[domain]_mediator_pattern/mediator/[domain]_mediator_interface.py`
  - `[domain]_mediator_pattern/mediator/[domain]_concrete_mediator.py`
  - `[domain]_mediator_pattern/component/[domain]_base_component.py`
  - `[domain]_mediator_pattern/component/[variant]_component.py`

### 3.5 Memento
- **Modular Layout:**
  - `[domain]_memento_pattern/originator/[domain]_originator.py`
  - `[domain]_memento_pattern/memento/[domain]_memento.py`
  - `[domain]_memento_pattern/caretaker/[domain]_caretaker.py`

### 3.6 Observer
- **Modular Layout:**
  - `[domain]_observer_pattern/publisher/[domain]_publisher_interface.py`
  - `[domain]_observer_pattern/publisher/[domain]_concrete_publisher.py`
  - `[domain]_observer_pattern/subscriber/[domain]_subscriber_interface.py`
  - `[domain]_observer_pattern/subscriber/[variant]_subscriber.py`

### 3.7 State
- **Modular Layout:**
  - `[domain]_state_pattern/state/[domain]_state_interface.py`
  - `[domain]_state_pattern/state/[variant]_state.py`
  - `[domain]_state_pattern/context/[domain]_context.py`

### 3.8 Strategy
- **Modular Layout:**
  - `[domain]_strategy_pattern/strategy/[domain]_strategy_interface.py`
  - `[domain]_strategy_pattern/strategy/[variant]_strategy.py`
  - `[domain]_strategy_pattern/context/[domain]_context.py`

### 3.9 Template Method
- **Modular Layout:**
  - `[domain]_template_method_pattern/abstract_class/[domain]_abstract_template.py`
  - `[domain]_template_method_pattern/concrete_class/[variant]_template.py`

### 3.10 Visitor
- **Modular Layout:**
  - `[domain]_visitor_pattern/element/[domain]_element_interface.py`
  - `[domain]_visitor_pattern/element/[domain]_element.py`
  - `[domain]_visitor_pattern/visitor/[domain]_visitor_interface.py`
  - `[domain]_visitor_pattern/visitor/[variant]_visitor.py`