import React, { ReactNode } from 'react';
import Header from './Header';
import Footer from './Footer';
import ErrorBoundary from '../ErrorBoundary';

interface LayoutProps {
    children: ReactNode;
    currentPage?: string;
}

const Layout: React.FC<LayoutProps> = ({ children, currentPage }) => {
    return (
        <div>
            <ErrorBoundary
                fallback={
                    <div>
                        <div>
                            <h2>
                                Navigation Error
                            </h2>
                            <p>
                                There was an error loading the navigation. Please refresh the page.
                            </p>
                            <button
                                onClick={() => window.location.reload()}
                            >
                                Refresh Page
                            </button>
                        </div>
                    </div>
                }
            >
                <Header currentPage={currentPage} />
            </ErrorBoundary>

            <main>
                <ErrorBoundary>
                    {children}
                </ErrorBoundary>
            </main>

            <ErrorBoundary
                fallback={
                    <footer>
                        <div>
                            <p>
                                Footer temporarily unavailable
                            </p>
                        </div>
                    </footer>
                }
            >
                <Footer />
            </ErrorBoundary>
        </div>
    );
};

export default Layout;