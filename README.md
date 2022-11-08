# hass-foldingathomecontrol

[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE.md)

[![hacs][hacsbadge]][hacs]
![HACS Installs][hacs-installs-shield]
![Project Maintenance][maintenance-shield]
[![BuyMeCoffee][buymecoffeebadge]][buymecoffee]

[![Community Forum][forum-shield]][forum]

_Component to integrate with [Folding@Home][Folding@Home]._

**This component will set up the following platforms.**

Platform | Description
-- | --
`button` | Pause and Unpause Folding@Home clients.
`sensor` | Show stats from Folding@Home clients.
`select` | Select Power Setting Folding@Home clients.

![example][exampleimg]
![configuration][configurationimg]

## Setup

Follow [this](https://linustechtips.com/main/topic/990176-howto-remotely-access-your-folding-systems-part-1-fahcontrol/)
guide in order to allow other clients on your local network to access your Folding@Home client.

## Installation

### HACS

The easiest way to add this to your Homeassistant installation is using [HACS](https://hacs.xyz/).
And then follow the instructions under [Configuration](##configuration) below.

### Manual

1. Using the tool of choice open the directory (folder) for your HA configuration (where you find `configuration.yaml`).
2. If you do not have a `custom_components` directory (folder) there, you need to create it.
3. In the `custom_components` directory (folder) create a new folder called `foldingathomecontrol`.
4. Download _all_ the files from the `custom_components/foldingathomecontrol/` directory (folder) in this repository.
5. Place the files you downloaded in the new directory (folder) you created.
6. Restart Home Assistant
7. Choose:
   - Add `foldingathomecontrol:` to your HA configuration.
   - In the HA UI go to "Configuration" -> "Integrations" click "+" and search for "FoldingAtHomeControl"

Using your HA configuration directory (folder) as a starting point you should now also have this:

```text
custom_components/foldingathomecontrol/.translations/en.json
custom_components/foldingathomecontrol/__init__.py
custom_components/foldingathomecontrol/config_flow.py
custom_components/foldingathomecontrol/const.py
custom_components/foldingathomecontrol/foldingathomecontrol_client.py
custom_components/foldingathomecontrol/foldingathomecontrol_device.py
custom_components/foldingathomecontrol/manifest.json
custom_components/foldingathomecontrol/sensor.py
custom_components/foldingathomecontrol/services.py
custom_components/foldingathomecontrol/services.yaml
custom_components/foldingathomecontrol/timeparse.py
```

## Services

### foldingathomecontrol.pause

Pause one or all slots.

Name | Description | Example
-- | -- | --
`address` | `The IP address or hostname of the client. It can be found as part of the integration name.` | `localhost`
`slot` | `The slot to pause. Be sure to include the 0 in front if needed. Leave this out to pause all slots.` | `01`

### foldingathomecontrol.unpause

Unpause one or all slots.

Name | Description | Example
-- | -- | --
`address` | `The IP address or hostname of the client. It can be found as part of the integration name.` | `localhost`
`slot` | `The slot to unpause. Be sure to include the 0 in front if needed. Leave this out to unpause all slots.` | `01`

### foldingathomecontrol.shutdown

Shut down the client.

Name | Description | Example
-- | -- | --
`address` | `The IP address or hostname of the client. It can be found as part of the integration name.` | `localhost`

### foldingathomecontrol.request_work_server_assignment

Request a new assignment from the work server.

Name | Description | Example
-- | -- | --
`address` | `The IP address or hostname of the client. It can be found as part of the integration name.` | `localhost`

### foldingathomecontrol.set_power_level

Set the power level.

Name | Description | Example
-- | -- | --
`address` | `The IP address or hostname of the client. It can be found as part of the integration name.` | `localhost`
`power_level` | `The power level to set.` | `One of: LIGHT,MEDIUM,FULL`

### foldingathomecontrol.send_command

Set the power level.

Name | Description | Example
-- | -- | --
`address` | `The IP address or hostname of the client. It can be found as part of the integration name.` | `localhost`
`command` | `The command to send.` | `slot-info`

## Contributions are welcome

If you want to contribute to this please read the [Contribution guidelines](CONTRIBUTING.md)

***

[Folding@Home]: https://github.com/eifinger/PyFoldingAtHomeControl
[buymecoffee]: https://www.buymeacoffee.com/eifinger
[buymecoffeebadge]: https://img.shields.io/badge/buy%20me%20a%20coffee-donate-yellow.svg?style=for-the-badge
[commits-shield]: https://img.shields.io/github/commit-activity/y/eifinger/hass-foldingathomecontrol.svg?style=for-the-badge
[commits]: https://github.com/eifinger/hass-foldingathomecontrol/commits/main
[hacs]: https://github.com/hacs/integration
[hacsbadge]: https://img.shields.io/badge/HACS-Default-orange.svg?style=for-the-badge
[hacs-installs-shield]: https://img.shields.io/badge/dynamic/json?color=41BDF5&logo=home-assistant&label=installs&style=for-the-badge&cacheSeconds=15600&url=https://analytics.home-assistant.io/custom_integrations.json&query=$.foldingathomecontrol.total
[exampleimg]: https://github.com/eifinger/hass-foldingathomecontrol/blob/main/example.png?raw=true
[configurationimg]: https://github.com/eifinger/hass-foldingathomecontrol/blob/main/configuration.png?raw=true
[forum-shield]: https://img.shields.io/badge/community-forum-brightgreen.svg?style=for-the-badge
[forum]: https://community.home-assistant.io/
[license-shield]: https://img.shields.io/github/license/eifinger/hass-foldingathomecontrol.svg?style=for-the-badge
[maintenance-shield]: https://img.shields.io/badge/maintainer-Kevin%20Stillhammer%20%40eifinger-blue.svg?style=for-the-badge
[releases-shield]: https://img.shields.io/github/release/eifinger/hass-foldingathomecontrol.svg?style=for-the-badge
[releases]: https://github.com/eifinger/hass-foldingathomecontrol/releases
