import React, { useState, useEffect } from 'react';
import axios from 'axios';
import ResultsDisplay from '../components/ResultsDisplay';

const History = () => {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  const [selectedRecord, setSelectedRecord] = useState(null);
  const [loadingDetails, setLoadingDetails] = useState(false);

  useEffect(() => {
    fetchHistory();
  }, []);

  const fetchHistory = async () => {
    try {
      const response = await axios.get(`${import.meta.env.VITE_API_BASE_URL}/history/`);
      setHistory(response.data.results || []);
    } catch (err) {
      setError("Failed to load history.");
    } finally {
      setLoading(false);
    }
  };

  const openRecord = async (id) => {
    setLoadingDetails(true);
    try {
      const response = await axios.get(`${import.meta.env.VITE_API_BASE_URL}/history/${id}/`);
      setSelectedRecord(response.data);
    } catch (err) {
      alert("Failed to load record details.");
    } finally {
      setLoadingDetails(false);
    }
  };

  const getRiskColor = (level) => {
    switch (level) {
      case 'CRITICAL': return 'text-red-500 bg-red-500/10 border-red-500/30';
      case 'HIGH': return 'text-orange-500 bg-orange-500/10 border-orange-500/30';
      case 'MEDIUM': return 'text-yellow-500 bg-yellow-500/10 border-yellow-500/30';
      case 'LOW': return 'text-green-500 bg-green-500/10 border-green-500/30';
      default: return 'text-slate-400 bg-slate-800 border-slate-700';
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 py-12">
      <div className="mb-8 flex justify-between items-end">
        <div>
          <h1 className="text-3xl font-bold text-slate-100 mb-2">Analysis History</h1>
          <p className="text-slate-400">View your previously analyzed emails and their threat reports.</p>
        </div>
      </div>

      {loading ? (
        <div className="flex justify-center items-center h-64">
          <div className="w-8 h-8 border-4 border-cyan-500/30 border-t-cyan-500 rounded-full animate-spin"></div>
        </div>
      ) : error ? (
        <div className="p-4 bg-red-500/10 border border-red-500/30 rounded-lg text-red-400">{error}</div>
      ) : history.length === 0 ? (
        <div className="text-center p-12 bg-slate-900/50 border border-slate-800 rounded-xl">
          <span className="text-4xl mb-4 block">📭</span>
          <h3 className="text-xl text-slate-300 font-semibold mb-2">No History Found</h3>
          <p className="text-slate-500">You haven't analyzed any emails yet.</p>
        </div>
      ) : (
        <div className="bg-slate-900/50 border border-slate-800 rounded-xl overflow-hidden shadow-xl">
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="bg-slate-950 border-b border-slate-800 text-slate-400 text-sm uppercase tracking-wider">
                  <th className="p-4 font-semibold">Date</th>
                  <th className="p-4 font-semibold">Sender</th>
                  <th className="p-4 font-semibold">Subject</th>
                  <th className="p-4 font-semibold">Risk Level</th>
                  <th className="p-4 font-semibold text-center">Score</th>
                  <th className="p-4 font-semibold"></th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800">
                {history.map((record) => (
                  <tr key={record.id} className="hover:bg-slate-800/50 transition-colors">
                    <td className="p-4 text-slate-300 whitespace-nowrap">
                      {new Date(record.created_at).toLocaleDateString()}
                    </td>
                    <td className="p-4 text-slate-300 truncate max-w-xs" title={record.sender}>
                      {record.sender || 'Unknown'}
                    </td>
                    <td className="p-4 text-slate-300 truncate max-w-sm" title={record.subject}>
                      {record.subject || 'No Subject'}
                    </td>
                    <td className="p-4">
                      <span className={`px-3 py-1 rounded-full text-xs font-bold border ${getRiskColor(record.risk_level)}`}>
                        {record.risk_level}
                      </span>
                    </td>
                    <td className="p-4 text-center text-slate-300 font-bold">
                      {record.risk_score}
                    </td>
                    <td className="p-4 text-right">
                      <button 
                        onClick={() => openRecord(record.id)}
                        disabled={loadingDetails}
                        className="text-cyan-400 hover:text-cyan-300 font-medium text-sm transition-colors"
                      >
                        View Report
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Modal overlay */}
      {selectedRecord && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-sm overflow-y-auto">
          <div className="bg-slate-900 border border-slate-700 rounded-2xl w-full max-w-5xl my-8 flex flex-col max-h-[90vh]">
            <div className="flex justify-between items-center p-6 border-b border-slate-800">
              <h2 className="text-xl font-bold text-slate-100">Analysis Report</h2>
              <button 
                onClick={() => setSelectedRecord(null)}
                className="text-slate-400 hover:text-white text-3xl leading-none transition-colors"
              >
                &times;
              </button>
            </div>
            <div className="p-6 overflow-y-auto custom-scrollbar">
              <ResultsDisplay 
                result={selectedRecord.analysis_data} 
                onReset={() => setSelectedRecord(null)} 
              />
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default History;
