# node-checker - A Dwellir node monitoring tool

Tries to upen a socket connection to IP:port. If it fails, reports to [PagerDuty](https://www.pagerduty.com/).

## About 

Dwellir is a polkadot staking operation and this software is used to help monitoring our validators.

Stake your polkadot with us! https://dwellir.com

## Setup
```
virtualenv env
source env/bin/activate
pip install -r requirements.txt
pip install .
```

## Usage
`node-checker -c example.conf`  
This makes only one check per node and exits. Run this on schedule using e.g. cron or systemd.

Instructions for config file:
```
[PagerDuty]
api-token=Api token created with you PagerDuty account.
from-email=PagerDuty requires an email when creating incidents.
service-id=ID of the service created on PagerDuty.

[Nodes]
node1=IP:port
node2=IP:port
```

## Contributing

- Fork the project and clone locally.
- Create a new branch for what you're going to work on.
- Push to your origin repository.
- Create a new pull request in GitHub.
