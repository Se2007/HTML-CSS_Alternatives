import * as stylex from '@stylexjs/stylex';

const styles = stylex.create({
  body: {
    fontFamily: 'Arial, sans-serif',
    backgroundColor: '#f3f4f6',
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    minHeight: '100vh',
    margin: 0,
  },
  card: {
    position: 'relative',
    width: '320px',
    backgroundColor: '#ffffff',
    borderRadius: '12px',
    boxShadow: '0 4px 12px rgba(0, 0, 0, 0.1)',
    overflow: 'hidden',
  },
  badge: {
    display: 'inline-block',
    backgroundColor: '#ef4444',
    color: '#ffffff',
    fontSize: '12px',
    fontWeight: 'bold',
    padding: '4px 10px',
    borderRadius: '9999px',
    marginBottom: '12px',
  },
  cardBody: {
    padding: '16px',
  },
  cardTitle: {
    fontSize: '18px',
    fontWeight: 'bold',
    color: '#111827',
    marginBottom: '8px',
  },
  cardDescription: {
    fontSize: '14px',
    color: '#6b7280',
    lineHeight: 1.5,
    marginBottom: '16px',
  },
  cardMeta: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: '12px',
  },
  price: {
    fontSize: '20px',
    fontWeight: 'bold',
    color: '#111827',
  },
  rating: {
    fontSize: '14px',
    color: '#f59e0b',
    fontWeight: 600,
  },
  tags: {
    display: 'flex',
    gap: '8px',
    marginBottom: '16px',
  },
  tag: {
    fontSize: '12px',
    color: '#2563eb',
    backgroundColor: '#dbeafe',
    padding: '4px 10px',
    borderRadius: '6px',
  },
  btnPrimary: {
    width: '100%',
    backgroundColor: '#2563eb',
    color: '#ffffff',
    fontSize: '14px',
    fontWeight: 'bold',
    padding: '10px 0',
    border: 'none',
    borderRadius: '8px',
    cursor: 'pointer',
  },
});

export default function ProductCard() {
  return (
    <div {...stylex.props(styles.body)}>
      <div {...stylex.props(styles.card)}>
        <div {...stylex.props(styles.cardBody)}>
          <span {...stylex.props(styles.badge)}>New</span>
          <h2 {...stylex.props(styles.cardTitle)}>Wireless Headphones</h2>
          <p {...stylex.props(styles.cardDescription)}>
            Premium sound quality with active noise cancellation and 30-hour battery life.
          </p>

          <div {...stylex.props(styles.cardMeta)}>
            <span {...stylex.props(styles.price)}>$129.00</span>
            <span {...stylex.props(styles.rating)}>★ 4.8</span>
          </div>

          <div {...stylex.props(styles.tags)}>
            <span {...stylex.props(styles.tag)}>Audio</span>
            <span {...stylex.props(styles.tag)}>Wireless</span>
          </div>

          <button {...stylex.props(styles.btnPrimary)}>Add to Cart</button>
        </div>
      </div>
    </div>
  );
}
