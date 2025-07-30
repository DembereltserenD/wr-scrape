import type { AppProps } from 'next/app';
import { LanguageProvider } from '../contexts/LanguageContext';
import ErrorBoundary from '../components/ErrorBoundary';
import '../styles/globals.css';

export default function App({ Component, pageProps }: AppProps) {
    return (
        <ErrorBoundary
            fallback={
                <div className="min-h-screen bg-background-dark flex items-center justify-center">
                    <div className="bg-card-background rounded-xl p-8 max-w-md mx-4 text-center">
                        <h1 className="text-2xl font-bold text-white mb-4">
                            Application Error
                        </h1>
                        <p className="text-text-secondary mb-6">
                            The application encountered a critical error. Please refresh the page or try again later.
                        </p>
                        <button
                            onClick={() => window.location.reload()}
                            className="gaming-button text-white"
                        >
                            Refresh Application
                        </button>
                    </div>
                </div>
            }
        >
            <LanguageProvider>
                <ErrorBoundary
                    fallback={
                        <div className="min-h-screen bg-background-dark flex items-center justify-center">
                            <div className="bg-card-background rounded-xl p-8 max-w-md mx-4 text-center">
                                <h2 className="text-xl font-bold text-white mb-4">
                                    Language System Error
                                </h2>
                                <p className="text-text-secondary mb-6">
                                    The language system could not be initialized. The app will use default English.
                                </p>
                                <button
                                    onClick={() => window.location.reload()}
                                    className="gaming-button text-white"
                                >
                                    Retry
                                </button>
                            </div>
                        </div>
                    }
                >
                    <Component {...pageProps} />
                </ErrorBoundary>
            </LanguageProvider>
        </ErrorBoundary>
    );
}