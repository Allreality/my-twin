"""
Service Integration Layer for Agent Coordination - Fixed Version
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import time
from datetime import datetime
import logging

from agent_coordinator import AgentCoordinator

class AgentServiceIntegration:
    def __init__(self, port: int = 5006):
        self.port = port
        self.app = Flask(__name__)
        CORS(self.app)
        self.coordinator = AgentCoordinator(port=port)
        
        # Setup Flask logging
        logging.basicConfig(level=logging.INFO)
        self.app.logger.setLevel(logging.INFO)
        
        self._setup_routes()
        
    def _setup_routes(self):
        """Setup all API routes"""
        
        @self.app.route('/', methods=['GET'])
        def home():
            return jsonify({
                "service": "Total Reality Ecosystem - Agent Coordination API",
                "version": "1.0",
                "status": "running",
                "endpoints": {
                    "health": "/health",
                    "status": "/status",
                    "agents": "/agents",
                    "tasks": "/tasks",
                    "koya_strategy": "/strategy/koya",
                    "digital_twin": "/digital-twin/chat"
                }
            })
        
        @self.app.route('/health', methods=['GET'])
        def health_check():
            return jsonify({
                "status": "healthy",
                "timestamp": datetime.now().isoformat(),
                "coordinator": "running" if self.coordinator.running else "stopped",
                "agents": len(self.coordinator.agents),
                "tasks": {
                    "pending": len(self.coordinator.task_queue),
                    "total": len(self.coordinator.tasks)
                },
                "port": self.port
            })
        
        @self.app.route('/status', methods=['GET'])
        def get_status():
            """Get comprehensive system status"""
            status = self.coordinator.get_system_status()
            status['api_version'] = '1.0'
            status['endpoints_available'] = 6
            return jsonify(status)
        
        @self.app.route('/agents', methods=['GET'])
        def list_agents():
            """List all registered agents"""
            agents_data = []
            for agent_id, agent_info in self.coordinator.agents.items():
                agents_data.append({
                    "id": agent_info.id,
                    "name": agent_info.name,
                    "description": agent_info.description,
                    "status": agent_info.status.value,
                    "last_heartbeat": agent_info.last_heartbeat.isoformat()
                })
            return jsonify({
                "agents": agents_data,
                "total_count": len(agents_data)
            })
        
        @self.app.route('/tasks', methods=['GET'])
        def list_tasks():
            """List all tasks"""
            tasks_data = []
            for task in self.coordinator.tasks.values():
                tasks_data.append({
                    "id": task.id,
                    "agent_id": task.agent_id,
                    "task_type": task.task_type,
                    "priority": task.priority.name,
                    "status": task.status,
                    "created_at": task.created_at.isoformat() if task.created_at else None,
                    "payload_summary": {k: str(v)[:100] for k, v in task.payload.items()}
                })
            return jsonify({
                "tasks": tasks_data,
                "total_count": len(tasks_data),
                "pending_count": len(self.coordinator.task_queue)
            })
        
        @self.app.route('/strategy/koya', methods=['POST', 'GET'])
        def koya_strategy():
            """Handle Koya strategy requests"""
            if request.method == 'POST':
                # Execute the strategy
                try:
                    strategy_id = self.coordinator.execute_koya_strategy()
                    
                    return jsonify({
                        "success": True,
                        "strategy_id": strategy_id,
                        "status": "initiated",
                        "description": "Koya initiative 90-day strategy launched",
                        "tasks_created": len(self.coordinator.task_queue),
                        "timestamp": datetime.now().isoformat()
                    })
                except Exception as e:
                    return jsonify({
                        "success": False,
                        "error": str(e),
                        "timestamp": datetime.now().isoformat()
                    }), 500
            
            elif request.method == 'GET':
                # Return strategy information
                return jsonify({
                    "strategy": "Koya Initiative 90-Day Plan",
                    "description": "Automated business process execution for NIH SBIR grant pursuit",
                    "components": [
                        "Grant application automation (NIH SBIR)",
                        "Customer acquisition (Healthcare/Research)",
                        "Compliance monitoring (NIST SP 800-171)",
                        "Patent research and filing"
                    ],
                    "deadline": "2025-01-31",
                    "status": "ready"
                })
        
        @self.app.route('/digital-twin/chat', methods=['POST'])
        def chat_with_twin():
            """Chat with the digital twin through the API"""
            try:
                from complete_system import MyTwin
                twin = MyTwin()
                
                data = request.json
                if not data or 'message' not in data:
                    return jsonify({"error": "Missing 'message' in request body"}), 400
                
                message = data.get('message', '')
                response = twin.chat(message)
                
                return jsonify({
                    "success": True,
                    "response": response,
                    "message": message,
                    "timestamp": datetime.now().isoformat()
                })
                
            except Exception as e:
                return jsonify({
                    "success": False,
                    "error": str(e),
                    "timestamp": datetime.now().isoformat()
                }), 500
        
        # Error handlers
        @self.app.errorhandler(404)
        def not_found(error):
            return jsonify({
                "error": "Not Found",
                "message": "The requested endpoint was not found",
                "available_endpoints": ["/health", "/status", "/agents", "/tasks", "/strategy/koya", "/digital-twin/chat"]
            }), 404
        
        @self.app.errorhandler(405)
        def method_not_allowed(error):
            return jsonify({
                "error": "Method Not Allowed",
                "message": "This endpoint does not support the requested HTTP method"
            }), 405
    
    def start(self):
        """Start the service integration layer"""
        self.coordinator.start()
        
        print(f"🚀 Agent Coordination Service starting on port {self.port}")
        print("=" * 60)
        print("TOTAL REALITY ECOSYSTEM - AGENT COORDINATION API")
        print("=" * 60)
        print(f"REST API: http://localhost:{self.port}")
        print(f"Health Check: http://localhost:{self.port}/health")
        print(f"System Status: http://localhost:{self.port}/status")
        print(f"Execute Koya Strategy: POST http://localhost:{self.port}/strategy/koya")
        print("=" * 60)
        
        # Start Flask with better error handling
        self.app.run(host='0.0.0.0', port=self.port, debug=True, threaded=True)
    
    def stop(self):
        """Stop the service integration layer"""
        self.coordinator.stop()
