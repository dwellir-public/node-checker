from argparse import ArgumentParser
from configparser import ConfigParser
import socket
from pdpyras import APISession

def report_incident(node, config):
  api_token = config['PagerDuty'].get('api-token')
  from_email = config['PagerDuty'].get('from-email')
  session = APISession(api_token, default_from=from_email)

  payload = {
    "incident": {
      "type": "incident",
      "title": "Node {} is offline!".format(node),
      "service": {
        "id": config['PagerDuty'].get('service-id'),
        "type": "service_reference"
      },
      "body": {
        "type": "incident_body",
        "details": "Node {} is offline!".format(node)
      }
    }
  }
  session.rpost("incidents", json=payload)

def check_nodes(config):
  for node in config.items('Nodes'):
    name = node[0]
    ip = node[1].split(':')[0]
    port = node[1].split(':')[1]
    node_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    node_socket.settimeout(30)
    endpoint = (ip, int(port))
    try:
      node_socket.connect(endpoint)
      print("SUCCESS connecting to endpoint {} {}".format(name, endpoint))
    except:
      print("FAILED connecting to endpoint {} {}".format(name, endpoint))
      report_incident(node, config)

def main():
  args_parser = ArgumentParser(prog='node-checker')
  args_parser.add_argument("-c", "--config", required=True, help="read config from a file")
  args = args_parser.parse_args()
  config = ConfigParser()
  try:
    config.read_file(open(args.config))
  except Exception as exc:
      print(f"Unable to read config: {str(exc)}")
      exit(0)

  check_nodes(config)


if __name__ == "__main__":
  main()
