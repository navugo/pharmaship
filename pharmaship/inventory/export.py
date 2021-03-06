# -*- coding: utf-8; -*-
"""Export methods for Inventory application."""
import tarfile
import time
import io

import hashlib

from pathlib import PurePath

from yaml import dump
try:
    from yaml import CDumper as Dumper
except ImportError:
    from yaml import Dumper

from django.core import serializers
from django.conf import settings

from rest_framework.renderers import JSONRenderer

import pharmaship.inventory.models
import pharmaship.inventory.serializers

from pharmaship.core.utils import remove_yaml_pk, get_content_types
from pharmaship.core.utils import log, query_count_all


def serialize_allowance(allowance, content_types):
    """Export an allowance using the YAML format.

    To have an usable export, the broadcaster needs:
        - the :model:`pharmaship.inventory.Allowance` selected instance,
    And related to this instance:
        - the :model:`pharmaship.inventory.Molecule` objects list,
        - the :model:`pharmaship.inventory.Equipment` objects list,
        - the :model:`pharmaship.inventory.MoleculeReqQty` objects list,
        - the :model:`pharmaship.inventory.EquipmentReqQty` objects list,
        - the :model:`pharmaship.inventory.RescueBagReqQty` objects list,
        - the :model:`pharmaship.inventory.FirstAidKitReqQty` objects list,
        - the :model:`pharmaship.inventory.TelemedicalReqQty` objects list,
        - the :model:`pharmaship.inventory.LaboratoryReqQty` objects list.

    Returns a list of filenames and streams.
    """
    log.debug("Start serialize")

    renderer = JSONRenderer()
    # Molecules used by the allowance
    molecule_id_list = []
    equipment_id_list = []

    # Required quantities for molecules
    molecule_reqqty_list = pharmaship.inventory.models.MoleculeReqQty.objects.filter(allowance__in=[allowance]).prefetch_related("base")
    molecule_id_list += molecule_reqqty_list.values_list("base_id", flat=True)
    # molecule_reqqty_data = serializers.serialize(
    #     "yaml",
    #     molecule_reqqty_list,
    #     fields=('base', 'required_quantity'),
    #     use_natural_foreign_keys=True
    #     )
    # query_count_all()

    serialized = pharmaship.inventory.serializers.MoleculeReqQtySerializer(molecule_reqqty_list, many=True)
    molecule_reqqty_data = renderer.render(
        data=serialized.data,
        accepted_media_type='application/json; indent=2'
        )
    query_count_all()

    # Required quantities for equipments
    equipment_reqqty_list = pharmaship.inventory.models.EquipmentReqQty.objects.filter(allowance__in=[allowance]).prefetch_related("base")
    equipment_id_list += equipment_reqqty_list.values_list("base_id", flat=True)
    # equipment_reqqty_data = serializers.serialize(
    #     "yaml",
    #     equipment_reqqty_list,
    #     fields=('base', 'required_quantity'),
    #     use_natural_foreign_keys=True
    #     )
    # query_count_all()

    serialized = pharmaship.inventory.serializers.EquipmentReqQtySerializer(equipment_reqqty_list, many=True)
    equipment_reqqty_data = renderer.render(
        data=serialized.data,
        accepted_media_type='application/json; indent=2'
        )
    query_count_all()

    # Required quantities for Laboratory
    laboratory_reqqty_list = pharmaship.inventory.models.LaboratoryReqQty.objects.filter(allowance__in=[allowance]).prefetch_related("base")
    equipment_id_list += laboratory_reqqty_list.values_list("base_id", flat=True)
    # laboratory_reqqty_data = serializers.serialize(
    #     "yaml",
    #     laboratory_reqqty_list,
    #     fields=('base', 'required_quantity'),
    #     use_natural_foreign_keys=True
    #     )
    # query_count_all()

    serialized = pharmaship.inventory.serializers.LaboratoryReqQtySerializer(laboratory_reqqty_list, many=True)
    laboratory_reqqty_data = renderer.render(
        data=serialized.data,
        accepted_media_type='application/json; indent=2'
        )
    query_count_all()


    # Required quantities for Telemedical
    telemedical_reqqty_list = pharmaship.inventory.models.TelemedicalReqQty.objects.filter(allowance__in=[allowance]).prefetch_related("base")
    equipment_id_list += telemedical_reqqty_list.values_list("base_id", flat=True)
    # telemedical_reqqty_data = serializers.serialize(
    #     "yaml",
    #     telemedical_reqqty_list,
    #     fields=('base', 'required_quantity'),
    #     use_natural_foreign_keys=True
    #     )
    # query_count_all()

    serialized = pharmaship.inventory.serializers.TelemedicalReqQtySerializer(telemedical_reqqty_list, many=True)
    telemedical_reqqty_data = renderer.render(
        data=serialized.data,
        accepted_media_type='application/json; indent=2'
        )
    query_count_all()

    # Required quantities for First Aid Kit
    first_aid_kit_reqqty_list = pharmaship.inventory.models.FirstAidKitReqQty.objects.filter(allowance__in=[allowance]).prefetch_related("base")
    molecule_id_list += first_aid_kit_reqqty_list.filter(
        content_type_id=content_types["molecule"]
        ).values_list("object_id", flat=True)
    equipment_id_list += first_aid_kit_reqqty_list.filter(
        content_type_id=content_types["equipment"]
        ).values_list("object_id", flat=True)

    serialized = pharmaship.inventory.serializers.FirstAidKitReqQtySerializer(first_aid_kit_reqqty_list, many=True)
    first_aid_kit_reqqty_data = renderer.render(
        data=serialized.data,
        accepted_media_type='application/json; indent=2'
        )
    query_count_all()

    # Required quantities for Rescue Bag
    rescue_bag_reqqty_list = pharmaship.inventory.models.RescueBagReqQty.objects.filter(allowance__in=[allowance]).prefetch_related("base")
    molecule_id_list += rescue_bag_reqqty_list.filter(
        content_type_id=content_types["molecule"]
        ).values_list("object_id", flat=True)
    equipment_id_list += rescue_bag_reqqty_list.filter(
        content_type_id=content_types["equipment"]
        ).values_list("object_id", flat=True)

    serialized = pharmaship.inventory.serializers.RescueBagReqQtySerializer(rescue_bag_reqqty_list, many=True)
    rescue_bag_reqqty_data = renderer.render(
        data=serialized.data,
        accepted_media_type='application/json; indent=2'
        )
    query_count_all()

    # Equipment used by the allowance
    equipment_list = pharmaship.inventory.models.Equipment.objects.filter(id__in=equipment_id_list).prefetch_related("group")
    equipment_data = serializers.serialize(
        "yaml",
        equipment_list,
        use_natural_foreign_keys=True,
        fields=("name", "packaging", "consumable", "perishable", "picture", "group", "remark")
        )
    log.debug("Equipment")
    query_count_all()

    # Molecule used by the allowance
    molecule_list = pharmaship.inventory.models.Molecule.objects.filter(id__in=molecule_id_list).prefetch_related("group")
    molecule_data = serializers.serialize(
        "yaml",
        molecule_list,
        use_natural_foreign_keys=True,
        fields=("name", "roa", "dosage_form", "composition", "medicine_list", "group", "remark")
        )
    log.debug("Molecule")
    query_count_all()

    # Allowance record
    allowance_data = serializers.serialize(
        "yaml",
        (allowance,),
        fields=('name', 'author', 'version', 'date', 'additional'),
        use_natural_foreign_keys=True
        )
    log.debug("Allowance")
    query_count_all()

    log.debug("End serialize")

    # Returning a list with tuples: (filename, data)
    return ([
        ('inventory/molecule_obj.yaml', remove_yaml_pk(molecule_data)),
        ('inventory/equipment_obj.yaml', remove_yaml_pk(equipment_data)),

        ('inventory/molecule_reqqty.json', molecule_reqqty_data),
        ('inventory/equipment_reqqty.json', equipment_reqqty_data),

        ('inventory/laboratory_reqqty.json', laboratory_reqqty_data),
        ('inventory/telemedical_reqqty.json', telemedical_reqqty_data),

        ('inventory/first_aid_kit_reqqty.json', first_aid_kit_reqqty_data),
        ('inventory/rescue_bag_reqqty.json', rescue_bag_reqqty_data),

        ('inventory/allowance.yaml', remove_yaml_pk(allowance_data)),
    ], equipment_list)


def get_pictures(equipment_list):
    """Return a list of picture paths to include in the archive."""
    # Pictures attached to equipments
    pictures = equipment_list.exclude(picture='').values_list('picture', flat=True)

    return pictures


def get_hash(name, content=None, filename=None):
    """Return sha256 hash and filename for MANIFEST file."""
    if content is None and filename is None:
        return None

    m = hashlib.sha256()
    if content:
        if isinstance(content, bytes):
            m.update(content)
        else:
            m.update(bytes(content, "utf-8"))
    elif filename:
        try:
            with open(filename, 'rb') as fdesc:
                m.update(fdesc.read())
        except IOError as error:
            log.error("File %s not readable. %s", filename, error)
            return None

    return (name, m.hexdigest())


def create_tarinfo(name, content):
    if isinstance(content, bytes):
        f = io.BytesIO(content)
    else:
        f = io.BytesIO(bytes(content, "utf-8"))
    info = tarfile.TarInfo()
    info.name = name
    info.type = tarfile.REGTYPE
    info.uid = info.gid = 0
    info.uname = info.gname = "root"
    info.mtime = time.time()
    info.size = len(f.getvalue())

    return (info, f)


def create_manifest(items):
    content = ""
    for item in items:
        content += "{1}  {0}\n".format(item[0], item[1])

    return content


def create_package_yaml(allowance):
    """Export package info in YAML string."""
    content = {
        "info": {
            "author": allowance.author,
            "date": allowance.date,
            "version": allowance.version
        },
        "modules": {
            "inventory": {
                "install_file": False
            }
        }
    }
    content_string = dump(content, Dumper=Dumper)

    return content_string


def create_archive(allowance, file_obj):
    """Create an archive from the given `Allowance` instance.

    The response is a tar.gz file containing YAML files generated by the
    function `serialize_allowance`.
    """
    # Creating a tar.gz archive
    hashes = []

    serialized_data, equipment_list = serialize_allowance(
        allowance=allowance,
        content_types=get_content_types()
        )

    with tarfile.open(fileobj=file_obj, mode='w') as tar:
        # Processing the database
        for item in serialized_data:
            info, f = create_tarinfo(item[0], item[1])
            tar.addfile(info, f)

            hashes.append(get_hash(info.name, content=item[1]))

        # Adding the pictures of Equipment
        for item in get_pictures(equipment_list):
            picture_filename = settings.PICTURES_FOLDER / item
            log.debug(picture_filename)
            try:
                tar.add(picture_filename, arcname=PurePath("pictures", item))
            # TODO: Detail Exception
            except Exception as error:
                log.error("Error: %s", error)

            hashes.append(get_hash(PurePath("pictures", item), filename=picture_filename))

        # Add the MANIFEST
        package_content = create_package_yaml(allowance)
        info, f = create_tarinfo("package.yaml", package_content)
        tar.addfile(info, f)
        hashes.append(get_hash("package.yaml", content=package_content))

        # Add the MANIFEST
        manifest_content = create_manifest(hashes)
        info, f = create_tarinfo("MANIFEST", manifest_content)
        tar.addfile(info, f)

    return True
