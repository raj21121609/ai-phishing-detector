import React from 'react';

const ResultsDisplay = ({ result, onReset }) => {
  const {
    risk_score,
    risk_level,
    phishing_probability,
    email,
    threats,
    url_analysis,
    explanation
  } = result;

  const getRiskStyles = (level) => {
    switch (level) {
      case 'CRITICAL':
        return { color: 'text-red-500', bg: 'bg-red-500/10', border: 'border-red-500/30', icon: '🔴' };
      case 'HIGH':
        return { color: 'text-orange-500', bg: 'bg-orange-500/10', border: 'border-orange-500/30', icon: '🟠' };
      case 'MEDIUM':
        return { color: 'text-yellow-500', bg: 'bg-yellow-500/10', border: 'border-yellow-500/30', icon: '🟡' };
      case 'LOW':
      default:
        return { color: 'text-green-500', bg: 'bg-green-500/10', border: 'border-green-500/30', icon: '🟢' };
    }
  };

  const riskStyle = getRiskStyles(risk_level);

  return (
    <div className="space-y-8 animate-fade-in">
      {/* Header Section */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className={`p-6 rounded-xl border ${riskStyle.border} ${riskStyle.bg} flex items-center justify-between shadow-lg`}>
          <div>
            <h3 className="text-slate-400 text-sm font-semibold uppercase tracking-wider mb-1">Overall Risk</h3>
            <div className={`text-3xl font-bold ${riskStyle.color} flex items-center gap-3`}>
              <span className="text-2xl">{riskStyle.icon}</span>
              {risk_level} RISK
            </div>
          </div>
          <div className="text-right">
            <div className={`text-5xl font-bold ${riskStyle.color}`}>{risk_score}</div>
            <div className={`text-sm mt-1 ${riskStyle.color} opacity-80`}>/ 100</div>
          </div>
        </div>

        <div className="p-6 rounded-xl border border-slate-800 bg-slate-900/50 flex flex-col justify-center shadow-lg">
          <h3 className="text-slate-400 text-sm font-semibold uppercase tracking-wider mb-1">AI Phishing Probability</h3>
          <div className="text-3xl font-bold text-cyan-400">
            {(phishing_probability * 100).toFixed(1)}%
          </div>
          <div className="w-full bg-slate-800 rounded-full h-2.5 mt-3 overflow-hidden">
            <div 
              className="bg-cyan-400 h-2.5 rounded-full transition-all duration-1000 ease-out" 
              style={{ width: `${phishing_probability * 100}%` }}
            ></div>
          </div>
        </div>
      </div>

      {/* Explanation Section */}
      <div className="p-6 rounded-xl border border-slate-800 bg-slate-900/50 shadow-lg">
        <h2 className="text-xl font-semibold text-slate-200 mb-4 flex items-center gap-2">
          <span className="text-2xl">🧠</span> AI Analysis
        </h2>
        <p className="text-slate-300 text-lg mb-6 leading-relaxed">{explanation?.summary}</p>
        
        {explanation?.recommendation && (
          <div className="p-5 rounded-lg border border-cyan-500/30 bg-cyan-500/10 flex gap-4 items-start">
            <div className="text-cyan-400 text-xl mt-0.5">🛡️</div>
            <div>
              <h4 className="text-cyan-400 font-semibold mb-1 uppercase tracking-wide text-sm">Recommended Action</h4>
              <p className="text-slate-200">{explanation.recommendation}</p>
            </div>
          </div>
        )}
      </div>

      {/* Threat Cards */}
      {explanation?.reasons && explanation.reasons.length > 0 && (
        <div>
          <h2 className="text-xl font-semibold text-slate-200 mb-4 flex items-center gap-2">
            <span className="text-2xl">⚠️</span> {explanation.reasons.length} Suspicious Indicators Detected
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {explanation.reasons.map((reason, idx) => (
              <div key={idx} className="p-5 rounded-lg border border-slate-800 bg-slate-900/50 flex flex-col hover:border-slate-600 transition-colors">
                <div className="flex justify-between items-start mb-3">
                  <span className={`text-xs font-bold px-2.5 py-1 rounded-full ${reason.severity === 'HIGH' ? 'bg-red-500/20 text-red-400' : 'bg-yellow-500/20 text-yellow-400'}`}>
                    {reason.severity}
                  </span>
                  <span className="text-xs font-semibold text-slate-400 bg-slate-800 px-2.5 py-1 rounded-full uppercase tracking-wider">
                    {reason.category.replace('_', ' ')}
                  </span>
                </div>
                <p className="text-slate-300 leading-relaxed">{reason.message}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Deep Dive Section */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Sender Info */}
        <div className="p-6 rounded-xl border border-slate-800 bg-slate-900/50 shadow-lg">
          <h3 className="text-lg font-semibold text-slate-200 mb-4 flex items-center gap-2">
            <span className="text-xl">👤</span> Sender Details
          </h3>
          <div className="space-y-4">
            <div>
              <span className="text-slate-500 text-sm block mb-1">Sender Address:</span>
              <p className="text-slate-300 font-medium break-all bg-slate-950 p-2 rounded border border-slate-800">{email?.sender || 'Unknown / Not provided'}</p>
            </div>
            <div>
              <span className="text-slate-500 text-sm block mb-1">Subject:</span>
              <p className="text-slate-300 font-medium bg-slate-950 p-2 rounded border border-slate-800">{email?.subject || 'None'}</p>
            </div>
            {threats && threats.some(t => t.toLowerCase().includes('sender') || t.toLowerCase().includes('reply')) && (
               <div className="mt-4 p-3 bg-red-500/10 border border-red-500/30 rounded flex items-center gap-2">
                  <span className="text-red-400">⚠️</span>
                  <span className="text-sm text-red-400 font-medium">Suspicious sender indicators detected</span>
               </div>
            )}
          </div>
        </div>

        {/* URLs Info */}
        {url_analysis && url_analysis.length > 0 && (
          <div className="p-6 rounded-xl border border-slate-800 bg-slate-900/50 shadow-lg flex flex-col">
            <h3 className="text-lg font-semibold text-slate-200 mb-4 flex items-center gap-2">
              <span className="text-xl">🔗</span> URL Analysis ({url_analysis.length})
            </h3>
            <div className="space-y-4 overflow-y-auto pr-2 custom-scrollbar flex-1" style={{maxHeight: '300px'}}>
              {url_analysis.map((u, idx) => (
                <div key={idx} className="p-4 bg-slate-950 rounded-lg border border-slate-800 hover:border-slate-700 transition-colors">
                  <p className="text-sm text-cyan-400 break-all mb-3 font-mono bg-slate-900/50 p-2 rounded">{u.url}</p>
                  <div className="flex justify-between items-center text-sm mb-2">
                    <span className="text-slate-400">Risk Score:</span>
                    <span className={`font-bold ${u.risk_score > 50 ? 'text-red-400' : 'text-slate-300'}`}>{u.risk_score}</span>
                  </div>
                  {u.signals && u.signals.length > 0 && (
                    <div className="mt-3">
                      <span className="text-xs text-slate-500 uppercase tracking-wider mb-1 block">Signals:</span>
                      <ul className="text-xs text-slate-300 list-disc list-inside space-y-1 ml-1">
                        {u.signals.map((sig, sidx) => <li key={sidx}>{sig}</li>)}
                      </ul>
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      <div className="pt-8 border-t border-slate-800 flex justify-center">
        <button
          onClick={onReset}
          className="bg-slate-800 hover:bg-slate-700 text-slate-200 px-8 py-3 rounded-lg font-semibold transition-colors duration-200 flex items-center gap-2 shadow-lg"
        >
          <span className="text-lg">↺</span> Analyze Another Email
        </button>
      </div>
    </div>
  );
};

export default ResultsDisplay;
