""" Functions to add classes and properties to ontology """
from owlready2 import *

def classes_populate(onto):
    """ Creates ontology classes """
    with onto:
        class PrimaryEntity(Thing): pass # Primary entities
        class Factor(Thing): pass # Factor entities
        class Element(PrimaryEntity): pass # Food entities
        class Food(PrimaryEntity): pass
        class FoodElement(Factor): pass
        class Action(PrimaryEntity): pass # Action entities
        class TestAnalysis(Action): pass
        class Treatment(Action): pass
        class ConfirmedTestSyndromes(Factor): pass
        class ConfirmedTestDiseases(Factor): pass
        class SideEffect(Factor): pass
        class DiseaseProbability(Factor): pass
        class Disease(PrimaryEntity): pass # Disease entities
        class Syndrome(PrimaryEntity): pass
        class Precedent(PrimaryEntity): pass
        class PrecedentSyndrome(Factor): pass
        class DiseaseManifestation(Factor): pass
        class Place(PrimaryEntity): pass # Place entities
        class Country(Place): pass
        class Region(Place): pass
        class City(Place): pass
        class Case(PrimaryEntity): pass # Case entities
        class CaseDiagnosis(Factor): pass
        class CaseDiaryEntry(Factor): pass
        class Patient(PrimaryEntity): pass # Patient entities
        class Passport(PrimaryEntity): pass
        class MedicalWorker(Patient): pass
        class Doctor(MedicalWorker): pass
        class PatientAnamnesis(PrimaryEntity): pass # Ananmnesis entities
        class Occupation(Factor): pass
        class Pregnancy(Factor): pass
        class PregnancyDiaryEntry(Factor): pass
        class Visit(Factor): pass
        class Menstruation(Factor): pass
        class MenstruationManifestation(Factor): pass
        class Sequela(Factor): pass
        class Relative(Factor): pass
        class RationElement(Factor): pass
        class Residence(Factor): pass
        class Allergy(Factor): pass
        class AllergyManifestation(Factor): pass
        class Operation(Factor): pass
        class Personel(Factor): pass
        class OperationDiaryEntry(Factor): pass
    return onto

def properties_populate(onto):
    """ Creates ontology properties """
    with onto:
        class has_name(onto.PrimaryEntity >> str, FunctionalProperty): pass # Food relationships
        class has_ratio(onto.Factor >> float): pass
        class has_description(onto.PrimaryEntity >> str, FunctionalProperty): pass # Disease relationships
        class has_treatment(onto.PrimaryEntity >> onto.Treatment): pass
        class has_element(Thing >> onto.Element): pass
        class has_eliminated_disease(onto.TestAnalysis >> onto.Disease): pass
        class has_eliminated_syndrome(onto.TestAnalysis >> onto.Syndrome): pass
        class has_confirmed_syndrome(onto.TestAnalysis >> onto.ConfirmedTestSyndromes): pass
        class has_confirmed_disease(onto.TestAnalysis >> onto.ConfirmedTestDiseases): pass
        class has_disease(onto.Factor >> onto.Disease): pass
        class has_probability(onto.Factor >> float): pass
        class has_syndrome(onto.Factor >> onto.Syndrome): pass
        class has_precedent(onto.Factor >> onto.Precedent): pass
        class has_side_effect(onto.Treatment >> onto.SideEffect): pass
        class restrict_use_element(onto.PrimaryEntity >> onto.Element): pass
        class has_disease_probability(onto.PrimaryEntity >> onto.DiseaseProbability): pass
        class has_type(onto.PrimaryEntity >> str, FunctionalProperty): pass
        class has_question(onto.Precedent >> str, FunctionalProperty): pass
        class has_syndrome_probability(onto.PrimaryEntity >> onto.Factor): pass
        class has_status(DataProperty, FunctionalProperty): pass
        class has_manifestation(onto.PrimaryEntity >> onto.Factor): pass
        class has_stage(onto.Factor >> str): pass
        class has_region(onto.Country >> onto.Region): pass
        class has_city(onto.Region >> onto.City): pass
        class has_end(DataProperty, FunctionalProperty): pass
        class has_begin(DataProperty, FunctionalProperty): pass
        class has_diagnosis(onto.Case >> onto.CaseDiagnosis): pass
        class has_case_diary_entry(onto.Case >> onto.CaseDiaryEntry): pass
        class has_action(onto.CaseDiaryEntry >> onto.Action): pass
        class has_possible_diagnosis(onto.Case >> onto.DiseaseProbability): pass
        class has_passport(onto.Patient >> onto.Passport): pass
        class has_surname(onto.Passport >> str, FunctionalProperty): pass
        class has_patronymic(onto.Passport >> str, FunctionalProperty): pass
        class has_sex(onto.Passport >> str, FunctionalProperty): pass
        class has_bithday(onto.Passport >> datetime.date, FunctionalProperty): pass
        class has_photo(onto.Passport >> str, FunctionalProperty): pass
        class has_biography(onto.Passport >> str, FunctionalProperty): pass
        class has_case(onto.Doctor >> onto.Case): pass
        class has_occupation(onto.PatientAnamnesis >> onto.Occupation): pass
        class has_anamnesis(onto.Patient >> onto.PatientAnamnesis, FunctionalProperty): pass
        class works_in(onto.Occupation >> str, FunctionalProperty): pass
        class has_pregnancy(onto.PatientAnamnesis >> onto.Pregnancy): pass
        class has_pregnancy_diary_entry(onto.Pregnancy >> onto.PregnancyDiaryEntry): pass
        class has_visit(onto.PatientAnamnesis >> onto.Visit): pass
        class has_place(onto.Visit >> onto.Place, FunctionalProperty): pass
        class has_menstruation(onto.PatientAnamnesis >> onto.Menstruation): pass
        class treated_with(onto.Menstruation >> onto.Treatment): pass
        class menstruation_manifested_by(onto.Menstruation >> onto.MenstruationManifestation): pass
        class had_disease(onto.PatientAnamnesis >> onto.Disease): pass
        class has_sequela(onto.PatientAnamnesis >> onto.Sequela): pass
        class has_commentary(onto.Sequela >> str, FunctionalProperty): pass
        class has_date(onto.Factor >> datetime.date, FunctionalProperty): pass
        class has_relative(onto.PatientAnamnesis >> onto.Relative): pass
        class relative_with(onto.Relative >> onto.Patient, FunctionalProperty): pass
        class opened_case(onto.PatientAnamnesis >> onto.Case): pass
        class has_ration_element(onto.PatientAnamnesis >> onto.RationElement): pass
        class has_residence(onto.PatientAnamnesis >> onto.Residence): pass
        class has_residence_country(onto.Residence >> onto.Country, FunctionalProperty): pass
        class has_residence_region(onto.Residence >> onto.Region, FunctionalProperty): pass
        class has_residence_city(onto.Residence >> onto.City, FunctionalProperty): pass
        class has_residence_street(onto.Residence >> str, FunctionalProperty): pass
        class has_treatment(onto.Allergy >> onto.Treatment): pass
        class triggered_by(ObjectProperty):
            domain = [onto.Allergy]
            range = [onto.Precedent, onto.Element]
        class allergy_manifested_by(onto.Allergy >> onto.AllergyManifestation): pass
        class has_duration(onto.AllergyManifestation >> int, FunctionalProperty): pass
        class has_operation(onto.PatientAnamnesis >> onto.Operation): pass
        class has_operation_diary_entry(onto.Operation >> onto.OperationDiaryEntry): pass
        class action_taken(onto.Operation >> onto.OperationDiaryEntry): pass
        class has_personel(onto.Operation >> onto.Personel): pass
        class participated_as(onto.Personel >> onto.MedicalWorker, FunctionalProperty): pass
    return onto

def class_disjointness(onto):
    """ Sets disjoint classes """
    with onto:
        AllDisjoint((onto.MedicalWorker, onto.Doctor))
        AllDisjoint((onto.Treatment, onto.TestAnalysis))
        AllDisjoint((onto.Country, onto.Region, onto.City))
    return onto
