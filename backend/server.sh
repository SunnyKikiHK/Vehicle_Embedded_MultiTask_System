#!/bin/bash


# rm -rf redis-7.0.0
# wget http://download.redis.io/releases/redis-7.0.0.tar.gz
# tar -xzvf redis-7.0.0.tar.gz
# rm -rf redis-7.0.0.tar.gz
# cd redis-7.0.0
# make -j 10
# cd ..

# sudo apt update
# sudo apt install -y build-essential pkg-config

# touch src/logs/redis.log
nohup redis-7.0.0/src/redis-server > src/logs/redis.log 2>&1 &
echo "启动redis数据库.."
sleep 5s

################################################
# nav_server (port 8001)
nohup python src/mcp/server/nav_server.py > src/logs/nav.log 2>&1 &
echo "start nav server.."
sleep 5

# # vehicle_server (port 8002)
# nohup python vehicle_server.py > src/logs/vehicle.log 2>&1 &
# echo "start vehicle server.."
# sleep 5

# # ac_server (port 8003)
# nohup python ac_server.py > src/logs/ac.log 2>&1 &
# echo "start ac server.."
# sleep 5

# # media_server (port 8004)
# nohup python media_server.py > src/logs/media.log 2>&1 &
# echo "start media server.."
# sleep 5

# # phone_server (port 8005)
# nohup python phone_server.py > src/logs/phone.log 2>&1 &
# echo "start phone server.."
# sleep 5

# # calendar_server (port 8006)
# nohup python calendar_server.py > src/logs/calendar.log 2>&1 &
# echo "start calendar server.."
# sleep 5

# # weather_server (port 8007)
# nohup python weather_server.py > src/logs/weather.log 2>&1 &
# echo "start weather server.."
# sleep 5

# # interior_server (port 8008)
# nohup python interior_server.py > src/logs/interior.log 2>&1 &
# echo "start interior server.."
# sleep 5

# # hud_server (port 8009)
# nohup python hud_server.py > src/logs/hud.log 2>&1 &
# echo "start hud server.."
# sleep 5

# # system_server (port 8010)
# nohup python system_server.py > src/logs/system.log 2>&1 &
# echo "start system server.."
# sleep 5

# # wireless_server (port 8011)
# nohup python wireless_server.py > src/logs/wireless.log 2>&1 &
# echo "start wireless server.."
# sleep 5

# # camera_server (port 8012)
# nohup python camera_server.py > src/logs/camera.log 2>&1 &
# echo "start camera server.."
# sleep 5

# # interaction_server (port 8013)
# nohup python interaction_server.py > src/logs/interaction.log 2>&1 &
# echo "start interaction server.."
# sleep 5

# # app_server (port 8014)
# nohup python app_server.py > src/logs/app.log 2>&1 &
# echo "start app server.."
# sleep 5

# echo "All MCP servers started!"
