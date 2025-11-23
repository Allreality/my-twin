#!/bin/bash

# Backup script for Agent Coordination System
DATE=$(date +"%Y%m%d_%H%M%S")
BACKUP_DIR="twin_backup_${DATE}"

echo "🔄 Creating backup: $BACKUP_DIR"

mkdir -p "$BACKUP_DIR"

# Copy core system files
cp koya_initiative_knowledge.py "$BACKUP_DIR/"
cp complete_system.py "$BACKUP_DIR/"
cp agent_coordinator.py "$BACKUP_DIR/"
cp service_integration.py "$BACKUP_DIR/"
cp startup_agents.py "$BACKUP_DIR/"
cp AGENT_SYSTEM_README.md "$BACKUP_DIR/"

# Copy existing twin files
cp test_basic_twin.py "$BACKUP_DIR/" 2>/dev/null
cp .env "$BACKUP_DIR/" 2>/dev/null

echo "✅ Backup created: $BACKUP_DIR"
echo "📁 Files backed up:"
ls -la "$BACKUP_DIR/"

echo ""
echo "🎯 Your complete Koya Initiative automation system is preserved!"
