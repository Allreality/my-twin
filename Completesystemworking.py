"""
Digital Twin System with Koya Initiative Integration
"""

import json
import os

# Import Koya initiative knowledge
from koya_initiative_knowledge import KOYA_INITIATIVE_KNOWLEDGE, search_koya_knowledge

class MyTwin:
    """Digital Twin System with integrated Koya initiative knowledge"""
    
    def __init__(self):
        """Initialize the digital twin system"""
        self.name = "Akil's Digital Twin"
        self.knowledge_base = {
            "koya_initiative": KOYA_INITIATIVE_KNOWLEDGE,
            "personal_info": {
                "role": "Systems Analyst at Total Reality Global",
                "experience": "20+ years cybersecurity experience",
                "background": "Navy electronics training, former federal security clearance",
                "github": "Allreality"
            }
        }
        
    def chat(self, message):
        """Process a chat message and return a response"""
        message_lower = message.lower()
        
        if "koya" in message_lower:
            return self._handle_koya_query(message)
        elif any(term in message_lower for term in ["compliance", "nist", "800-171"]):
            return self._handle_compliance_query(message)
        elif any(term in message_lower for term in ["grant", "nih", "sbir", "funding"]):
            return self._handle_business_query(message)
        else:
            return self._handle_general_query(message)
    
    def _handle_koya_query(self, message):
        """Handle queries about the Koya initiative"""
        koya_info = self.knowledge_base["koya_initiative"]
        
        response = "## Koya Initiative Overview\n\n"
        response += f"**Description:** {koya_info['overview']['description']}\n\n"
        response += f"**Purpose:** {koya_info['overview']['purpose']}\n\n"
        
        response += "**Key Technical Components:**\n"
        for component in koya_info['technical_architecture']['core_components']:
            response += f"• {component}\n"
        
        response += "\n**Current Business Strategy:**\n"
        response += "• Targeting NIH SBIR program (January 2025 mandate)\n"
        response += "• 90-day plan for pilot customers and grant applications\n"
        response += "• Developing provisional patent for hardware-enforced compliance architecture\n"
        
        return response
    
    def _handle_compliance_query(self, message):
        """Handle compliance-related queries"""
        compliance_info = self.knowledge_base["koya_initiative"]["regulatory_compliance"]
        
        response = "## Compliance Architecture Details\n\n"
        response += "**Supported Frameworks:**\n"
        for framework in compliance_info["frameworks"]:
            response += f"• {framework}\n"
        
        response += "\n**Verification Methods:**\n"
        for method in compliance_info["verification_methods"]:
            response += f"• {method}\n"
        
        return response
    
    def _handle_business_query(self, message):
        """Handle business and grant-related queries"""
        business_info = self.knowledge_base["koya_initiative"]["business_strategy"]
        
        response = "## Business Strategy & Grant Opportunities\n\n"
        grant_info = business_info["grant_opportunities"][0]
        response += f"**Primary Target: {grant_info['program']}**\n"
        response += f"• Deadline: {grant_info['deadline']}\n"
        response += f"• Requirement: {grant_info['requirement']}\n"
        
        return response
    
    def _handle_general_query(self, message):
        """Handle general queries"""
        personal_info = self.knowledge_base["personal_info"]
        
        response = f"## {self.name} Information\n\n"
        response += f"**Role:** {personal_info['role']}\n"
        response += f"**Experience:** {personal_info['experience']}\n"
        response += f"**Background:** {personal_info['background']}\n"
        response += f"**GitHub:** {personal_info['github']}\n"
        
        response += "\nAsk me about the Koya initiative, compliance, or grants!"
        return response
    
    def search_knowledge(self, search_term):
        """Search through the knowledge base"""
        return search_koya_knowledge(search_term)
    
    def get_status(self):
        """Get the current status of the digital twin"""
        return {
            "name": self.name,
            "status": "Active",
            "knowledge_domains": list(self.knowledge_base.keys()),
            "primary_focus": "Koya Initiative Development",
            "last_updated": "November 2025"
        }