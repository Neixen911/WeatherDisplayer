#!/usr/bin/bash

function daemon {
	/usr/bin/python3 /home/mi/Documents/GitHub/WeatherDisplayer/data.py
}

function start {
	daemon &
	PID=$(pgrep -f data.py)
	echo $PID > /var/run/weather-daemon.pid
}

function stop {
	kill $(cat /var/run/weather-daemon.pid)
}

function restart {
	stop
	start
}

case "$1" in

	"start")
		echo "Start the weather daemon."
		start
		;;

	"stop")
		echo "Stop the waether daemon."
		stop
		;;

	"restart")
		echo "Restart the weather daemon."
		restart
		;;

	"*")
		echo "This is not an valid argument"
		;;
esac
