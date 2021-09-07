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
[maintenance-shield]: https://img.shields.io/badge/maintainer-Kevin%20Stillhammer%20%40eifinger-blue.svg?style=for-the-badge
[releases-shield]: https://img.shields.io/github/release/eifinger/hass-foldingathomecontrol.svg?style=for-the-badge
[releases]: https://github.com/eifinger/hass-foldingathomecontrol/releases
