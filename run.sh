#!/bin/bash
# ============================================================
#  Packet Drop Simulator - Run Script (POX Controller)
#  Author: VIJAY SURIYA P (PES1UG24AM320)
# ============================================================
# Usage:
#   chmod +x run.sh
#   ./run.sh setup       # First time only - install POX
#   ./run.sh controller  # Terminal 1 - start POX controller
#   ./run.sh topology    # Terminal 2 - start Mininet
#   ./run.sh flowtable   # Check installed flow rules
#   ./run.sh clean       # Cleanup
# ============================================================

ACTION="${1:-help}"

case "$ACTION" in

  setup)
    echo "======================================"
    echo "  Setting up POX Controller"
    echo "======================================"
    # Install POX if not present
    if [ ! -d ~/pox ]; then
      git clone https://github.com/noxrepo/pox.git ~/pox
      echo "POX cloned to ~/pox"
    else
      echo "POX already installed at ~/pox"
    fi
    # Copy controller to POX ext folder
    cp packet_drop_controller.py ~/pox/ext/
    echo "Controller copied to ~/pox/ext/"
    echo ""
    echo "Setup complete! Now run:"
    echo "  Terminal 1: ./run.sh controller"
    echo "  Terminal 2: ./run.sh topology"
    ;;

  controller)
    echo "======================================"
    echo "  Starting POX Controller"
    echo "======================================"
    echo "Keep this terminal open."
    echo "Run './run.sh topology' in a NEW terminal."
    echo ""
    # Copy latest controller to POX ext
    cp packet_drop_controller.py ~/pox/ext/ 2>/dev/null
    python3 ~/pox/pox.py packet_drop_controller
    ;;

  topology)
    echo "======================================"
    echo "  Starting Mininet Topology"
    echo "======================================"
    sudo mn \
      --custom topology.py \
      --topo droptopo \
      --controller remote,ip=127.0.0.1,port=6633 \
      --switch ovsk \
      --mac
    ;;

  flowtable)
    echo "======================================"
    echo "  Flow Table - Switch s1"
    echo "======================================"
    sudo ovs-ofctl dump-flows s1
    ;;

  clean)
    echo "Cleaning up Mininet..."
    sudo mn -c
    echo "Done."
    ;;

  help|*)
    echo ""
    echo "  Packet Drop Simulator (POX)"
    echo "  Author: VIJAY SURIYA P (PES1UG24AM320)"
    echo ""
    echo "  FIRST TIME:"
    echo "    ./run.sh setup"
    echo ""
    echo "  EVERY TIME:"
    echo "    Terminal 1: ./run.sh controller"
    echo "    Terminal 2: ./run.sh topology"
    echo ""
    echo "  IN MININET CLI:"
    echo "    h1 ping -c 4 h2    <- should SUCCEED"
    echo "    h1 ping -c 4 h3    <- should FAIL (drop rule)"
    echo "    pingall"
    echo ""
    echo "  OTHER:"
    echo "    ./run.sh flowtable  Check flow rules"
    echo "    ./run.sh clean      Cleanup"
    echo ""
    ;;
esac
