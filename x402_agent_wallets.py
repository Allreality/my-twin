"""
x402 Protocol Agent Wallet Configuration
=========================================
Multi-Agent Autonomous Payment System on Solana

Treasury: MidnightBotBank (master wallet)
Active Agents: Integration, Compliance, Developer, Digital Twin

All payments route through MidnightBotBank per x402 protocol
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
from datetime import datetime
from enum import Enum


# ============================================================================
# SOLANA WALLET ADDRESSES - PRODUCTION CONFIGURATION
# ============================================================================

class AgentWalletAddresses:
    """
    Production Solana wallet addresses for agent system
    All on Solana blockchain
    """
    
    # MASTER TREASURY - All payments route through here
    MIDNIGHT_BOT_BANK = "3Amc3tkRvijtrRtE6XVAkYd8UxF9VKqm7mqDdyT6FPWm"
    
    # ACTIVE AGENT WALLETS
    INTEGRATION_BOT = "7xbS8JuRLoVeQsb1Sp6Bc4ESShp6LEb2eoJtjohr65KK"
    COMPLIANCE_AI = "4ppPain22Fx54vXvE4Fvk7cYjx4emkfTHVAQpobc4pLv"
    DEVELOPER_AI = "FXL7intKqJPSvXorpNLePakfRbjqs3iJU18ftSZ9GVTr"
    
    # DIGITAL TWIN WALLET (to be added if separate)
    DIGITAL_TWIN = Fe6AiMpMPjqJ5rSpZ6ck4SmQitepuK1koGB64QtGWe7i
    
    @classmethod
    def get_all_agents(cls) -> Dict[str, str]:
        """Get all active agent wallets"""
        return {
            'integration_bot': cls.INTEGRATION_BOT,
            'compliance_ai': cls.COMPLIANCE_AI,
            'developer_ai': cls.DEVELOPER_AI,
        }
    
    @classmethod
    def get_treasury(cls) -> str:
        """Get treasury address"""
        return cls.MIDNIGHT_BOT_BANK


# ============================================================================
# AGENT ROLES & CAPABILITIES
# ============================================================================

class AgentRole(Enum):
    """Define what each agent is responsible for"""
    TREASURY = "treasury"              # MidnightBotBank - master treasury
    INTEGRATION = "integration"        # Integration bot - system integration
    COMPLIANCE = "compliance"          # ComplianceAI - regulatory compliance
    DEVELOPER = "developer"            # DeveloperAI - development operations
    DIGITAL_TWIN = "digital_twin"      # Digital Twin - gallery & consultation


@dataclass
class AgentConfig:
    """Configuration for each agent"""
    agent_id: str
    role: AgentRole
    wallet_address: str
    description: str
    capabilities: List[str]
    payment_permissions: Dict[str, float]  # What they can pay for and limits
    treasury_percentage: float = 0.1  # Default 10% to treasury


# ============================================================================
# AGENT CONFIGURATIONS
# ============================================================================

AGENT_CONFIGURATIONS = {
    'midnight_bot_bank': AgentConfig(
        agent_id='midnight_bot_bank',
        role=AgentRole.TREASURY,
        wallet_address=AgentWalletAddresses.MIDNIGHT_BOT_BANK,
        description='Master treasury for x402 protocol - all payments route through here',
        capabilities=[
            'receive_all_treasury_fees',
            'fund_agent_wallets',
            'approve_large_transactions',
            'maintain_system_reserves',
            'distribute_to_temne_abara_nation'
        ],
        payment_permissions={
            'any': float('inf')  # No limits on treasury
        },
        treasury_percentage=0.0  # Treasury doesn't pay itself
    ),
    
    'integration_bot': AgentConfig(
        agent_id='integration_bot',
        role=AgentRole.INTEGRATION,
        wallet_address=AgentWalletAddresses.INTEGRATION_BOT,
        description='Handles system integrations, API connections, service coordination',
        capabilities=[
            'pay_api_services',
            'purchase_integration_tools',
            'compensate_service_providers',
            'fund_infrastructure_costs',
            'handle_digital_twin_payments'  # Can serve as digital twin wallet
        ],
        payment_permissions={
            'api_services': 10.0,           # Max 10 SOL per API payment
            'integration_tools': 50.0,      # Max 50 SOL for tools
            'infrastructure': 25.0,         # Max 25 SOL for infrastructure
            'service_providers': 100.0,     # Max 100 SOL for providers
            'daily_limit': 200.0           # Total daily limit
        },
        treasury_percentage=0.1
    ),
    
    'compliance_ai': AgentConfig(
        agent_id='compliance_ai',
        role=AgentRole.COMPLIANCE,
        wallet_address=AgentWalletAddresses.COMPLIANCE_AI,
        description='Monitors compliance, validates transactions, ensures regulatory adherence',
        capabilities=[
            'pay_compliance_services',
            'purchase_audit_tools',
            'compensate_legal_advisors',
            'fund_regulatory_reporting',
            'validate_agent_transactions'
        ],
        payment_permissions={
            'compliance_services': 20.0,    # Max 20 SOL for compliance
            'audit_tools': 30.0,            # Max 30 SOL for auditing
            'legal_advisors': 50.0,         # Max 50 SOL for legal
            'regulatory': 15.0,             # Max 15 SOL for reporting
            'daily_limit': 100.0
        },
        treasury_percentage=0.1
    ),
    
    'developer_ai': AgentConfig(
        agent_id='developer_ai',
        role=AgentRole.DEVELOPER,
        wallet_address=AgentWalletAddresses.DEVELOPER_AI,
        description='Handles development operations, infrastructure, technical resources',
        capabilities=[
            'pay_cloud_services',
            'purchase_development_tools',
            'compensate_developers',
            'fund_infrastructure',
            'handle_technical_subscriptions'
        ],
        payment_permissions={
            'cloud_services': 50.0,         # Max 50 SOL for cloud
            'dev_tools': 30.0,              # Max 30 SOL for tools
            'developers': 100.0,            # Max 100 SOL for compensation
            'infrastructure': 75.0,         # Max 75 SOL for infra
            'subscriptions': 25.0,          # Max 25 SOL for subs
            'daily_limit': 250.0
        },
        treasury_percentage=0.1
    ),
}


# ============================================================================
# x402 PAYMENT ROUTING RULES
# ============================================================================

X402_ROUTING_RULES = {
    'treasury_address': AgentWalletAddresses.MIDNIGHT_BOT_BANK,
    'treasury_percentage': 0.1,  # 10% of all transactions
    'minimum_transaction': 0.001,  # Minimum 0.001 SOL
    'require_approval_above': 100.0,  # Transactions >100 SOL need approval
    
    'payment_flow': {
        'description': 'x402 protocol payment flow',
        'steps': [
            '1. Agent initiates payment',
            '2. Validate against agent permissions',
            '3. Check collective benefit score',
            '4. Route 10% to MidnightBotBank treasury',
            '5. Forward 90% to final recipient',
            '6. Log transaction to InfluxDB',
            '7. Update agent balance'
        ]
    },
    
    'collective_benefit_threshold': 0.5,  # Minimum score to approve
    
    'audit_requirements': {
        'log_to_influxdb': True,
        'include_fields': [
            'timestamp',
            'agent_id',
            'from_wallet',
            'to_wallet',
            'amount',
            'purpose',
            'treasury_fee',
            'benefit_score',
            'tx_hash',
            'status'
        ]
    }
}


# ============================================================================
# TEMNE ABARA NATION TREASURY INTEGRATION
# ============================================================================

TEMNE_ABARA_CONFIG = {
    'description': 'Temne Abara Nation - Ultimate beneficiary of treasury fees',
    'master_treasury': AgentWalletAddresses.MIDNIGHT_BOT_BANK,
    
    'distribution_schedule': {
        'frequency': 'monthly',  # Or weekly, daily as preferred
        'percentage_to_nation': 0.9,  # 90% of treasury goes to Temne Abara
        'percentage_retained': 0.1    # 10% kept for operational reserves
    },
    
    'use_cases': [
        'Community development',
        'Infrastructure investment',
        'Cultural preservation',
        'Economic empowerment',
        'Educational programs'
    ]
}


# ============================================================================
# USAGE EXAMPLES
# ============================================================================

def get_agent_config(agent_id: str) -> AgentConfig:
    """Get configuration for specific agent"""
    return AGENT_CONFIGURATIONS.get(agent_id)


def validate_payment(agent_id: str, purpose: str, amount: float) -> Dict:
    """
    Validate if agent can make this payment
    
    Returns:
        dict with 'valid' bool and 'reason' if invalid
    """
    config = get_agent_config(agent_id)
    
    if not config:
        return {'valid': False, 'reason': f'Agent {agent_id} not found'}
    
    # Check if agent has capability for this purpose
    purpose_category = classify_purpose(purpose)
    
    if purpose_category not in config.payment_permissions:
        return {
            'valid': False,
            'reason': f'Agent not authorized for {purpose_category}'
        }
    
    # Check amount limits
    max_allowed = config.payment_permissions[purpose_category]
    if amount > max_allowed:
        return {
            'valid': False,
            'reason': f'Amount {amount} exceeds limit {max_allowed} for {purpose_category}'
        }
    
    # Check daily limit
    daily_limit = config.payment_permissions.get('daily_limit', float('inf'))
    # TODO: Check actual daily spend from InfluxDB
    
    return {'valid': True, 'reason': 'Payment authorized'}


def classify_purpose(purpose: str) -> str:
    """
    Classify payment purpose into category
    Uses AI to determine category from description
    """
    purpose_lower = purpose.lower()
    
    # Simple keyword matching (in production, use Claude for classification)
    if any(word in purpose_lower for word in ['api', 'service', 'subscription']):
        return 'api_services'
    elif any(word in purpose_lower for word in ['cloud', 'infrastructure', 'server']):
        return 'infrastructure'
    elif any(word in purpose_lower for word in ['compliance', 'audit', 'legal']):
        return 'compliance_services'
    elif any(word in purpose_lower for word in ['developer', 'compensation', 'contractor']):
        return 'developers'
    else:
        return 'general'


def get_payment_routing(amount: float) -> Dict:
    """
    Calculate payment routing per x402 protocol
    
    Args:
        amount: Total payment amount in SOL
    
    Returns:
        dict with treasury_amount, recipient_amount, percentages
    """
    treasury_percentage = X402_ROUTING_RULES['treasury_percentage']
    
    treasury_amount = amount * treasury_percentage
    recipient_amount = amount * (1 - treasury_percentage)
    
    return {
        'total_amount': amount,
        'treasury_amount': treasury_amount,
        'recipient_amount': recipient_amount,
        'treasury_address': X402_ROUTING_RULES['treasury_address'],
        'treasury_percentage': treasury_percentage
    }


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    print("="*60)
    print("x402 PROTOCOL - AGENT WALLET CONFIGURATION")
    print("="*60)
    
    print("\nTREASURY:")
    print(f"  MidnightBotBank: {AgentWalletAddresses.MIDNIGHT_BOT_BANK}")
    
    print("\nACTIVE AGENTS:")
    for agent_id, config in AGENT_CONFIGURATIONS.items():
        if agent_id != 'midnight_bot_bank':
            print(f"\n  {config.agent_id.upper()}:")
            print(f"    Address: {config.wallet_address}")
            print(f"    Role: {config.role.value}")
            print(f"    Capabilities: {len(config.capabilities)}")
            print(f"    Treasury %: {config.treasury_percentage * 100}%")
    
    print("\n" + "="*60)
    print("PAYMENT ROUTING EXAMPLE")
    print("="*60)
    
    # Example payment
    payment_amount = 10.0  # 10 SOL
    routing = get_payment_routing(payment_amount)
    
    print(f"\nPayment: {routing['total_amount']} SOL")
    print(f"  To Treasury: {routing['treasury_amount']} SOL ({routing['treasury_percentage']*100}%)")
    print(f"  To Recipient: {routing['recipient_amount']} SOL ({(1-routing['treasury_percentage'])*100}%)")
    print(f"  Treasury Address: {routing['treasury_address']}")
    
    print("\n" + "="*60)
    print("VALIDATION EXAMPLE")
    print("="*60)
    
    # Example validation
    validation = validate_payment(
        agent_id='integration_bot',
        purpose='Purchase Claude API credits',
        amount=5.0
    )
    
    print(f"\nAgent: integration_bot")
    print(f"Purpose: Purchase Claude API credits")
    print(f"Amount: 5.0 SOL")
    print(f"Valid: {validation['valid']}")
    if not validation['valid']:
        print(f"Reason: {validation['reason']}")