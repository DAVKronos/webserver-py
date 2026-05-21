import { useTranslation } from 'react-i18next';

const AgendaItemTypeName = ({ agendaItemType, fallback = '' }) => {
  const { i18n } = useTranslation('generic');
  
  if (!agendaItemType) {
    return fallback ? <>{fallback}</> : null;
  }
  
  const language = i18n?.language?.split('-')[0] ?? 'en';
  
  const name = language === 'nl' 
    ? agendaItemType.name_nl 
    : agendaItemType.name_en;
  
  const text = name 
    ?? (language === 'nl' ? agendaItemType.name_en : agendaItemType.name_nl)
    ?? fallback;
  
  if (!text) {
    return null;
  }
  
  return <>{text}</>;
};

export { AgendaItemTypeName };