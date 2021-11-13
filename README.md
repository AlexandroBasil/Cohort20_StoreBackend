# Backend for online store

## Alexandro Garcia

## Help:

### Start DB Service (WSL):
```
sudo service mongodb status
sudo service mongodb start
sudo service mongodb stop
```
### Delete all your orders

mongo
use onlinestore
db.order.remove({})
