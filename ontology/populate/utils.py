""" Common functions for populationg ontology """
from hashlib import md5

def generate_id(class_name, item_name):
    """ Creates id for item by hashing """
    item_hash = md5(item_name.encode("utf-8")).hexdigest()
    return class_name + "-" + item_hash

def batch_add_instances(prototype, instance_dict):
    """ Adds class instances to ontology and returns dictionary of them """
    prototype_name = prototype.name
    return {k: (prototype(generate_id(prototype_name, k), **instance_dict[k]) if instance_dict[k]
                else prototype(generate_id(prototype_name, k))) for k in instance_dict.keys()}
