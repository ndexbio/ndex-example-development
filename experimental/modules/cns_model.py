indra_edge_types = ["Acetylation",
                    "Dephosphorylation",
                    "Phosphorylation",
                    "RasGef",
                    "Ribosylation",
                    "Ubiquitination"
                    ]

predicate_translation = {
    "Phosphorylation": "phosphorylates",
    "controls-phosphorylation-of": "phosphorylates",
    "Acetylation": "acetylates",
    "Dephosphorylation": "dephosphorylates",
    "RasGef": "negativeRegulationViaGEF"
}

directed_predicates = [
    "phosphorylates",
    "acetylates",
    "dephosphorylates",
]


class predicate:
    def __init__(self,
                 predicate_name=None,
                 long_name=None,
                 is_a=None,
                 translation_of=None,
                 directed=False,
                 contact=False,
                 negative=False,
                 description=None
                 ):
        self.is_a = set()
        self.is_a_names = is_a or []
        self.sub_types = set()
        self.predicate_name = unicode(predicate_name)
        self.long_name = long_name
        self.translation_of = translation_of or []
        self.directed = directed
        self.contact = contact
        self.negative = negative
        self.description = description

    def get_name(self):
        return self.predicate_name

    def get_directed(self):
        return self.directed

    def add_sub_type(self, sub_type):
        self.sub_types.add(sub_type)
        sub_type.is_a.add(self)


class predicateOntology:
    def __init__(self,
                 predicate_list):
        self.predicate_map = {}
        self.translation_map = {}
        for p in predicate_list:
            n = p.get_name()
            self.predicate_map[n] = p

        for sub_type in predicate_list:
            for predicate_name in sub_type.is_a:
                p = self.get_predicate(predicate_name)
                p.add_subtype(sub_type)

        for predicate in predicate_list:
            self.translation_map[predicate.predicate_name] = predicate
            for name in predicate.translation_of:
                self.translation_map[unicode(name)] = predicate

    def get_predicate(self, predicate_name):
        return self.predicate_map.get(predicate_name)

    def translate_name(self, name):
        return self.translation_map.get(name) or self.get_predicate(name)

def get_directed_predicates():
    directed_list = []
    for predicate in predicates:
        if predicate.get_directed():
            directed_list.append(predicate.get_name())
    return directed_list


predicates = [
    predicate(predicate_name="assoc",
              description="Unspecified association between things: "
                          "entities, processes, phenotypes, etc.",
              long_name="association",

              ),
    predicate(predicate_name="physInt",
              description="Unspecified physical interaction between entity types.",
              translation_of=["interactsWith",
                              "interacts with",
                              'PROTEIN_INTERACTION'
                              ],
              is_a=["assoc"],
              contact=True,
              long_name="physicalInteraction"
              ),
    predicate(predicate_name="genInt",
              description="Genetic interaction between genes. gene1 genInt gene2 indicates " \
                          "that the combination of alterations (mutations, knockdown, etc) " \
                          "in those genes produces a phenotype that deviates from the phenotype " \
                          "expected by simple combinations of phenotypes resulting from " \
                          "single alterations. The phenotype which is affected by the " \
                          "interaction can be specified using the syntheticPhenotype attribute " \
                          "of the edge.",
              is_a=["assoc"],
              long_name="geneticInteraction"
              ),
    predicate(predicate_name="posGenInt",
              description="A genInt in which the phenotype is increased and the alterations are " \
                          "inhibitory. syntheticPhenotype=GO:0008219 ('cell death') describes " \
                          "the archetypical 'synthetic lethal' genetic interaction where " \
                          "dual deletions result in cell death and single deletions do not.",
              is_a=["genInt"],
              long_name="positiveGeneticInteraction"
              ),
    predicate(predicate_name="negGenInt",
              description="A genInt in which the phenotype is decreased and the alterations are " \
                          "inhibitory. A negGenInt B + syntheticPhenotype=GO:0016049 ('cell growth') " \
                          "indicates that growth is decreased more by simultaneous inhibition than " \
                          "the sum of the single inhibition effects.",
              is_a=["genInt"],
              long_name="negativeGeneticInteraction",
              negative=True
              ),
    predicate(predicate_name="binds",
              is_a='physInt',
              contact=True,
              translation_of=[
                  'in-complex-with',
                  'COMPLEX_EXPANSION',
                  'Complex'
              ],
              description="A binds B describes a physical binding - an interaction of " \
                          "sufficient duration for the combined species to be detected. " \
                          "This is of course a definition that is dependent on the experimental " \
                          "technique used to assess binding."
              ),
    predicate(predicate_name="isA",
              directed=True),
    predicate(predicate_name='partOf',
              directed=True),

    # ---------------------------------
    # unspecified regulation
    # ---------------------------------

    predicate(predicate_name='reg',
              long_name='regulates',
              directed=True,
              is_a=['assoc'],
              translation_of=[
                  'controls-state-change-of',
                  'UNKNOWN_TRANSITION',
                  'MODULATION'
              ]
              ),
    predicate(predicate_name='posReg',
              long_name='positivelyRegulates',
              directed=True,
              is_a=["reg"],
              translation_of=[
                  'POSITIVE_INFLUENCE',
                  'activates'
              ],
              ),
    predicate(predicate_name='negReg',
              long_name='negativelyRegulates',
              directed=True,
              negative=True,
              is_a=["reg"],
              translation_of=[
                  'NEGATIVE_INFLUENCE',
                  'inhibits',
                  'INHIBITION'
              ],
              ),
    predicate(predicate_name='posPhysReg',
              long_name='positivePhysicalRegulation',
              is_a=['posReg'],
              directed=True,
              contact=True,
              translation_of=[
                  'PHYSICAL_STIMULATION',
                  'CATALYSIS'
              ]),

    # ---------------------------------
    # regulation of specific states
    # ---------------------------------

    # amounts
    predicate(predicate_name='abReg',
              long_name='abundanceRegulation',
              is_a=['reg'],
              directed=True,
              description="unspecified regulation of abundance",
              translation_of=[]
              ),

    predicate(predicate_name='posAbReg',
              long_name='positiveAbundanceRegulation',
              is_a=['abReg'],
              directed=True,
              description="increases abundance",
              translation_of=[
                  "IncreaseAmount"
              ]),

    predicate(predicate_name='negAbReg',
              long_name='negativeAbundanceRegulation',
              is_a=['abReg'],
              directed=True,
              description="decreases abundance",
              translation_of=[
                  "DecreaseAmount"

              ]),

    # transport
    predicate(predicate_name='tportReg',
              long_name='transportRegulation',
              is_a=['reg'],
              directed=True,
              description="unspecified regulation of transport",
              translation_of=[
                  'controls-transport-of'
              ]),

    # transcription
    predicate(predicate_name='tReg',
              long_name='transcriptionalRegulation',
              is_a=['reg'],
              directed=True,
              description="unspecified regulation of expression",
              translation_of=[
                  'controls-expression-of'
              ]),
    # ---------------------------------
    # protein modifications
    # ---------------------------------

    predicate(predicate_name="addPM",
              long_name="add protein modification",
              is_a=['reg', 'physInt'],
              contact=True,
              directed=True,
              translation_of=[]
              ),

    predicate(predicate_name="removePM",
              long_name="remove protein modification",
              is_a=['reg', 'physInt'],
              contact=True,
              directed=True,
              translation_of=[]
              ),

    predicate(predicate_name="phos",
              long_name="phosphorylates",
              is_a=['addPM'],
              contact=True,
              directed=True,
              translation_of=[
                  "Phosphorylation",
                  "controls-phosphorylation-of"
              ]
              ),

    predicate(predicate_name="dePhos",
              long_name="dephosphorylates",
              is_a=["removePM"],
              contact=True,
              directed=True,
              translation_of=[
                  "Dephosphorylation",
              ]
              ),

    predicate(predicate_name="acet",
              long_name="acetylates",
              is_a=['addPM'],
              contact=True,
              directed=True,
              translation_of=[
                  "Acetylation",
                  "controls-acetylation-of"
              ]
              ),
    predicate(predicate_name="deAcet",
              long_name="deacetylates",
              is_a=["removePM"],
              contact=True,
              directed=True,
              translation_of=[
                  "Deacetylation",
              ]
              ),
    predicate(predicate_name="meth",
              long_name="methylates",
              is_a=['addPM'],
              contact=True,
              directed=True,
              translation_of=[
                  "Methylation",
                  "controls-methylation-of"
              ]
              ),
    predicate(predicate_name="deMeth",
              long_name="demethylates",
              is_a=["removePM"],
              contact=True,
              directed=True,
              translation_of=[
                  "Demethylation",
              ]
              ),
    predicate(predicate_name="ub",
              long_name="ubiquitinates",
              is_a=['addPM'],
              contact=True,
              directed=True,
              translation_of=[
                  "Ubiquitination",
                  "controls-ubiquitination-of"
              ]
              ),
    predicate(predicate_name="deUb",
              long_name="deubiquitinates",
              is_a=["removePM"],
              contact=True,
              directed=True,
              translation_of=[
                  "Deubiquitination",
              ]
              ),

]
