#!/usr/bin/env python3



###


# XSD 1.1, Part 1: 3.1.1 Components and Properties
class Absent:
	def __repr__(self):
		return "Absent()"

# XSD 1.1, Part 1: 3.1.1 Components and Properties
class Keyword(str):
	def __init__(self, name):
		self.name = name

	def __repr__(self):
		return "{}({})".format(self.__class__.__name__, repr(self.name))


###


# XSD 1.1, Part 1: 3.1.1 Components and Properties
class PropertyGroup:
	def __init__(self, **properties):
		pass

	def __repr__(self):
		return "{}({})".format(self.__class__.__name__, ", ".join(list(map(lambda x: "{}={}".format(x[0], repr(x[1])), sorted(self.__dict__.items())))))

	def get_required_property(self, properties, property_name):
		property_value = properties.get(property_name)

		if property_value is None:
			raise KeyError("'{}' is a required property".format(property_name))

		return property_value

	def get_optional_property(self, properties, property_name):
		return properties.get(property_name, Absent())


# XSD 1.1, Part 1: 2.2 XSD Abstract Data Model
class Component(PropertyGroup):
	def __init__(self, **properties):
		super().__init__(**properties)


# XSD 1.1, Part 1: 3.1.1 Components and Properties
class PropertyRecord(PropertyGroup):
	def __init__(self, **properties):
		super().__init__(**properties)


###


# XSD 1.1, Part 1: 3.15.1 The Annotation Schema Component
class Annotation(Component):
	def __init__(self, **properties):
		super().__init__(**properties)

		application_information = properties.get("application_information", [])
		user_information = properties.get("user_information", [])
		attributes = properties.get("attributes", set())

		# TODO: Enforce Element information item on 'application_information'.
		if isinstance(application_information, list):# and all(isinstance(application_item, ElementInformationItem) for application_item in application_information):
			self.application_information = application_information
		else:
			raise TypeError("'application_information' must be a list of Element information items")

		# TODO: Enforce Element information item on 'user_information'.
		if isinstance(user_information, list):# and all(isinstance(user_item, ElementInformationItem) for user_item in user_information):
			self.user_information = user_information
		else:
			raise TypeError("'user_information' must be a list of Element information items")

		# TODO: Enforce Attribute information item on 'attributes'.
		if isinstance(attributes, set):# and all(isinstance(user_item, AttributeInformationItem) for user_item in attributes):
			self.attributes = attributes
		else:
			raise TypeError("'attributes' must be a set of Attribute information items")


# XSD 1.1, Part 1: 3.15.1 The Annotation Schema Component
class AnnotatedComponent(Component):
	def __init__(self, **properties):
		super().__init__(**properties)

		annotations = properties.get("annotations", [])

		if isinstance(annotations, list) and all(isinstance(annotation, Annotation) for annotation in annotations):
			self.annotations = annotations
		else:
			raise TypeError("'annotations' must be a list of Annotation components")


# XSD 1.1, Part 1: 2.2.1 Type Definition Components
class TypeDefinition(AnnotatedComponent):
	def __init__(self, **properties):
		super().__init__(**properties)


# XSD 1.1, Part 1: 3.4.1 The Complex Type Definition Schema Component
class ComplexTypeDefinition(TypeDefinition):
	def __init__(self, **properties):
		super().__init__(**properties)

		name = self.get_optional_property(properties, "name")
		target_namespace = self.get_optional_property(properties, "target_namespace")
		base_type_definition = self.get_required_property(properties, "base_type_definition")
		final = properties.get("final", set())
		context = self.get_optional_property(properties, "context")
		derivation_method = self.get_required_property(properties, "derivation_method")
		abstract = self.get_required_property(properties, "abstract")
		attribute_uses = properties.get("attribute_uses", set())
		attribute_wildcard = self.get_optional_property(properties, "attribute_wildcard")
		content_type = self.get_required_property(properties, "content_type")
		prohibited_substitutions = properties.get("prohibited_substitutions", set())
		assertions = properties.get("assertions", [])

		# TODO: Enforce xs:NCName on 'name'.
		if isinstance(name, (Absent, str)):
			self.name = name
		else:
			raise TypeError("'name' must be an xs:NCName value")

		# TODO: Enforce xs:anyURI on 'target_namespace'.
		if isinstance(target_namespace, (Absent, str)):
			self.target_namespace = target_namespace
		else:
			raise TypeError("'target_namespace' must be an xs:anyURI value")

		if isinstance(base_type_definition, TypeDefinition):
			self.base_type_definition = base_type_definition
		else:
			raise TypeError("'base_type_definition' must be a Type Definition component")

		if isinstance(final, set) and all(isinstance(f, Keyword) for f in final) and final <= { Keyword("extension"), Keyword("restriction") }:
			self.final = final
		else:
			raise TypeError("'final' must be a subset of { 'extension', 'restriction' }")

		if isinstance(self.name, Absent):
			if isinstance(context, (ElementDeclaration, ComplexTypeDefinition)):
				self.context = context
			else:
				raise TypeError("'context' must be either an Element Declaration component or a Complex Type Definition component if 'name' is absent")
		else:
			if isinstance(context, Absent):
				self.context = context
			else:
				raise TypeError("'context' must be absent if 'name' is not absent")

		if isinstance(derivation_method, Keyword) and derivation_method in { Keyword("extension"), Keyword("restriction") }:
			self.derivation_method = derivation_method
		else:
			raise TypeError("'derivation_method' must be one of { 'extension', 'restriction' }")

		# TODO: Enforce xs:boolean on 'abstract'.
		if isinstance(abstract, bool):
			self.abstract = abstract
		else:
			raise TypeError("'abstract' must be an xs:boolean value")

		if isinstance(attribute_uses, set) and all(isinstance(attribute_use, AttributeUse) for attribute_use in attribute_uses):
			self.attribute_uses = attribute_uses
		else:
			raise TypeError("'attribute_uses' must be a set of Attribute Use components")

		if isinstance(attribute_wildcard, (Absent, Wildcard)):
			self.attribute_wildcard = attribute_wildcard
		else:
			raise TypeError("'attribute_wildcard' must be a Wildcard component")

		if isinstance(content_type, ContentType):
			self.content_type = content_type
		else:
			raise TypeError("'content_type' must be a ContentType property record")

		if isinstance(prohibited_substitutions, set) and all(isinstance(prohibited_substitution, Keyword) for prohibited_substitution in prohibited_substitutions) and prohibited_substitutions <= { Keyword("extension"), Keyword("restriction") }:
			self.prohibited_substitutions = prohibited_substitutions
		else:
			raise TypeError("'prohibited_substitutions' must be a subset of { 'extension', 'restriction' }")

		if isinstance(assertions, list) and all(isinstance(assertion, Assertion) for assertion in assertions):
			self.assertions = assertions
		else:
			raise TypeError("'assertions' must be a list of Assertion components")



# XSD 1.1, Part 1: 3.16.1 The Simple Type Definition Schema Component
# XSD 1.1, Part 2: 4.1.1 The Simple Type Definition Schema Component
class SimpleTypeDefinitionBase(TypeDefinition):
	def __init__(self, **properties):
		super().__init__(**properties)

		name = self.get_optional_property(properties, "name")
		target_namespace = self.get_optional_property(properties, "target_namespace")
		final = properties.get("final", set())
		context = self.get_optional_property(properties, "context")
		base_type_definition = self.get_required_property(properties, "base_type_definition")
		facets = properties.get("facets", set())
		fundamental_facets = properties.get("fundamental_facets", set())
		variety = self.get_optional_property(properties, "variety")
		primitive_type_definition = self.get_optional_property(properties, "primitive_type_definition")
		item_type_definition = self.get_optional_property(properties, "item_type_definition")
		member_type_definitions = self.get_optional_property(properties, "member_type_definitions")

		# TODO: Enforce xs:NCName on 'name'.
		if isinstance(name, (Absent, str)):
			self.name = name
		else:
			raise TypeError("'name' must be an xs:NCName value")

		# TODO: Enforce xs:anyURI on 'target_namespace'.
		if isinstance(target_namespace, (Absent, str)):
			self.target_namespace = target_namespace
		else:
			raise TypeError("'target_namespace' must be an xs:anyURI value")

		if isinstance(final, set) and all(isinstance(f, Keyword) for f in final) and final <= { Keyword("restriction"), Keyword("extension"), Keyword("list"), Keyword("union") }:
			self.final = final
		else:
			raise TypeError("'final' must be a subset of { 'restriction', 'extension', 'list', 'union' }")

		if isinstance(self.name, Absent):
			if isinstance(context, (AttributeDeclaration, ElementDeclaration, ComplexTypeDefinition, SimpleTypeDefinitionBase)):
				self.context = context
			else:
				raise TypeError("'context' must be an Attribute Declaration component, an Element Declaration component, a Complex Type Definition component, or a Simple Type Definition component if 'name' is absent")
		else:
			if isinstance(context, Absent):
				self.context = context
			else:
				raise TypeError("'context' must be absent if 'name' is not absent")

		if isinstance(base_type_definition, TypeDefinition):
			self.base_type_definition = base_type_definition
		else:
			raise TypeError("'base_type_definition' must be a Type Definition component")

		if isinstance(facets, set) and all(isinstance(facet, ConstrainingFacet) for facet in facets):
			self.facets = facets
		else:
			raise TypeError("'facets' must be a set of Constraining Facet components")

		if isinstance(fundamental_facets, set) and all(isinstance(fundamental_facet, FundamentalFacet) for fundamental_facet in fundamental_facets):
			self.fundamental_facets = fundamental_facets
		else:
			raise TypeError("'fundamental_facets' must be a set of Fundamental Facet components")

		if isinstance(variety, Absent) or (isinstance(variety, Keyword) and variety in { Keyword("atomic"), Keyword("list"), Keyword("union") }):
			self.variety = variety
		else:
			raise TypeError("'variety' must be one of { 'atomic', 'list', 'union' }")

		# TODO: Enforce primitive built-in definition on 'primitive_type_definition'.
		if isinstance(primitive_type_definition, (Absent, SimpleTypeDefinitionBase)):
			self.primitive_type_definition = primitive_type_definition
		else:
			raise TypeError("'primitive_type_definition' must be a Simple Type Definition component")

		assert isinstance(self.variety, Keyword)

		if self.variety == Keyword("list"):
			# TODO: Enforce value restrictions on 'item_type_definition'.
			if isinstance(item_type_definition, SimpleTypeDefinitionBase):
				self.item_type_definition = item_type_definition
			else:
				raise TypeError("'item_type_definition' must be a Simple Type Definition component if 'variety' is 'list'")
		else:
			if isinstance(item_type_definition, Absent):
				self.item_type_definition = item_type_definition
			else:
				raise TypeError("'item_type_definition' must be absent if 'variety' is not 'list'")

		assert isinstance(self.variety, Keyword)

		if self.variety == Keyword("union"):
			if isinstance(member_type_definitions, set) and all(isinstance(member_type_definition, SimpleTypeDefinition) for member_type_definition in member_type_definitions):
				self.member_type_definitions = member_type_definitions
			else:
				raise TypeError("'member_type_definitions' must be a list of Simple Type Definition components if 'variety' is 'union'")
		else:
			if isinstance(member_type_definitions, Absent):
				self.member_type_definitions = member_type_definitions
			else:
				raise TypeError("'member_type_definitions' must be absent if 'variety' is not 'union'")


# XSD 1.1, Part 1: 3.16.1 The Simple Type Definition Schema Component
# XSD 1.1, Part 2: 4.1.1 The Simple Type Definition Schema Component
class SimpleTypeDefinition(SimpleTypeDefinitionBase):
	def __init__(self, **properties):
		super().__init__(**properties)

		if not isinstance(self.base_type_definition, SimpleTypeDefinition):
			raise TypeError("'base_type_definition' must be a Simple Type Definition component")

		if isinstance(self.variety, Absent):
			raise KeyError("'variety' is a required property")

		assert isinstance(self.variety, Keyword)

		if self.variety == Keyword("atomic"):
			if isinstance(self.primitive_type_definition, Absent):
				raise TypeError("'primitive_type_definition' must be a Simple Type Definition component if 'variety' is 'atomic'")
		else:
			if not isinstance(self.primitive_type_definition, Absent):
				raise TypeError("'primitive_type_definition' must be absent if 'variety' is not 'atomic'")


# XSD 1.1, Part 1: 2.2.3.2 Particle
class Term(AnnotatedComponent):
	def __init__(self, **properties):
		super().__init__(**properties)


# XSD 1.1, Part 1: 3.3.1 The Element Declaration Schema Component
class ElementDeclaration(Term):
	def __init__(self, **properties):
		super().__init__(**properties)

		name = self.get_required_property(properties, "name")
		target_namespace = self.get_optional_property(properties, "target_namespace")
		type_definition = self.get_required_property(properties, "type_definition")
		type_table = self.get_optional_property(properties, "type_table")
		scope = self.get_required_property(properties, "scope")
		value_constraint = self.get_optional_property(properties, "value_constraint")
		nillable = self.get_required_property(properties, "nillable")
		identity_constraint_definitions = properties.get("identity_constraint_definitions", set())
		substitution_group_affiliations = properties.get("substitution_group_affiliations", set())
		substitution_group_exclusions = properties.get("substitution_group_exclusions", set())
		disallowed_substitutions = properties.get("disallowed_substitutions", set())
		abstract = self.get_required_property(properties, "abstract")

		# TODO: Enforce xs:NCName on 'name'.
		if isinstance(name, str):
			self.name = name
		else:
			raise TypeError("'name' must be an xs:NCName value")

		# TODO: Enforce xs:anyURI on 'target_namespace'.
		if isinstance(target_namespace, (Absent, str)):
			self.target_namespace = target_namespace
		else:
			raise TypeError("'target_namespace' must be an xs:anyURI value")

		if isinstance(type_definition, TypeDefinition):
			self.type_definition = type_definition
		else:
			raise TypeError("'type_definition' must be a Type Definition component")

		if isinstance(type_table, (Absent, TypeTable)):
			self.type_table = type_table
		else:
			raise TypeError("'type_table' must be a Type Table property record")

		if isinstance(scope, ElementDeclarationScope):
			self.scope = scope
		else:
			raise TypeError("'scope' must be an Element Declaration Scope property record")

		if isinstance(value_constraint, (Absent, ElementDeclarationValueConstraint)):
			self.value_constraint = value_constraint
		else:
			raise TypeError("'value_constraint' must be an Element Declaration Value Constraint property record")

		# TODO: Enforce xs:boolean on 'nillable'.
		if isinstance(nillable, bool):
			self.nillable = nillable
		else:
			raise TypeError("'nillable' must be an xs:boolean value")

		if isinstance(identity_constraint_definitions, set) and all(isinstance(identity_constraint_definition, IdentityConstraintDefinition) for identity_constraint_definition in identity_constraint_definitions):
			self.identity_constraint_definitions = identity_constraint_definitions
		else:
			raise TypeError("'identity_constraint_definitions' must be a set of Identity-Constraint Definition components")

		if isinstance(substitution_group_affiliations, set) and all(isinstance(substitution_group_affiliation, ElementDeclaration) for substitution_group_affiliation in substitution_group_affiliations):
			self.substitution_group_affiliations = substitution_group_affiliations
		else:
			raise TypeError("'substitution_group_affiliations' must be a set of Element Declaration components")

		if isinstance(substitution_group_exclusions, set) and all(isinstance(substitution_group_exclusion, Keyword) for substitution_group_exclusion in substitution_group_exclusions) and substitution_group_exclusions <= { Keyword("extension"), Keyword("restriction") }:
			self.substitution_group_exclusions = substitution_group_exclusions
		else:
			raise TypeError("'substitution_group_exclusions' must be a subset of { 'extension', 'restriction' }")

		if isinstance(disallowed_substitutions, set) and all(isinstance(disallowed_substitution, Keyword) for disallowed_substitution in disallowed_substitutions) and disallowed_substitutions <= { Keyword("substitution"), Keyword("extension"), Keyword("restriction") }:
			self.disallowed_substitutions = disallowed_substitutions
		else:
			raise TypeError("'disallowed_substitutions' must be a subset of { 'substitution', 'extension', 'restriction' }")

		# TODO: Enforce xs:boolean on 'abstract'.
		if isinstance(abstract, bool):
			self.abstract = abstract
		else:
			raise TypeError("'abstract' must be an xs:boolean value")


# XSD 1.1, Part 1: 3.8.1 The Model Group Schema Component
class ModelGroup(Term):
	def __init__(self, **properties):
		super().__init__(**properties)

		compositor = self.get_required_property(properties, "compositor")
		particles = properties.get("particles", [])

		if isinstance(compositor, Keyword) and compositor in { Keyword("all"), Keyword("choice"), Keyword("sequence") }:
			self.compositor = compositor
		else:
			raise TypeError("'compositor' must be one of { 'all', 'choice', 'sequence' }")

		if isinstance(particles, list) and all(isinstance(particle, Particle) for particle in particles):
			self.particles = particles
		else:
			raise TypeError("'particles' must be a list of Particle components")


# XSD 1.1, Part 1: 3.10.1 The Wildcard Schema Component
class Wildcard(Term):
	def __init__(self, **properties):
		super().__init__(**properties)

		namespace_constraint = self.get_required_property(properties, "namespace_constraint")
		process_contents = self.get_required_property(properties, "process_contents")

		if isinstance(namespace_constraint, NamespaceConstraint):
			self.namespace_constraint = namespace_constraint
		else:
			raise TypeError("'namespace_constraint' must be a Namespace Constraint property record")

		if isinstance(process_contents, Keyword) and process_contents in { Keyword("skip"), Keyword("strict"), Keyword("lax") }:
			self.process_contents = process_contents
		else:
			raise TypeError("'process_contents' must be one of { 'skip', 'strict', 'lax' }")


# XSD 1.1, Part 1: 3.9.1 The Particle Schema Component
# NOTE: The spec doesn't explicitly call Particle an Annotated Component.
class Particle(AnnotatedComponent):
	def __init__(self, **properties):
		super().__init__(**properties)

		min_occurs = self.get_required_property(properties, "min_occurs")
		max_occurs = self.get_required_property(properties, "max_occurs")
		term = self.get_required_property(properties, "term")

		# TODO: Enforce xs:nonNegativeInteger on 'min_occurs'.
		if isinstance(min_occurs, int) and min_occurs >= 0:
			self.min_occurs = min_occurs
		else:
			raise TypeError("'min_occurs' must be an xs:nonNegativeInteger value")

		# TODO: Enforce xs:positiveInteger on 'max_occurs'.
		# NOTE: The spec just says "positive integer", not "xs:positiveInteger".
		if (isinstance(max_occurs, int) and max_occurs >= 1) or (isinstance(max_occurs, Keyword) and max_occurs == Keyword("unbounded")):
			self.max_occurs = max_occurs
		else:
			raise TypeError("'max_occurs' must be an xs:positiveInteger value or 'unbounded'")

		if isinstance(term, Term):
			self.term = term
		else:
			raise TypeError("'term' must be a Term component")


# XSD 1.1, Part 1: 3.2.1 The Attribute Declaration Schema Component
class AttributeDeclaration(AnnotatedComponent):
	def __init__(self, **properties):
		super().__init__(**properties)

		name = self.get_required_property(properties, "name")
		target_namespace = self.get_optional_property(properties, "target_namespace")
		type_definition = self.get_required_property(properties, "type_definition")
		scope = self.get_required_property(properties, "scope")
		value_constraint = self.get_optional_property(properties, "value_constraint")
		inheritable = self.get_required_property(properties, "inheritable")

		# TODO: Enforce xs:NCName on 'name'.
		if isinstance(name, str):
			self.name = name
		else:
			raise TypeError("'name' must be an xs:NCName value")

		# TODO: Enforce xs:anyURI on 'target_namespace'.
		if isinstance(target_namespace, (Absent, str)):
			self.target_namespace = target_namespace
		else:
			raise TypeError("'target_namespace' must be an xs:anyURI value")

		if isinstance(type_definition, SimpleTypeDefinition):
			self.type_definition = type_definition
		else:
			raise TypeError("'type_definition' must be a Simple Type Definition component")

		if isinstance(scope, AttributeDeclarationScope):
			self.scope = scope
		else:
			raise TypeError("'scope' must be an Attribute Declaration Scope property record")

		if isinstance(value_constraint, (Absent, AttributeDeclarationValueConstraint)):
			self.value_constraint = value_constraint
		else:
			raise TypeError("'value_constraint' must be an Attribute Declaration Value Constraint property record")

		# TODO: Enforce xs:boolean on 'inheritable'.
		if isinstance(inheritable, bool):
			self.inheritable = inheritable
		else:
			raise TypeError("'inheritable' must be an xs:boolean value")



# XSD 1.1, Part 1: 3.5.1 The Attribute Use Schema Component
class AttributeUse(AnnotatedComponent):
	def __init__(self, **properties):
		super().__init__(**properties)

		required = self.get_required_property(properties, "required")
		attribute_declaration = self.get_required_property(properties, "attribute_declaration")
		value_constraint = self.get_optional_property(properties, "value_constraint")
		inheritable = self.get_required_property(properties, "inheritable")

		# TODO: Enforce xs:boolean on 'required'.
		if isinstance(required, bool):
			self.required = required
		else:
			raise TypeError("'required' must be an xs:boolean value")

		if isinstance(attribute_declaration, AttributeDeclaration):
			self.attribute_declaration = attribute_declaration
		else:
			raise TypeError("'attribute_declaration' must be an Attribute Declaration component")

		if isinstance(value_constraint, (Absent, AttributeUseValueConstraint)):
			self.value_constraint = value_constraint
		else:
			raise TypeError("'value_constraint' must be an Attribute Declaration Value Constraint property record")

		# TODO: Enforce xs:boolean on 'inheritable'.
		if isinstance(inheritable, bool):
			self.inheritable = inheritable
		else:
			raise TypeError("'inheritable' must be an xs:boolean value")


# XSD 1.1, Part 1: 3.6.1 The Attribute Group Definition Schema Component
class AttributeGroupDefinition(AnnotatedComponent):
	def __init__(self, **properties):
		super().__init__(**properties)

		name = self.get_required_property(properties, "name")
		target_namespace = self.get_optional_property(properties, "target_namespace")
		attribute_uses = properties.get("attribute_uses", set())
		attribute_wildcard = self.get_optional_property(properties, "attribute_wildcard")

		# TODO: Enforce xs:NCName on 'name'.
		if isinstance(name, str):
			self.name = name
		else:
			raise TypeError("'name' must be an xs:NCName value")

		# TODO: Enforce xs:anyURI on 'target_namespace'.
		if isinstance(target_namespace, (Absent, str)):
			self.target_namespace = target_namespace
		else:
			raise TypeError("'target_namespace' must be an xs:anyURI value")

		if isinstance(attribute_uses, set) and all(isinstance(attribute_use, AttributeUse) for attribute_use in attribute_uses):
			self.attribute_uses = attribute_uses
		else:
			raise TypeError("'attribute_uses' must be a set of Attribute Use components")

		if isinstance(attribute_wildcard, (Absent, Wildcard)):
			self.attribute_wildcard = attribute_wildcard
		else:
			raise TypeError("'attribute_wildcard' must be a Wildcard component")


# XSD 1.1, Part 1: 3.7.1 The Model Group Definition Schema Component
class ModelGroupDefinition(AnnotatedComponent):
	def __init__(self, **properties):
		super().__init__(**properties)

		name = self.get_required_property(properties, "name")
		target_namespace = self.get_optional_property(properties, "target_namespace")
		model_group = self.get_required_property(properties, "model_group")

		# TODO: Enforce xs:NCName on 'name'.
		if isinstance(name, str):
			self.name = name
		else:
			raise TypeError("'name' must be an xs:NCName value")

		# TODO: Enforce xs:anyURI on 'target_namespace'.
		if isinstance(target_namespace, (Absent, str)):
			self.target_namespace = target_namespace
		else:
			raise TypeError("'target_namespace' must be an xs:anyURI value")

		if isinstance(model_group, ModelGroup):
			self.model_group = model_group
		else:
			raise TypeError("'model_group' must be a Model Group component")


# XSD 1.1, Part 1: 3.11.1 The Identity-constraint Definition Schema Component
class IdentityConstraintDefinition(AnnotatedComponent):
	def __init__(self, **properties):
		super().__init__(**properties)

		name = self.get_required_property(properties, "name")
		target_namespace = self.get_optional_property(properties, "target_namespace")
		identity_constraint_category = self.get_required_property(properties, "identity_constraint_category")
		selector = self.get_required_property(properties, "selector")
		fields = properties.get("fields", [])
		referenced_key = self.get_optional_property(properties, "referenced_key")

		# TODO: Enforce xs:NCName on 'name'.
		if isinstance(name, str):
			self.name = name
		else:
			raise TypeError("'name' must be an xs:NCName value")

		# TODO: Enforce xs:anyURI on 'target_namespace'.
		if isinstance(target_namespace, (Absent, str)):
			self.target_namespace = target_namespace
		else:
			raise TypeError("'target_namespace' must be an xs:anyURI value")

		if isinstance(identity_constraint_category, Keyword) and identity_constraint_category in { Keyword("key"), Keyword("keyref"), Keyword("unique") }:
			self.identity_constraint_category = identity_constraint_category
		else:
			raise TypeError("'identity_constraint_category' must be one of { 'key', 'keyref', 'unique' }")

		if isinstance(selector, XPathExpression):
			self.selector = selector
		else:
			raise TypeError("'selector' must be an XPath Expression property record")

		if isinstance(fields, list) and all(isinstance(field, XPathExpression) for field in fields):
			self.fields = fields
		else:
			raise TypeError("'fields' must be a list of XPath Expression property records")

		assert isinstance(self.identity_constraint_category, Keyword)

		if self.identity_constraint_category == Keyword("keyref"):
			if isinstance(referenced_key, IdentityConstraintDefinition):
				assert isinstance(referenced_key.identity_constraint_category, Keyword)

				if referenced_key.identity_constraint_category in { Keyword("key"), Keyword("unique") }:
					self.referenced_key = referenced_key
				else:
					raise TypeError("'identity_constraint_category' of 'referenced_key' must be one of { 'key', 'unique' }")
			else:
				raise TypeError("'referenced_key' must be an Identity-Constraint Definition component")
		else:
			if isinstance(referenced_key, Absent):
				self.referenced_key = referenced_key
			else:
				raise TypeError("'referenced_key' must be absent if 'identity_constraint_category' is not 'keyref'")


# XSD 1.1, Part 1: 3.12.1 The Type Alternative Schema Component
class TypeAlternative(AnnotatedComponent):
	def __init__(self, **properties):
		super().__init__(**properties)

		test = self.get_optional_property(properties, "test")
		type_definition = self.get_required_property(properties, "type_definition")

		if isinstance(test, (Absent, XPathExpression)):
			self.test = test
		else:
			raise TypeError("'test' must be an XPath Expression property record")

		if isinstance(type_definition, TypeDefinition):
			self.type_definition = type_definition
		else:
			raise TypeError("'type_definition' must be a Type Definition component")


# XSD 1.1, Part 1: 3.13.1 The Assertion Schema Component
class Assertion(AnnotatedComponent):
	def __init__(self, **properties):
		super().__init__(**properties)

		test = self.get_required_property(properties, "test")

		if isinstance(test, XPathExpression):
			self.test = test
		else:
			raise TypeError("'test' must be an XPath Expression property record")


# XSD 1.1, Part 1: 3.14.1 The Notation Declaration Schema Component
class NotationDeclaration(AnnotatedComponent):
	def __init__(self, **properties):
		super().__init__(**properties)

		name = self.get_required_property(properties, "name")
		target_namespace = self.get_optional_property(properties, "target_namespace")
		system_identifier = self.get_optional_property(properties, "system_identifier")
		target_identifier = self.get_optional_property(properties, "target_identifier")

		# Enforce the mutually-dependendent property requirement.
		if isinstance(system_identifier, Absent) and isinstance(target_identifier, Absent):
			raise KeyError("One of 'system_identifier' or 'target_identifier' is a required property")

		# TODO: Enforce xs:NCName on 'name'.
		if isinstance(name, str):
			self.name = name
		else:
			raise TypeError("'name' must be an xs:NCName value")

		# TODO: Enforce xs:anyURI on 'target_namespace'.
		if isinstance(target_namespace, (Absent, str)):
			self.target_namespace = target_namespace
		else:
			raise TypeError("'target_namespace' must be an xs:anyURI value")

		# TODO: Enforce xs:anyURI on 'system_identifier'.
		if isinstance(system_identifier, (Absent, str)):
			self.system_identifier = system_identifier
		else:
			raise TypeError("'system_identifier' must be an xs:anyURI value")

		# TODO: Enforce XML publicID on 'target_identifier'.
		if isinstance(target_identifier, (Absent, str)):
			self.target_identifier = target_identifier
		else:
			raise TypeError("'target_identifier' must be an XML publicID value")


# XSD 1.1, Part 1: 3.17.1 The Schema Itself
class Schema(AnnotatedComponent):
	def __init__(self, **properties):
		super().__init__(**properties)

		type_definitions = properties.get("type_definitions", set())
		attribute_declarations = properties.get("attribute_declarations", set())
		element_declarations = properties.get("element_declarations", set())
		attribute_group_definitions = properties.get("attribute_group_definitions", set())
		model_group_definitions = properties.get("model_group_definitions", set())
		notation_declarations = properties.get("notation_declarations", set())
		identity_constraint_definitions = properties.get("identity_constraint_definitions", set())

		if isinstance(type_definitions, set) and all(isinstance(type_definition, TypeDefinition) for type_definition in type_definitions):
			self.type_definitions = type_definitions
		else:
			raise TypeError("'type_definitions' must be a set of Type Definition components")

		if isinstance(attribute_declarations, set) and all(isinstance(attribute_declaration, AttributeDeclaration) for attribute_declaration in attribute_declarations):
			self.attribute_declarations = attribute_declarations
		else:
			raise TypeError("'attribute_declarations' must be a set of Attribute Declaration components")

		if isinstance(element_declarations, set) and all(isinstance(element_declaration, ElementDeclaration) for element_declaration in element_declarations):
			self.element_declarations = element_declarations
		else:
			raise TypeError("'element_declarations' must be a set of Element Declaration components")

		if isinstance(attribute_group_definitions, set) and all(isinstance(attribute_group_definition, AttributeGroupDefinition) for attribute_group_definition in attribute_group_definitions):
			self.attribute_group_definitions = attribute_group_definitions
		else:
			raise TypeError("'attribute_group_definitions' must be a set of Attribute Group Definition components")

		if isinstance(model_group_definitions, set) and all(isinstance(model_group_definition, ModelGroupDefinition) for model_group_definition in model_group_definitions):
			self.model_group_definitions = model_group_definitions
		else:
			raise TypeError("'model_group_definitions' must be a set of Model Group Definition components")

		if isinstance(notation_declarations, set) and all(isinstance(notation_declaration, NotationDeclaration) for notation_declaration in notation_declarations):
			self.notation_declarations = notation_declarations
		else:
			raise TypeError("'notation_declarations' must be a set of Notation Declaration components")

		if isinstance(identity_constraint_definitions, set) and all(isinstance(identity_constraint_definition, IdentityConstraintDefinition) for identity_constraint_definition in identity_constraint_definitions):
			self.identity_constraint_definitions = identity_constraint_definitions
		else:
			raise TypeError("'identity_constraint_definitions' must be a set of Identity-Constraint Definition components")


###


# XSD 1.1, Part 1: 3.2.1 The Attribute Declaration Schema Component
# XSD 1.1, Part 1: 3.3.1 The Element Declaration Schema Component
class Scope(PropertyRecord):
	def __init__(self, **properties):
		super().__init__(**properties)

		variety = self.get_required_property(properties, "variety")
		parent = self.get_optional_property(properties, "parent")

		if isinstance(variety, Keyword) and variety in { Keyword("global"), Keyword("local") }:
			self.variety = variety
		else:
			raise TypeError("'variety' must be one of { 'global', 'local' }")

		assert isinstance(self.variety, Keyword)

		if self.variety != Keyword("local"):
			if isinstance(parent, Absent):
				self.parent = parent
			else:
				raise TypeError("'parent' must be absent if 'variety' is not 'local'")


# XSD 1.1, Part 1: 3.2.1 The Attribute Declaration Schema Component
class AttributeDeclarationScope(Scope):
	def __init__(self, **properties):
		super().__init__(**properties)

		assert isinstance(self.variety, Keyword)

		if self.variety == Keyword("local"):
			if isinstance(parent, (ComplexTypeDefinition, AttributeGroupDefinition)):
				self.parent = parent
			else:
				raise TypeError("'parent' must be either a Complex Type Definition component or an Attribute Group Definition component if 'variety' is 'local'")


# XSD 1.1, Part 1: 3.3.1 The Element Declaration Schema Component
class ElementDeclarationScope(Scope):
	def __init__(self, **properties):
		super().__init__(**properties)

		assert isinstance(self.variety, Keyword)

		if self.variety == Keyword("local"):
			if isinstance(parent, (ComplexTypeDefinition, ModelGroupDefinition)):
				self.parent = parent
			else:
				raise TypeError("'parent' must be either a Complex Type Definition component or a Model Group Definition component if 'variety' is 'local'")


# XSD 1.1, Part 1: 3.2.1 The Attribute Declaration Schema Component
# XSD 1.1, Part 1: 3.3.1 The Element Declaration Schema Component
# XSD 1.1, Part 1: 3.5.1 The Attribute Use Schema Component
class ValueConstraint(PropertyRecord):
	def __init__(self, **properties):
		super().__init__(**properties)

		variety = self.get_required_property(properties, "variety")
		value = self.get_required_property(properties, "value")
		lexical_form = self.get_required_property(properties, "lexical_form")

		if isinstance(variety, Keyword) and variety in { Keyword("default"), Keyword("fixed") }:
			self.variety = variety
		else:
			raise TypeError("'variety' must be one of { 'default', 'fixed' }")

		# TODO: Enforce 'actual value' on 'value'.
		if isinstance(value, str):
			self.value = value
		else:
			raise TypeError("'value' must be an actual value")

		# TODO: Enforce 'character string' on 'lexical form'.
		if isinstance(lexical_form, str):
			self.lexical_form = lexical_form
		else:
			raise TypeError("'lexical_form' must be a character string")


# XSD 1.1, Part 1: 3.2.1 The Attribute Declaration Schema Component
class AttributeDeclarationValueConstraint(ValueConstraint):
	def __init__(self, **properties):
		super().__init__(**properties)


# XSD 1.1, Part 1: 3.3.1 The Element Declaration Schema Component
class ElementDeclarationValueConstraint(ValueConstraint):
	def __init__(self, **properties):
		super().__init__(**properties)


# XSD 1.1, Part 1: 3.5.1 The Attribute Use Schema Component
class AttributeUseValueConstraint(ValueConstraint):
	def __init__(self, **properties):
		super().__init__(**properties)


# XSD 1.1, Part 1: 3.3.1 The Element Declaration Schema Component
class TypeTable(PropertyRecord):
	def __init__(self, **properties):
		super().__init__(**properties)

		alternatives = properties.get("alternatives", [])
		default_type_definition = self.get_required_property(properties, "default_type_definition")

		if isinstance(alternatives, list) and all(isinstance(alternative, TypeAlternative) for alternative in alternatives):
			self.alternatives = alternatives
		else:
			raise TypeError("'alternatives' must be a list of Type Alternative components")

		if isinstance(default_type_definition, TypeAlternative):
			self.default_type_definition = default_type_definition
		else:
			raise TypeError("'default_type_definition' must be a Type Alternative component")


# XSD 1.1, Part 1: 3.4.1 The Complex Type Definition Schema Component
class ContentType(PropertyRecord):
	def __init__(self, **properties):
		super().__init__(**properties)

		variety = self.get_required_property(properties, "variety")
		particle = self.get_optional_property(properties, "particle")
		open_content = self.get_optional_property(properties, "open_content")
		simple_type_definition = self.get_optional_property(properties, "simple_type_definition")

		if isinstance(variety, Keyword) and variety in { Keyword("empty"), Keyword("simple"), Keyword("element-only"), Keyword("mixed") }:
			self.variety = variety
		else:
			raise TypeError("'variety' must be one of { 'empty', 'simple', 'element-only', 'mixed' }")

		assert isinstance(self.variety, Keyword)

		if self.variety in { Keyword("element-only"), Keyword("mixed") }:
			if isinstance(particle, Particle):
				self.particle = particle
			else:
				raise TypeError("'particle' must be a Particle component if 'variety' is 'element-only' or 'mixed'")
		else:
			if isinstance(particle, Absent):
				self.particle = particle
			else:
				raise TypeError("'particle' must be absent if 'variety' is not 'element-only' or 'mixed'")

		assert isinstance(self.variety, Keyword)

		if self.variety in { Keyword("element-only"), Keyword("mixed") }:
			if isinstance(open_content, (Absent, OpenContent)):
				self.open_content = open_content
			else:
				raise TypeError("'open_content' must be an Open Content property record if 'variety' is 'element-only' or 'mixed'")
		else:
			if isinstance(open_content, Absent):
				self.open_content = open_content
			else:
				raise TypeError("'open_content' must be absent if 'variety' is not 'element-only' or 'mixed'")

		assert isinstance(self.variety, Keyword)

		if self.variety == Keyword("simple"):
			if isinstance(simple_type_definition, SimpleTypeDefinition):
				self.simple_type_definition = simple_type_definition
			else:
				raise TypeError("'simple_type_definition' must be a Simple Type Definition component if 'variety' is 'simple'")
		else:
			if isinstance(simple_type_definition, Absent):
				self.simple_type_definition = simple_type_definition
			else:
				raise TypeError("'simple_type_definition' must be absent if 'variety' is not 'simple'")


# XSD 1.1, Part 1: 3.4.1 The Complex Type Definition Schema Component
class OpenContent(PropertyRecord):
	def __init__(self, **properties):
		super().__init__(**properties)

		mode = self.get_required_property(properties, "mode")
		wildcard = self.get_required_property(properties, "wildcard")

		if isinstance(mode, Keyword) and mode in { Keyword("interleave"), Keyword("suffix") }:
			self.mode = mode
		else:
			raise TypeError("'mode' must be one of { 'interleave', 'suffix' }")

		if isinstance(wildcard, Wildcard):
			self.wildcard = wildcard
		else:
			raise TypeError("'wildcard' must be a Wildcard component")


# XSD 1.1, Part 1: 3.10.1 The Wildcard Schema Component
class NamespaceConstraint(PropertyRecord):
	def __init__(self, **properties):
		super().__init__(**properties)

		variety = self.get_required_property(properties, "variety")
		namespaces = self.get_required_property(properties, "namespaces")
		disallowed_names = self.get_required_property(properties, "disallowed_names")

		if isinstance(variety, Keyword) and variety in { Keyword("any"), Keyword("enumeration"), Keyword("not") }:
			self.variety = variety
		else:
			raise TypeError("'variety' must be one of { 'any', 'enumeration', 'not' }")

		# TODO: Enforce xs:anyURI on 'namespaces'.
		if isinstance(namespaces, set) and all(isinstance(namespace, (Absent, str)) for namespace in namespaces):
			self.namespaces = namespaces
		else:
			raise TypeError("'namespaces' must be a set each of whose members is either an xs:anyURI value or the distinguished value absent")

		# TODO: Enforce xs:QName on 'disallowed_names'.
		if isinstance(disallowed_names, set) and all(isinstance(disallowed_name, str) or (isinstance(disallowed_name, Keyword) and disallowed_name in { Keyword("defined"), Keyword("sibling") }) for disallowed_name in disallowed_names):
			self.disallowed_names = disallowed_names
		else:
			raise TypeError("'disallowed_names' must be a set each of whose members is either an xs:QName value or the keyword 'defined' or the keyword 'sibling'")


# XSD 1.1, Part 1: 3.13.1 The Assertion Schema Component
class XPathExpression(PropertyRecord):
	def __init__(self, **properties):
		super().__init__(**properties)

		namespace_bindings = properties.get("namespace_bindings", set())
		default_namespace = self.get_optional_property(properties, "default_namespace")
		base_uri = self.get_optional_property(properties, "base_uri")
		expression = self.get_required_property(properties, "expression")

		if isinstance(namespace_bindings, set) and all(isinstance(namespace_binding, NamespaceBinding) for namespace_binding in namespace_bindings):
			self.namespace_bindings = namespace_bindings
		else:
			raise TypeError("'namespace_bindings' must be a set of Namespace Binding property records")

		# TODO: Enforce xs:anyURI on 'default_namespace'.
		if isinstance(default_namespace, (Absent, str)):
			self.default_namespace = default_namespace
		else:
			raise TypeError("'default_namespace' must be an xs:anyURI value")

		# TODO: Enforce xs:anyURI on 'base_uri'.
		if isinstance(base_uri, (Absent, str)):
			self.base_uri = base_uri
		else:
			raise TypeError("'base_uri' must be an xs:anyURI value")

		# TODO: Enforce XPath 2.0 expression on 'expression'.
		if isinstance(expression, str):
			self.expression = expression
		else:
			raise TypeError("'expression' must be an XPath 2.0 expression")


# XSD 1.1, Part 1: 3.13.1 The Assertion Schema Component
class NamespaceBinding(PropertyRecord):
	def __init__(self, **properties):
		super().__init__(**properties)

		prefix = self.get_required_property(properties, "prefix")
		namespace = self.get_required_property(properties, "namespace")

		# TODO: Enforce xs:NCName on 'prefix'.
		if isinstance(prefix, str):
			self.prefix = prefix
		else:
			raise TypeError("'prefix' must be an xs:NCName value")

		# TODO: Enforce xs:anyURI on 'namespace'.
		if isinstance(namespace, str):
			self.namespace = namespace
		else:
			raise TypeError("'namespace' must be an xs:anyURI value")


####


# XSD 1.1, Part 2: 4.2 Fundamental Facets
class FundamentalFacet(Component):
	def __init__(self, **properties):
		super().__init__(**properties)


# XSD 1.1, Part 2: 4.2.1.1 The ordered Schema Component
class Ordered(FundamentalFacet):
	def __init__(self, **properties):
		super().__init__(**properties)

		value = self.get_required_property(properties, "value")

		if isinstance(value, Keyword) and value in { Keyword("false"), Keyword("partial"), Keyword("total") }:
			self.value = value
		else:
			raise TypeError("'value' must be one of { 'false', 'partial', 'total' }")


# XSD 1.1, Part 2: 4.2.2.1 The bounded Schema Component
class Bounded(FundamentalFacet):
	def __init__(self, **properties):
		super().__init__(**properties)

		value = self.get_required_property(properties, "value")

		# TODO: Enforce xs:boolean on 'value'.
		if isinstance(value, bool):
			self.value = value
		else:
			raise TypeError("'value' must be an xs:boolean value")


# XSD 1.1, Part 2: 4.2.3.1 The cardinality Schema Component
class Cardinality(FundamentalFacet):
	def __init__(self, **properties):
		super().__init__(**properties)

		value = self.get_required_property(properties, "value")

		if isinstance(value, Keyword) and value in { Keyword("finite"), Keyword("countably infinite") }:
			self.value = value
		else:
			raise TypeError("'value' must be one of { 'finite', 'countably infinite' }")


# XSD 1.1, Part 2: 4.2.4.1 The numeric Schema Component
class Numeric(FundamentalFacet):
	def __init__(self, **properties):
		super().__init__(**properties)

		value = self.get_required_property(properties, "value")

		# TODO: Enforce xs:boolean on 'value'.
		if isinstance(value, bool):
			self.value = value
		else:
			raise TypeError("'value' must be an xs:boolean value")


####


# XSD 1.1, Part 2: 4.3 Constraining Facets
class ConstrainingFacet(AnnotatedComponent):
	def __init__(self, **properties):
		super().__init__(**properties)


# XSD 1.1, Part 2: 4.3.1.1 The length Schema Component
class Length(ConstrainingFacet):
	def __init__(self, **properties):
		super().__init__(**properties)

		value = self.get_required_property(properties, "value")
		fixed = self.get_required_property(properties, "fixed")

		# TODO: Enforce xs:nonNegativeInteger on 'value'.
		if isinstance(value, int) and value >= 0:
			self.value = value
		else:
			raise TypeError("'value' must be an xs:nonNegativeInteger value")

		# TODO: Enforce xs:boolean on 'fixed'.
		if isinstance(fixed, bool):
			self.fixed = fixed
		else:
			raise TypeError("'fixed' must be an xs:boolean fixed")


# XSD 1.1, Part 2: 4.3.2.1 The minLength Schema Component
class MinLength(ConstrainingFacet):
	def __init__(self, **properties):
		super().__init__(**properties)

		value = self.get_required_property(properties, "value")
		fixed = self.get_required_property(properties, "fixed")

		# TODO: Enforce xs:nonNegativeInteger on 'value'.
		if isinstance(value, int) and value >= 0:
			self.value = value
		else:
			raise TypeError("'value' must be an xs:nonNegativeInteger value")

		# TODO: Enforce xs:boolean on 'fixed'.
		if isinstance(fixed, bool):
			self.fixed = fixed
		else:
			raise TypeError("'fixed' must be an xs:boolean fixed")


# XSD 1.1, Part 2: 4.3.3.1 The maxLength Schema Component
class MaxLength(ConstrainingFacet):
	def __init__(self, **properties):
		super().__init__(**properties)

		value = self.get_required_property(properties, "value")
		fixed = self.get_required_property(properties, "fixed")

		# TODO: Enforce xs:nonNegativeInteger on 'value'.
		if isinstance(value, int) and value >= 0:
			self.value = value
		else:
			raise TypeError("'value' must be an xs:nonNegativeInteger value")

		# TODO: Enforce xs:boolean on 'fixed'.
		if isinstance(fixed, bool):
			self.fixed = fixed
		else:
			raise TypeError("'fixed' must be an xs:boolean fixed")


# XSD 1.1, Part 2: 4.3.4.1 The pattern Schema Component
class Pattern(ConstrainingFacet):
	def __init__(self, **properties):
		super().__init__(**properties)

		value = self.get_required_property(properties, "value")

		# TODO: Enforce regular expressions on 'value'.
		if isinstance(value, set) and (len(value) > 0) and all(isinstance(v, str) for v in value):
			self.value = value
		else:
			raise TypeError("'value' must be a non-empty set of regular expressions")


# XSD 1.1, Part 2: 4.3.5.1 The enumeration Schema Component
class Enumeration(ConstrainingFacet):
	def __init__(self, **properties):
		super().__init__(**properties)

		value = properties.get("value", set())

		# TODO: Enforce value space on 'value'.
		if isinstance(value, set):# and all(isinstance(v, x) for v in value):
			self.value = value
		else:
			raise TypeError("'value' must be a set of values from the value space of 'base_type_definition'")


# XSD 1.1, Part 2: 4.3.6.1 The whiteSpace Schema Component
class WhiteSpace(ConstrainingFacet):
	def __init__(self, **properties):
		super().__init__(**properties)

		value = self.get_required_property(properties, "value")
		fixed = self.get_required_property(properties, "fixed")

		if isinstance(value, Keyword) and value in { Keyword("preserve"), Keyword("replace"), Keyword("collapse") }:
			self.value = value
		else:
			raise TypeError("'value' must be one of { 'preserve', 'replace', 'collapse' }")

		# TODO: Enforce xs:boolean on 'fixed'.
		if isinstance(fixed, bool):
			self.fixed = fixed
		else:
			raise TypeError("'fixed' must be an xs:boolean fixed")


# XSD 1.1, Part 2: 4.3.7.1 The maxInclusive Schema Component
class MaxInclusive(ConstrainingFacet):
	def __init__(self, **properties):
		super().__init__(**properties)

		value = self.get_required_property(properties, "value")
		fixed = self.get_required_property(properties, "fixed")

		# TODO: Enforce value space on 'value'.
		if True:
			self.value = value
		else:
			raise TypeError("'value' must be a value from the value space of 'base_type_definition'")

		# TODO: Enforce xs:boolean on 'fixed'.
		if isinstance(fixed, bool):
			self.fixed = fixed
		else:
			raise TypeError("'fixed' must be an xs:boolean fixed")

# XSD 1.1, Part 2: 4.3.8.1 The maxExclusive Schema Component
class MaxExclusive(ConstrainingFacet):
	def __init__(self, **properties):
		super().__init__(**properties)

		value = self.get_required_property(properties, "value")
		fixed = self.get_required_property(properties, "fixed")

		# TODO: Enforce value space on 'value'.
		if True:
			self.value = value
		else:
			raise TypeError("'value' must be a value from the value space of 'base_type_definition'")

		# TODO: Enforce xs:boolean on 'fixed'.
		if isinstance(fixed, bool):
			self.fixed = fixed
		else:
			raise TypeError("'fixed' must be an xs:boolean fixed")

# XSD 1.1, Part 2: 4.3.9.1 The minExclusive Schema Component
class MinExclusive(ConstrainingFacet):
	def __init__(self, **properties):
		super().__init__(**properties)

		value = self.get_required_property(properties, "value")
		fixed = self.get_required_property(properties, "fixed")

		# TODO: Enforce value space on 'value'.
		if True:
			self.value = value
		else:
			raise TypeError("'value' must be a value from the value space of 'base_type_definition'")

		# TODO: Enforce xs:boolean on 'fixed'.
		if isinstance(fixed, bool):
			self.fixed = fixed
		else:
			raise TypeError("'fixed' must be an xs:boolean fixed")

# XSD 1.1, Part 2: 4.3.10.1 The minInclusive Schema Component
class MinInclusive(ConstrainingFacet):
	def __init__(self, **properties):
		super().__init__(**properties)

		value = self.get_required_property(properties, "value")
		fixed = self.get_required_property(properties, "fixed")

		# TODO: Enforce value space on 'value'.
		if True:
			self.value = value
		else:
			raise TypeError("'value' must be a value from the value space of 'base_type_definition'")

		# TODO: Enforce xs:boolean on 'fixed'.
		if isinstance(fixed, bool):
			self.fixed = fixed
		else:
			raise TypeError("'fixed' must be an xs:boolean fixed")

# XSD 1.1, Part 2: 4.3.11.1 The totalDigits Schema Component
class TotalDigits(ConstrainingFacet):
	def __init__(self, **properties):
		super().__init__(**properties)

		value = self.get_required_property(properties, "value")
		fixed = self.get_required_property(properties, "fixed")

		# TODO: Enforce xs:positiveInteger on 'value'.
		if isinstance(value, int) and value >= 1:
			self.value = value
		else:
			raise TypeError("'value' must be an xs:positiveInteger value")

		# TODO: Enforce xs:boolean on 'fixed'.
		if isinstance(fixed, bool):
			self.fixed = fixed
		else:
			raise TypeError("'fixed' must be an xs:boolean fixed")

# XSD 1.1, Part 2: 4.3.12.1 The fractionDigits Schema Component
class FractionDigits(ConstrainingFacet):
	def __init__(self, **properties):
		super().__init__(**properties)

		value = self.get_required_property(properties, "value")
		fixed = self.get_required_property(properties, "fixed")

		# TODO: Enforce xs:nonNegativeInteger on 'value'.
		if isinstance(value, int) and value >= 0:
			self.value = value
		else:
			raise TypeError("'value' must be an xs:nonNegativeInteger value")

		# TODO: Enforce xs:boolean on 'fixed'.
		if isinstance(fixed, bool):
			self.fixed = fixed
		else:
			raise TypeError("'fixed' must be an xs:boolean fixed")

# XSD 1.1, Part 2: 4.3.13.1 The assertions Schema Component
class Assertions(ConstrainingFacet):
	def __init__(self, **properties):
		super().__init__(**properties)

		value = properties.get("value", [])

		if isinstance(assertions, list) and all(isinstance(assertion, Assertion) for assertion in assertions):
			self.assertions = assertions
		else:
			raise TypeError("'assertions' must be a list of Assertion components")


# XSD 1.1, Part 2: 4.3.14.1 The explicitTimezone Schema Component
class ExplicitTimezone(ConstrainingFacet):
	def __init__(self, **properties):
		super().__init__(**properties)

		value = self.get_required_property(properties, "value")
		fixed = self.get_required_property(properties, "fixed")

		if isinstance(value, Keyword) and value in { Keyword("required"), Keyword("prohibited"), Keyword("optional") }:
			self.value = value
		else:
			raise TypeError("'value' must be one of { 'required', 'prohibited', 'optional' }")

		# TODO: Enforce xs:boolean on 'fixed'.
		if isinstance(fixed, bool):
			self.fixed = fixed
		else:
			raise TypeError("'fixed' must be an xs:boolean fixed")


