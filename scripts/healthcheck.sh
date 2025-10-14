#!/bin/bash
################################################################################
# MIRAI Health Check Script
# 
# Production-grade health check for MIRAI AI Agent
# 
# Version: 2.0.0
# Codename: Evolution
#
# Usage:
#   ./healthcheck.sh              # Human-readable output
#   ./healthcheck.sh --json       # JSON output for monitoring
#   ./healthcheck.sh --quiet      # Only exit code (0=healthy, 1=unhealthy)
#   ./healthcheck.sh --verbose    # Detailed output
#
# Exit codes:
#   0 - All checks passed (healthy)
#   1 - One or more checks failed (unhealthy)
#   2 - Script error
#
# Integration:
#   - Systemd: ExecStartPre=/path/to/healthcheck.sh
#   - Monitoring: Nagios, Datadog, etc.
#   - CI/CD: Pre-deployment check
################################################################################

set -e  # Exit on error (except in checks)

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
MIRAI_DIR="${PROJECT_ROOT}/mirai-agent"
PYTHON_CMD="python3"
OUTPUT_FORMAT="human"  # human, json, quiet
VERBOSE=0

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --json)
            OUTPUT_FORMAT="json"
            shift
            ;;
        --quiet)
            OUTPUT_FORMAT="quiet"
            shift
            ;;
        --verbose)
            VERBOSE=1
            shift
            ;;
        --help|-h)
            echo "Usage: $0 [--json|--quiet|--verbose|--help]"
            echo ""
            echo "Options:"
            echo "  --json     Output in JSON format"
            echo "  --quiet    Only return exit code"
            echo "  --verbose  Detailed output"
            echo "  --help     Show this help"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            echo "Use --help for usage information"
            exit 2
            ;;
    esac
done

# Check results storage
declare -a CHECKS
TOTAL_CHECKS=0
PASSED_CHECKS=0
FAILED_CHECKS=0

################################################################################
# Helper Functions
################################################################################

log_verbose() {
    if [[ $VERBOSE -eq 1 ]] && [[ "$OUTPUT_FORMAT" != "json" ]] && [[ "$OUTPUT_FORMAT" != "quiet" ]]; then
        echo -e "${BLUE}[VERBOSE]${NC} $1"
    fi
}

log_info() {
    if [[ "$OUTPUT_FORMAT" == "human" ]]; then
        echo -e "$1"
    fi
}

add_check() {
    local name="$1"
    local status="$2"  # "pass" or "fail"
    local message="$3"
    
    TOTAL_CHECKS=$((TOTAL_CHECKS + 1))
    
    if [[ "$status" == "pass" ]]; then
        PASSED_CHECKS=$((PASSED_CHECKS + 1))
    else
        FAILED_CHECKS=$((FAILED_CHECKS + 1))
    fi
    
    CHECKS+=("{\"name\":\"$name\",\"status\":\"$status\",\"message\":\"$message\"}")
}

print_check() {
    local name="$1"
    local status="$2"
    local message="$3"
    
    if [[ "$OUTPUT_FORMAT" == "human" ]]; then
        if [[ "$status" == "pass" ]]; then
            printf "  ${GREEN}✅${NC} %-25s %s\n" "$name" "$message"
        else
            printf "  ${RED}❌${NC} %-25s %s\n" "$name" "$message"
        fi
    fi
}

################################################################################
# Health Checks
################################################################################

check_python_version() {
    log_verbose "Checking Python version..."
    
    local required_major=3
    local required_minor=10
    
    if command -v $PYTHON_CMD &> /dev/null; then
        local version=$($PYTHON_CMD --version 2>&1 | awk '{print $2}')
        local major=$(echo $version | cut -d. -f1)
        local minor=$(echo $version | cut -d. -f2)
        
        if [[ $major -ge $required_major ]] && [[ $minor -ge $required_minor ]]; then
            add_check "Python" "pass" "$version"
            print_check "Python" "pass" "$version"
            return 0
        else
            add_check "Python" "fail" "Version $version < ${required_major}.${required_minor}"
            print_check "Python" "fail" "Version $version < ${required_major}.${required_minor}"
            return 1
        fi
    else
        add_check "Python" "fail" "Not found"
        print_check "Python" "fail" "Not found"
        return 1
    fi
}

check_mirai_installation() {
    log_verbose "Checking MIRAI installation..."
    
    if [[ -d "$MIRAI_DIR" ]]; then
        if [[ -f "$MIRAI_DIR/core/autonomous_agent.py" ]]; then
            add_check "MIRAI Installation" "pass" "Found at $MIRAI_DIR"
            print_check "MIRAI Installation" "pass" "Found"
            return 0
        else
            add_check "MIRAI Installation" "fail" "Core files missing"
            print_check "MIRAI Installation" "fail" "Core files missing"
            return 1
        fi
    else
        add_check "MIRAI Installation" "fail" "Directory not found: $MIRAI_DIR"
        print_check "MIRAI Installation" "fail" "Not found"
        return 1
    fi
}

check_api_key() {
    log_verbose "Checking OpenAI API key..."
    
    if [[ -n "$OPENAI_API_KEY" ]]; then
        local masked_key="${OPENAI_API_KEY:0:10}...${OPENAI_API_KEY: -4}"
        add_check "API Key" "pass" "Set (env): $masked_key"
        print_check "API Key" "pass" "Set (env)"
        return 0
    else
        # Check config file as fallback
        local config_file="$MIRAI_DIR/configs/api_keys.json"
        if [[ -f "$config_file" ]]; then
            if grep -q "openai_api_key" "$config_file" 2>/dev/null; then
                add_check "API Key" "pass" "Set (config)"
                print_check "API Key" "pass" "Set (config)"
                return 0
            fi
        fi
        
        add_check "API Key" "fail" "Not found (env or config)"
        print_check "API Key" "fail" "Not found"
        return 1
    fi
}

check_config_file() {
    log_verbose "Checking configuration file..."
    
    local config_file="$PROJECT_ROOT/configs/mirai.yaml"
    
    if [[ -f "$config_file" ]]; then
        # Try to parse YAML (basic check)
        if grep -q "version:" "$config_file" 2>/dev/null; then
            local version=$(grep "^version:" "$config_file" | awk '{print $2}' | tr -d '"')
            add_check "Config" "pass" "v$version"
            print_check "Config" "pass" "v$version"
            return 0
        else
            add_check "Config" "fail" "Invalid format"
            print_check "Config" "fail" "Invalid format"
            return 1
        fi
    else
        add_check "Config" "fail" "Not found: $config_file"
        print_check "Config" "fail" "Not found"
        return 1
    fi
}

check_memory_database() {
    log_verbose "Checking memory database..."
    
    # Try to get DB path from config
    local db_path="$MIRAI_DIR/data/mirai_memory.db"
    
    # Check if parent directory exists
    local db_dir=$(dirname "$db_path")
    if [[ ! -d "$db_dir" ]]; then
        add_check "Memory DB" "fail" "Data directory not found"
        print_check "Memory DB" "fail" "Not initialized"
        return 1
    fi
    
    # Check if DB exists
    if [[ -f "$db_path" ]]; then
        local db_size=$(du -h "$db_path" | awk '{print $1}')
        add_check "Memory DB" "pass" "Initialized ($db_size)"
        print_check "Memory DB" "pass" "Initialized ($db_size)"
        return 0
    else
        # DB doesn't exist yet - this is OK for first run
        add_check "Memory DB" "pass" "Ready (not yet used)"
        print_check "Memory DB" "pass" "Ready"
        return 0
    fi
}

check_logger() {
    log_verbose "Checking logger configuration..."
    
    # Check if log directory is writable
    local log_dir="/tmp"
    
    if [[ -w "$log_dir" ]]; then
        # Try to create a test log file
        local test_log="$log_dir/mirai_healthcheck_test.log"
        if touch "$test_log" 2>/dev/null; then
            rm -f "$test_log"
            add_check "Logger" "pass" "Writable ($log_dir)"
            print_check "Logger" "pass" "Ready"
            return 0
        else
            add_check "Logger" "fail" "Cannot write to $log_dir"
            print_check "Logger" "fail" "Not writable"
            return 1
        fi
    else
        add_check "Logger" "fail" "Directory not writable: $log_dir"
        print_check "Logger" "fail" "Not writable"
        return 1
    fi
}

check_core_modules() {
    log_verbose "Checking core Python modules..."
    
    cd "$MIRAI_DIR"
    
    local test_script='
import sys
try:
    from core.autonomous_agent import AutonomousAgent
    from core.config_loader import get_config
    from core.memory_manager import MemoryManager
    from core.logger import MiraiLogger
    print("OK")
    sys.exit(0)
except ImportError as e:
    print(f"FAIL: {e}")
    sys.exit(1)
'
    
    local result=$($PYTHON_CMD -c "$test_script" 2>&1)
    local exit_code=$?
    
    if [[ $exit_code -eq 0 ]]; then
        add_check "Core Modules" "pass" "All importable"
        print_check "Core Modules" "pass" "All importable"
        return 0
    else
        add_check "Core Modules" "fail" "$result"
        print_check "Core Modules" "fail" "Import error"
        return 1
    fi
}

check_dependencies() {
    log_verbose "Checking Python dependencies..."
    
    cd "$MIRAI_DIR"
    
    # Check if venv exists
    if [[ -d "venv" ]]; then
        local venv_python="venv/bin/python3"
        if [[ -f "$venv_python" ]]; then
            # Check key dependencies
            local deps=("openai" "pyyaml")
            local missing_deps=()
            
            for dep in "${deps[@]}"; do
                if ! $venv_python -c "import $dep" 2>/dev/null; then
                    missing_deps+=("$dep")
                fi
            done
            
            if [[ ${#missing_deps[@]} -eq 0 ]]; then
                add_check "Dependencies" "pass" "All installed"
                print_check "Dependencies" "pass" "All installed"
                return 0
            else
                add_check "Dependencies" "fail" "Missing: ${missing_deps[*]}"
                print_check "Dependencies" "fail" "Missing: ${missing_deps[*]}"
                return 1
            fi
        fi
    fi
    
    # No venv, check system-wide
    local deps=("openai" "yaml")
    local missing_deps=()
    
    for dep in "${deps[@]}"; do
        if ! $PYTHON_CMD -c "import $dep" 2>/dev/null; then
            missing_deps+=("$dep")
        fi
    done
    
    if [[ ${#missing_deps[@]} -eq 0 ]]; then
        add_check "Dependencies" "pass" "All installed (system)"
        print_check "Dependencies" "pass" "All installed"
        return 0
    else
        add_check "Dependencies" "fail" "Missing: ${missing_deps[*]}"
        print_check "Dependencies" "fail" "Missing packages"
        return 1
    fi
}

check_disk_space() {
    log_verbose "Checking disk space..."
    
    local data_dir="$MIRAI_DIR/data"
    local available=$(df -h "$data_dir" 2>/dev/null | awk 'NR==2 {print $4}')
    local usage=$(df -h "$data_dir" 2>/dev/null | awk 'NR==2 {print $5}' | tr -d '%')
    
    if [[ -n "$usage" ]]; then
        if [[ $usage -lt 90 ]]; then
            add_check "Disk Space" "pass" "$available available (${usage}% used)"
            print_check "Disk Space" "pass" "$available available"
            return 0
        else
            add_check "Disk Space" "fail" "Low space: ${usage}% used"
            print_check "Disk Space" "fail" "Low space (${usage}%)"
            return 1
        fi
    else
        add_check "Disk Space" "fail" "Cannot check"
        print_check "Disk Space" "fail" "Cannot check"
        return 1
    fi
}

################################################################################
# Main Execution
################################################################################

main() {
    # Print header (if not quiet/json)
    if [[ "$OUTPUT_FORMAT" == "human" ]]; then
        echo ""
        echo "╔══════════════════════════════════════════════════════════════════════╗"
        echo "║  MIRAI Health Check                                                 ║"
        echo "╚══════════════════════════════════════════════════════════════════════╝"
        echo ""
    fi
    
    # Run all checks
    check_python_version || true
    check_mirai_installation || true
    check_api_key || true
    check_config_file || true
    check_memory_database || true
    check_logger || true
    check_core_modules || true
    check_dependencies || true
    check_disk_space || true
    
    # Determine overall health
    local overall_status="healthy"
    if [[ $FAILED_CHECKS -gt 0 ]]; then
        overall_status="unhealthy"
    fi
    
    # Output results
    if [[ "$OUTPUT_FORMAT" == "json" ]]; then
        # JSON output
        local checks_json=$(printf '%s,' "${CHECKS[@]}" | sed 's/,$//')
        echo "{"
        echo "  \"status\": \"$overall_status\","
        echo "  \"timestamp\": \"$(date -Iseconds)\","
        echo "  \"total_checks\": $TOTAL_CHECKS,"
        echo "  \"passed_checks\": $PASSED_CHECKS,"
        echo "  \"failed_checks\": $FAILED_CHECKS,"
        echo "  \"checks\": [$checks_json]"
        echo "}"
    elif [[ "$OUTPUT_FORMAT" == "human" ]]; then
        # Human-readable summary
        echo ""
        echo "──────────────────────────────────────────────────────────────────────"
        echo "Summary: $PASSED_CHECKS/$TOTAL_CHECKS checks passed"
        echo ""
        
        if [[ "$overall_status" == "healthy" ]]; then
            echo -e "${GREEN}🎉 All systems operational!${NC}"
        else
            echo -e "${RED}⚠️  Some components need attention${NC}"
            echo -e "${YELLOW}Run with --verbose for details${NC}"
        fi
        echo ""
    fi
    
    # Return appropriate exit code
    if [[ "$overall_status" == "healthy" ]]; then
        exit 0
    else
        exit 1
    fi
}

# Run main function
main "$@"
