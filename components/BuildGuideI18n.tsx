import React from 'react';
import { useTranslation } from '../utils/i18n';

interface BuildGuideProps {
  builds: {
    core_items: string[];
    starting_items: string[];
    boots: string[];
    situational: string[];
  };
  runes: {
    primary: {
      tree: string;
      keystone: string;
      runes: string[];
    };
    secondary: {
      tree: string;
      runes: string[];
    };
  };
}

const BuildGuideI18n: React.FC<BuildGuideProps> = ({ builds, runes }) => {
  const { t } = useTranslation();

  const getRuneTreeTranslation = (tree: string) => {
    const key = tree.toLowerCase();
    return t(`runes.trees.${key}`) || tree;
  };

  return (
    <div className="space-y-6">
      {/* Items Build */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h3 className="text-xl font-bold mb-4 text-gray-800">
          {t('builds.title')}
        </h3>
        
        <div className="space-y-4">
          <div>
            <h4 className="font-semibold text-gray-700 mb-2">
              {t('builds.starting_items')}
            </h4>
            <div className="flex flex-wrap gap-2">
              {builds.starting_items.map((item, index) => (
                <span key={index} className="bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm">
                  {item}
                </span>
              ))}
            </div>
          </div>

          <div>
            <h4 className="font-semibold text-gray-700 mb-2">
              {t('builds.core_items')}
            </h4>
            <div className="space-y-2">
              {builds.core_items.map((item, index) => (
                <div key={index} className="flex items-center space-x-2">
                  <span className="bg-blue-500 text-white w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold">
                    {index + 1}
                  </span>
                  <span className="text-gray-700">{item}</span>
                </div>
              ))}
            </div>
          </div>

          <div>
            <h4 className="font-semibold text-gray-700 mb-2">
              {t('builds.boots')}
            </h4>
            <div className="flex flex-wrap gap-2">
              {builds.boots.map((boot, index) => (
                <span key={index} className="bg-yellow-100 text-yellow-800 px-3 py-1 rounded-full text-sm">
                  {boot}
                </span>
              ))}
            </div>
          </div>

          <div>
            <h4 className="font-semibold text-gray-700 mb-2">
              {t('builds.situational')}
            </h4>
            <div className="flex flex-wrap gap-2">
              {builds.situational.map((item, index) => (
                <span key={index} className="bg-purple-100 text-purple-800 px-3 py-1 rounded-full text-sm">
                  {item}
                </span>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Runes */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h3 className="text-xl font-bold mb-4 text-gray-800">
          {t('runes.title')}
        </h3>
        
        <div className="space-y-4">
          <div>
            <h4 className="font-semibold text-gray-700 mb-2">
              {t('runes.primary')} ({getRuneTreeTranslation(runes.primary.tree)})
            </h4>
            <div className="space-y-2">
              <div className="bg-yellow-100 border border-yellow-300 p-2 rounded">
                <span className="font-bold text-yellow-800">{runes.primary.keystone}</span>
                <span className="text-xs text-yellow-600 ml-2">
                  ({t('runes.keystone')})
                </span>
              </div>
              {runes.primary.runes.map((rune, index) => (
                <div key={index} className="bg-blue-50 border border-blue-200 p-2 rounded">
                  <span className="text-blue-800">{rune}</span>
                </div>
              ))}
            </div>
          </div>

          <div>
            <h4 className="font-semibold text-gray-700 mb-2">
              {t('runes.secondary')} ({getRuneTreeTranslation(runes.secondary.tree)})
            </h4>
            <div className="space-y-2">
              {runes.secondary.runes.map((rune, index) => (
                <div key={index} className="bg-green-50 border border-green-200 p-2 rounded">
                  <span className="text-green-800">{rune}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default BuildGuideI18n;
