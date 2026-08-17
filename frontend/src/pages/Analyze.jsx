import React, { useState } from 'react';
import axios from 'axios';
import ResultsDisplay from '../components/ResultsDisplay';

const Analyze = () => {
  const [emailText, setEmailText] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [result, setResult] = useState(null);

  const handleAnalyze = async () => {
    if (!emailText.trim()) {
      setError("Please paste an email to analyze.");
      return;
    }
    
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await axios.post(`${import.meta.env.VITE_API_BASE_URL}/analyze/`, {
        email_text: emailText
      });
      setResult(response.data);
    } catch (err) {
      if (err.response && err.response.data && err.response.data.message) {
        setError(err.response.data.message);
      } else if (err.response && err.response.data && err.response.data.email_text) {
        setError(err.response.data.email_text[0]);
      } else {
        setError("An error occurred while connecting to the server. Please try again.");
      }
    } finally {
      setLoading(false);
    }
  };

  const handleClear = () => {
    setEmailText('');
    setError(null);
  };

  return (
    <div className="max-w-5xl mx-auto px-4 py-12">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-slate-100 mb-2">Analyze Email</h1>
        <p className="text-slate-400">Paste suspicious email content below to analyze it for threats.</p>
      </div>

      {result ? (
        <ResultsDisplay result={result} onReset={() => setResult(null)} />
      ) : (
        <div className="bg-slate-900/50 border border-slate-800 rounded-xl p-6 shadow-xl">
          <div className="mb-4">
            <textarea
              className="w-full h-64 bg-slate-950 border border-slate-700 rounded-lg p-4 text-slate-300 focus:outline-none focus:border-cyan-500 focus:ring-1 focus:ring-cyan-500 transition-all resize-y font-mono text-sm"
              placeholder="Paste the email source or text here..."
              value={emailText}
              onChange={(e) => setEmailText(e.target.value)}
              disabled={loading}
            ></textarea>
            <div className="flex justify-end mt-2">
              <span className={`text-xs ${emailText.length > 90000 ? 'text-orange-400' : 'text-slate-500'}`}>
                {emailText.length} / 100,000 characters
              </span>
            </div>
          </div>

          {error && (
            <div className="mb-6 p-4 bg-red-500/10 border border-red-500/30 rounded-lg flex items-center gap-3">
              <span className="text-red-400 text-xl">⚠️</span>
              <span className="text-red-400 font-medium">{error}</span>
            </div>
          )}

          <div className="flex gap-4">
            <button
              onClick={handleAnalyze}
              disabled={loading || !emailText.trim()}
              className={`flex-1 bg-cyan-600 hover:bg-cyan-500 text-white font-semibold py-3 px-6 rounded-lg transition-colors flex justify-center items-center shadow-lg ${loading || !emailText.trim() ? 'opacity-50 cursor-not-allowed' : ''}`}
            >
              {loading ? (
                <div className="flex items-center gap-2">
                  <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
                  Analyzing...
                </div>
              ) : (
                'Analyze Email'
              )}
            </button>
            <button
              onClick={handleClear}
              disabled={loading || !emailText.length}
              className={`px-8 py-3 bg-slate-800 hover:bg-slate-700 text-slate-300 font-semibold rounded-lg transition-colors shadow-lg ${loading || !emailText.length ? 'opacity-50 cursor-not-allowed' : ''}`}
            >
              Clear
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default Analyze;
