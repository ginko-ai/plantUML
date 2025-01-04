# UML Relationship Types

## Inheritance (Generalization)
- Syntax: `<|--` (solid line with hollow arrow)
- Example: `Class01 <|-- Class02`
- Meaning: Class02 inherits from Class01
- Usage: Represents "is-a" relationships
- Characteristics:
  - Child class inherits all properties and methods from parent
  - Strong coupling between classes
  - Cannot be easily changed at runtime

## Composition
- Syntax: `*--` (solid line with filled diamond)
- Example: `Class03 *-- Class04`
- Meaning: Class03 contains Class04 as a part
- Usage: Represents "owns" relationships with strong lifecycle dependency
- Characteristics:
  - Part cannot exist without the whole
  - When whole is destroyed, parts are destroyed
  - Exclusive ownership

## Aggregation
- Syntax: `o--` (solid line with hollow diamond)
- Example: `Class05 o-- Class06`
- Meaning: Class05 has Class06 as an element
- Usage: Represents "has-a" relationships with weak lifecycle dependency
- Characteristics:
  - Parts can exist independently of the whole
  - Shared ownership possible
  - Parts can be reused by other containers

## Association
- Syntax: `-->` (solid arrow)
- Example: `Class13 --> Class14`
- Meaning: Class13 uses Class14
- Usage: Represents relationships between independent classes
- Characteristics:
  - Objects know about each other
  - Can be unidirectional or bidirectional
  - Typically implemented as class attributes

## Dependency
- Syntax: `..>` (dashed arrow)
- Example: `Class15 ..> Class16`
- Meaning: Class15 depends on Class16
- Usage: Represents temporary relationships
- Characteristics:
  - Typically method parameters or local variables
  - Weaker than association
  - Changes in supplier may affect client

## Realization (Implementation)
- Syntax: `<|..` (dashed line with hollow arrow)
- Example: `Class11 <|.. Class12`
- Meaning: Class12 implements interface Class11
- Usage: Represents interface implementation
- Characteristics:
  - Implementation must provide all interface methods
  - Supports polymorphism
  - Common in design patterns

## Multiplicity
- Syntax: Using text labels like "1" or "many"
- Example: `Class01 "1" *-- "many" Class02`
- Usage: Specifies number of instances in relationship
- Common notations:
  - "1": Exactly one
  - "*" or "many": Zero or more
  - "0..1": Zero or one
  - "1..*": One or more

