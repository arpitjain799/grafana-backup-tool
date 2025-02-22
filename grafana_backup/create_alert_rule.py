import json
from grafana_backup.dashboardApi import create_alert_rule, get_grafana_version
from packaging import version


def main(args, settings, file_path):
    grafana_url = settings.get('GRAFANA_URL')
    http_post_headers = settings.get('HTTP_POST_HEADERS')
    http_post_headers['x-disable-provenance']='*'
    verify_ssl = settings.get('VERIFY_SSL')
    client_cert = settings.get('CLIENT_CERT')
    debug = settings.get('DEBUG')

    with open(file_path, 'r') as f:
        data = f.read()

    grafana_version = get_grafana_version(grafana_url, verify_ssl)
    minimum_version = version.parse('9.4.0')

    if minimum_version <= grafana_version:
        alert_rule = json.loads(data)
        result = create_alert_rule(json.dumps(alert_rule), grafana_url, http_post_headers, verify_ssl, client_cert, debug)
        print("create alert rule: {0}, status: {1}, msg: {2}".format(alert_rule['title'], result[0], result[1]))
    else:
        print("Unable to create alert rules, requires Grafana version {0} or above. Current version is {1}".format(minimum_version, grafana_version))
