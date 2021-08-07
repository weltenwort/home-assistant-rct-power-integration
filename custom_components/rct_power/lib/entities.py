import re
from typing import List

from homeassistant.components.sensor import STATE_CLASS_MEASUREMENT
from homeassistant.const import DEVICE_CLASS_BATTERY
from rctclient.registry import REGISTRY

from .entity import (
    BatteryEntityDescriptor,
    EntityDescriptor,
    EntityUpdatePriority,
    FaultEntityDescriptor,
    InverterEntityDescriptor,
    MeteredResetFrequency,
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
        state_class=STATE_CLASS_MEASUREMENT,
        metered_reset=MeteredResetFrequency.INITIALLY,
    ),
    BatteryEntityDescriptor(
        ["battery.discharged_amp_hours"],
        entity_name="Battery Discharge Total",
        update_priority=EntityUpdatePriority.INFREQUENT,
        state_class=STATE_CLASS_MEASUREMENT,
        metered_reset=MeteredResetFrequency.INITIALLY,
    ),
    BatteryEntityDescriptor(
        ["battery.current"],
        entity_name="Battery Current",
        update_priority=EntityUpdatePriority.FREQUENT,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    BatteryEntityDescriptor(
        ["battery.voltage"],
        entity_name="Battery Voltage",
        update_priority=EntityUpdatePriority.FREQUENT,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    BatteryEntityDescriptor(
        ["battery.maximum_charge_voltage"],
        entity_name="Battery Maximum Charging Voltage",
        update_priority=EntityUpdatePriority.FREQUENT,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    BatteryEntityDescriptor(
        ["battery.minimum_discharge_voltage"],
        entity_name="Battery Minimum Discharging Voltage",
        update_priority=EntityUpdatePriority.FREQUENT,
        state_class=STATE_CLASS_MEASUREMENT,
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
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    BatteryEntityDescriptor(
        ["battery.stored_energy"],
        entity_name="Battery Stored Energy",
        update_priority=EntityUpdatePriority.FREQUENT,
        state_class=STATE_CLASS_MEASUREMENT,
        metered_reset=MeteredResetFrequency.INITIALLY,
    ),
    BatteryEntityDescriptor(
        ["battery.ah_capacity"],
        entity_name="Battery Charge Capacity",
        update_priority=EntityUpdatePriority.INFREQUENT,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    BatteryEntityDescriptor(
        ["battery.soc"],
        entity_name="Battery State of Charge",
        update_priority=EntityUpdatePriority.FREQUENT,
        state_class=STATE_CLASS_MEASUREMENT,
        device_class=DEVICE_CLASS_BATTERY,
    ),
    BatteryEntityDescriptor(
        ["battery.soc_target"],
        entity_name="Battery State of Charge Target",
        update_priority=EntityUpdatePriority.FREQUENT,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    BatteryEntityDescriptor(
        ["battery.soc_target_low"],
        entity_name="Battery State of Charge Low Target",
        update_priority=EntityUpdatePriority.FREQUENT,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    BatteryEntityDescriptor(
        ["battery.soc_target_high"],
        entity_name="Battery State of Charge High Target",
        update_priority=EntityUpdatePriority.FREQUENT,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    BatteryEntityDescriptor(
        ["battery.soh"],
        entity_name="Battery State of Health",
        update_priority=EntityUpdatePriority.INFREQUENT,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    BatteryEntityDescriptor(
        ["battery.cycles"],
        entity_name="Battery Cycles",
        update_priority=EntityUpdatePriority.INFREQUENT,
        state_class=STATE_CLASS_MEASUREMENT,
        metered_reset=MeteredResetFrequency.INITIALLY,
    ),
    InverterEntityDescriptor(
        ["adc.u_acc"],
        entity_name="Inverter Battery Voltage",
        state_class=STATE_CLASS_MEASUREMENT,
    ),
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
    InverterEntityDescriptor(
        ["db.core_temp"],
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    InverterEntityDescriptor(
        ["db.temp1"],
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    InverterEntityDescriptor(
        ["dc_conv.dc_conv_struct[0].enabled"], entity_name="Generator A Connected"
    ),
    InverterEntityDescriptor(
        ["dc_conv.dc_conv_struct[0].mpp.fixed_voltage"],
        entity_name="Generator A MPP Fixed Voltage",
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    InverterEntityDescriptor(
        ["dc_conv.dc_conv_struct[0].mpp.mpp_step"],
        entity_name="Generator A MPP Search Step",
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    InverterEntityDescriptor(
        ["dc_conv.dc_conv_struct[0].p_dc"],
        entity_name="Generator A Power",
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    InverterEntityDescriptor(
        ["dc_conv.dc_conv_struct[0].rescan_correction"],
        entity_name="Generator A MPP Rescan Correction",
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    InverterEntityDescriptor(
        ["dc_conv.dc_conv_struct[0].u_sg_lp"],
        entity_name="Generator A Voltage",
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    InverterEntityDescriptor(
        ["dc_conv.dc_conv_struct[1].enabled"],
        entity_name="Generator B Connected",
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    InverterEntityDescriptor(
        ["dc_conv.dc_conv_struct[1].mpp.fixed_voltage"],
        entity_name="Generator B MPP Fixed Voltage",
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    InverterEntityDescriptor(
        ["dc_conv.dc_conv_struct[1].mpp.mpp_step"],
        entity_name="Generator B MPP Search Step",
    ),
    InverterEntityDescriptor(
        ["dc_conv.dc_conv_struct[1].p_dc"],
        entity_name="Generator B Power",
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    InverterEntityDescriptor(
        ["dc_conv.dc_conv_struct[1].rescan_correction"],
        entity_name="Generator B MPP Rescan Correction",
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    InverterEntityDescriptor(
        ["dc_conv.dc_conv_struct[1].u_sg_lp"],
        entity_name="Generator B Voltage",
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    InverterEntityDescriptor(
        ["dc_conv.start_voltage"],
        entity_name="Inverter DC Start Voltage",
        update_priority=EntityUpdatePriority.STATIC,
        state_class=STATE_CLASS_MEASUREMENT,
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
    InverterEntityDescriptor(
        ["g_sync.p_ac_sum"],
        entity_name="Inverter AC Power",
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    InverterEntityDescriptor(
        ["g_sync.p_ac[0]"],
        entity_name="Inverter Power P1",
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    InverterEntityDescriptor(
        ["g_sync.p_ac[1]"],
        entity_name="Inverter Power P2",
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    InverterEntityDescriptor(
        ["g_sync.p_ac[2]"],
        entity_name="Inverter Power P3",
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    InverterEntityDescriptor(
        ["g_sync.p_ac_load_sum_lp"],
        entity_name="Consumer Power",
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    InverterEntityDescriptor(
        ["g_sync.p_ac_load[0]"],
        entity_name="Consumer Power P1",
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    InverterEntityDescriptor(
        ["g_sync.p_ac_load[1]"],
        entity_name="Consumer Power P2",
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    InverterEntityDescriptor(
        ["g_sync.p_ac_load[2]"],
        entity_name="Consumer Power P3",
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    InverterEntityDescriptor(
        ["g_sync.p_acc_lp"],
        entity_name="Battery Power",
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    InverterEntityDescriptor(
        ["g_sync.p_ac_grid_sum_lp"],
        entity_name="Grid Power",
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    InverterEntityDescriptor(
        ["rb485.f_grid[0]"],
        entity_name="Grid Frequency P1",
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    InverterEntityDescriptor(
        ["rb485.f_grid[1]"],
        entity_name="Grid Frequency P2",
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    InverterEntityDescriptor(
        ["rb485.f_grid[2]"],
        entity_name="Grid Frequency P3",
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    InverterEntityDescriptor(
        ["rb485.u_l_grid[0]"],
        entity_name="Grid Voltage P1",
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    InverterEntityDescriptor(
        ["rb485.u_l_grid[1]"],
        entity_name="Grid Voltage P2",
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    InverterEntityDescriptor(
        ["rb485.u_l_grid[2]"],
        entity_name="Grid Voltage P3",
        state_class=STATE_CLASS_MEASUREMENT,
    ),
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
        state_class=STATE_CLASS_MEASUREMENT,
        metered_reset=MeteredResetFrequency.DAILY,
    ),
    InverterEntityDescriptor(
        ["energy.e_load_month"],
        entity_name="Consumer Energy Consumption Month",
        update_priority=EntityUpdatePriority.INFREQUENT,
        state_class=STATE_CLASS_MEASUREMENT,
        metered_reset=MeteredResetFrequency.MONTHLY,
    ),
    InverterEntityDescriptor(
        ["energy.e_load_year"],
        entity_name="Consumer Energy Consumption Year",
        update_priority=EntityUpdatePriority.INFREQUENT,
        state_class=STATE_CLASS_MEASUREMENT,
        metered_reset=MeteredResetFrequency.YEARLY,
    ),
    InverterEntityDescriptor(
        ["energy.e_load_total"],
        entity_name="Consumer Energy Consumption Total",
        update_priority=EntityUpdatePriority.INFREQUENT,
        state_class=STATE_CLASS_MEASUREMENT,
        metered_reset=MeteredResetFrequency.INITIALLY,
    ),
    InverterEntityDescriptor(
        ["energy.e_ac_day"],
        entity_name="Inverter Energy Production Day",
        update_priority=EntityUpdatePriority.INFREQUENT,
        state_class=STATE_CLASS_MEASUREMENT,
        metered_reset=MeteredResetFrequency.DAILY,
    ),
    InverterEntityDescriptor(
        ["energy.e_ac_month"],
        entity_name="Inverter Energy Production Month",
        update_priority=EntityUpdatePriority.INFREQUENT,
        state_class=STATE_CLASS_MEASUREMENT,
        metered_reset=MeteredResetFrequency.MONTHLY,
    ),
    InverterEntityDescriptor(
        ["energy.e_ac_year"],
        entity_name="Inverter Energy Production Year",
        update_priority=EntityUpdatePriority.INFREQUENT,
        state_class=STATE_CLASS_MEASUREMENT,
        metered_reset=MeteredResetFrequency.YEARLY,
    ),
    InverterEntityDescriptor(
        ["energy.e_ac_total"],
        entity_name="Inverter Energy Production Total",
        update_priority=EntityUpdatePriority.INFREQUENT,
        state_class=STATE_CLASS_MEASUREMENT,
        metered_reset=MeteredResetFrequency.INITIALLY,
    ),
    InverterEntityDescriptor(
        ["energy.e_grid_feed_day"],
        entity_name="Grid Energy Production Day",
        update_priority=EntityUpdatePriority.INFREQUENT,
        state_class=STATE_CLASS_MEASUREMENT,
        metered_reset=MeteredResetFrequency.DAILY,
    ),
    InverterEntityDescriptor(
        ["energy.e_grid_feed_month"],
        entity_name="Grid Energy Production Month",
        update_priority=EntityUpdatePriority.INFREQUENT,
        state_class=STATE_CLASS_MEASUREMENT,
        metered_reset=MeteredResetFrequency.MONTHLY,
    ),
    InverterEntityDescriptor(
        ["energy.e_grid_feed_year"],
        entity_name="Grid Energy Production Year",
        update_priority=EntityUpdatePriority.INFREQUENT,
        state_class=STATE_CLASS_MEASUREMENT,
        metered_reset=MeteredResetFrequency.YEARLY,
    ),
    InverterEntityDescriptor(
        ["energy.e_grid_feed_total"],
        entity_name="Grid Energy Production Total",
        update_priority=EntityUpdatePriority.INFREQUENT,
        state_class=STATE_CLASS_MEASUREMENT,
        metered_reset=MeteredResetFrequency.INITIALLY,
    ),
    InverterEntityDescriptor(
        ["energy.e_grid_load_day"],
        entity_name="Grid Energy Consumption Day",
        update_priority=EntityUpdatePriority.INFREQUENT,
        state_class=STATE_CLASS_MEASUREMENT,
        metered_reset=MeteredResetFrequency.DAILY,
    ),
    InverterEntityDescriptor(
        ["energy.e_grid_load_month"],
        entity_name="Grid Energy Consumption Month",
        update_priority=EntityUpdatePriority.INFREQUENT,
        state_class=STATE_CLASS_MEASUREMENT,
        metered_reset=MeteredResetFrequency.MONTHLY,
    ),
    InverterEntityDescriptor(
        ["energy.e_grid_load_year"],
        entity_name="Grid Energy Consumption Year",
        update_priority=EntityUpdatePriority.INFREQUENT,
        state_class=STATE_CLASS_MEASUREMENT,
        metered_reset=MeteredResetFrequency.YEARLY,
    ),
    InverterEntityDescriptor(
        ["energy.e_grid_load_total"],
        entity_name="Grid Energy Consumption Total",
        update_priority=EntityUpdatePriority.INFREQUENT,
        state_class=STATE_CLASS_MEASUREMENT,
        metered_reset=MeteredResetFrequency.INITIALLY,
    ),
    InverterEntityDescriptor(
        ["energy.e_ext_day"],
        entity_name="External Energy Production Day",
        update_priority=EntityUpdatePriority.INFREQUENT,
        state_class=STATE_CLASS_MEASUREMENT,
        metered_reset=MeteredResetFrequency.DAILY,
    ),
    InverterEntityDescriptor(
        ["energy.e_ext_month"],
        entity_name="External Energy Production Month",
        update_priority=EntityUpdatePriority.INFREQUENT,
        state_class=STATE_CLASS_MEASUREMENT,
        metered_reset=MeteredResetFrequency.MONTHLY,
    ),
    InverterEntityDescriptor(
        ["energy.e_ext_year"],
        entity_name="External Energy Production Year",
        update_priority=EntityUpdatePriority.INFREQUENT,
        state_class=STATE_CLASS_MEASUREMENT,
        metered_reset=MeteredResetFrequency.YEARLY,
    ),
    InverterEntityDescriptor(
        ["energy.e_ext_total"],
        entity_name="External Energy Production Total",
        update_priority=EntityUpdatePriority.INFREQUENT,
        state_class=STATE_CLASS_MEASUREMENT,
        metered_reset=MeteredResetFrequency.INITIALLY,
    ),
    InverterEntityDescriptor(
        ["energy.e_dc_day[0]"],
        entity_name="Generator A Energy Production Day",
        update_priority=EntityUpdatePriority.INFREQUENT,
        state_class=STATE_CLASS_MEASUREMENT,
        metered_reset=MeteredResetFrequency.DAILY,
    ),
    InverterEntityDescriptor(
        ["energy.e_dc_month[0]"],
        entity_name="Generator A Energy Production Month",
        update_priority=EntityUpdatePriority.INFREQUENT,
        state_class=STATE_CLASS_MEASUREMENT,
        metered_reset=MeteredResetFrequency.MONTHLY,
    ),
    InverterEntityDescriptor(
        ["energy.e_dc_year[0]"],
        entity_name="Generator A Energy Production Year",
        update_priority=EntityUpdatePriority.INFREQUENT,
        state_class=STATE_CLASS_MEASUREMENT,
        metered_reset=MeteredResetFrequency.YEARLY,
    ),
    InverterEntityDescriptor(
        ["energy.e_dc_total[0]"],
        entity_name="Generator A Energy Production Total",
        update_priority=EntityUpdatePriority.INFREQUENT,
        state_class=STATE_CLASS_MEASUREMENT,
        metered_reset=MeteredResetFrequency.INITIALLY,
    ),
    InverterEntityDescriptor(
        ["energy.e_dc_day[1]"],
        entity_name="Generator B Energy Production Day",
        update_priority=EntityUpdatePriority.INFREQUENT,
        state_class=STATE_CLASS_MEASUREMENT,
        metered_reset=MeteredResetFrequency.DAILY,
    ),
    InverterEntityDescriptor(
        ["energy.e_dc_month[1]"],
        entity_name="Generator B Energy Production Month",
        update_priority=EntityUpdatePriority.INFREQUENT,
        state_class=STATE_CLASS_MEASUREMENT,
        metered_reset=MeteredResetFrequency.MONTHLY,
    ),
    InverterEntityDescriptor(
        ["energy.e_dc_year[1]"],
        entity_name="Generator B Energy Production Year",
        update_priority=EntityUpdatePriority.INFREQUENT,
        state_class=STATE_CLASS_MEASUREMENT,
        metered_reset=MeteredResetFrequency.YEARLY,
    ),
    InverterEntityDescriptor(
        ["energy.e_dc_total[1]"],
        entity_name="Generator B Energy Production Total",
        update_priority=EntityUpdatePriority.INFREQUENT,
        state_class=STATE_CLASS_MEASUREMENT,
        metered_reset=MeteredResetFrequency.INITIALLY,
    ),
]
