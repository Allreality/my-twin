# 🤖 my-twin: AI Digital Twin System

A sophisticated digital twin implementation featuring advanced memory systems, contextual personality modeling, and multi-domain knowledge integration. Built for creating AI agents that maintain consistent personality, emotional awareness, and context across interactions.

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-active-success.svg)]()

## 📋 Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Architecture](#architecture)
- [System Components](#system-components)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Usage Examples](#usage-examples)
- [Memory Systems](#memory-systems)
- [Personality System](#personality-system)
- [Integrations](#integrations)
- [Development](#development)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)

## 🌟 Overview

**my-twin** is an advanced AI digital twin system that creates persistent, context-aware AI agents with:

- **Multi-layered Memory Architecture**: Emotional, semantic, and working memory systems
- **Dynamic Personality Modeling**: Customizable personality traits that influence responses
- **Context Awareness**: Maintains conversation history and situational understanding
- **Domain Knowledge Integration**: Specialized knowledge bases (e.g., BlackArt Gallery)
- **Blockchain Integration**: x402 agent wallet system for autonomous operations
- **Extensible Architecture**: Modular design for easy feature addition

### What is a Digital Twin?

A digital twin is a virtual representation that maintains state, personality, and knowledge across interactions. Unlike stateless chatbots, my-twin:

- Remembers past conversations and emotional context
- Develops consistent personality traits over time
- Integrates domain-specific expertise
- Maintains working memory for active tasks
- Stores semantic knowledge for long-term understanding

## 🚀 Key Features

### Memory Systems
- **Emotional State Management**: Tracks and responds to emotional context
- **Semantic Memory**: Long-term knowledge storage and retrieval
- **Working Memory**: Short-term context for active conversations

### Personality Engine
- Customizable personality traits and characteristics
- Context-aware response modulation
- Consistent behavior patterns across interactions

### Knowledge Integration
- BlackArt VIP Gallery knowledge base integration
- Extensible knowledge domains
- Dynamic knowledge retrieval and application

### Advanced Capabilities
- Context-aware response generation
- Multi-domain expertise
- Blockchain wallet integration (x402)
- Autonomous agent capabilities

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Digital Twin Core                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  Emotional   │  │   Semantic   │  │   Working    │     │
│  │    State     │  │    Memory    │  │    Memory    │     │
│  │   System     │  │   Storage    │  │   Context    │     │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘     │
│         │                  │                  │             │
│         └──────────┬───────┴──────────────────┘             │
│                    │                                        │
│         ┌──────────▼──────────┐                            │
│         │   Personality       │                            │
│         │   Engine            │                            │
│         │   - Base Traits     │                            │
│         │   - Custom Mods     │                            │
│         └──────────┬──────────┘                            │
│                    │                                        │
│         ┌──────────▼──────────┐                            │
│         │   Context Aware     │                            │
│         │   Twin Architecture │                            │
│         │   - State Mgmt      │                            │
│         │   - Response Gen    │                            │
│         └──────────┬──────────┘                            │
│                    │                                        │
└────────────────────┼────────────────────────────────────────┘
                     │
         ┌───────────┼───────────┐
         │           │           │
    ┌────▼────┐ ┌───▼────┐ ┌───▼────┐
    │ Knowledge│ │  x402  │ │External│
    │   Bases  │ │ Wallet │ │  APIs  │
    │(BlackArt)│ │ System │ │        │
    └──────────┘ └────────┘ └────────┘
```

## 🧩 System Components

### Core Modules

#### 1. Memory Systems

**Emotional State (`emotional_state.py`)**
- Tracks emotional context across interactions
- Influences response tone and content
- Maintains emotional history

**Semantic Memory (`semantic_memory.py`)**
- Long-term knowledge storage
- Fact retrieval and integration
- Domain expertise management

**Working Memory (`working_memory.py`)**
- Short-term context management
- Active conversation state
- Task-specific information retention

#### 2. Personality System

**Personality Engine (`personality.py`)**
- Base personality trait definitions
- Response style modulation
- Behavioral consistency enforcement

**Custom Personality (`personality_custom.py`)**
- User-defined personality modifications
- Specialized behavior patterns
- Domain-specific personality traits

**Personality Profile (`my_PERSONALITY.txt`)**
- Natural language personality description
- Trait definitions and values
- Behavioral guidelines

#### 3. Architecture Components

**Digital Twin Architecture (`digital_twin_architecture.py`)**
- Core digital twin implementation
- State management
- Component integration

**Context-Aware Implementation (`context_aware_twin_architecture.py`)**
- Advanced context handling
- Multi-turn conversation management
- Situational awareness

**Complete System (`complete_system.py`)**
- Unified system integration
- End-to-end functionality
- Production-ready implementation

#### 4. Knowledge Integration

**BlackArt Gallery Knowledge (`blackart_gallery_knowledge.py`)**
- Specialized art gallery domain knowledge
- Artist and artwork information
- Gallery operations expertise

#### 5. Blockchain Integration

**x402 Agent Wallets (`x402_agent_wallets.py`)**
- Autonomous agent wallet management
- Blockchain transaction capabilities
- Payment processing for AI operations

## 📦 Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Virtual environment (recommended)

### Setup

1. **Clone the repository**
```bash
git clone https://github.com/Allreality/my-twin.git
cd my-twin
```

2. **Create virtual environment**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment**
```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your configuration
nano .env  # or your preferred editor
```

5. **Run setup verification**
```bash
python verify_setup.py
```

6. **Quick setup script** (alternative)
```bash
chmod +x quick_setup.sh
./quick_setup.sh
```

## 🎯 Quick Start

### Basic Usage

```python
from digital_twin_architecture import DigitalTwin

# Initialize the digital twin
twin = DigitalTwin(
    personality_file="my_PERSONALITY.txt",
    enable_memory=True
)

# Interact with your twin
response = twin.process_input("Hello, how are you?")
print(response)

# Access memory systems
emotional_context = twin.emotional_state.get_current_state()
print(f"Current emotional state: {emotional_context}")
```

### With Context Awareness

```python
from context_aware_twin_architecture import ContextAwareTwin

# Initialize with full context awareness
twin = ContextAwareTwin(
    personality_profile="my_PERSONALITY.txt",
    knowledge_bases=["blackart_gallery_knowledge"]
)

# Multi-turn conversation with context
twin.start_conversation()
response1 = twin.chat("Tell me about the gallery")
response2 = twin.chat("What's special about the featured artists?")
# Context from previous turns is maintained
```

### Testing

```bash
# Run basic twin tests
python test_basic_twin.py

# Test Claude integration
python test_claude_basic.py
```

## 📁 Project Structure

```
my-twin/
├── README.md                              # This file
├── requirements.txt                       # Python dependencies
├── .env.example                           # Environment template
├── quick_setup.sh                         # Setup automation
│
├── Core Architecture
│   ├── digital_twin_architecture.py       # Core twin implementation
│   ├── context_aware_twin_architecture.py # Context-aware features
│   └── complete_system.py                 # Integrated system
│
├── Memory Systems
│   ├── emotional_state.py                 # Emotional tracking
│   ├── semantic_memory.py                 # Long-term knowledge
│   └── working_memory.py                  # Short-term context
│
├── Personality
│   ├── personality.py                     # Base personality engine
│   ├── personality_custom.py              # Custom modifications
│   └── my_PERSONALITY.txt                 # Personality profile
│
├── Knowledge & Integration
│   ├── blackart_gallery_knowledge.py      # Domain knowledge
│   └── x402_agent_wallets.py              # Blockchain integration
│
├── Testing & Verification
│   ├── test_basic_twin.py                 # Basic tests
│   ├── test_claude_basic.py               # Claude integration tests
│   └── verify_setup.py                    # Setup verification
│
└── Documentation
    ├── ARCHITECTURE_DIAGRAMS.txt          # Architecture details
    ├── CONTEXT_AWARE_IMPLEMENTATION.md    # Context system docs
    ├── DIGITAL_TWIN_COMPARISON.md         # Design comparisons
    └── QUICK_REFERENCE.md                 # Quick command reference
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file with the following:

```bash
# API Keys
ANTHROPIC_API_KEY=your_claude_api_key_here
OPENAI_API_KEY=your_openai_key_here  # If using OpenAI

# Twin Configuration
TWIN_NAME=MyTwin
TWIN_PERSONALITY=my_PERSONALITY.txt
ENABLE_MEMORY=true
ENABLE_EMOTIONAL_STATE=true

# Memory Settings
SEMANTIC_MEMORY_LIMIT=1000
WORKING_MEMORY_LIMIT=50
EMOTIONAL_STATE_DECAY=0.95

# Knowledge Bases
ENABLE_BLACKART_KNOWLEDGE=true

# Blockchain (x402)
X402_WALLET_ENABLED=false
X402_NETWORK=testnet
```

### Personality Configuration

Edit `my_PERSONALITY.txt` to customize your twin's personality:

```text
Name: [Your Twin's Name]
Core Traits:
- Trait 1: [Description]
- Trait 2: [Description]
- Trait 3: [Description]

Communication Style:
[Describe how the twin should communicate]

Knowledge Domains:
[List areas of expertise]

Behavioral Guidelines:
[Specific behavioral instructions]
```

## 💡 Usage Examples

### Example 1: Emotional Context

```python
from emotional_state import EmotionalState

# Initialize emotional tracking
emotions = EmotionalState()

# Process emotional input
emotions.update("I'm feeling excited about this project!")
current_mood = emotions.get_mood()
print(f"Current mood: {current_mood}")  # Output: positive, excited

# Emotional influence on responses
response_tone = emotions.get_response_tone()
# Use tone to modulate twin's response
```

### Example 2: Semantic Memory

```python
from semantic_memory import SemanticMemory

# Initialize long-term memory
memory = SemanticMemory()

# Store knowledge
memory.store("The BlackArt Gallery features 8 artworks by Audley 'Cisco' Hutson")
memory.store("The gallery specializes in contemporary African American art")

# Retrieve relevant knowledge
info = memory.retrieve("Tell me about the gallery")
print(info)
```

### Example 3: Complete System

```python
from complete_system import MyTwin

# Initialize complete system
twin = MyTwin()

# Start a conversation session
twin.start_session()

# Multi-turn conversation with full capabilities
response1 = twin.chat("Hello!")
response2 = twin.chat("What can you tell me about art?")
response3 = twin.chat("How do you remember our conversations?")

# System maintains:
# - Emotional context
# - Conversation history
# - Personality consistency
# - Domain knowledge

twin.end_session()
```

### Example 4: BlackArt Gallery Integration

```python
from blackart_gallery_knowledge import BlackArtKnowledge

# Initialize gallery knowledge
gallery = BlackArtKnowledge()

# Query gallery information
artist_info = gallery.get_artist_info("Audley 'Cisco' Hutson")
artwork_list = gallery.get_artworks()
gallery_details = gallery.get_gallery_info()

print(f"Featured Artist: {artist_info}")
print(f"Total Artworks: {len(artwork_list)}")
```

## 🧠 Memory Systems

### Emotional State System

The emotional state system tracks and responds to emotional context:

**Features:**
- Emotion detection from user input
- Emotional state tracking over time
- Mood influence on responses
- Emotional decay (emotions fade naturally)

**States Tracked:**
- Joy, sadness, anger, fear, surprise, disgust
- Intensity levels (0.0 to 1.0)
- Temporal decay
- Context-based activation

### Semantic Memory

Long-term knowledge storage and retrieval:

**Capabilities:**
- Fact storage with timestamps
- Knowledge categorization
- Relevance-based retrieval
- Knowledge integration

**Use Cases:**
- Domain expertise storage
- Historical context
- User preferences
- Learned information

### Working Memory

Short-term context management:

**Functions:**
- Conversation history
- Active task tracking
- Context window management
- Information prioritization

**Limits:**
- Configurable context window
- Automatic pruning of old context
- Priority-based retention

## 👤 Personality System

### Base Personality

Defined in `personality.py`, includes:
- Core trait definitions
- Response style patterns
- Behavioral guidelines
- Communication preferences

### Custom Modifications

`personality_custom.py` allows for:
- User-specific trait adjustments
- Domain-specific behaviors
- Specialized response patterns
- Override mechanisms

### Personality Profile

`my_PERSONALITY.txt` provides:
- Natural language personality description
- Trait values and intensities
- Behavioral examples
- Communication guidelines

## 🔗 Integrations

### BlackArt VIP Gallery

**Purpose:** Specialized knowledge domain for art gallery operations

**Features:**
- Artist information (Audley "Cisco" Hutson)
- Artwork catalog (8 featured pieces)
- Gallery operations knowledge
- Art domain expertise

**Website:** [blackart.vip](https://blackart.vip)

### x402 Agent Wallets

**Purpose:** Blockchain integration for autonomous AI agents

**Capabilities:**
- Wallet management
- Transaction processing
- Payment handling
- Autonomous operations

**Use Cases:**
- AI agent payments
- Autonomous trading
- Service monetization
- Blockchain interactions

## 🛠️ Development

### Running Tests

```bash
# Basic functionality tests
python test_basic_twin.py

# Claude integration tests
python test_claude_basic.py

# Verify complete setup
python verify_setup.py
```

### Adding New Features

1. **New Knowledge Domain:**
```python
# Create new knowledge module
# knowledge/my_domain.py

class MyDomainKnowledge:
    def __init__(self):
        self.knowledge_base = {}
    
    def load_knowledge(self):
        # Load domain-specific knowledge
        pass
```

2. **Custom Memory Type:**
```python
# Extend memory system
from semantic_memory import SemanticMemory

class CustomMemory(SemanticMemory):
    def __init__(self):
        super().__init__()
        # Add custom functionality
```

3. **Personality Trait:**
```python
# Add to personality_custom.py
def add_custom_trait(trait_name, trait_value):
    # Implement new personality trait
    pass
```

### Code Style

- Follow PEP 8 guidelines
- Use type hints where appropriate
- Document functions with docstrings
- Keep modules focused and cohesive

## 🗺️ Roadmap

### Current Version: 1.0
- ✅ Core digital twin architecture
- ✅ Multi-layered memory systems
- ✅ Personality engine
- ✅ BlackArt gallery integration
- ✅ x402 wallet integration

### Planned Features: 1.1
- 🔄 Enhanced emotional intelligence
- 🔄 Multi-modal input support (images, audio)
- 🔄 Advanced context windowing
- 🔄 Performance optimization

### Future: 2.0
- 📋 Multi-agent collaboration
- 📋 Unreal Engine 5 integration
- 📋 InfluxDB metrics integration
- 📋 Real-time learning capabilities
- 📋 Voice interaction support

## 👥 Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/my-twin.git
cd my-twin

# Add upstream remote
git remote add upstream https://github.com/Allreality/my-twin.git

# Create development branch
git checkout -b dev

# Install dev dependencies
pip install -r requirements-dev.txt
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with Claude AI assistance
- Inspired by digital twin research and cognitive architectures
- BlackArt VIP Gallery collaboration
- Community feedback and contributions

## 📞 Contact & Support

- **GitHub Issues:** [Report bugs or request features](https://github.com/Allreality/my-twin/issues)
- **Discussions:** [Community discussions](https://github.com/Allreality/my-twin/discussions)
- **Author:** Allreality
- **Project Link:** [https://github.com/Allreality/my-twin](https://github.com/Allreality/my-twin)

## 🔖 Related Projects

- [Total Reality Ecosystem](https://github.com/Allreality) - Blockchain integration platform
- [Claude-Proof](https://github.com/Allreality/claude-proof) - Project protection system

---

**Made with 🤖 by Allreality | Digital Twin Technology**

*Creating AI that remembers, learns, and grows*
