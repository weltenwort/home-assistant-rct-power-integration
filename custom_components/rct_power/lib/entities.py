import re
from typing import List

from homeassistant.components.sensor import STATE_CLASS_MEASUREMENT
from homeassistant.const import DEVICE_CLASS_BATTERY
from rctclient.registry import REGISTRY

from .entity import (
    EntityUpdatePriority,
    MeteredResetFrequency,
    RctPowerSensorEntityDescription,
)


def get_matching_names(expression: str):
    compiled_expression = re.compile(expression)
    return [
        object_info.name
        for object_info in REGISTRY.all()
        if compiled_expression.match(object_info.name) is not None
    ]


battery_sensor_entity_descriptions: List[RctPowerSensorEntityDescription] = [
    RctPowerSensorEntityDescription(
        key="battery.bms_sn",
        name="Battery Management System Serial Number",
        update_priority=EntityUpdatePriority.STATIC,
    ),
    RctPowerSensorEntityDescription(
        key="battery.bms_software_version",
        name="Battery Management System Software Version",
        update_priority=EntityUpdatePriority.STATIC,
    ),
    RctPowerSensorEntityDescription(
        key="battery.module_sn[0]",
        name="Battery Module 1 Serial Number",
        update_priority=EntityUpdatePriority.STATIC,
    ),
    RctPowerSensorEntityDescription(
        key="battery.module_sn[1]",
        name="Battery Module 2 Serial Number",
        update_priority=EntityUpdatePriority.STATIC,
    ),
    RctPowerSensorEntityDescription(
        key="battery.module_sn[2]",
        name="Battery Module 3 Serial Number",
        update_priority=EntityUpdatePriority.STATIC,
    ),
    RctPowerSensorEntityDescription(
        key="battery.module_sn[3]",
        name="Battery Module 4 Serial Number",
        update_priority=EntityUpdatePriority.STATIC,
    ),
    RctPowerSensorEntityDescription(
        key="battery.module_sn[4]",
        name="Battery Module 5 Serial Number",
        update_priority=EntityUpdatePriority.STATIC,
    ),
    RctPowerSensorEntityDescription(
        key="battery.module_sn[5]",
        name="Battery Module 6 Serial Number",
        update_priority=EntityUpdatePriority.STATIC,
    ),
    RctPowerSensorEntityDescription(
        key="battery.charged_amp_hours",
        name="Battery Charge Total",
        update_priority=EntityUpdatePriority.INFREQUENT,
        state_class=STATE_CLASS_MEASUREMENT,
        metered_reset=MeteredResetFrequency.INITIALLY,
    ),
    RctPowerSensorEntityDescription(
        key="battery.discharged_amp_hours",
        name="Battery Discharge Total",
        update_priority=EntityUpdatePriority.INFREQUENT,
        state_class=STATE_CLASS_MEASUREMENT,
        metered_reset=MeteredResetFrequency.INITIALLY,
    ),
    RctPowerSensorEntityDescription(
        key="battery.current",
        name="Battery Current",
        update_priority=EntityUpdatePriority.FREQUENT,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    RctPowerSensorEntityDescription(
        key="battery.voltage",
        name="Battery Voltage",
        update_priority=EntityUpdatePriority.FREQUENT,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    RctPowerSensorEntityDescription(
        key="battery.maximum_charge_voltage",
        name="Battery Maximum Charging Voltage",
        update_priority=EntityUpdatePriority.FREQUENT,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    RctPowerSensorEntityDescription(
        key="battery.minimum_discharge_voltage",
        name="Battery Minimum Discharging Voltage",
        update_priority=EntityUpdatePriority.FREQUENT,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    RctPowerSensorEntityDescription(
        key="battery.maximum_discharge_current",
        name="Battery Maximum Discharging Current",
        update_priority=EntityUpdatePriority.FREQUENT,
    ),
    RctPowerSensorEntityDescription(
        key="battery.temperature",
        name="Battery Temperature",
        update_priority=EntityUpdatePriority.FREQUENT,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    RctPowerSensorEntityDescription(
        key="battery.stored_energy",
        name="Battery Stored Energy",
        update_priority=EntityUpdatePriority.FREQUENT,
        state_class=STATE_CLASS_MEASUREMENT,
        metered_reset=MeteredResetFrequency.INITIALLY,
    ),
    RctPowerSensorEntityDescription(
        key="battery.ah_capacity",
        name="Battery Charge Capacity",
        update_priority=EntityUpdatePriority.INFREQUENT,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    RctPowerSensorEntityDescription(
        key="battery.soc",
        name="Battery State of Charge",
        update_priority=EntityUpdatePriority.FREQUENT,
        state_class=STATE_CLASS_MEASUREMENT,
        device_class=DEVICE_CLASS_BATTERY,
    ),
    RctPowerSensorEntityDescription(
        key="battery.soc_target",
        name="Battery State of Charge Target",
        update_priority=EntityUpdatePriority.FREQUENT,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    RctPowerSensorEntityDescription(
        key="battery.soc_target_low",
        name="Battery State of Charge Low Target",
        update_priority=EntityUpdatePriority.FREQUENT,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    RctPowerSensorEntityDescription(
        key="battery.soc_target_high",
        name="Battery State of Charge High Target",
        update_priority=EntityUpdatePriority.FREQUENT,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    RctPowerSensorEntityDescription(
        key="battery.soh",
        name="Battery State of Health",
        update_priority=EntityUpdatePriority.INFREQUENT,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    RctPowerSensorEntityDescription(
        key="battery.cycles",
        name="Battery Cycles",
        update_priority=EntityUpdatePriority.INFREQUENT,
        state_class=STATE_CLASS_MEASUREMENT,
        metered_reset=MeteredResetFrequency.INITIALLY,
    ),
]

inverter_sensor_entity_descriptions: List[RctPowerSensorEntityDescription] = [
    RctPowerSensorEntityDescription(
        key="adc.u_acc",
        name="Inverter Battery Voltage",
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    RctPowerSensorEntityDescription(
        key="android_description",
        name="Inverter Device Name",
        update_priority=EntityUpdatePriority.STATIC,
    ),
    RctPowerSensorEntityDescription(
        key="buf_v_control.power_reduction_max_solar",
        name="Generator Maximum Power",
        update_priority=EntityUpdatePriority.STATIC,
    ),
    RctPowerSensorEntityDescription(
        key="buf_v_control.power_reduction_max_solar_grid",
        name="Grid Maximum Feed Power",
        update_priority=EntityUpdatePriority.STATIC,
    ),
    RctPowerSensorEntityDescription(
        key="db.core_temp",
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    RctPowerSensorEntityDescription(
        key="db.temp1",
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    RctPowerSensorEntityDescription(
        key="dc_conv.dc_conv_struct[0].enabled", name="Generator A Connected"
    ),
    RctPowerSensorEntityDescription(
        key="dc_conv.dc_conv_struct[0].mpp.fixed_voltage",
        name="Generator A MPP Fixed Voltage",
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    RctPowerSensorEntityDescription(
        key="dc_conv.dc_conv_struct[0].mpp.mpp_step",
        name="Generator A MPP Search Step",
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    RctPowerSensorEntityDescription(
        key="dc_conv.dc_conv_struct[0].p_dc",
        name="Generator A Power",
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    RctPowerSensorEntityDescription(
        key="dc_conv.dc_conv_struct[0].rescan_correction",
        name="Generator A MPP Rescan Correction",
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    RctPowerSensorEntityDescription(
        key="dc_conv.dc_conv_struct[0].u_sg_lp",
        name="Generator A Voltage",
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    RctPowerSensorEntityDescription(
        key="dc_conv.dc_conv_struct[1].enabled",
        name="Generator B Connected",
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    RctPowerSensorEntityDescription(
        key="dc_conv.dc_conv_struct[1].mpp.fixed_voltage",
        name="Generator B MPP Fixed Voltage",
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    RctPowerSensorEntityDescription(
        key="dc_conv.dc_conv_struct[1].mpp.mpp_step",
        name="Generator B MPP Search Step",
    ),
    RctPowerSensorEntityDescription(
        key="dc_conv.dc_conv_struct[1].p_dc",
        name="Generator B Power",
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    RctPowerSensorEntityDescription(
        key="dc_conv.dc_conv_struct[1].rescan_correction",
        name="Generator B MPP Rescan Correction",
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    RctPowerSensorEntityDescription(
        key="dc_conv.dc_conv_struct[1].u_sg_lp",
        name="Generator B Voltage",
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    RctPowerSensorEntityDescription(
        key="dc_conv.start_voltage",
        name="Inverter DC Start Voltage",
        update_priority=EntityUpdatePriority.STATIC,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    RctPowerSensorEntityDescription(
        key="inverter_sn",
        name="Inverter Serial Number",
        update_priority=EntityUpdatePriority.STATIC,
    ),
    RctPowerSensorEntityDescription(
        key="svnversion",
        name="Inverter Software Version",
        update_priority=EntityUpdatePriority.INFREQUENT,
    ),
    RctPowerSensorEntityDescription(
        key="flash_rtc.time_stamp_update",
        name="Date of Last Update",
        update_priority=EntityUpdatePriority.INFREQUENT,
    ),
    RctPowerSensorEntityDescription(
        key="g_sync.p_ac_sum",
        name="Inverter AC Power",
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    RctPowerSensorEntityDescription(
        key="g_sync.p_ac[0]",
        name="Inverter Power P1",
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    RctPowerSensorEntityDescription(
        key="g_sync.p_ac[1]",
        name="Inverter Power P2",
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    RctPowerSensorEntityDescription(
        key="g_sync.p_ac[2]",
        name="Inverter Power P3",
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    RctPowerSensorEntityDescription(
        key="g_sync.p_ac_load_sum_lp",
        name="Consumer Power",
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    RctPowerSensorEntityDescription(
        key="g_sync.p_ac_load[0]",
        name="Consumer Power P1",
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    RctPowerSensorEntityDescription(
        key="g_sync.p_ac_load[1]",
        name="Consumer Power P2",
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    RctPowerSensorEntityDescription(
        key="g_sync.p_ac_load[2]",
        name="Consumer Power P3",
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    RctPowerSensorEntityDescription(
        key="g_sync.p_acc_lp",
        name="Battery Power",
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    RctPowerSensorEntityDescription(
        key="g_sync.p_ac_grid_sum_lp",
        name="Grid Power",
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    RctPowerSensorEntityDescription(
        key="rb485.f_grid[0]",
        name="Grid Frequency P1",
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    RctPowerSensorEntityDescription(
        key="rb485.f_grid[1]",
        name="Grid Frequency P2",
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    RctPowerSensorEntityDescription(
        key="rb485.f_grid[2]",
        name="Grid Frequency P3",
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    RctPowerSensorEntityDescription(
        key="rb485.u_l_grid[0]",
        name="Grid Voltage P1",
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    RctPowerSensorEntityDescription(
        key="rb485.u_l_grid[1]",
        name="Grid Voltage P2",
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    RctPowerSensorEntityDescription(
        key="rb485.u_l_grid[2]",
        name="Grid Voltage P3",
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    RctPowerSensorEntityDescription(
        key="energy.e_load_day",
        name="Consumer Energy Consumption Day",
        update_priority=EntityUpdatePriority.INFREQUENT,
        state_class=STATE_CLASS_MEASUREMENT,
        metered_reset=MeteredResetFrequency.DAILY,
    ),
    RctPowerSensorEntityDescription(
        key="energy.e_load_month",
        name="Consumer Energy Consumption Month",
        update_priority=EntityUpdatePriority.INFREQUENT,
        state_class=STATE_CLASS_MEASUREMENT,
        metered_reset=MeteredResetFrequency.MONTHLY,
    ),
    RctPowerSensorEntityDescription(
        key="energy.e_load_year",
        name="Consumer Energy Consumption Year",
        update_priority=EntityUpdatePriority.INFREQUENT,
        state_class=STATE_CLASS_MEASUREMENT,
        metered_reset=MeteredResetFrequency.YEARLY,
    ),
    RctPowerSensorEntityDescription(
        key="energy.e_load_total",
        name="Consumer Energy Consumption Total",
        update_priority=EntityUpdatePriority.INFREQUENT,
        state_class=STATE_CLASS_MEASUREMENT,
        metered_reset=MeteredResetFrequency.INITIALLY,
    ),
    RctPowerSensorEntityDescription(
        key="energy.e_ac_day",
        name="Inverter Energy Production Day",
        update_priority=EntityUpdatePriority.INFREQUENT,
        state_class=STATE_CLASS_MEASUREMENT,
        metered_reset=MeteredResetFrequency.DAILY,
    ),
    RctPowerSensorEntityDescription(
        key="energy.e_ac_month",
        name="Inverter Energy Production Month",
        update_priority=EntityUpdatePriority.INFREQUENT,
        state_class=STATE_CLASS_MEASUREMENT,
        metered_reset=MeteredResetFrequency.MONTHLY,
    ),
    RctPowerSensorEntityDescription(
        key="energy.e_ac_year",
        name="Inverter Energy Production Year",
        update_priority=EntityUpdatePriority.INFREQUENT,
        state_class=STATE_CLASS_MEASUREMENT,
        metered_reset=MeteredResetFrequency.YEARLY,
    ),
    RctPowerSensorEntityDescription(
        key="energy.e_ac_total",
        name="Inverter Energy Production Total",
        update_priority=EntityUpdatePriority.INFREQUENT,
        state_class=STATE_CLASS_MEASUREMENT,
        metered_reset=MeteredResetFrequency.INITIALLY,
    ),
    RctPowerSensorEntityDescription(
        key="energy.e_grid_feed_day",
        name="Grid Energy Production Day",
        update_priority=EntityUpdatePriority.INFREQUENT,
        state_class=STATE_CLASS_MEASUREMENT,
        metered_reset=MeteredResetFrequency.DAILY,
    ),
    RctPowerSensorEntityDescription(
        key="energy.e_grid_feed_month",
        name="Grid Energy Production Month",
        update_priority=EntityUpdatePriority.INFREQUENT,
        state_class=STATE_CLASS_MEASUREMENT,
        metered_reset=MeteredResetFrequency.MONTHLY,
    ),
    RctPowerSensorEntityDescription(
        key="energy.e_grid_feed_year",
        name="Grid Energy Production Year",
        update_priority=EntityUpdatePriority.INFREQUENT,
        state_class=STATE_CLASS_MEASUREMENT,
        metered_reset=MeteredResetFrequency.YEARLY,
    ),
    RctPowerSensorEntityDescription(
        key="energy.e_grid_feed_total",
        name="Grid Energy Production Total",
        update_priority=EntityUpdatePriority.INFREQUENT,
        state_class=STATE_CLASS_MEASUREMENT,
        metered_reset=MeteredResetFrequency.INITIALLY,
    ),
    RctPowerSensorEntityDescription(
        key="energy.e_grid_load_day",
        name="Grid Energy Consumption Day",
        update_priority=EntityUpdatePriority.INFREQUENT,
        state_class=STATE_CLASS_MEASUREMENT,
        metered_reset=MeteredResetFrequency.DAILY,
    ),
    RctPowerSensorEntityDescription(
        key="energy.e_grid_load_month",
        name="Grid Energy Consumption Month",
        update_priority=EntityUpdatePriority.INFREQUENT,
        state_class=STATE_CLASS_MEASUREMENT,
        metered_reset=MeteredResetFrequency.MONTHLY,
    ),
    RctPowerSensorEntityDescription(
        key="energy.e_grid_load_year",
        name="Grid Energy Consumption Year",
        update_priority=EntityUpdatePriority.INFREQUENT,
        state_class=STATE_CLASS_MEASUREMENT,
        metered_reset=MeteredResetFrequency.YEARLY,
    ),
    RctPowerSensorEntityDescription(
        key="energy.e_grid_load_total",
        name="Grid Energy Consumption Total",
        update_priority=EntityUpdatePriority.INFREQUENT,
        state_class=STATE_CLASS_MEASUREMENT,
        metered_reset=MeteredResetFrequency.INITIALLY,
    ),
    RctPowerSensorEntityDescription(
        key="energy.e_ext_day",
        name="External Energy Production Day",
        update_priority=EntityUpdatePriority.INFREQUENT,
        state_class=STATE_CLASS_MEASUREMENT,
        metered_reset=MeteredResetFrequency.DAILY,
    ),
    RctPowerSensorEntityDescription(
        key="energy.e_ext_month",
        name="External Energy Production Month",
        update_priority=EntityUpdatePriority.INFREQUENT,
        state_class=STATE_CLASS_MEASUREMENT,
        metered_reset=MeteredResetFrequency.MONTHLY,
    ),
    RctPowerSensorEntityDescription(
        key="energy.e_ext_year",
        name="External Energy Production Year",
        update_priority=EntityUpdatePriority.INFREQUENT,
        state_class=STATE_CLASS_MEASUREMENT,
        metered_reset=MeteredResetFrequency.YEARLY,
    ),
    RctPowerSensorEntityDescription(
        key="energy.e_ext_total",
        name="External Energy Production Total",
        update_priority=EntityUpdatePriority.INFREQUENT,
        state_class=STATE_CLASS_MEASUREMENT,
        metered_reset=MeteredResetFrequency.INITIALLY,
    ),
    RctPowerSensorEntityDescription(
        key="energy.e_dc_day[0]",
        name="Generator A Energy Production Day",
        update_priority=EntityUpdatePriority.INFREQUENT,
        state_class=STATE_CLASS_MEASUREMENT,
        metered_reset=MeteredResetFrequency.DAILY,
    ),
    RctPowerSensorEntityDescription(
        key="energy.e_dc_month[0]",
        name="Generator A Energy Production Month",
        update_priority=EntityUpdatePriority.INFREQUENT,
        state_class=STATE_CLASS_MEASUREMENT,
        metered_reset=MeteredResetFrequency.MONTHLY,
    ),
    RctPowerSensorEntityDescription(
        key="energy.e_dc_year[0]",
        name="Generator A Energy Production Year",
        update_priority=EntityUpdatePriority.INFREQUENT,
        state_class=STATE_CLASS_MEASUREMENT,
        metered_reset=MeteredResetFrequency.YEARLY,
    ),
    RctPowerSensorEntityDescription(
        key="energy.e_dc_total[0]",
        name="Generator A Energy Production Total",
        update_priority=EntityUpdatePriority.INFREQUENT,
        state_class=STATE_CLASS_MEASUREMENT,
        metered_reset=MeteredResetFrequency.INITIALLY,
    ),
    RctPowerSensorEntityDescription(
        key="energy.e_dc_day[1]",
        name="Generator B Energy Production Day",
        update_priority=EntityUpdatePriority.INFREQUENT,
        state_class=STATE_CLASS_MEASUREMENT,
        metered_reset=MeteredResetFrequency.DAILY,
    ),
    RctPowerSensorEntityDescription(
        key="energy.e_dc_month[1]",
        name="Generator B Energy Production Month",
        update_priority=EntityUpdatePriority.INFREQUENT,
        state_class=STATE_CLASS_MEASUREMENT,
        metered_reset=MeteredResetFrequency.MONTHLY,
    ),
    RctPowerSensorEntityDescription(
        key="energy.e_dc_year[1]",
        name="Generator B Energy Production Year",
        update_priority=EntityUpdatePriority.INFREQUENT,
        state_class=STATE_CLASS_MEASUREMENT,
        metered_reset=MeteredResetFrequency.YEARLY,
    ),
    RctPowerSensorEntityDescription(
        key="energy.e_dc_total[1]",
        name="Generator B Energy Production Total",
        update_priority=EntityUpdatePriority.INFREQUENT,
        state_class=STATE_CLASS_MEASUREMENT,
        metered_reset=MeteredResetFrequency.INITIALLY,
    ),
]

fault_sensor_entity_descriptions: List[RctPowerSensorEntityDescription] = [
    RctPowerSensorEntityDescription(
        key="fault.flt",
        object_names=[
            "fault[0].flt",
            "fault[1].flt",
            "fault[2].flt",
            "fault[3].flt",
        ],
        name="Faults",
    ),
]

sensor_entity_descriptions = [
    *battery_sensor_entity_descriptions,
    *inverter_sensor_entity_descriptions,
    *fault_sensor_entity_descriptions,
]

all_entity_descriptions = [*sensor_entity_descriptions]
