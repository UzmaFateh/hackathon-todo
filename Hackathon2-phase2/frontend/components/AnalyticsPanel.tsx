import { useState } from 'react';
import { getAnalytics } from '@/lib/api';
import useApi from '@/lib/useApi';

export function AnalyticsPanel() {
    const [insight, setInsight] = useState<string | null>(null);
    const analyticsApi = useApi<{ insight: string }>();

    const handleGenerateInsights = async () => {
        try {
            const data = await analyticsApi.execute(() => getAnalytics());
            if (data) {
                setInsight(data.insight);
            }
        } catch (error) {
            console.error('Failed to generate insights:', error);
        }
    };

    return (
        <div className="glass-panel p-6 mb-8 relative overflow-hidden group">
            <div className="absolute top-0 right-0 p-4 opacity-10 group-hover:opacity-20 transition-opacity">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-24 w-24 text-primary-500" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M12.316 3.051a1 1 0 01.633 1.265l-4 12a1 1 0 11-1.898-.632l4-12a1 1 0 011.265-.633zM5.707 6.293a1 1 0 010 1.414L3.414 10l2.293 2.293a1 1 0 11-1.414 1.414l-3-3a1 1 0 010-1.414l3-3a1 1 0 011.414 0zm8.586 0a1 1 0 011.414 0l3 3a1 1 0 010 1.414l-3 3a1 1 0 11-1.414-1.414L16.586 10l-2.293-2.293a1 1 0 010-1.414z" clipRule="evenodd" />
                </svg>
            </div>

            <div className="relative z-10">
                <div className="flex items-center justify-between mb-4">
                    <h2 className="text-xl font-bold text-gradient flex items-center gap-2">
                        <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-primary-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                        </svg>
                        AI Insights
                    </h2>
                    {!insight && (
                        <button
                            onClick={handleGenerateInsights}
                            disabled={analyticsApi.loading}
                            className="btn-luxury px-4 py-2 text-sm flex items-center gap-2"
                        >
                            {analyticsApi.loading ? (
                                <>
                                    <span className="animate-spin rounded-full h-4 w-4 border-t-2 border-b-2 border-white"></span>
                                    Analyzing...
                                </>
                            ) : (
                                <>
                                    <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19.428 15.428a2 2 0 00-1.022-.547l-2.384-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" />
                                    </svg>
                                    Generate Insights
                                </>
                            )}
                        </button>
                    )}
                </div>

                {analyticsApi.error && (
                    <div className="p-4 bg-error-500/10 border border-error-500/20 rounded-xl text-error-200 mb-4">
                        <p className="flex items-center gap-2">
                            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                                <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                            </svg>
                            {analyticsApi.error.message || "Failed to generate insights. Please try again."}
                        </p>
                    </div>
                )}

                {insight && (
                    <div className="animate-in fade-in slide-in-from-bottom-4 duration-500">
                        <div className="prose prose-invert max-w-none">
                            <div className="bg-white/5 rounded-xl p-6 border border-white/10 shadow-inner">
                                <div className="flex items-start gap-4">
                                    <div className="flex-shrink-0 mt-1">
                                        <div className="w-8 h-8 rounded-full bg-gradient-to-br from-primary-400 to-secondary-500 flex items-center justify-center text-white shadow-lg">
                                            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                                                <path d="M5 3a2 2 0 00-2 2v2a2 2 0 002 2h2a2 2 0 002-2V5a2 2 0 00-2-2H5zM5 11a2 2 0 00-2 2v2a2 2 0 002 2h2a2 2 0 002-2v-2a2 2 0 00-2-2H5zM11 5a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V5zM11 13a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z" />
                                            </svg>
                                        </div>
                                    </div>
                                    <div className="flex-1">
                                        <p className="text-gray-200 whitespace-pre-line leading-relaxed text-lg">
                                            {insight}
                                        </p>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div className="mt-4 text-right">
                            <button
                                onClick={handleGenerateInsights}
                                className="text-sm text-primary-400 hover:text-primary-300 transition-colors flex items-center gap-1 ml-auto"
                            >
                                <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                                </svg>
                                Refresh Analysis
                            </button>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
}
