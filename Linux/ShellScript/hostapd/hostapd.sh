#!/bin/sh
start() {
    /usr/sbin/rfkill unblock all
    /usr/sbin/service  network-manager stop
    sysctl net.ipv4.conf.all.forwarding=1     
    hostapd -B /etc/hostapd/hostapd.conf 
    /sbin/ip addr add 192.168.122.1/24 dev wlan0 
    /usr/sbin/service dnsmasq restart
    echo 1 > /proc/sys/net/ipv4/ip_forward 
    iptables -F
    iptables -X
    iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
}
stop() { 
    /sbin/iptables -t nat -D POSTROUTING -o eth0 -j MASQUERADE 
    /usr/sbin/service dnsmasq stop 
    /usr/bin/pkill hostapd 
    /sbin/ip link set down dev wlan0
    /usr/sbin/service  network-manager start
}
case "$1" in
'start') 
  start 
  ;;
'stop') 
  stop 
  ;;
*) 
echo "usage $0 start|stop"
esac
