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
