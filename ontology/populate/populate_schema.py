""" Functions to add classes and properties to ontology """
from owlready2 import *

def classes_populate(onto):
    """ Creates ontology classes """
    with onto:
        class Term(Thing): pass
        class PrecedentName(Term): pass
        class DiseaseName(Term): pass
        class BodyPartName(Term): pass
        class CircumstanceName(Term): pass
        class SubstanceName(Term): pass
        class Precedent(Thing): pass
        class PsychiatricEvaluation(Precedent): pass
        class LaboratoryDiagnostic(Precedent): pass
        class BloodTest(LaboratoryDiagnostic): pass
        class PhysicalExamination(Precedent): pass
        class SubstanceIntake(Precedent): pass
        class BodyPart(Thing): pass
        class Organ(BodyPart): pass
        class Disease(Thing): pass
        class InternalDisease(Disease): pass
        class OncologicalDisease(Disease): pass
        class Trauma(Disease): pass
        class Circumstance(Thing): pass
        class GeneticalDisorder(Disease): pass
        class InfectiousDisease(Disease): pass
        class PsychiatricDisease(Disease): pass
        class Substance(Thing): pass
        class Medicine(Substance): pass
    return onto

def properties_populate(onto):
    """ Creates ontology properties """
    with onto:
        class named_as(onto.Term >> str, FunctionalProperty): pass
        class associated_with(onto.Term >> str): pass
        class has_name(ObjectProperty, FunctionalProperty):
            domain = [onto.Precedent, onto.Disease, onto.BodyPart, onto.Substance]
            range = [onto.Term]
        class characterised_by(onto.Precedent >> str, FunctionalProperty): pass
        class aquired_by(onto.Precedent >> str, FunctionalProperty): pass
        class caused_by(onto.Precedent >> onto.Disease): pass
        class affects(onto.Disease >> onto.BodyPart): pass
        class specified_by(onto.Disease >> onto.Disease): pass
        class treat_as(onto.Disease >> str, FunctionalProperty): pass
        class described_as(DataProperty, FunctionalProperty):
            domain = [onto.Disease, onto.Substance]
            range = [str]
        class taken(onto.SubstanceIntake >> onto.Substance): pass
        class prescribe(onto.Disease >> onto.Substance): pass
        class occurs_in(onto.Trauma >> onto.Circumstance): pass
    return onto

def class_disjointness(onto):
    """ Sets disjoint classes """
    with onto:
        AllDisjoint((onto.InternalDisease,
                     onto.OncologicalDisease,
                     onto.Trauma,
                     onto.GeneticalDisorder,
                     onto.InfectiousDisease,
                     onto.PsychiatricDisease))
        AllDisjoint((onto.SubstanceIntake,
                     onto.PhysicalExamination,
                     onto.LaboratoryDiagnostic,
                     onto.PsychiatricEvaluation))
    return onto

def classes_restrictions(onto):
    """ Sets restrictions for classes """
    onto.Term.equivalent_to = [onto.named_as.some(str)]
    onto.Precedent.equivalent_to = [onto.has_name.exactly(1, onto.PrecedentName) &
                                    onto.characterised_by.exactly(1, str) &
                                    onto.aquired_by.exactly(1, str) &
                                    onto.caused_by.exactly(1, onto.Disease)]
    onto.BodyPart.equivalent_to = [onto.has_name.exactly(1, onto.BodyPartName)]
    onto.Disease.equivalent_to = [onto.affects.some(onto.BodyPart) &
                                  onto.treat_as.exactly(1, str) &
                                  onto.described_as.exactly(1, onto.str)]
    onto.Trauma.equivalent_to = [onto.Disease & onto.occurs_in.some(onto.Circumstance)]
    onto.Substance.equivalent_to = [onto.described_as.exactly(1, str) &
                                    onto.has_name.exactly(1, onto.SubstanceName)]
    onto.SubstanceIntake.equivalent_to = [onto.Substance & onto.taken.some(onto.Substance)]
    return onto
