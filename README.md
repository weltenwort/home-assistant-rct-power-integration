# RCT Power integration

[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE)

[![pre-commit][pre-commit-shield]][pre-commit]
[![Black][black-shield]][black]

[![hacs][hacsbadge]][hacs]
[![Project Maintenance][maintenance-shield]][user_profile]
[![BuyMeCoffee][buymecoffeebadge]][buymecoffee]

[![Discord][discord-shield]][discord]
[![Community Forum][forum-shield]][forum]

**This component will set up the following platforms.**

| Platform | Description                   |
| -------- | ----------------------------- |
| `sensor` | Show info from RCT Power API. |

## Installation

### Via the HACS integration

1. Install the "RCT Power" integration using [HACS].
2. In the HA UI go to "Configuration" -> "Integrations" click "+" and search for "RCT Power"

### Via manual download

1. Using the tool of choice open the directory (folder) for your HA configuration (where you find `configuration.yaml`).
2. If you do not have a `custom_components` directory (folder) there, you need to create it.
3. In the `custom_components` directory (folder) create a new folder called `rct_power`.
4. Download _all_ the files from the `custom_components/rct_power/` directory (folder) in this repository.
5. Place the files you downloaded in the new directory (folder) you created.
6. Restart Home Assistant
7. In the HA UI go to "Configuration" -> "Integrations" click "+" and search for "RCT Power"

## Configuration

Upon installation the integration accepts the following configuration parameters:

- `Host name`: The local IP address or host name of the inverter.
- `Port`: The port of the inverter's API, defaults to `8899`.
- `Name`: This name is used as a prefix to the entities created by this integration and can be used to disambiguate multiple inverters.

After installation the integration allows for the following configuration parameters to be changed:

- `Frequent polling interval`: The polling interval in seconds for entities updated frequently, defaults to `30`.
- `Infrequent polling interval`: The polling interval in seconds for entities updated infrequently, defaults to `180`.
- `Static polling interval`: The polling interval in seconds for entities updated seldomly, defaults to `3600`.

## Usage with the built-in energy dashboard

You can use the entities provided by this integration on Home Assistant's
built-in energy dashboard. For that purpose, navigate to "Configuration" ->
"Energy" and choose the following entities.

Please note that the entity names in your installation are prefixed with the
inverter name chosen during installation of the integration, so interpret the
entity names mentioned below to be entity name suffixes.

Also note that after configuration the energy dashboard might take several hours
to show any data, because Home Assistant calculates the underlying statistics
only on an hourly basis.

### Electricity grid

| Configuration item | Entity name                             | Note                                                   |
| ------------------ | --------------------------------------- | ------------------------------------------------------ |
| Grid consumption   | `Grid Energy Consumption Total`         |                                                        |
| Return to grid     | `Grid Energy Production Absolute Total` | Make sure to use the "Absolute" variant of this entity |

### Solar panels

You can configure the two generator strings A and B separately or combined
depending on your preference.

#### Separate generator strings

| Configuration item | Entity name                           |
| ------------------ | ------------------------------------- |
| Solar Production   | `Generator A Energy Production Total` |
| Solar Production   | `Generator B Energy Production Total` |

#### Combined generator strings

| Configuration item | Entity name                              |
| ------------------ | ---------------------------------------- |
| Solar Production   | `All Generators Energy Production Total` |

### Home Battery Storage

| Configuration item                                 | Entity name             |
| -------------------------------------------------- | ----------------------- |
| Battery systems - Energy going into the battery    | `Battery Stored Energy` |
| Battery systems - Energy coming out of the battery | `Battery Used Energy`   |

## Most commonly used entities

:warning: This list is incomplete and the interpretations might be incorrect due to a lack of official documentation.

### Grid

| Entity name                                  | Unit | Description                                                                      |
| -------------------------------------------- | ---- | -------------------------------------------------------------------------------- |
| Grid Frequency                               | Hz   | the instantaneous overall grid frequency                                         |
| Grid Frequency P1/P2/P3                      | Hz   | the instantaneous grid frequency on phase 1/2/3                                  |
| Grid Power                                   | W    | the instantaneous power consumed from (`> 0`) or fed into (`< 0`) the grid       |
| Grid Power P1/P2/P3                          | W    | the instantaneous power consumed from or fed into the grid on phase 1/2/3        |
| Grid Voltage P1/P2/P3                        | W    | the instantaneous grid voltage on phase 1/2/3                                    |
| Grid Energy Consumption Day/Month/Year/Total | Wh   | the cumulative energy consumed from the grid                                     |
| Grid Energy Production Day/Month/Year/Total  | Wh   | the cumulative energy fed into the grid                                          |
| Grid Energy Production Absolute Total        | kWh  | the absolute value of the cumulative energy fed into the grid since installation |
| Grid Maximum Feed Power                      | W    | the maximum power the inverter is configured to feed into the grid               |

### Battery

| Entity name                    | Unit | Description                                                                   |
| ------------------------------ | ---- | ----------------------------------------------------------------------------- |
| Battery Power                  | W    | the instantaneous power consumed from (`> 0`) or fed into (`< 0`) the battery |
| Battery Current                | A    | the instantaneous current flowing from or to the battery                      |
| Battery Voltage                | V    | the instantaneous voltage of the battery                                      |
| Battery Temperature            | °C   | the instantaneous temperature of the battery                                  |
| Battery Cycles                 |      | the recorded full charge/discharge cycles of the battery                      |
| Battery State of Charge        | %    | the instantaneous state of charge of the battery                              |
| Battery State of Charge Target | %    | the state of charge of the battery aimed for by the system                    |
| Battery State of Health        | %    | the estimated state of health of the battery                                  |
| Battery Stored Energy          | Wh   | the cumulative energy fed into the battery                                    |
| Battery Used Energy            | Wh   | the cumulative energy consumed from the battery                               |
| Battery Status                 |      | the current battery status (incomplete)                                       |

### Household consumers and producers

| Entity name                                      | Unit | Description                                                            |
| ------------------------------------------------ | ---- | ---------------------------------------------------------------------- |
| Consumer Energy Consumption Day/Month/Year/Total | Wh   | the cumulative energy consumed by the household (from any source)      |
| Consumer Power                                   | W    | the instantaneous power consumed by the household                      |
| Consumer Power P1/P2/P3                          | W    | the instantaneous power consumed by the household on phase 1/2/3       |
| External Energy Production Day/Month/Year/Total  | Wh   | the cumulative energy produced by the external producer (if installed) |

### Photovoltaic generators

| Entity name                                        | Unit | Description                                                           |
| -------------------------------------------------- | ---- | --------------------------------------------------------------------- |
| Generator A Energy Production Day/Month/Year/Total | Wh   | the cumulative energy produced by generator string A                  |
| Generator B Energy Production Day/Month/Year/Total | Wh   | the cumulative energy produced by generator string B                  |
| All Generators Energy Production Total             | Wh   | the sum of the cumulative energy produced by both generator strings   |
| Generator A Power                                  | W    | the instantaneous power produced by generator string A                |
| Generator B Power                                  | W    | the instantaneous power produced by generator string B                |
| All Generators Power                               | W    | the sum of the instantaneous power produced by both generator strings |
| Generator A Voltage                                | V    | the instantaneous voltage produced by generator string A              |
| Generator B Voltage                                | V    | the instantaneous voltage produced by generator string B              |
| Generator Maximum Power                            | W    | the configured combined maximum power of both generator strings       |
| Insulation Resistance                              | Ohm  |                                                                       |
| Insulation Resistance Positive/Negative Input      | Ohm  |                                                                       |
| Minimum Insulation Resistance                      | Ohm  |                                                                       |

### Inverter

| Entity name                                     | Unit | Description                                                   |
| ----------------------------------------------- | ---- | ------------------------------------------------------------- |
| Inverter AC Power                               | W    | the instantaneous AC power transmitted by the inverter        |
| Inverter Energy Production Day/Month/Year/Total | Wh   | the cumulative energy produced by the inverter                |
| Inverter Power P1/P2/P3                         | W    | the instantaneous power consumed or generated by the inverter |
| Inverter Serial Number                          |      | the serial number of the inverter                             |
| Faults                                          |      | a bitmask of the failures reported by the inverter            |

## Contributions are welcome!

If you want to contribute to this please read the [Contribution guidelines](CONTRIBUTING.md)

## Credits

This would have been a lot more difficult if not for [@svalouch](https://github.com/svalouch)'s [`python-rctclient`](https://github.com/svalouch/python-rctclient) library. Thank you!

This project was generated from [@oncleben31](https://github.com/oncleben31)'s [Home Assistant Custom Component Cookiecutter](https://github.com/oncleben31/cookiecutter-homeassistant-custom-component) template.

Code template was mainly taken from [@Ludeeus](https://github.com/ludeeus)'s [integration_blueprint][integration_blueprint] template

---

[integration_blueprint]: https://github.com/custom-components/integration_blueprint
[black]: https://github.com/psf/black
[black-shield]: https://img.shields.io/badge/code%20style-black-000000.svg?style=for-the-badge
[buymecoffee]: https://www.buymeacoffee.com/weltenwort
[buymecoffeebadge]: https://img.shields.io/badge/buy%20me%20a%20coffee-donate-yellow.svg?style=for-the-badge
[commits-shield]: https://img.shields.io/github/commit-activity/y/weltenwort/home-assistant-rct-power-integration.svg?style=for-the-badge
[commits]: https://github.com/weltenwort/home-assistant-rct-power-integration/commits/main
[hacs]: https://hacs.xyz
[hacsbadge]: https://img.shields.io/badge/HACS-Default-orange.svg?style=for-the-badge
[discord]: https://discord.gg/Qa5fW2R
[discord-shield]: https://img.shields.io/discord/330944238910963714.svg?style=for-the-badge
[exampleimg]: example.png
[forum-shield]: https://img.shields.io/badge/community-forum-brightgreen.svg?style=for-the-badge
[forum]: https://community.home-assistant.io/
[license-shield]: https://img.shields.io/github/license/weltenwort/home-assistant-rct-power-integration.svg?style=for-the-badge
[maintenance-shield]: https://img.shields.io/badge/maintainer-%40weltenwort-blue.svg?style=for-the-badge
[pre-commit]: https://github.com/pre-commit/pre-commit
[pre-commit-shield]: https://img.shields.io/badge/pre--commit-enabled-brightgreen?style=for-the-badge
[releases-shield]: https://img.shields.io/github/release/weltenwort/home-assistant-rct-power-integration.svg?style=for-the-badge
[releases]: https://github.com/weltenwort/home-assistant-rct-power-integration/releases
[user_profile]: https://github.com/weltenwort
