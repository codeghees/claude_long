# Claude Long-Running Analysis Platform

A platform for conducting extended, iterative analysis tasks using Claude AI, with support for self-steering system prompts and persistent session management.

## Features

- 🤖 Long-running Claude AI analysis sessions
- 🔄 Iterative thinking with configurable iterations
- 🎯 Dynamic system prompt updates during analysis
- ⏱️ Rate limit protection with 10s timeouts
- 📊 Real-time progress tracking
- 💾 Persistent session storage
- 📝 Markdown-formatted responses
- 🔍 Detailed analysis history

## Architecture

- Backend: FastAPI + Claude API
- Frontend: React with real-time updates
- Storage: File-based session persistence
- Rate Limiting: 10-second intervals between API calls

## Prerequisites

- Python 3.8+
- Node.js 14+
- Anthropic API key
- npm or yarn

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/claude-long.git
   cd claude-long
   ```

2. Create and activate virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   cd frontend
   npm install
   ```

4. Set up environment variables:
   Create a `.env` file in the root directory with:
   ```
   ANTHROPIC_API_KEY=your_api_key_here
   ```

## Usage

1. Start the backend server:
   ```bash
   uvicorn main:app --reload --port 8000
   ```

2. Start the frontend development server:
   ```bash
   cd frontend
   npm start
   ```

3. Access the application at `http://localhost:3000`

## Usage

1. **Starting an Analysis**
   - Enter your analysis task in the main textarea
   - Optionally provide an initial system prompt
   - Click "Start Analysis" to begin

2. **Monitoring Progress**
   - View real-time updates of the analysis
   - Each iteration is timestamped and preserved
   - Track Claude's thought process and conclusions

3. **Steering the Analysis**
   - Update the system prompt at any time
   - Each prompt update is recorded in the session history
   - Use the "Process Next Iteration" button to trigger new analysis steps

4. **Session Management**
   - Sessions are automatically saved
   - Access historical sessions using their ID
   - All interactions are preserved for review

## API Endpoints

- `POST /start_analysis`
  - Start a new analysis session
  - Parameters: task, system_prompt (optional), iteration_count (optional)

- `GET /analysis_status/{session_id}`
  - Get current status and history of an analysis session

- `POST /update_system_prompt`
  - Update the system prompt for ongoing analysis
  - Parameters: session_id, new_prompt

- `POST /process_iteration/{session_id}`
  - Trigger the next iteration of analysis

## Best Practices

1. **Rate Limiting**
   - Respect the 10-second timeout between iterations
   - Monitor API usage and adjust timeouts if needed

2. **System Prompts**
   - Start with general prompts and let Claude specialize
   - Use prompt updates to guide analysis direction
   - Document prompt changes in session history

3. **Session Management**
   - Keep session IDs for important analyses
   - Review iteration history for insights
   - Export sessions for documentation

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License - See LICENSE file for details

## Support

For issues and feature requests, please use the GitHub issue tracker.

## Project Structure
claude_long/
├── main.py # FastAPI backend
├── requirements.txt # Python dependencies
├── analysis_sessions/ # Session storage
├── search/ # Analysis modules
│ └── analyzer.py # Claude integration
└── frontend/ # React frontend
├── src/
│ ├── App.js # Main application
│ └── ...
└── package.json