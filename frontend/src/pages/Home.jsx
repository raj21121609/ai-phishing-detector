import { Link } from 'react-router-dom';

const Home = () => {
  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 md:py-24">
      <div className="text-center max-w-3xl mx-auto">
        <h1 className="text-4xl md:text-6xl font-extrabold tracking-tight mb-6">
          Defend against <span className="text-primary">Phishing</span> with Advanced AI
        </h1>
        <p className="text-lg md:text-xl text-slate-400 mb-10">
          PhishGuard AI analyzes emails in real-time using multiple layers of machine learning to detect zero-day threats, malicious URLs, and deceptive sender behavior.
        </p>
        <Link
          to="/analyze"
          className="inline-flex items-center justify-center px-8 py-4 border border-transparent text-base font-medium rounded-lg text-white bg-primary hover:bg-sky-600 md:text-lg transition-transform hover:scale-105 shadow-lg shadow-primary/25"
        >
          Analyze an Email Now
        </Link>
      </div>

      <div className="mt-24 grid grid-cols-1 md:grid-cols-3 gap-8">
        {/* Feature 1 */}
        <div className="glass-panel p-6 rounded-xl hover:border-primary/50 transition-colors">
          <div className="w-12 h-12 bg-primary/20 rounded-lg flex items-center justify-center mb-4">
            <svg className="w-6 h-6 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
          </div>
          <h3 className="text-xl font-bold mb-2">AI Detection</h3>
          <p className="text-slate-400 text-sm">
            Leverages state-of-the-art machine learning models to classify email intent and identify subtle social engineering tactics.
          </p>
        </div>
        
        {/* Feature 2 */}
        <div className="glass-panel p-6 rounded-xl hover:border-primary/50 transition-colors">
          <div className="w-12 h-12 bg-primary/20 rounded-lg flex items-center justify-center mb-4">
            <svg className="w-6 h-6 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1" />
            </svg>
          </div>
          <h3 className="text-xl font-bold mb-2">URL Analysis</h3>
          <p className="text-slate-400 text-sm">
            Deep inspection of embedded links against known threat databases and domain reputation algorithms.
          </p>
        </div>

        {/* Feature 3 */}
        <div className="glass-panel p-6 rounded-xl hover:border-primary/50 transition-colors">
          <div className="w-12 h-12 bg-primary/20 rounded-lg flex items-center justify-center mb-4">
            <svg className="w-6 h-6 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
            </svg>
          </div>
          <h3 className="text-xl font-bold mb-2">Explainable Results</h3>
          <p className="text-slate-400 text-sm">
            We don't just give a score. We provide transparent reasoning so you understand exactly why an email was flagged.
          </p>
        </div>
      </div>
    </div>
  );
};

export default Home;
