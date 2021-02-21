import re
from typing import List

from rctclient.registry import REGISTRY

from .entity import (
    AttributesEntityDescriptor,
    BatteryEntityDescriptor,
    EntityDescriptor,
    InverterEntityDescriptor,
)


def get_matching_names(expression: str):
    compiled_expression = re.compile(expression)
    return [
        object_info.name
        for object_info in REGISTRY.all()
        if compiled_expression.match(object_info.name) != None
    ]


known_entities: List[EntityDescriptor] = [
    BatteryEntityDescriptor(
        ["battery.bms_sn"], entity_name="Battery Management System Serial Number"
    ),
    BatteryEntityDescriptor(
        ["battery.bms_software_version"],
        entity_name="Battery Management System Software Version",
    ),
    InverterEntityDescriptor(["adc.u_acc"], entity_name="Inverter Battery Voltage"),
    InverterEntityDescriptor(
        ["android_description"], entity_name="Inverter Device Name"
    ),
    InverterEntityDescriptor(
        ["buf_v_control.power_reduction_max_solar"],
        entity_name="Generator Maximum Power",
    ),
    InverterEntityDescriptor(
        ["buf_v_control.power_reduction_max_solar_grid"],
        entity_name="Grid Maximum Feed Power",
    ),
    InverterEntityDescriptor(["db.core_temp"]),
    InverterEntityDescriptor(["db.temp1"]),
    InverterEntityDescriptor(
        ["dc_conv.dc_conv_struct[0].enabled"], entity_name="Generator A Connected"
    ),
    InverterEntityDescriptor(
        ["dc_conv.dc_conv_struct[0].mpp.fixed_voltage"],
        entity_name="Generator A MPP Fixed Voltage",
    ),
    InverterEntityDescriptor(
        ["dc_conv.dc_conv_struct[0].mpp.mpp_step"],
        entity_name="Generator A MPP Search Step",
    ),
    InverterEntityDescriptor(
        ["dc_conv.dc_conv_struct[0].p_dc"], entity_name="Generator A Power"
    ),
    InverterEntityDescriptor(
        ["dc_conv.dc_conv_struct[0].p_dc_lp"], entity_name="Generator A Power (lp)"
    ),
    InverterEntityDescriptor(
        ["dc_conv.dc_conv_struct[0].rescan_correction"],
        entity_name="Generator A MPP Rescan Correction",
    ),
    InverterEntityDescriptor(
        ["dc_conv.dc_conv_struct[0].u_sg_lp"], entity_name="Generator A Voltage"
    ),
    InverterEntityDescriptor(
        ["dc_conv.dc_conv_struct[1].enabled"], entity_name="Generator B Connected"
    ),
    InverterEntityDescriptor(
        ["dc_conv.dc_conv_struct[1].mpp.fixed_voltage"],
        entity_name="Generator B MPP Fixed Voltage",
    ),
    InverterEntityDescriptor(
        ["dc_conv.dc_conv_struct[1].mpp.mpp_step"],
        entity_name="Generator B MPP Search Step",
    ),
    InverterEntityDescriptor(
        ["dc_conv.dc_conv_struct[1].p_dc"], entity_name="Generator B Power"
    ),
    InverterEntityDescriptor(
        ["dc_conv.dc_conv_struct[1].p_dc_lp"], entity_name="Generator B Power (lp)"
    ),
    InverterEntityDescriptor(
        ["dc_conv.dc_conv_struct[1].rescan_correction"],
        entity_name="Generator B MPP Rescan Correction",
    ),
    InverterEntityDescriptor(
        ["dc_conv.dc_conv_struct[1].u_sg_lp"], entity_name="Generator B Voltage"
    ),
    InverterEntityDescriptor(
        ["dc_conv.start_voltage"], entity_name="Inverter DC Start Voltage"
    ),
    InverterEntityDescriptor(["g_sync.p_ac_sum"], entity_name="Inverter AC Power"),
    InverterEntityDescriptor(["inverter_sn"], entity_name="Inverter Serial Number"),
    InverterEntityDescriptor(["svnversion"], entity_name="Inverter Software Version"),
    InverterEntityDescriptor(
        ["flash_rtc.time_stamp_update"], entity_name="Date of Last Update"
    ),
    InverterEntityDescriptor(["fault[0].flt"], entity_name="Faults 0"),
    InverterEntityDescriptor(["fault[1].flt"], entity_name="Faults 1"),
    InverterEntityDescriptor(["fault[2].flt"], entity_name="Faults 2"),
    InverterEntityDescriptor(["fault[3].flt"], entity_name="Faults 3"),
    InverterEntityDescriptor(["g_sync.p_ac_load_sum_lp"], entity_name="Consumer Load"),
    InverterEntityDescriptor(["g_sync.p_acc_lp"], entity_name="Battery Load"),
    AttributesEntityDescriptor(
        get_matching_names(r"^g_sync\."), entity_name="Group g_sync"
    ),
    AttributesEntityDescriptor(
        get_matching_names(r"^rb485\."), entity_name="Group rb485"
    ),
    AttributesEntityDescriptor(
        get_matching_names(r"^p_rec"), entity_name="Group p_rec"
    ),
    AttributesEntityDescriptor(get_matching_names(r"^nsm\."), entity_name="Group nsm"),
    AttributesEntityDescriptor(
        get_matching_names(r"^power_mng\."), entity_name="Group power_mng"
    ),
]


# DEVICE_OBJECT_IDS = list(
#     REGISTRY.get_by_name(object_name).object_id
#     for object_name in [
#         "inverter_sn",
#         "svnversion",
#         "battery.bms_sn",
#         "battery.bms_software_version",
#         "android_description",
#     ]
# )
