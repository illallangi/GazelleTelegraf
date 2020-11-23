from typing import Dict

from click import STRING, command, option

from illallangi.orpheusapi import API as ORP_API, ENDPOINTDEF as ORP_ENDPOINTDEF

from telegraf_pyplug.main import print_influxdb_format

METRICNAMEDEF = 'gazelle'


@command()
@option('--metric-name',
        type=STRING,
        required=False,
        default=METRICNAMEDEF)
@option('--orpheus-api-key',
        envvar='ORPHEUS_API_KEY',
        type=STRING)
@option('--redacted-api-key',
        type=STRING)
@option('--orpheus-endpoint',
        type=STRING,
        required=False,
        default=ORP_ENDPOINTDEF)
def cli(
        metric_name,
        orpheus_api_key,
        orpheus_endpoint,
        redacted_api_key):

    if (orpheus_api_key):
        orp_api = ORP_API(orpheus_api_key, orpheus_endpoint, success_expiry=600)
        orp_index = orp_api.get_index()

        tags: Dict[str, str] = {
            'id': orp_index.id,
            'username': orp_index.username,
            'class': orp_index.userstats.userclass,
            'tracker': 'ORP'
        }

        fields: Dict[str, int] = {
            'uploaded': int(orp_index.userstats.uploaded),
            'downloaded': int(orp_index.userstats.downloaded),
            'ratio': orp_index.userstats.ratio,
            'requiredratio': orp_index.userstats.requiredratio,
            'bonuspoints': orp_index.userstats.bonuspoints,
            'bonuspointsperhour': orp_index.userstats.bonuspointsperhour
        }

        print_influxdb_format(
            measurement=metric_name,
            tags=tags,
            fields=fields,
            add_timestamp=True
        )


if __name__ == "__main__":
    cli()
