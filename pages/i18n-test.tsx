import React from 'react';
import Head from 'next/head';
import { LanguageProvider } from '../contexts/LanguageContext';
import LanguageSwitcher from '../components/LanguageSwitcher';
import I18nDemo from '../components/I18nDemo';

const I18nTestPage: React.FC = () => {
  return (
    <LanguageProvider>
      <Head>
        <title>I18n System Test - Wild Rift Guide</title>
        <meta name="description" content="Testing internationalization system" />
      </Head>

      <div className="min-h-screen bg-gray-50">
        {/* Header */}
        <header className="bg-white shadow-sm border-b">
          <div className="container mx-auto px-4 py-3">
            <div className="flex justify-between items-center">
              <h1 className="text-xl font-bold text-gray-800">
                I18n System Test
              </h1>
              <LanguageSwitcher />
            </div>
          </div>
        </header>

        {/* Main Content */}
        <main className="container mx-auto px-4 py-8">
          <I18nDemo />
        </main>
      </div>
    </LanguageProvider>
  );
};

export default I18nTestPage;