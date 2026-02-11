#!/bin/bash

set -e

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

print_success() {
    echo -e "${GREEN}[ok]${NC} $1"
}

print_error() {
    echo -e "${RED}[warning]${NC} $1"
}

print_info() {
    echo -e "${YELLOW}[info]${NC} $1"
}

check_python() {
    if command -v python3 &> /dev/null; then
        print_success "Python 3 found: $(python3 --version)"
        return 0
    elif command -v python &> /dev/null; then
        version=$(python --version 2>&1)
        if [[ $version == *"Python 3"* ]]; then
            print_success "Python found: $version"
            return 0
        fi
    fi
    
    print_error "Python 3 is not installed or not in PATH"
    exit 1
}

main() {
    check_python

    case "${1:-}" in
        "start")
            print_info "Starting system monitor..."
            python3 system-monitor.py
            ;;
        "help")
            echo ""
            echo "Usage: $0 {start|help}"
            echo ""
            echo "Commands:"
            echo "  start     Start monitoring"
            echo "  help    Show help"
            ;;
        *)
            print_error "Unknown command: $1"
            echo ""
            echo "Usage: $0 {start|help}"
            echo ""
            echo "Commands:"
            echo "  start   Start monitoring"
            echo "  help    Show help"
            exit 1
            ;;
    esac
}

main "$@"
