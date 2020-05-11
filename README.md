# hass-foldingathomecontrol

[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE.md)

[![hacs][hacsbadge]][hacs]
![Project Maintenance][maintenance-shield]
[![BuyMeCoffee][buymecoffeebadge]][buymecoffee]

[![Community Forum][forum-shield]][forum]

_Component to integrate with [Folding@Home][Folding@Home]._

**This component will set up the following platforms.**

Platform | Description
-- | --
`sensor` | Show stats from Folding@Home clients.

![example][exampleimg]

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

## Configuration

### Example configuration.yaml

```yaml
foldingathomecontrol:
  - address: "localhost"
    port: 36330
    password: "password"
```

### Configuration options

Key | Type | Required | Default | Description
-- | -- | -- | -- | --
`address` | `string` | `False` | `localhost` | IP address or hostname where the Folding@Home client is running on. Default is `localhost`.
`port` | `int` | `False` | `36330` | Port of the client. Default is `36330`.
`password` | `string` | `False` | - | Password for the client if configured.

## Contributions are welcome!

If you want to contribute to this please read the [Contribution guidelines](CONTRIBUTING.md)

***

[Folding@Home]: https://github.com/eifinger/PyFoldingAtHomeControl
[buymecoffee]: https://www.buymeacoffee.com/eifinger
[buymecoffeebadge]: https://img.shields.io/badge/buy%20me%20a%20coffee-donate-yellow.svg?style=for-the-badge
[commits-shield]: https://img.shields.io/github/commit-activity/y/eifinger/hass-foldingathomecontrol.svg?style=for-the-badge
[commits]: https://github.com/eifinger/hass-foldingathomecontrol/commits/master
[hacs]: https://github.com/custom-components/hacs
[hacsbadge]: https://img.shields.io/badge/HACS-Default-orange.svg?style=for-the-badge
[exampleimg]: example.png
[forum-shield]: https://img.shields.io/badge/community-forum-brightgreen.svg?style=for-the-badge
[forum]: https://community.home-assistant.io/
[license-shield]: https://img.shields.io/github/license/eifinger/hass-foldingathomecontrol.svg?style=for-the-badge
[maintenance-shield]: https://img.shields.io/badge/maintainer-Kevin%20Eifinger%20%40eifinger-blue.svg?style=for-the-badge
[releases-shield]: https://img.shields.io/github/release/eifinger/hass-foldingathomecontrol.svg?style=for-the-badge
[releases]: https://github.com/eifinger/hass-foldingathomecontrol/releases
