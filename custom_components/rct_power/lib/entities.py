import re
from typing import List

from rctclient.registry import REGISTRY

from .entity import (
    AttributesEntityDescriptor,
    BatteryEntityDescriptor,
    EntityDescriptor,
    EntityUpdatePriority,
    FaultEntityDescriptor,
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
        ["battery.bms_sn"],
        entity_name="Battery Management System Serial Number",
        update_priority=EntityUpdatePriority.STATIC,
    ),
    BatteryEntityDescriptor(
        ["battery.bms_software_version"],
        entity_name="Battery Management System Software Version",
        update_priority=EntityUpdatePriority.INFREQUENT,
    ),
    InverterEntityDescriptor(["adc.u_acc"], entity_name="Inverter Battery Voltage"),
    InverterEntityDescriptor(
        ["android_description"],
        entity_name="Inverter Device Name",
        update_priority=EntityUpdatePriority.STATIC,
    ),
    InverterEntityDescriptor(
        ["buf_v_control.power_reduction_max_solar"],
        entity_name="Generator Maximum Power",
        update_priority=EntityUpdatePriority.STATIC,
    ),
    InverterEntityDescriptor(
        ["buf_v_control.power_reduction_max_solar_grid"],
        entity_name="Grid Maximum Feed Power",
        update_priority=EntityUpdatePriority.STATIC,
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
        ["dc_conv.dc_conv_struct[1].rescan_correction"],
        entity_name="Generator B MPP Rescan Correction",
    ),
    InverterEntityDescriptor(
        ["dc_conv.dc_conv_struct[1].u_sg_lp"], entity_name="Generator B Voltage"
    ),
    InverterEntityDescriptor(
        ["dc_conv.start_voltage"],
        entity_name="Inverter DC Start Voltage",
        update_priority=EntityUpdatePriority.STATIC,
    ),
    InverterEntityDescriptor(
        ["inverter_sn"],
        entity_name="Inverter Serial Number",
        update_priority=EntityUpdatePriority.STATIC,
    ),
    InverterEntityDescriptor(
        ["svnversion"],
        entity_name="Inverter Software Version",
        update_priority=EntityUpdatePriority.INFREQUENT,
    ),
    InverterEntityDescriptor(
        ["flash_rtc.time_stamp_update"],
        entity_name="Date of Last Update",
        update_priority=EntityUpdatePriority.INFREQUENT,
    ),
    InverterEntityDescriptor(["g_sync.p_ac_sum"], entity_name="Inverter AC Power"),
    InverterEntityDescriptor(["g_sync.p_ac[0]"], entity_name="Inverter Power P1"),
    InverterEntityDescriptor(["g_sync.p_ac[1]"], entity_name="Inverter Power P2"),
    InverterEntityDescriptor(["g_sync.p_ac[2]"], entity_name="Inverter Power P3"),
    InverterEntityDescriptor(["g_sync.p_ac_load_sum_lp"], entity_name="Consumer Power"),
    InverterEntityDescriptor(["g_sync.p_ac_load[0]"], entity_name="Consumer Power P1"),
    InverterEntityDescriptor(["g_sync.p_ac_load[1]"], entity_name="Consumer Power P2"),
    InverterEntityDescriptor(["g_sync.p_ac_load[2]"], entity_name="Consumer Power P3"),
    InverterEntityDescriptor(["g_sync.p_acc_lp"], entity_name="Battery Power"),
    InverterEntityDescriptor(["g_sync.p_ac_grid_sum_lp"], entity_name="Grid Power"),
    InverterEntityDescriptor(["rb485.f_grid[0]"], entity_name="Grid Frequency P1"),
    InverterEntityDescriptor(["rb485.f_grid[1]"], entity_name="Grid Frequency P2"),
    InverterEntityDescriptor(["rb485.f_grid[2]"], entity_name="Grid Frequency P3"),
    InverterEntityDescriptor(["rb485.u_l_grid[0]"], entity_name="Grid Voltage P1"),
    InverterEntityDescriptor(["rb485.u_l_grid[1]"], entity_name="Grid Voltage P2"),
    InverterEntityDescriptor(["rb485.u_l_grid[2]"], entity_name="Grid Voltage P3"),
    FaultEntityDescriptor(
        [
            "fault[0].flt",
            "fault[1].flt",
            "fault[2].flt",
            "fault[3].flt",
        ],
        entity_name="Faults",
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
