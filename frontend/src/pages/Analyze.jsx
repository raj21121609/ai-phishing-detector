import { useState } from 'react';
import axios from 'axios';

const Analyze = () => {
  const [emailText, setEmailText] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [result, setResult] = useState(null);

  const API_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';

  const handleAnalyze = async () => {
    if (!emailText.trim()) {
      setError("Email text cannot be empty.");
      return;
    }
    
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await axios.post(`${API_URL}/analyze/`, {
        email_text: emailText
      });
      setResult(response.data);
    } catch (err) {
      setError(err.response?.data?.email_text?.[0] || err.message || "An error occurred.");
    } finally {
      setLoading(false);
    }
  };

  const handleClear = () => {
    setEmailText('');
    setResult(null);
    setError(null);
  };

  return (
    <div className="max-w-4xl mx-auto px-4 py-12">
      <div className="mb-8">
        <h1 className="text-3xl font-bold mb-2">Analyze Email</h1>
        <p className="text-slate-400">Paste the suspicious email content below to analyze it for threats.</p>
      </div>

      <div className="glass-panel p-6 rounded-xl">
        <div className="mb-4">
          <textarea
            className="w-full h-64 bg-slate-950 border border-slate-700 rounded-lg p-4 text-slate-100 placeholder-slate-600 focus:outline-none focus:border-primary focus:ring-1 focus:ring-primary transition-colors"
            placeholder="Paste email headers and body here..."
            value={emailText}
            onChange={(e) => setEmailText(e.target.value)}
          ></textarea>
          <div className="flex justify-end mt-2 text-xs text-slate-500">
            {emailText.length} characters
          </div>
        </div>

        {error && (
          <div className="mb-4 p-4 bg-red-900/30 border border-red-500/50 rounded-lg text-red-200">
            {typeof error === 'string' ? error : JSON.stringify(error)}
          </div>
        )}

        <div className="flex space-x-4">
          <button
            onClick={handleAnalyze}
            disabled={loading}
            className="flex-1 bg-primary hover:bg-sky-600 text-white font-medium py-3 px-6 rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center"
          >
            {loading ? (
              <>
                <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Analyzing...
              </>
            ) : (
              'Analyze Email'
            )}
          </button>
          <button
            onClick={handleClear}
            disabled={loading}
            className="px-6 py-3 bg-slate-800 hover:bg-slate-700 text-slate-200 font-medium rounded-lg transition-colors disabled:opacity-50"
          >
            Clear
          </button>
        </div>
      </div>

      {result && (
        <div className="mt-8 glass-panel p-6 rounded-xl border-green-500/30 bg-green-900/10">
          <h2 className="text-xl font-bold mb-4 text-green-400">Analysis Result</h2>
          <div className="bg-slate-950 p-4 rounded-lg overflow-x-auto border border-slate-800">
            <pre className="text-sm text-slate-300">
              {JSON.stringify(result, null, 2)}
            </pre>
          </div>
        </div>
      )}
    </div>
  );
};

export default Analyze;
