import { style } from '@vanilla-extract/css';

export const body = style({
  fontFamily: 'Arial, sans-serif',
  backgroundColor: '#f3f4f6',
  display: 'flex',
  justifyContent: 'center',
  alignItems: 'center',
  minHeight: '100vh',
  margin: 0,
});

export const card = style({
  position: 'relative',
  width: '320px',
  backgroundColor: '#ffffff',
  borderRadius: '12px',
  boxShadow: '0 4px 12px rgba(0, 0, 0, 0.1)',
  overflow: 'hidden',
});

export const badge = style({
  display: 'inline-block',
  backgroundColor: '#ef4444',
  color: '#ffffff',
  fontSize: '12px',
  fontWeight: 'bold',
  padding: '4px 10px',
  borderRadius: '9999px',
  marginBottom: '12px',
});

export const cardBody = style({
  padding: '16px',
});

export const cardTitle = style({
  fontSize: '18px',
  fontWeight: 'bold',
  color: '#111827',
  marginBottom: '8px',
});

export const cardDescription = style({
  fontSize: '14px',
  color: '#6b7280',
  lineHeight: 1.5,
  marginBottom: '16px',
});

export const cardMeta = style({
  display: 'flex',
  justifyContent: 'space-between',
  alignItems: 'center',
  marginBottom: '12px',
});

export const price = style({
  fontSize: '20px',
  fontWeight: 'bold',
  color: '#111827',
});

export const rating = style({
  fontSize: '14px',
  color: '#f59e0b',
  fontWeight: 600,
});

export const tags = style({
  display: 'flex',
  gap: '8px',
  marginBottom: '16px',
});

export const tag = style({
  fontSize: '12px',
  color: '#2563eb',
  backgroundColor: '#dbeafe',
  padding: '4px 10px',
  borderRadius: '6px',
});

export const btnPrimary = style({
  width: '100%',
  backgroundColor: '#2563eb',
  color: '#ffffff',
  fontSize: '14px',
  fontWeight: 'bold',
  padding: '10px 0',
  border: 'none',
  borderRadius: '8px',
  cursor: 'pointer',
});
