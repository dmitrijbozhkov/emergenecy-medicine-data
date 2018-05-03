""" Adds ontology body parts """
from owlready2 import *
from populate.utils import batch_add_instances

def names_body_parts(name_dict):
    """ Creates dictionary of body parts from dictionary of body part names """
    return {k: {"has_name": name_dict[k]} for k in name_dict.keys()}

def body_areas(onto):
    """ Adds body areas class instances """
    areas_names = {
        "Голова": {"named_as": "Голова"},
        "Торс": {"named_as": "Торс"},
        "Рука": {"named_as": "Рука"},
        "Нога": {"named_as": "Нога"}
    }
    areas_names = batch_add_instances(onto.BodyPartName, areas_names)
    areas = names_body_parts(areas_names)
    return batch_add_instances(onto.BodyPart, areas)

def body_parts(onto, areas):
    """ Adds body parts to body parts """
    head_names = {
        "Макушка": {"named_as": "Макушка"},
        "Лоб": {"named_as": "Лоб"},
        "Затылок": {"named_as": "Затылок"},
        "Виски": {"named_as": "Виски"},
        "Глаза": {"named_as": "Глаза"},
        "Нос": {"named_as": "Нос"},
        "Рот": {"named_as": "Рот"},
        "Лицо": {"named_as": "Лицо"},
        "Уши": {"named_as": "Уши"},
        "Скулы": {"named_as": "Скулы"},
        "Щёки": {"named_as": "Щёки"},
        "Подбородок": {"named_as": "Подбородок"},
        "Шея": {"named_as": "Шея"}
    }
    torso_names = {
        "Грудь": {"named_as": "Грудь"},
        "Эпигастральная область": {"named_as": "Эпигастральная область"},
        "Подреберье": {"named_as": "Подреберье"},
        "Живот": {"named_as": "Живот"},
        "Пупок": {"named_as": "Пупок"},
        "Пах": {"named_as": "Пах"},
        "Спина": {"named_as": "Спина"},
        "Поясница": {"named_as": "Поясница"},
        "Ягодица": {"named_as": "Ягодица"}
    }
    hand_names = {
        "Плечо": {"named_as": "Плечо"},
        "Локоть": {"named_as": "Локоть"},
        "Надплечье": {"named_as": "Надплечье"},
        "Запястье": {"named_as": "Запястье"},
        "Ладонь": {"named_as": "Ладонь"},
        "Пальцы": {"named_as": "Пальцы"}
    }
    leg_names = {
        "Бедро": {"named_as": "Бедро"},
        "Колено": {"named_as": "Колено"},
        "Подколенная ямка": {"named_as": "Подколенная ямка"},
        "Лодыжка": {"named_as": "Лодыжка"},
        "Тыльная сторона стопы": {"named_as": "Тыльная сторона стопы"},
        "Пальцы": {"named_as": "Пальцы"},
        "Пятка": {"named_as": "Пятка"}
    }
    head_names = batch_add_instances(onto.BodyPartName, head_names) # adding body part names
    torso_names = batch_add_instances(onto.BodyPartName, torso_names)
    hand_names = batch_add_instances(onto.BodyPartName, hand_names)
    leg_names = batch_add_instances(onto.BodyPartName, leg_names)
    part_head = names_body_parts(head_names)
    part_torso = names_body_parts(torso_names)
    part_hand = names_body_parts(hand_names)
    part_leg = names_body_parts(leg_names)
    part_head = batch_add_instances(onto.BodyPart, part_head) # adding body parts
    part_torso = batch_add_instances(onto.BodyPart, part_torso)
    part_hand = batch_add_instances(onto.BodyPart, part_hand)
    part_leg = batch_add_instances(onto.BodyPart, part_leg)
    areas["Голова"].contains = [part_head[p] for p in part_head.keys()] # setting contains relation
    areas["Торс"].contains = [part_torso[p] for p in part_torso.keys()]
    areas["Рука"].contains = [part_hand[p] for p in part_hand.keys()]
    areas["Нога"].contains = [part_leg[p] for p in part_leg.keys()]
    return {
        "Голова": part_head,
        "Торс": part_torso,
        "Рука": part_hand,
        "Нога": part_leg
    }

def organs(onto, parts):
    """ Adds organs to body parts """
    head_names = {
        "Головной мозг": {"named_as": "Головной мозг"},
        "Зуб": {"named_as": "Зуб"},
        "Язык": {"named_as": "Язык"},
        "Гортань": {"named_as": "Гортань"},
        "Дёсна": {"named_as": "Дёсна"}
    }
    torso_names = {
        "Пищевод": {"named_as": "Пищевод"},
        "Трахея": {"named_as": "Трахея"},
        "Лёгкие": {"named_as": "Лёгкие"},
        "Сердце": {"named_as": "Сердце"},
        "Печень": {"named_as": "Печень"},
        "Желудок": {"named_as": "Желудок"},
        "Селезёнка": {"named_as": "Селезёнка"},
        "Почки": {"named_as": "Почки"},
        "Кишечник": {"named_as": "Кишечник"},
        "Мочевой пузырь": {"named_as": "Мочевой пузырь"},
        "Прямая кишка": {"named_as": "Прямая кишка"}
    }
    head_names = batch_add_instances(onto.BodyPartName, head_names)
    torso_names = batch_add_instances(onto.BodyPartName, torso_names)
    organ_head = names_body_parts(head_names)
    organ_torso = names_body_parts(torso_names)
    organ_head = batch_add_instances(onto.Organ, organ_head)
    organ_torso = batch_add_instances(onto.Organ, organ_torso)
    parts["Макушка"].contains = [organ_head["Головной мозг"]]
    parts["Лоб"].contains = [organ_head["Головной мозг"]]
    parts["Затылок"].contains = [organ_head["Головной мозг"]]
    parts["Виски"].contains = [organ_head["Головной мозг"]]
    parts["Шея"].contains = [organ_head["Гортань"], organ_torso["Трахея"], organ_torso["Пищевод"]]
    parts["Рот"].contains = [organ_head["Зуб"], organ_head["Язык"], organ_head["Дёсна"]]
    parts["Грудь"].contains = [organ_torso["Лёгкие"],
                               organ_torso["Сердце"],
                               organ_torso["Трахея"],
                               organ_torso["Пищевод"],
                               organ_torso["Печень"],
                               organ_torso["Желудок"]]
    parts["Эпигастральная область"].contains = [organ_torso["Печень"], organ_torso["Желудок"]]
    parts["Подреберье"].contains = [organ_torso["Селезёнка"],
                                    organ_torso["Печень"],
                                    organ_torso["Желудок"],
                                    organ_torso["Кишечник"]]
    parts["Живот"].contains = [organ_torso["Селезёнка"], organ_torso["Кишечник"], organ_torso["Почки"]]
    parts["Пупок"].contains = [organ_torso["Кишечник"]]
    parts["Пах"].contains = [organ_torso["Кишечник"], organ_torso["Мочевой пузырь"], organ_torso["Прямая кишка"]]
    return {
        "Голова": organ_head,
        "Торс": organ_torso
    }
