import re
from typing import List

from rctclient.registry import REGISTRY

from .entity import (
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
        if compiled_expression.match(object_info.name) is not None
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
        update_priority=EntityUpdatePriority.STATIC,
    ),
    BatteryEntityDescriptor(
        ["battery.module_sn[0]"],
        entity_name="Battery Module 1 Serial Number",
        update_priority=EntityUpdatePriority.STATIC,
    ),
    BatteryEntityDescriptor(
        ["battery.module_sn[1]"],
        entity_name="Battery Module 2 Serial Number",
        update_priority=EntityUpdatePriority.STATIC,
    ),
    BatteryEntityDescriptor(
        ["battery.module_sn[2]"],
        entity_name="Battery Module 3 Serial Number",
        update_priority=EntityUpdatePriority.STATIC,
    ),
    BatteryEntityDescriptor(
        ["battery.module_sn[3]"],
        entity_name="Battery Module 4 Serial Number",
        update_priority=EntityUpdatePriority.STATIC,
    ),
    BatteryEntityDescriptor(
        ["battery.module_sn[4]"],
        entity_name="Battery Module 5 Serial Number",
        update_priority=EntityUpdatePriority.STATIC,
    ),
    BatteryEntityDescriptor(
        ["battery.module_sn[5]"],
        entity_name="Battery Module 6 Serial Number",
        update_priority=EntityUpdatePriority.STATIC,
    ),
    BatteryEntityDescriptor(
        ["battery.charged_amp_hours"],
        entity_name="Battery Charge Total",
        update_priority=EntityUpdatePriority.INFREQUENT,
    ),
    BatteryEntityDescriptor(
        ["battery.discharged_amp_hours"],
        entity_name="Battery Discharge Total",
        update_priority=EntityUpdatePriority.INFREQUENT,
    ),
    BatteryEntityDescriptor(
        ["battery.current"],
        entity_name="Battery Current",
        update_priority=EntityUpdatePriority.FREQUENT,
    ),
    BatteryEntityDescriptor(
        ["battery.voltage"],
        entity_name="Battery Voltage",
        update_priority=EntityUpdatePriority.FREQUENT,
    ),
    BatteryEntityDescriptor(
        ["battery.maximum_charge_voltage"],
        entity_name="Battery Maximum Charging Voltage",
        update_priority=EntityUpdatePriority.FREQUENT,
    ),
    BatteryEntityDescriptor(
        ["battery.minimum_discharge_voltage"],
        entity_name="Battery Minimum Discharging Voltage",
        update_priority=EntityUpdatePriority.FREQUENT,
    ),
    BatteryEntityDescriptor(
        ["battery.maximum_discharge_current"],
        entity_name="Battery Maximum Discharging Current",
        update_priority=EntityUpdatePriority.FREQUENT,
    ),
    BatteryEntityDescriptor(
        ["battery.temperature"],
        entity_name="Battery Temperature",
        update_priority=EntityUpdatePriority.FREQUENT,
    ),
    BatteryEntityDescriptor(
        ["battery.stored_energy"],
        entity_name="Battery Stored Energy",
        update_priority=EntityUpdatePriority.FREQUENT,
    ),
    BatteryEntityDescriptor(
        ["battery.ah_capacity"],
        entity_name="Battery Charge Capacity",
        update_priority=EntityUpdatePriority.INFREQUENT,
    ),
    BatteryEntityDescriptor(
        ["battery.soc"],
        entity_name="Battery State of Charge",
        update_priority=EntityUpdatePriority.FREQUENT,
    ),
    BatteryEntityDescriptor(
        ["battery.soc_target"],
        entity_name="Battery State of Charge Target",
        update_priority=EntityUpdatePriority.FREQUENT,
    ),
    BatteryEntityDescriptor(
        ["battery.soc_target_low"],
        entity_name="Battery State of Charge Low Target",
        update_priority=EntityUpdatePriority.FREQUENT,
    ),
    BatteryEntityDescriptor(
        ["battery.soc_target_high"],
        entity_name="Battery State of Charge High Target",
        update_priority=EntityUpdatePriority.FREQUENT,
    ),
    BatteryEntityDescriptor(
        ["battery.soh"],
        entity_name="Battery State of Health",
        update_priority=EntityUpdatePriority.INFREQUENT,
    ),
    BatteryEntityDescriptor(
        ["battery.cycles"],
        entity_name="Battery Cycles",
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
    InverterEntityDescriptor(
        ["energy.e_load_day"],
        entity_name="Consumer Energy Consumption Day",
        update_priority=EntityUpdatePriority.INFREQUENT,
    ),
    InverterEntityDescriptor(
        ["energy.e_load_month"],
        entity_name="Consumer Energy Consumption Month",
        update_priority=EntityUpdatePriority.INFREQUENT,
    ),
    InverterEntityDescriptor(
        ["energy.e_load_year"],
        entity_name="Consumer Energy Consumption Year",
        update_priority=EntityUpdatePriority.INFREQUENT,
    ),
    InverterEntityDescriptor(
        ["energy.e_load_total"],
        entity_name="Consumer Energy Consumption Total",
        update_priority=EntityUpdatePriority.INFREQUENT,
    ),
    InverterEntityDescriptor(
        ["energy.e_ac_day"],
        entity_name="Inverter Energy Production Day",
        update_priority=EntityUpdatePriority.INFREQUENT,
    ),
    InverterEntityDescriptor(
        ["energy.e_ac_month"],
        entity_name="Inverter Energy Production Month",
        update_priority=EntityUpdatePriority.INFREQUENT,
    ),
    InverterEntityDescriptor(
        ["energy.e_ac_year"],
        entity_name="Inverter Energy Production Year",
        update_priority=EntityUpdatePriority.INFREQUENT,
    ),
    InverterEntityDescriptor(
        ["energy.e_ac_total"],
        entity_name="Inverter Energy Production Total",
        update_priority=EntityUpdatePriority.INFREQUENT,
    ),
    InverterEntityDescriptor(
        ["energy.e_grid_feed_day"],
        entity_name="Grid Energy Production Day",
        update_priority=EntityUpdatePriority.INFREQUENT,
    ),
    InverterEntityDescriptor(
        ["energy.e_grid_feed_month"],
        entity_name="Grid Energy Production Month",
        update_priority=EntityUpdatePriority.INFREQUENT,
    ),
    InverterEntityDescriptor(
        ["energy.e_grid_feed_year"],
        entity_name="Grid Energy Production Year",
        update_priority=EntityUpdatePriority.INFREQUENT,
    ),
    InverterEntityDescriptor(
        ["energy.e_grid_feed_total"],
        entity_name="Grid Energy Production Total",
        update_priority=EntityUpdatePriority.INFREQUENT,
    ),
    InverterEntityDescriptor(
        ["energy.e_grid_load_day"],
        entity_name="Grid Energy Consumption Day",
        update_priority=EntityUpdatePriority.INFREQUENT,
    ),
    InverterEntityDescriptor(
        ["energy.e_grid_load_month"],
        entity_name="Grid Energy Consumption Month",
        update_priority=EntityUpdatePriority.INFREQUENT,
    ),
    InverterEntityDescriptor(
        ["energy.e_grid_load_year"],
        entity_name="Grid Energy Consumption Year",
        update_priority=EntityUpdatePriority.INFREQUENT,
    ),
    InverterEntityDescriptor(
        ["energy.e_grid_load_total"],
        entity_name="Grid Energy Consumption Total",
        update_priority=EntityUpdatePriority.INFREQUENT,
    ),
    InverterEntityDescriptor(
        ["energy.e_ext_day"],
        entity_name="External Energy Production Day",
        update_priority=EntityUpdatePriority.INFREQUENT,
    ),
    InverterEntityDescriptor(
        ["energy.e_ext_month"],
        entity_name="External Energy Production Month",
        update_priority=EntityUpdatePriority.INFREQUENT,
    ),
    InverterEntityDescriptor(
        ["energy.e_ext_year"],
        entity_name="External Energy Production Year",
        update_priority=EntityUpdatePriority.INFREQUENT,
    ),
    InverterEntityDescriptor(
        ["energy.e_ext_total"],
        entity_name="External Energy Production Total",
        update_priority=EntityUpdatePriority.INFREQUENT,
    ),
    InverterEntityDescriptor(
        ["energy.e_dc_day[0]"],
        entity_name="Generator A Energy Production Day",
        update_priority=EntityUpdatePriority.INFREQUENT,
    ),
    InverterEntityDescriptor(
        ["energy.e_dc_month[0]"],
        entity_name="Generator A Energy Production Month",
        update_priority=EntityUpdatePriority.INFREQUENT,
    ),
    InverterEntityDescriptor(
        ["energy.e_dc_year[0]"],
        entity_name="Generator A Energy Production Year",
        update_priority=EntityUpdatePriority.INFREQUENT,
    ),
    InverterEntityDescriptor(
        ["energy.e_dc_total[0]"],
        entity_name="Generator A Energy Production Total",
        update_priority=EntityUpdatePriority.INFREQUENT,
    ),
    InverterEntityDescriptor(
        ["energy.e_dc_day[1]"],
        entity_name="Generator B Energy Production Day",
        update_priority=EntityUpdatePriority.INFREQUENT,
    ),
    InverterEntityDescriptor(
        ["energy.e_dc_month[1]"],
        entity_name="Generator B Energy Production Month",
        update_priority=EntityUpdatePriority.INFREQUENT,
    ),
    InverterEntityDescriptor(
        ["energy.e_dc_year[1]"],
        entity_name="Generator B Energy Production Year",
        update_priority=EntityUpdatePriority.INFREQUENT,
    ),
    InverterEntityDescriptor(
        ["energy.e_dc_total[1]"],
        entity_name="Generator B Energy Production Total",
        update_priority=EntityUpdatePriority.INFREQUENT,
    ),
]
