#!/bin/bash

# System Resource Monitor
# Demonstrates monitoring and logging system resources

# Function to display CPU and memory usage
view_cpu_memory() {
    echo "==================== CPU & Memory Usage ===================="
    top -b -n 1 | head -n 10
    echo "==========================================================="
}

# Function to display disk usage
view_disk_usage() {
    echo "==================== Disk Usage ============================"
    df -h
    echo "==========================================================="
}

# Function to display running processes
view_running_processes() {
    echo "==================== Active Processes ======================"
    ps aux --sort=-%mem | head -n 10
    echo "==========================================================="
}

# Function to save report to a file
generate_report() {
    output_file="sys_report_$(date +'%Y%m%d_%H%M%S').txt"
    echo "Generating system report..."
    {
        echo "==================== CPU & Memory Usage ====================";
        top -b -n 1 | head -n 10;
        echo "";
        echo "==================== Disk Usage ============================";
        df -h;
        echo "";
        echo "==================== Active Processes ======================";
        ps aux --sort=-%mem | head -n 10;
    } > "$output_file"
    echo "Report saved as $output_file"
}

# Main menu
while true; do
    echo ""
    echo "--------------- System Resource Monitor ----------------"
    echo "1. View CPU and Memory Usage"
    echo "2. View Disk Usage"
    echo "3. View Top Active Processes"
    echo "4. Generate System Report"
    echo "5. Exit"
    echo "--------------------------------------------------------"
    read -p "Enter your choice (1-5): " choice
    case $choice in
        1) view_cpu_memory ;;
        2) view_disk_usage ;;
        3) view_running_processes ;;
        4) generate_report ;;
        5) echo "Exiting the System Resource Monitor. Have a nice day!"; exit 0 ;;
        *) echo "Invalid choice. Please select between 1-5." ;;
    esac
done