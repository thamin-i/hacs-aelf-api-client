# AELF API Client (unofficial)

AELF API Client (unofficial) is a custom Home Assistant Community Store (HACS) integration that fetches liturgical data from the [AELF](https://api.aelf.org) API. This integration allows you to display masses and other prayers directly in your Home Assistant instance.

- Fetches liturgical informations from the AELF API.
- Generate one Home Assisant device per AELF entity (mass, compline, lauds, readings, none, sext, terce, vespers)

## Installation

### Prerequisites

- Home Assistant version 2023.0.0 or later.
- HACS (Home Assistant Community Store) installed in your Home Assistant instance.

### Steps to Install

1. Open HACS in your Home Assistant instance.
2. Go to the "Integrations" section.
3. Click on the three-dot menu in the top-right corner and select "Custom repositories."
4. Add the following repository URL: `https://github.com/thamin-i/hacs-aelf-api-client` and select the category as "Integration."
5. Search for "AELF API Client (unofficial)" in the HACS Integrations section and click "Install."
6. Restart Home Assistant to complete the installation.

## Configuration

1. After restarting Home Assistant, go to **Settings** > **Devices & Services** > **Integrations**.
2. Click on "Add Integration" and search for "AELF API Client (unofficial)".
3. Follow the on-screen instructions to configure the integration.

## Requirements

This integration requires the following Python libraries, which are automatically installed:

- `aiohttp~=3.11.16`
- `voluptuous~=0.15.2`

## Integration Details

- **Domain**: `hacs-aelf-api-client`
- **IoT Class**: Cloud Polling
- **Integration Type**: hub

## Troubleshooting

If you encounter any issues:

1. Ensure that your Home Assistant version meets the minimum requirement (2023.0.0).
2. Verify that the Messes Info website is accessible from your network.
3. Check the Home Assistant logs for error messages related to the `hacs-aelf-api-client` integration.

## Contributing

Contributions are welcome! If you would like to contribute to this project, please open an issue or submit a pull request on the [GitHub repository](https://github.com/thamin-i/hacs-aelf-api-client).

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Markdown cards examples

_Replace the sensor ID in the examples by your own sensor ID_

Use the below markdown to display the daily complines in your dashboard:
``` markdown
{% set compline = state_attr('sensor.complines_for_france_updated_every_1_0_hours', 'compline') %}

## Introduction
<details>
<summary>Introduction</summary>
{{ compline.introduction }}
</details>

## Hymne
<details>
<summary>Hymne</summary>
{{ compline.hymne.texte }}
</details>

## Psaume {{ compline.psaume_1.reference }}
<details>
<summary>Psaume {{ compline.psaume_1.reference }}</summary>
Antiene: {{ compline.antienne_1 }}
{{ compline.psaume_1.texte }}
</details>

## Psaume {{ compline.psaume_2.reference }}
<details>
<summary>Psaume {{ compline.psaume_2.reference }}</summary>
{{ compline.psaume_2.texte }}
Antiene: {{ compline.antienne_1 }}
</details>

## Parole de Dieu
<details>
<summary>Parole de Dieu</summary>
{{ compline.pericope.texte }}
{{ compline.repons }}
</details>

## Cantique de Syméon
<details>
<summary>Cantique de Syméon</summary>
Antiene: {{ compline.antienne_symeon }}
{{ compline.cantique_symeon.texte }}
Antiene: {{ compline.antienne_symeon }}
</details>

## Oraison et bénédiction
<details>
<summary>Oraison et bénédiction</summary>
{{compline.oraison}}
{{compline.benediction}}
</details>

## {{compline.hymne_mariale.titre}}
<details>
<summary>{{compline.hymne_mariale.titre}}</summary>
{{compline.hymne_mariale.texte}}
</details>
```

Use the below markdown to display the daily masses in your dashboard:
``` markdown
{% for mass in state_attr('sensor.mass_for_france_updated_every_1_0_hours', 'mass') %}

## {{ mass.nom }}

{% for lecture in mass.lectures %}

---

### {{ lecture.type.replace("_", " ") }}

<details>
{% if lecture.titre is not none %}
<summary><i>{{ lecture.titre }}</i></summary>
{% else %}
<summary>Psaume</summary>
{% endif %}

{{ lecture.contenu }}
</details>

{% endfor %}

---
---

{% endfor %}
```
