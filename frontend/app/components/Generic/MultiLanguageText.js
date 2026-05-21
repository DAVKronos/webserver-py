import React from 'react'
import { useTranslation } from 'react-i18next';

const MultiLanguageText = ({ nl, en, renderFunction, fallback = '' }) => {
  const { i18n } = useTranslation();
  
 
  const language = i18n?.language?.split('-')[0] ?? 'en';
  
  let text;
  if (language === 'nl') {
    text = nl;
  } else if (language === 'en') {
    text = en;
  } else {
    text = nl ?? en ?? fallback;
  }

  if (renderFunction && typeof renderFunction === 'function') {
    return renderFunction(text ?? fallback);
  }
  
  if (text == null) {
    return fallback ? <>{fallback}</> : null;
  }
  
  return <>{text}</>;
};

export default MultiLanguageText;