import json
import markdown
import os
from datetime import datetime

def create_html_report(json_path, output_path):
    # Read JSON file
    with open(json_path, 'r') as f:
        analysis_data = json.load(f)
    
    # Create a simple project description
    project_description = """
    <div class="project-description">
        <h2>About Claude Long Analysis Platform</h2>
        <p>
            This platform enables extended AI analysis sessions using Claude, featuring:
        </p>
        <ul>
            <li>Long-running analysis capabilities with iterative thinking</li>
            <li>Real-time progress tracking and session management</li>
            <li>Dynamic system prompts for steering analysis direction</li>
            <li>Built with FastAPI backend and React frontend</li>
            <li>Automatic rate limiting and persistent storage</li>
        </ul>
    </div>
    """
    
    # Create HTML content
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Claude Long Analysis Report</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body {{ padding: 2rem; }}
            .analysis-section {{ margin-bottom: 2rem; }}
            .iteration {{ 
                background-color: #f8f9fa;
                padding: 1rem;
                margin-bottom: 1rem;
                border-radius: 0.25rem;
            }}
            .timestamp {{
                color: #6c757d;
                font-size: 0.875rem;
            }}
            pre {{ 
                background-color: #f8f9fa;
                padding: 1rem;
                border-radius: 0.25rem;
            }}
            .readme-section {{
                margin-top: 3rem;
                padding-top: 2rem;
                border-top: 1px solid #dee2e6;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1 class="mb-4">Claude Long Analysis Report</h1>
            
            <div class="analysis-section">
                <h2>Analysis Details</h2>
                <p><strong>Session ID:</strong> {analysis_data['session_id']}</p>
                <p><strong>Start Time:</strong> {datetime.fromisoformat(analysis_data['start_time']).strftime('%Y-%m-%d %H:%M:%S')}</p>
                <p><strong>Status:</strong> {analysis_data['status']}</p>
                <p><strong>Task:</strong> {analysis_data['task']}</p>
                
                <h3 class="mt-4">Analysis Iterations</h3>
                {generate_iterations_html(analysis_data['iterations'])}
            </div>

            <div class="readme-section">
                {project_description}
            </div>
        </div>
        
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    </body>
    </html>
    """
    
    # Write HTML file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

def generate_iterations_html(iterations):
    html = ""
    for iteration in iterations:
        timestamp = datetime.fromisoformat(iteration['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
        html += f"""
        <div class="iteration">
            <div class="timestamp mb-2">{timestamp}</div>
            <div class="content">
                {markdown.markdown(iteration['content'])}
            </div>
        </div>
        """
    return html

if __name__ == "__main__":
    # Paths to your files
    json_path = "/mnt/d/dl/claude_long/analysis_sessions/20241101_192023.json"
    output_path = "analysis_report.html"
    
    create_html_report(json_path, output_path)
    print(f"Report generated successfully at: {output_path}")