/*
Title: DHCP Socket Overflow
Description: DHCP Socket Overflow
Sort: 2
*/

Every new container running will create a new *Virtual Network Interface* and each interface will request DHCPD service.
As we are running a lot of containers and they don't need to get anything from DHCP, we can simply exclude the virtual container interfaces from dhcpcd.

```bash
sudo vi /etc/dhcpcd.conf

# Insert the following line at the end:
denyinterfaces veth*
```