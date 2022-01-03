from argparse import ArgumentParser
from configparser import ConfigParser
import socket
import asyncio
import websockets
from pdpyras import APISession
import time

def report_incident(node, config):
  api_token = config['PagerDuty'].get('api-token')
  if not api_token:
    print("WARNING: no PagerDuty api token set!", flush=True)
    return
  from_email = config['PagerDuty'].get('from-email')
  if not from_email:
    print("WARNING: no PagerDuty email set!", flush=True)
    return
  service_id = config['PagerDuty'].get('service-id')
  if not service_id:
    print("WARNING: no PagerDuty service id set!", flush=True)
    return
  session = APISession(api_token, default_from=from_email)

  payload = {
    "incident": {
      "type": "incident",
      "title": "Node {} is offline!".format(node),
      "service": {
        "id": service_id,
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
      print("SUCCESS connecting to endpoint {} {}".format(name, endpoint), flush=True)
    except Exception as e:
      print("FAILED connecting to endpoint {} {}".format(name, endpoint), flush=True)
      print(e, flush=True)
      report_incident(node, config)

def check_websocket_nodes(config):
  async def test_connection():
    await asyncio.wait_for(websockets.connect('wss://' + node[1]), timeout=3)
  for node in config.items('WebsocketNodes'):
    # RPC node sometimes fails to open a websocket connection with log message:
    # "Unable to build WebSocket connection WS Error <Capacity>: Unable to add another connection to the event loop"
    # Assuming this is normal for a websocket service, retry a few times before reporting.
    max_tries = 5
    for current_try in range(max_tries):
      try:
        asyncio.get_event_loop().run_until_complete(test_connection())
        print("SUCCESS connecting to endpoint {} ({})".format(node[0], node[1]), flush=True)
        break
      except Exception:
        print("FAILED connecting to endpoint {} ({})".format(node[0], node[1]), flush=True)
        if current_try == max_tries-1:
          report_incident(node, config)
        else:
          time.sleep(5)

def main():
  args_parser = ArgumentParser(prog='node-checker')
  args_parser.add_argument("-c", "--config", required=True, help="read config from a file")
  args = args_parser.parse_args()
  config = ConfigParser()
  try:
    config.read_file(open(args.config))
  except Exception as exc:
      print(f"Unable to read config: {str(exc)}", flush=True)
      exit(0)

  check_nodes(config)
  check_websocket_nodes(config)

if __name__ == "__main__":
  main()
