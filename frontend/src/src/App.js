import React, { useState, useEffect } from 'react';
import axios from 'axios';

function App() {
  const [task, setTask] = useState('');
  const [sessionId, setSessionId] = useState(null);
  const [analysisData, setAnalysisData] = useState(null);
  const [isProcessing, setIsProcessing] = useState(false);

  const startAnalysis = async () => {
    try {
      const response = await axios.post('http://localhost:8000/start_analysis', {
        task
      });
      setSessionId(response.data.session_id);
    } catch (error) {
      console.error('Error starting analysis:', error);
    }
  };

  const processNextIteration = async () => {
    if (!sessionId || isProcessing) return;
    try {
      setIsProcessing(true);
      await axios.post(`http://localhost:8000/process_iteration/${sessionId}`);
    } catch (error) {
      console.error('Error processing iteration:', error);
      alert(`Error: ${error.response?.data?.detail || 'Failed to process iteration'}`);
    } finally {
      setIsProcessing(false);
    }
  };

  useEffect(() => {
    const fetchStatus = async () => {
      if (!sessionId) return;
      try {
        const response = await axios.get(`http://localhost:8000/analysis_status/${sessionId}`);
        setAnalysisData(response.data);
      } catch (error) {
        console.error('Error fetching status:', error);
      }
    };

    if (sessionId) {
      const interval = setInterval(fetchStatus, 5000);
      return () => clearInterval(interval);
    }
  }, [sessionId]);

  useEffect(() => {
    if (sessionId && !isProcessing) {
      const timeout = setTimeout(processNextIteration, 2000);
      return () => clearTimeout(timeout);
    }
  }, [sessionId, isProcessing, analysisData]);

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl mb-4">Claude Long-Running Analysis</h1>
      
      <div className="mb-4">
        <textarea
          className="w-full p-2 border rounded"
          value={task}
          onChange={(e) => setTask(e.target.value)}
          placeholder="Enter your analysis task..."
          rows={4}
        />
      </div>

      <div className="mb-4">
        <button
          className="bg-blue-500 text-white px-4 py-2 rounded mr-2"
          onClick={startAnalysis}
        >
          Start Analysis
        </button>
      </div>

      {analysisData && (
        <div className="mt-4">
          <h2 className="text-xl mb-2">Analysis Progress</h2>
          <div className="border rounded p-4">
            <p>Session ID: {analysisData.session_id}</p>
            <p>Status: {analysisData.status}</p>
            <div className="mt-4">
              <h3 className="text-lg mb-2">Iterations:</h3>
              {analysisData.iterations.map((iteration, index) => (
                <details key={index} className="mb-4 p-2 border rounded">
                  <summary className="cursor-pointer">
                    <span>Time: {new Date(iteration.timestamp).toLocaleString()}</span>
                    <span> | Type: {iteration.type}</span>
                  </summary>
                  <pre className="whitespace-pre-wrap mt-2">{iteration.content}</pre>
                </details>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;