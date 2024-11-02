# Claude Long-Running Analysis Platform

A powerful platform for conducting sophisticated, long-running analysis tasks using Claude AI, featuring dynamic system prompts and persistent session tracking.

## Key Features

- 🧠 Advanced iterative analysis powered by Claude AI
- 🔄 Configurable analysis iterations with fine-grained control
- 🎯 Dynamic system prompts that evolve during analysis
- ⚡️ Smart rate limiting with 10s cooldowns
- 📊 Real-time progress monitoring
- 💾 Automatic session persistence
- 📝 Rich Markdown output
- 🔍 Comprehensive analysis history

## Technical Stack

- **Backend**: FastAPI for high-performance async API
- **AI Engine**: Claude API integration
- **Frontend**: React with real-time updates
- **Storage**: File-based session management
- **Rate Limiting**: 10-second interval throttling

## Getting Started

### Prerequisites

- Python 3.8+
- Node.js 14+
- Anthropic API key
- npm or yarn

### Setup

1. Clone repository:
   ```bash
   git clone https://github.com/yourusername/claude-long.git
   cd claude-long
   ```

2. Set up environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Install frontend:
   ```bash
   cd frontend
   npm install
   ```

4. Configure `.env`:
   ```
   ANTHROPIC_API_KEY=your_api_key_here
   ```

### Launch

1. Backend:
   ```bash
   uvicorn main:app --reload --port 8000
   ```

2. Frontend:
   ```bash
   cd frontend
   npm start
   ```

Access at `http://localhost:3000`

## Usage

### Analysis Workflow

1. **Start**
   - Define objective
   - Set initial prompts (optional)
   - Launch analysis

2. **Monitor**
   - Track real-time progress
   - Review iteration logs
   - Follow reasoning process

3. **Control**
   - Adjust system prompts
   - Track prompt evolution
   - Manage iterations

4. **Sessions**
   - Automatic persistence
   - Retrieve by ID
   - Complete history

## API Reference

- `POST /start_analysis`
  - Start new session
  - Parameters: task, system_prompt, iteration_count

- `GET /analysis_status/{session_id}`
  - Get session status and history

- `POST /update_system_prompt`
  - Update active prompt
  - Parameters: session_id, new_prompt

- `POST /process_iteration/{session_id}`
  - Trigger next iteration

## Best Practices

- Respect 10-second cooldowns
- Start with broad prompts
- Document prompt changes
- Save important session IDs
- Export for documentation

## Development

### Contributing

1. Fork repository
2. Create feature branch
3. Submit pull request

### License

MIT License - See LICENSE file

### Support

Use [GitHub Issue Tracker](https://github.com/yourusername/claude-long/issues)
