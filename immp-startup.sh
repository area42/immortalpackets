#!/bin/bash
# PMSO fw initializer
#
# pmso-fw:   Pedro Oliveira FW builder
#
# chkconfig: 345 03 03
# description:  This is a daemon for managing firewall scripts \
#               config file should be located in \
#               /etc/sysconfig/iptables
#
# notes:        please set rc.status according to your OS / Distro
# processname: pmso-fw
# pidfile: /var/run/pmso-fw.pid
#

. /etc/rc.status
rc_reset

SERVICE="pmso-fw"
IPT4="/usr/sbin/iptables"
PROCESS_APPLY="/usr/sbin/iptables-apply"
CONFIG_FILE="/etc/sysconfig/iptables"
LIST_RULES="/usr/sbin/iptables-save"
PIDFILE="/var/run/pmso-fw.pid"

test -f $CONFIG_FILE

start() {
  stop
  sleep 3650d &
  echo $! > $PIDFILE
  echo -n $"Starting $SERVICE "
  `$PROCESS_RESTORE < $CONFIG_FILE`
  RETVAL=$?
  rc_status -v
}

stop() {
  echo -n $"Stopping $SERVICE "
  $IPT4 -F && \
  $IPT4 -X && \
  $IPT4 -t nat -F && \
  $IPT4 -t nat -X && \
  $IPT4 -t mangle -F && \
  $IPT4 -t mangle -X && \
  $IPT4 -P INPUT ACCEPT && \
  $IPT4 -P FORWARD ACCEPT && \
  $IPT4 -P OUTPUT ACCEPT
  RETVAL=$?
  rc_status -v
}

restart() {
  stop
  start
}

stat() {
  $LIST_RULES
  RETVAL=$?
  rc_status -v
}

# See how we were called.
case "$1" in
  start|stop|restart)
    $1
  ;;
  status)
    echo -n "Checking status of $SERVICE "
    rc_status -v
  ;;
  *)
    echo $"Usage: $0 {start|stop|status|restart}"
    rc_failed 2
    rc_exit
  ;;
esac
rc_exit
